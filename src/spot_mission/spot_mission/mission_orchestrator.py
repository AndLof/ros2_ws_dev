#!/usr/bin/env python3

import csv
import math
import subprocess
import time
from enum import Enum, auto

import rclpy
from rclpy.node import Node
from rclpy.time import Time
from rclpy.qos import QoSProfile, QoSDurabilityPolicy, QoSReliabilityPolicy

from geometry_msgs.msg import PoseStamped

from tf2_ros import (
    Buffer,
    TransformListener,
    LookupException,
    ConnectivityException,
    ExtrapolationException,
)


class State(Enum):
    INIT = auto()
    NAVIGATE = auto()
    RUN_NBV = auto()
    WAIT = auto()
    RESET_ARM = auto()
    DONE = auto()
    ERROR = auto()


# ----------------------------- utility geometriche -----------------------------
def yaw_to_quaternion(yaw):
    """Yaw (rad) -> (x, y, z, w), rotazione attorno a Z (robot su piano)."""
    return (0.0, 0.0, math.sin(yaw / 2.0), math.cos(yaw / 2.0))


def quaternion_to_yaw(x, y, z, w):
    """Estrae lo yaw (rad) da un quaternione."""
    return math.atan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y * y + z * z))


def angle_diff(a, b):
    """Differenza angolare minima (rad) riportata in [-pi, pi]."""
    return (a - b + math.pi) % (2.0 * math.pi) - math.pi


# --------------------------------- orchestratore -------------------------------
class MissionOrchestrator(Node):
    def __init__(self):
        super().__init__("mission_orchestrator")

        # ---------------------------- Parametri ----------------------------
        self.declare_parameter("csv_path", "spot_positions.csv")
        self.declare_parameter("goal_topic", "goaltospot")
        self.declare_parameter("fixed_frame", "spot_odom")      # frame FISSO di riferimento
        self.declare_parameter("spot_base_frame", "spot_body")  # frame di Spot che si muove
        self.declare_parameter("yaw_in_degrees", True)          # nel CSV yaw_deg è in gradi
        self.declare_parameter("only_valid", True)              # naviga solo zone con valid=True

        # comandi dei nodi one-shot (ros2 run ...  oppure  ros2 launch ...)
        self.declare_parameter("nbv_cmd", ["ros2", "run", "kinova_moveit_cpp", "kinova_explorer_nbv_v2"])
        self.declare_parameter("move_ee_cmd", ["ros2", "run", "kinova_moveit_cpp", "move_ee"])

        # tolleranze / tempi
        self.declare_parameter("pos_tol", 0.15)            # m
        self.declare_parameter("yaw_tol", 0.10)            # rad (~5.7 deg)
        self.declare_parameter("arrival_hold_s", 5.0)      # posa stabile richiesta all'arrivo
        self.declare_parameter("post_nbv_wait_s", 2.0)     # attesa fine NBV -> reset braccio
        self.declare_parameter("post_arm_wait_s", 3.0)     # attesa fine reset braccio -> prossima goal
        self.declare_parameter("nav_timeout_s", 120.0)     # timeout navigazione (per zona)
        self.declare_parameter("phase_timeout_s", 300.0)   # timeout NBV / reset braccio
        self.declare_parameter("republish_period_s", 0.0)  # re-invio goal (0 = una volta sola)
        self.declare_parameter("tick_period_s", 0.2)

        gp = self.get_parameter
        self.csv_path        = gp("csv_path").value
        self.goal_topic      = gp("goal_topic").value
        self.fixed_frame     = gp("fixed_frame").value
        self.base_frame      = gp("spot_base_frame").value
        self.yaw_in_deg      = gp("yaw_in_degrees").value
        self.only_valid      = gp("only_valid").value
        self.nbv_cmd         = list(gp("nbv_cmd").value)
        self.move_ee_cmd     = list(gp("move_ee_cmd").value)
        self.pos_tol         = gp("pos_tol").value
        self.yaw_tol         = gp("yaw_tol").value
        self.arrival_hold_s  = gp("arrival_hold_s").value
        self.post_nbv_wait_s = gp("post_nbv_wait_s").value
        self.post_arm_wait_s = gp("post_arm_wait_s").value
        self.nav_timeout_s   = gp("nav_timeout_s").value
        self.phase_timeout_s = gp("phase_timeout_s").value
        self.republish_s     = gp("republish_period_s").value
        tick_s               = gp("tick_period_s").value

        # ---------------------- Publisher su goaltospot ----------------------
        qos = QoSProfile(depth=1)
        qos.reliability = QoSReliabilityPolicy.RELIABLE
        qos.durability = QoSDurabilityPolicy.TRANSIENT_LOCAL
        self.goal_pub = self.create_publisher(PoseStamped, self.goal_topic, qos)

        # ------------------------------- TF -------------------------------
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # ------------------------- Carica le pose -------------------------
        self.goals = self.load_goals(self.csv_path)
        self.get_logger().info(f"Caricate {len(self.goals)} pose da '{self.csv_path}'.")

        # ------------------------------ Stato ------------------------------
        self.idx = 0
        self.results = []          # lista di (zona, esito)
        self.proc = None           # sottoprocesso corrente (NBV o move_ee)
        self.in_pos_since = None   # istante da cui Spot è "in posizione"
        self.last_republish_t = 0.0
        self.wait_until = 0.0      # scadenza dell'attesa passiva (stato WAIT)
        self.after_wait = None     # cosa fare al termine dell'attesa
        self.state = State.INIT
        self.state_entry_t = self.now()

        self.timer = self.create_timer(tick_s, self.tick)
        self.get_logger().info("Orchestratore pronto. Avvio missione.")

    # ------------------------------ utility ------------------------------
    @staticmethod
    def now():
        return time.monotonic()

    def load_goals(self, path):

        goals = []
        skipped = 0
        with open(path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                r = {(k or "").strip().lower(): (v or "").strip() for k, v in row.items()}

                is_valid = r.get("valid", "true").lower() in ("true", "1", "yes")
                if self.only_valid and not is_valid:
                    skipped += 1
                    continue

                x = float(r["pose_x_m"])
                y = float(r["pose_y_m"])
                yaw = float(r.get("yaw_deg", r.get("yaw", "0")))
                if self.yaw_in_deg:
                    yaw = math.radians(yaw)
                zone = r.get("zone_id", str(len(goals) + 1))
                goals.append({"zone": zone, "x": x, "y": y, "yaw": yaw})
        if skipped:
            self.get_logger().warn(f"Saltate {skipped} zone con valid=False.")
        return goals

    def enter(self, state):
        self.state = state
        self.state_entry_t = self.now()
        self.in_pos_since = None
        self.last_republish_t = 0.0
        suffix = ""
        if self.idx < len(self.goals):
            g = self.goals[self.idx]
            suffix = f" (zona {g['zone']}, {self.idx + 1}/{len(self.goals)})"
        self.get_logger().info(f"--> Stato: {state.name}{suffix}")

    def publish_goal(self, goal):
        msg = PoseStamped()
        msg.header.frame_id = self.fixed_frame
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.pose.position.x = goal["x"]
        msg.pose.position.y = goal["y"]
        msg.pose.position.z = 0.0
        qx, qy, qz, qw = yaw_to_quaternion(goal["yaw"])
        msg.pose.orientation.x = qx
        msg.pose.orientation.y = qy
        msg.pose.orientation.z = qz
        msg.pose.orientation.w = qw
        self.goal_pub.publish(msg)

    def spot_pose(self):
        """(x, y, yaw) di Spot in spot_odom, oppure None se la TF non è disponibile."""
        try:
            t = self.tf_buffer.lookup_transform(self.fixed_frame, self.base_frame, Time())
        except (LookupException, ConnectivityException, ExtrapolationException):
            return None
        tr = t.transform.translation
        ro = t.transform.rotation
        return (tr.x, tr.y, quaternion_to_yaw(ro.x, ro.y, ro.z, ro.w))

    def start_process(self, cmd):
        self.get_logger().info(f"Avvio processo: {' '.join(cmd)}")
        try:
            self.proc = subprocess.Popen(cmd)
            return True
        except Exception as e:  # eseguibile inesistente, ecc.
            self.get_logger().error(f"Impossibile avviare {cmd}: {e}")
            self.proc = None
            return False

    def kill_proc(self):
        if self.proc is None:
            return
        self.proc.terminate()
        try:
            self.proc.wait(timeout=5.0)
        except subprocess.TimeoutExpired:
            self.proc.kill()
        self.proc = None

    def poll_current_process(self, phase):
        """Ritorna 'running' / 'done' / 'timeout' per il sottoprocesso corrente."""
        t = self.now()
        ret = 0 if self.proc is None else self.proc.poll()
        if ret is None:  # ancora in esecuzione
            if (t - self.state_entry_t) > self.phase_timeout_s:
                self.get_logger().error(f"Timeout {phase}: termino il processo.")
                self.kill_proc()
                return "timeout"
            return "running"
        # terminato
        if self.proc is not None:
            log = self.get_logger().info if ret == 0 else self.get_logger().warn
            log(f"{phase} terminato (exit={ret}).")
            self.proc = None
        return "done"

    def begin_wait(self, seconds, after, note=""):
        """Attesa passiva di `seconds`, poi transizione.
        after: 'TO_RESET_ARM' (lancia move_ee) oppure 'TO_NEXT' (prossima zona)."""
        self.wait_until = self.now() + seconds
        self.after_wait = after
        self.get_logger().info(f"Attendo {seconds:.1f}s {note}.")
        self.enter(State.WAIT)

    def advance(self, status):
        zone = self.goals[self.idx]["zone"]
        self.results.append((zone, status))
        self.get_logger().info(f"Zona {zone}: {status}. Passo alla successiva.")
        self.idx += 1
        self.enter(State.NAVIGATE if self.idx < len(self.goals) else State.DONE)

    def finish(self, success):
        self.timer.cancel()
        tag = "COMPLETATA" if success else "INTERROTTA"
        self.get_logger().info(f"Missione {tag}. Esiti: {self.results}")
        rclpy.shutdown()

    # -------------------------- macchina a stati --------------------------
    def tick(self):
        s = self.state

        if s == State.INIT:
            if not self.goals:
                self.get_logger().error("Nessuna posa caricata dal CSV.")
                return self.enter(State.ERROR)
            self.enter(State.NAVIGATE)

        elif s == State.NAVIGATE:
            self.do_navigate()

        elif s == State.RUN_NBV:
            res = self.poll_current_process("NBV")
            if res == "timeout":
                self.enter(State.ERROR)
            elif res == "done":
                # NBV finito -> attesa, poi lancio il reset del braccio
                self.begin_wait(self.post_nbv_wait_s, "TO_RESET_ARM",
                                "prima di riposizionare il braccio")

        elif s == State.WAIT:
            if self.now() >= self.wait_until:
                if self.after_wait == "TO_RESET_ARM":
                    if self.start_process(self.move_ee_cmd):
                        self.enter(State.RESET_ARM)
                    else:
                        self.enter(State.ERROR)
                elif self.after_wait == "TO_NEXT":
                    self.advance("OK")

        elif s == State.RESET_ARM:
            res = self.poll_current_process("RESET_ARM")
            if res == "timeout":
                self.enter(State.ERROR)
            elif res == "done":
                # braccio riposizionato -> attesa, poi prossima zona
                self.begin_wait(self.post_arm_wait_s, "TO_NEXT",
                                "prima della prossima goal di Spot")

        elif s == State.DONE:
            self.finish(success=True)

        elif s == State.ERROR:
            self.finish(success=False)

    def do_navigate(self):
        goal = self.goals[self.idx]
        t = self.now()

        # (ri)pubblica la goal: subito all'ingresso, poi ogni republish_s
        # (utile perché goaltospot è fire-and-forget: un re-invio riafferma
        #  lo stesso target). republish_period_s = 0 -> pubblica una volta sola.
        if self.last_republish_t == 0.0 or (
            self.republish_s > 0 and (t - self.last_republish_t) >= self.republish_s
        ):
            self.publish_goal(goal)
            self.last_republish_t = t

        # timeout di navigazione -> salto la zona
        if (t - self.state_entry_t) > self.nav_timeout_s:
            self.get_logger().warn(f"Timeout navigazione (zona {goal['zone']}).")
            return self.advance("SKIP_NAV")

        pose = self.spot_pose()
        if pose is None:
            return  # TF non ancora disponibile: riprovo al prossimo tick
        x, y, yaw = pose
        d = math.hypot(x - goal["x"], y - goal["y"])
        dyaw = abs(angle_diff(yaw, goal["yaw"]))

        if d <= self.pos_tol and dyaw <= self.yaw_tol:
            # richiedo che la condizione sia STABILE per arrival_hold_s
            if self.in_pos_since is None:
                self.in_pos_since = t
            elif (t - self.in_pos_since) >= self.arrival_hold_s:
                self.get_logger().info(
                    f"Arrivato zona {goal['zone']} "
                    f"(d={d:.2f} m, dyaw={math.degrees(dyaw):.1f} deg)."
                )
                if self.start_process(self.nbv_cmd):
                    self.enter(State.RUN_NBV)
                else:
                    self.enter(State.ERROR)
        else:
            self.in_pos_since = None  # uscito dalla tolleranza: azzero il conteggio


def main():
    rclpy.init()
    node = MissionOrchestrator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.kill_proc()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()


# -----------------------------------------------------------------------------
# appunti per il lancio. (occhio se cambio in kinova_explorer_nbv_v3)
#
#   ros2 run kinova_moveit_cpp mission_orchestrator --ros-args \
#     -p csv_path:=/ros2_ws_dev/step12/spot_positions.csv \
#     -p fixed_frame:=spot_odom \
#     -p spot_base_frame:=spot_body
#
# I default puntano a kinova_moveit_cpp / kinova_explorer_nbv_v2 / move_ee

