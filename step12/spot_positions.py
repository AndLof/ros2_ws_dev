#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
import math
import argparse
import numpy as np
from PIL import Image
from scipy import ndimage
import cv2

# =============================================================================
#  PARAMETRI (tutti modificabili)
# =============================================================================

# --- Geometria della ricerca ---
#N_DIRECTIONS      = 16                # numero di direzioni equidistanti
N_DIRECTIONS      = 24
ANGLE_OFFSET_DEG  = 0.0               # sfasamento del ventaglio di direzioni
#DISTANCES_M       = [1.0, 1.5, 2.0, 2.5, 3.0]   # distanze candidate dal centro zona [m]
DISTANCES_M       = [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0]
# --- Ingombro di Spot (footprint del rettangolino) ---
SPOT_LENGTH_M     = 1.10              # lunghezza corpo Spot [m]
SPOT_WIDTH_M      = 0.50              # larghezza corpo Spot [m]
FOOTPRINT_INFLATION_M = 0.0           # margine di sicurezza aggiunto attorno [m]

# --- FOV per il tie-break (parametri dinamici) ---
FOV_RANGE_M       = 3.0              # portata della FOV [m]
FOV_HALF_ANGLE_DEG= 35.0             # semi-apertura della FOV [deg]
W_COVERAGE        = 1.0             # peso: copertura zona nella FOV (da massimizzare)
W_OBSTACLE        = 1.0             # peso: ostacoli frontali nella FOV (da minimizzare)

# --- Validita' ---
FREE_ONLY         = True             # posa valida SOLO se il footprint e' tutto su BIANCO (libero)
ALLOW_UNKNOWN_GROUND = False         # se True (con FREE_ONLY), lo "sconosciuto" e' calpestabile
                                     #   (bloccano solo nero-ostacolo e rosa-zona). Pose piu' vicine
                                     #   ma NON garantite raggiungibili da Nav2 (spazio non noto).
BLOCK_UNKNOWN     = False            # (solo se FREE_ONLY=False) se True, il grigio sconosciuto blocca
UNKNOWN_GRAY      = 192              # valore RGB del grigio "sconosciuto" (riempimento pieno)

# --- Pulizia opzionale della maschera ostacoli (0 = disattivata, per aderire allo spec) ---
MIN_OBSTACLE_COMP_PX = 0            # rimuove componenti nere piu' piccole di N px (speckle)
OBSTACLE_OPEN_KERNEL = 0            # apertura morfologica k x k (0/1 = off) per togliere linee sottili

# --- Calibrazione (None = auto-detect dall'immagine) ---
PX_PER_METER      = None            # scala px/m; None -> stimata dalle griglie
ORIGIN_PX         = None            # (x,y) pixel dell'origine (0,0); None -> pallino blu

# --- CSV opzionale delle zone dal "primo codice" (piu' preciso della detection) ---
# Se fornito, deve avere colonne con centro in metri. Colonne accettate:
#   id (opz.), x_m, y_m   (oppure  x, y).
ZONES_CSV_IN      = None

# --- Soglie colore (RGB) ---
def m_black(R,G,B):  return (R<80)&(G<80)&(B<80)
def m_white(R,G,B):  return (R>238)&(G>238)&(B>238)
def m_blue(R,G,B):   return (B>150)&(R<110)&(G<130)
def m_red(R,G,B):    return (R>150)&(G<95)&(B<95)
def m_pink(R,G,B):   return (R>200)&(G>110)&(G<205)&(B>110)&(B<205)&(R>G+25)
def m_graybg(R,G,B): return (abs(R-G)<14)&(abs(G-B)<14)&(R>150)&(R<220)
def m_unknown(R,G,B):return (abs(R-UNKNOWN_GRAY)<=3)&(abs(G-UNKNOWN_GRAY)<=3)&(abs(B-UNKNOWN_GRAY)<=3)

# --- Disegno ---
COL_FILL   = (60, 120, 235)   # blu chiaro (RGB) riempimento footprint
COL_EDGE   = (10,  40, 150)   # blu scuro bordo
COL_ARROW  = (10,  30, 110)   # freccia
FILL_ALPHA = 0.35

# =============================================================================
#  UTILITY DI PARSING DELLA MAPPA
# =============================================================================

def detect_plot_frame(black):
    """Rileva il rettangolo degli assi (spines nere continue)."""
    H, W = black.shape
    colsum = black.sum(0); rowsum = black.sum(1)
    cols = np.where(colsum > 0.6*H)[0]
    rows = np.where(rowsum > 0.6*W)[0]
    L, Rt = int(cols.min()), int(cols.max())
    T, Bt = int(rows.min()), int(rows.max())
    return L, Rt, T, Bt

def detect_legend_bbox(a, L, Rt, T):
    """Rileva il riquadro della legenda (rettangolo bianco in alto a destra)."""
    R,G,B = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
    white = (R>245)&(G>245)&(B>245)
    x0 = L + int(0.62*(Rt-L))                 # cerca solo nel settore alto-destra
    sub = np.zeros_like(white)
    sub[T:T+int(0.55*(a.shape[0]-T)), x0:Rt] = white[T:T+int(0.55*(a.shape[0]-T)), x0:Rt]
    lbl, n = ndimage.label(sub)
    best = None
    for i in range(1, n+1):
        ys, xs = np.where(lbl==i)
        if len(xs) < 1500:
            continue
        if best is None or len(xs) > best[0]:
            best = (len(xs), (xs.min(), xs.max(), ys.min(), ys.max()))
    if best is None:
        return None
    xmin,xmax,ymin,ymax = best[1]
    pad = 14
    # estende un po' verso il basso per includere le voci impilate
    return (max(L,xmin-pad), min(Rt,xmax+pad), max(T,ymin-pad), ymax+int(0.9*(ymax-ymin))+pad)

def detect_scale_px_per_m(a, L, Rt, T, Bt):
    """Stima px/m dalla spaziatura delle griglie (linee grigio ~196)."""
    R,G,B = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
    grid = (abs(R-196)<12)&(abs(G-196)<12)&(abs(B-196)<12)
    def positions(line):
        idx = np.where(line)[0]
        if len(idx)==0: return []
        cl=[]; s=p=idx[0]
        for v in idx[1:]:
            if v-p>4: cl.append((s+p)/2); s=v
            p=v
        cl.append((s+p)/2); return cl
    diffs=[]
    for y in range(T+10, Bt-10, 3):
        d = np.diff(positions(grid[y, L+3:Rt-3]))
        diffs += [x for x in d if 95<x<128]
    for x in range(L+10, Rt-10, 3):
        d = np.diff(positions(grid[T+3:Bt-3, x]))
        diffs += [v for v in d if 95<v<128]
    if len(diffs) < 5:
        raise RuntimeError("Impossibile stimare la scala dalle griglie; imposta PX_PER_METER a mano.")
    return float(np.median(diffs))

def detect_origin_px(a, legend_bbox):
    """Origine (0,0) = pallino blu di Spot (il piu' grande, fuori dalla legenda)."""
    R,G,B = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
    blue = m_blue(R,G,B)
    lbl,n = ndimage.label(blue)
    best=None
    for i in range(1,n+1):
        ys,xs=np.where(lbl==i)
        cx,cy=xs.mean(),ys.mean()
        if legend_bbox and (legend_bbox[0]<=cx<=legend_bbox[1] and legend_bbox[2]<=cy<=legend_bbox[3]):
            continue
        if best is None or len(xs)>best[0]:
            best=(len(xs),(cx,cy))
    if best is None:
        raise RuntimeError("Pallino blu (origine) non trovato; imposta ORIGIN_PX a mano.")
    return best[1]

def detect_zone_centers(a, legend_bbox):
    """Centri zona = cerchietti rossi (componenti rosse grandi = gli anelli)."""
    R,G,B = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
    red = m_red(R,G,B)
    lbl,n = ndimage.label(red)
    centers=[]
    for i in range(1,n+1):
        ys,xs=np.where(lbl==i)
        if len(xs) < 600:          # scarta le cifre (piccole) e il rumore
            continue
        cx,cy=xs.mean(),ys.mean()
        if legend_bbox and (legend_bbox[0]<=cx<=legend_bbox[1] and legend_bbox[2]<=cy<=legend_bbox[3]):
            continue
        rad=((xs.max()-xs.min())+(ys.max()-ys.min()))/4.0
        centers.append((cx,cy,rad))
    return centers

# =============================================================================
#  GEOMETRIA POSE / COLLISIONE / FOV
# =============================================================================

def rect_corners(cx, cy, length, width, yaw):
    """4 vertici del rettangolo (footprint) centrato in (cx,cy), asse lungo = yaw."""
    fx, fy = math.cos(yaw), math.sin(yaw)          # avanti (in spazio-immagine)
    lx, ly = -fy, fx                                # sinistra
    hl, hw = length/2.0, width/2.0
    pts=[]
    for sl, sw in [(+1,+1),(+1,-1),(-1,-1),(-1,+1)]:
        pts.append((cx + sl*hl*fx + sw*hw*lx,
                    cy + sl*hl*fy + sw*hw*ly))
    return np.array(pts, dtype=np.float32)

def footprint_ok(corners, obstacle, nogo):
    """True se il footprint non tocca ostacoli ne' zone vietate (fuori mappa/legenda)."""
    H,W = obstacle.shape
    x0=int(np.floor(corners[:,0].min())); x1=int(np.ceil(corners[:,0].max()))
    y0=int(np.floor(corners[:,1].min())); y1=int(np.ceil(corners[:,1].max()))
    if x0<0 or y0<0 or x1>=W or y1>=H:
        return False
    mask = np.zeros((y1-y0+1, x1-x0+1), np.uint8)
    poly = (corners - [x0,y0]).astype(np.int32)
    cv2.fillConvexPoly(mask, poly, 1)
    m = mask.astype(bool)
    if nogo[y0:y1+1, x0:x1+1][m].any():
        return False
    if obstacle[y0:y1+1, x0:x1+1][m].any():
        return False
    return True

def fov_score(cx, cy, yaw, zone_mask, zone_total, obstacle, range_px, half_ang):
    """Ritorna (coverage_frac, obstacle_frac) per la FOV a settore."""
    H,W = obstacle.shape
    x0=max(0,int(cx-range_px)); x1=min(W,int(cx+range_px)+1)
    y0=max(0,int(cy-range_px)); y1=min(H,int(cy+range_px)+1)
    yy,xx = np.mgrid[y0:y1, x0:x1]
    dx = xx-cx; dy = yy-cy
    dist = np.hypot(dx,dy)
    ang = np.arctan2(dy,dx)
    dang = np.abs((ang-yaw+math.pi) % (2*math.pi) - math.pi)
    insec = (dist<=range_px)&(dang<=half_ang)
    nsec = int(insec.sum())
    if nsec==0:
        return 0.0, 0.0
    cov = int((zone_mask[y0:y1, x0:x1] & insec).sum())
    obs = int((obstacle[y0:y1, x0:x1]  & insec).sum())
    coverage_frac = cov/float(zone_total) if zone_total>0 else 0.0
    obstacle_frac = obs/float(nsec)
    return coverage_frac, obstacle_frac

# =============================================================================
#  DRAW
# =============================================================================

def draw_pose(canvas, cx, cy, corners, yaw, length_px):
    overlay = canvas.copy()
    poly = corners.astype(np.int32)
    cv2.fillConvexPoly(overlay, poly, COL_FILL)
    cv2.addWeighted(overlay, FILL_ALPHA, canvas, 1-FILL_ALPHA, 0, canvas)
    cv2.polylines(canvas, [poly], True, COL_EDGE, 2, cv2.LINE_AA)
    tip = (int(cx+0.5*length_px*math.cos(yaw)), int(cy+0.5*length_px*math.sin(yaw)))
    cv2.arrowedLine(canvas, (int(cx),int(cy)), tip, COL_ARROW, 2, cv2.LINE_AA, tipLength=0.35)

# =============================================================================
#  MAIN
# =============================================================================

def run(in_png, out_png, out_csv):
    img = Image.open(in_png).convert("RGB")
    a = np.array(img)
    H,W,_ = a.shape
    R,G,B = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)

    # --- parsing mappa ---
    black = m_black(R,G,B)
    L,Rt,T,Bt = detect_plot_frame(black)
    legend = detect_legend_bbox(a, L, Rt, T)
    scale  = PX_PER_METER if PX_PER_METER else detect_scale_px_per_m(a, L, Rt, T, Bt)
    origin = ORIGIN_PX if ORIGIN_PX else detect_origin_px(a, legend)
    ox, oy = origin

    # --- maschere ---
    m = 3  # margine per escludere i bordi del frame
    playable = np.zeros((H,W), bool)
    playable[T+m:Bt-m, L+m:Rt-m] = True
    if legend:
        lx0,lx1,ly0,ly1 = legend
        playable[ly0:ly1+1, lx0:lx1+1] = False
    nogo = ~playable

    # --- maschera "ostacoli" per la collisione del footprint ---
    obstacle = black & playable
    # pulizia opzionale del nero (di default disattivata)
    if OBSTACLE_OPEN_KERNEL and OBSTACLE_OPEN_KERNEL > 1:
        k = np.ones((OBSTACLE_OPEN_KERNEL, OBSTACLE_OPEN_KERNEL), np.uint8)
        obstacle = cv2.morphologyEx(obstacle.astype(np.uint8), cv2.MORPH_OPEN, k).astype(bool)
    if MIN_OBSTACLE_COMP_PX and MIN_OBSTACLE_COMP_PX > 1:
        lbl_o, no = ndimage.label(obstacle, structure=np.ones((3,3)))
        if no > 0:
            sz = ndimage.sum(np.ones_like(lbl_o), lbl_o, range(1, no+1))
            keep = np.zeros(no+1, bool); keep[1:] = np.array(sz) >= MIN_OBSTACLE_COMP_PX
            obstacle = keep[lbl_o]

    pink = m_pink(R,G,B) & playable

    if FREE_ONLY:
        # posa valida SOLO su bianco: bloccano nero, sconosciuto (192), zona (rosa) e i cerchietti rossi.
        # Le griglie (196/220) NON bloccano perche' fuori dalla banda dello sconosciuto.
        red     = m_red(R,G,B) & playable
        blocked = obstacle | pink | red
        if not ALLOW_UNKNOWN_GROUND:
            blocked = blocked | (m_unknown(R,G,B) & playable)
    else:
        blocked = obstacle
        if BLOCK_UNKNOWN:
            blocked = blocked | (m_unknown(R,G,B) & playable)

    # --- centri zona ---
    if ZONES_CSV_IN and os.path.exists(ZONES_CSV_IN):
        zones = []
        with open(ZONES_CSV_IN, newline="") as f:
            rd = csv.DictReader(f)
            for row in rd:
                if row.get("type") and row["type"] != "zone_of_interest":
                    continue                       # salta la riga SPOT/robot_start
                try:
                    zid = int(float(row["id"]))    # salta id non numerici (es. 'SPOT')
                except (ValueError, KeyError, TypeError):
                    continue
                xk = "x_m" if "x_m" in row else ("x" if "x" in row else None)
                yk = "y_m" if "y_m" in row else ("y" if "y" in row else None)
                xm, ym = float(row[xk]), float(row[yk])
                try:
                    rad = float(row["inscribed_radius_m"])*scale
                except (ValueError, KeyError, TypeError):
                    rad = 0.4*scale
                cx = ox + xm*scale; cy = oy - ym*scale
                zones.append((cx, cy, rad, zid))
    else:
        det = detect_zone_centers(a, legend)
        # ordina in senso orario partendo da Est (deterministico) e assegna id 1..N
        det.sort(key=lambda c: math.atan2(c[1]-oy, c[0]-ox))
        zones = [(cx,cy,rad,None) for (cx,cy,rad) in det]

    # --- assegna i pixel pink alla zona piu' vicina (per la copertura FOV) ---
    zc = np.array([[z[0],z[1]] for z in zones])
    ys,xs = np.where(pink)
    zone_pink_masks=[]
    if len(xs)>0 and len(zc)>0:
        d2 = (xs[:,None]-zc[None,:,0])**2 + (ys[:,None]-zc[None,:,1])**2
        assign = d2.argmin(1)
    for k in range(len(zones)):
        zm = np.zeros((H,W), bool)
        if len(xs)>0:
            sel = assign==k
            zm[ys[sel], xs[sel]] = True
        zone_pink_masks.append(zm)

    # --- parametri in pixel ---
    Lpx = (SPOT_LENGTH_M + 2*FOOTPRINT_INFLATION_M)*scale
    Wpx = (SPOT_WIDTH_M  + 2*FOOTPRINT_INFLATION_M)*scale
    fov_range_px = FOV_RANGE_M*scale
    fov_half = math.radians(FOV_HALF_ANGLE_DEG)
    dirs = [math.radians(ANGLE_OFFSET_DEG + k*360.0/N_DIRECTIONS) for k in range(N_DIRECTIONS)]

    canvas = a.copy()
    results = []

    for k,(cx,cy,rad,zid) in enumerate(zones):
        zone_id = zid if zid is not None else (k+1)
        zmask = zone_pink_masks[k]
        ztot  = int(zmask.sum())
        chosen = None

        for d in DISTANCES_M:                      # ciclo per distanza crescente
            dpx = d*scale
            valid=[]
            for th in dirs:                        # ciclo completo su tutte le direzioni
                px = cx + dpx*math.cos(th)
                py = cy + dpx*math.sin(th)
                yaw = math.atan2(cy-py, cx-px)     # guarda il centro zona
                corners = rect_corners(px, py, Lpx, Wpx, yaw)
                if not footprint_ok(corners, blocked, nogo):
                    continue
                cov, obs = fov_score(px,py,yaw, zmask, ztot, obstacle, fov_range_px, fov_half)
                score = W_COVERAGE*cov - W_OBSTACLE*obs
                valid.append(dict(px=px,py=py,yaw=yaw,d=d,dir=math.degrees(th)%360,
                                  corners=corners,cov=cov,obs=obs,score=score))
            if valid:                              # primo ciclo con pose valide vince
                chosen = max(valid, key=lambda v: v["score"])
                break

        # --- registra e disegna ---
        if chosen:
            px,py = chosen["px"], chosen["py"]
            xm = (px-ox)/scale; ym = -(py-oy)/scale
            # Convenzione yaw richiesta: SINISTRA=0, BASSO=90, DESTRA=180, ALTO=270.
            # La geometria interna usa Est=0 (spazio-immagine); qui rimappo: yaw_user = (180 - yaw_geom) mod 360.
            yaw_deg = (180.0 - math.degrees(chosen["yaw"])) % 360.0
            draw_pose(canvas, px, py, chosen["corners"], chosen["yaw"], Lpx)
            cv2.putText(canvas, str(zone_id), (int(px)+8, int(py)-8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, COL_EDGE, 2, cv2.LINE_AA)
            results.append([zone_id, round((cx-ox)/scale,3), round(-(cy-oy)/scale,3),
                            round(xm,3), round(ym,3), round(yaw_deg,1),
                            chosen["d"], round(chosen["dir"],1),
                            int(round(px)), int(round(py)),
                            round(chosen["cov"],4), round(chosen["obs"],4), True])
        else:
            results.append([zone_id, round((cx-ox)/scale,3), round(-(cy-oy)/scale,3),
                            "", "", "", "", "", "", "", "", "", False])

    # --- salva PNG ---
    Image.fromarray(canvas).save(out_png)

    # --- salva CSV ---
    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["zone_id","zone_x_m","zone_y_m",
                    "pose_x_m","pose_y_m","yaw_deg","distance_m","direction_deg",
                    "pose_x_px","pose_y_px","fov_coverage_frac","fov_obstacle_frac","valid"])
        w.writerows(results)

    # --- report a video ---
    print(f"Frame assi: x[{L},{Rt}] y[{T},{Bt}]  |  origine px=({ox:.1f},{oy:.1f})  |  scala={scale:.2f} px/m")
    if legend: print(f"Legenda mascherata: x[{legend[0]},{legend[1]}] y[{legend[2]},{legend[3]}]")
    id_src = "CSV primo codice" if (ZONES_CSV_IN and os.path.exists(ZONES_CSV_IN)) else \
             "assegnati per posizione (NON coincidono con i numeri disegnati: usa ZONES_CSV_IN per averli esatti)"
    print(f"Zone trovate: {len(zones)}  |  id: {id_src}")
    print(f"direzioni={N_DIRECTIONS}  distanze={DISTANCES_M} m")
    for r in results:
        if r[-1]:
            print(f"  zona {r[0]}: pose=({r[3]:+.2f},{r[4]:+.2f}) m yaw={r[5]}deg "
                  f"d={r[6]}m dir={r[7]}deg cov={r[10]} obs={r[11]}")
        else:
            print(f"  zona {r[0]}: NESSUNA posa valida (prova ad aumentare le distanze o ridurre l'ingombro)")
    print(f"\nOutput:\n  {out_png}\n  {out_csv}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i","--input",  default="zones_of_interest.png")
    ap.add_argument("-o","--output", default="spot_positions.png")
    ap.add_argument("-c","--csv",    default="spot_positions.csv")
    ap.add_argument("-z","--zones",  default=None, help="CSV zone dal primo codice (id,x_m,y_m)")
    args = ap.parse_args()
    if args.zones:
        ZONES_CSV_IN = args.zones
    run(args.input, args.output, args.csv)
