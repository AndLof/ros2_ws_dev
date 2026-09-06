#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import zlib
import sqlite3
import numpy as np
import scipy.ndimage as ndi

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.lines import Line2D

# ----------------------------------------------------------------------------
# PARAMETRI (tutti regolabili - questo e' il "cervello" del criterio)
# ----------------------------------------------------------------------------
# Criterio: una "zona di interesse" e' una porzione di spazio (libero o non
# osservato) RACCHIUSA dagli ostacoli/muri e collegata alla stanza principale
# solo attraverso un IMBOCCO STRETTO -> un'alcova/nicchia dietro gli arredi,
# difficile da vedere dal centro, dove una persona puo' nascondersi.
MOUTH_MAX_M      = 0.90   # larghezza massima dell'imbocco da "sigillare": piu'
                          # piccola -> solo nicchie molto chiuse; piu' grande ->
                          # anche aree solo parzialmente nascoste.
PERSON_RADIUS_M  = 0.30   # raggio min. del cerchio inscritto (persona accovacciata
                          # ~ disco di 0.40 m di diametro)
MIN_AREA_M2      = 0.13   # area minima della zona
DROP_BORDER      = True   # scarta zone che toccano il bordo mappa (esterno)
SHOW_TRAJECTORY  = False  # disegna la traiettoria di mappatura (contesto)


# ----------------------------------------------------------------------------
# Lettura del database RTAB-Map
# ----------------------------------------------------------------------------
def load_occupancy_grid(db_path):
    """Restituisce (grid, xmin, ymin, res, poses) dalla tabella Admin.

    grid: np.int8 di forma (H, W) con convenzione ROS
          riga -> y (origine in basso), colonna -> x.
    poses: np.float32 (N, 3) traiettoria ottimizzata (x, y, z) o array vuoto.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT opt_map, opt_poses, opt_map_x_min, opt_map_y_min, "
                "opt_map_resolution FROM Admin")
    opt_map, opt_poses, xmin, ymin, res = cur.fetchone()
    conn.close()

    if opt_map is None:
        raise RuntimeError(
            "Admin.opt_map e' vuoto: la mappa non e' stata ottimizzata/salvata. "
            "Apri il .db in rtabmap, esegui 'Edit > Generate 2D occupancy grid' "
            "e ri-salva, oppure ricostruiscila dalle celle per-nodo.")

    raw = np.frombuffer(zlib.decompress(opt_map), dtype=np.int8)

    # La griglia non porta dimensioni esplicite: le ricaviamo fattorizzando
    # il numero di celle in modo che la traiettoria cada sullo spazio libero.
    grid = _reshape_and_orient(raw, opt_poses, xmin, ymin, res)

    poses = np.empty((0, 3), dtype=np.float32)
    if opt_poses is not None:
        p = np.frombuffer(zlib.decompress(opt_poses), dtype=np.float32).reshape(-1, 12)
        poses = np.stack([p[:, 3], p[:, 7], p[:, 11]], axis=1)
    return grid, float(xmin), float(ymin), float(res), poses


def _reshape_and_orient(raw, opt_poses, xmin, ymin, res):
    """Trova forma/orientamento della griglia massimizzando la frazione di
    keyframe della traiettoria che cadono su celle libere."""
    n = raw.size
    # tutte le coppie di fattori (h, w) con h*w == n
    factors = [(h, n // h) for h in range(1, int(n ** 0.5) + 1) if n % h == 0]
    candidates = []
    for h, w in factors:
        candidates += [(h, w), (w, h)]

    if opt_poses is None:
        # senza traiettoria: scegli la forma piu' "quadrata"
        h, w = min(candidates, key=lambda s: abs(s[0] - s[1]))
        return raw.reshape(h, w)

    p = np.frombuffer(zlib.decompress(opt_poses), dtype=np.float32).reshape(-1, 12)
    tx, ty = p[:, 3], p[:, 7]
    best, best_score = None, -1.0
    for (h, w) in candidates:
        grid = raw.reshape(h, w)
        col = ((tx - xmin) / res).astype(int)
        row = ((ty - ymin) / res).astype(int)
        ok = (col >= 0) & (col < w) & (row >= 0) & (row < h)
        if ok.sum() == 0:
            continue
        frac_free = np.mean(grid[row[ok], col[ok]] == 0)
        score = frac_free * (ok.sum() / len(tx))
        if score > best_score:
            best_score, best = score, grid
    return best


# ----------------------------------------------------------------------------
# Rilevamento delle zone di interesse
# ----------------------------------------------------------------------------
def _room_center(free, grid):
    """Centroide del piu' grande spazio libero navigabile (= centro stanza,
    posizione di scansione di Spot allo step 2). Restituisce (row, col) su
    una cella libera."""
    fl, nf = ndi.label(free, structure=ndi.generate_binary_structure(2, 1))
    if nf == 0:
        return (grid.shape[0] / 2.0, grid.shape[1] / 2.0)
    sizes = ndi.sum(np.ones_like(fl), fl, index=range(1, nf + 1))
    biggest = int(np.argmax(sizes)) + 1
    cen = ndi.center_of_mass(fl == biggest)
    cr, cc = int(round(cen[0])), int(round(cen[1]))
    if not free[cr, cc]:                    # snap alla cella libera piu' vicina
        rr, ccol = np.where(fl == biggest)
        j = np.argmin((rr - cr) ** 2 + (ccol - cc) ** 2)
        cr, cc = int(rr[j]), int(ccol[j])
    return (float(cr), float(cc))


def _disk(r):
    """Elemento strutturante a disco di raggio r (in celle)."""
    r = int(r)
    if r < 1:
        return np.array([[1]], dtype=bool)
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return (x * x + y * y) <= r * r


def detect_zones(grid, res):

    free = grid == 0
    occ  = grid == 100
    unk  = grid == -1
    st4 = ndi.generate_binary_structure(2, 1)   # 4-connettivita'
    st8 = ndi.generate_binary_structure(2, 2)   # 8-connettivita'

    # centro stanza = posa di scansione di Spot (step 2 della tesi)
    room_center_rc = _room_center(free, grid)
    cr, cc = int(round(room_center_rc[0])), int(round(room_center_rc[1]))

    # impronta della stanza: celle esplorate (libero|occupato) con i buchi interni
    # riempiti -> include lo sconosciuto realmente RACCHIUSO ed esclude il grande
    # anello sconosciuto esterno (che resta connesso al bordo mappa).
    footprint = ndi.binary_fill_holes(free | occ)

    # sigillatura: chiudo gli ostacoli con un disco di raggio R (= meta' imbocco).
    R = max(1, int(round(MOUTH_MAX_M / 2.0 / res)))
    occ_closed = ndi.binary_closing(occ, structure=_disk(R), border_value=0)

    # spazio aperto dopo aver tappato i varchi stretti, dentro l'impronta stanza
    openspace = (~occ_closed) & footprint

    # componenti connesse (4-conn: l'imbocco tappato separa davvero le regioni)
    lab, nlab = ndi.label(openspace, structure=st4)
    if nlab == 0:
        masks = dict(free=free, occ=occ, unk=unk, footprint=footprint,
                     openspace=openspace, occ_closed=occ_closed,
                     main_region=np.zeros_like(free), alcoves=np.zeros_like(free))
        return [], room_center_rc, masks

    # corpo principale = componente che contiene il centro stanza
    main_lbl = int(lab[cr, cc])
    if main_lbl == 0:                       # centro caduto su cella sigillata
        sizes = ndi.sum(np.ones_like(lab), lab, index=range(1, nlab + 1))
        main_lbl = int(np.argmax(sizes)) + 1
    main_region = (lab == main_lbl)

    # alcove = spazio aperto sigillato diverso dal corpo principale, ricondotto
    # alle celle originali libere o sconosciute (no celle "inventate" dalla chiusura)
    alcove_mask = (lab != main_lbl) & (lab != 0) & (free | unk)

    # rietichetto le alcove (8-conn) e filtro per capienza/posizione
    comp, ncomp = ndi.label(alcove_mask, structure=st8)
    min_area_cells = MIN_AREA_M2 / (res * res)

    H, W = grid.shape
    occ_dil  = ndi.binary_dilation(occ,          structure=st8)

    zones = []
    for k in range(1, ncomp + 1):
        m = comp == k
        ncell = int(m.sum())
        if ncell < min_area_cells:
            continue

        # cerchio massimo inscrivibile nella nicchia (raggio = max distance transform)
        dt = ndi.distance_transform_edt(m) * res
        insc_r = float(dt.max())
        if insc_r < PERSON_RADIUS_M:
            continue

        rr, ccl = np.where(m)
        touches_border = (rr.min() == 0 or ccl.min() == 0 or
                          rr.max() == H - 1 or ccl.max() == W - 1)
        if DROP_BORDER and touches_border:     # tocca il bordo -> "esterno", scarta
            continue

        # statistiche di bordo (per il CSV / trasparenza del criterio):
        # quanta parte del contorno tocca ostacoli e quanta affaccia sulla stanza.
        border = m & ~ndi.binary_erosion(m, structure=st8)
        nb = max(int(border.sum()), 1)
        f_obst = float((border & occ_dil).sum()) / nb
        frac_unknown = float((m & unk).sum()) / ncell    # quota mai osservata direttamente

        r_peak, c_peak = np.unravel_index(np.argmax(dt), dt.shape)
        zones.append(dict(
            cells=ncell,
            area_m2=ncell * res * res,
            inscribed_r=insc_r,
            f_obst=f_obst,
            frac_unknown=frac_unknown,     # quota di celle non osservate (0..1)
            row=float(r_peak), col=float(c_peak),     # punto piu' profondo (centro disco)
            row_cen=float(rr.mean()), col_cen=float(ccl.mean()),
            bbox=(int(rr.min()), int(rr.max()), int(ccl.min()), int(ccl.max())),
            rows=rr, cols=ccl,                         # celle della nicchia (per il fill)
        ))

    # ordina per capienza: prima le nicchie con cerchio inscritto piu' grande
    zones.sort(key=lambda z: (z["inscribed_r"], z["area_m2"]), reverse=True)

    masks = dict(free=free, occ=occ, unk=unk, footprint=footprint,
                 openspace=openspace, occ_closed=occ_closed,
                 main_region=main_region, alcoves=alcove_mask)
    return zones, room_center_rc, masks


# ----------------------------------------------------------------------------
# Conversione celle <-> coordinate mondo
# ----------------------------------------------------------------------------
def cell_to_world(row, col, xmin, ymin, res):
    x = xmin + (col + 0.5) * res
    y = ymin + (row + 0.5) * res
    return x, y


# ----------------------------------------------------------------------------
# Output
# ----------------------------------------------------------------------------
def render_png(grid, xmin, ymin, res, zones, room_center_rc, poses, out_png):
    H, W = grid.shape
    extent = [xmin, xmin + W * res, ymin, ymin + H * res]

    disp = np.full(grid.shape, 0.75)   # sconosciuto = grigio chiaro
    disp[grid == 0] = 1.0              # libero = bianco
    disp[grid == 100] = 0.0           # occupato = nero

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(disp, cmap="gray", origin="lower", extent=extent,
              interpolation="nearest", vmin=0, vmax=1)

    if SHOW_TRAJECTORY and len(poses):
        ax.plot(poses[:, 0], poses[:, 1], "-", color="#3aa0ff",
                lw=0.8, alpha=0.4, zorder=2)

    # zone di interesse: riempimento rosso traslucido (forma reale) + cerchietto
    # sul punto piu' profondo + numero
    overlay = np.zeros((H, W, 4), dtype=float)
    for z in zones:
        overlay[z["rows"], z["cols"]] = (1.0, 0.0, 0.0, 0.45)
    ax.imshow(overlay, origin="lower", extent=extent,
              interpolation="nearest", zorder=4)

    for i, z in enumerate(zones, start=1):
        x, y = cell_to_world(z["row"], z["col"], xmin, ymin, res)
        # cerchietto modesto attorno al punto piu' profondo (= cerchio inscritto)
        rad = max(z["inscribed_r"], 0.30)
        ax.add_patch(Circle((x, y), rad, fill=False, edgecolor="red",
                            lw=2.0, zorder=5))
        ax.text(x, y, str(i), color="red", fontsize=11, fontweight="bold",
                ha="center", va="center", zorder=6,
                bbox=dict(boxstyle="circle,pad=0.12", fc="white",
                          ec="red", lw=1.2))

    # Spot al centro stanza (pallino blu)
    sx, sy = cell_to_world(room_center_rc[0], room_center_rc[1], xmin, ymin, res)
    ax.plot(sx, sy, "o", color="#1565ff", ms=14, mec="white", mew=1.6, zorder=7)
    ax.text(sx, sy - 0.35, "SPOT", color="#1565ff", fontsize=10,
            fontweight="bold", ha="center", va="top", zorder=7)

    ax.set_xlabel("x [m]"); ax.set_ylabel("y [m]")
    ax.set_title("Zone di interesse (regioni nascoste) - mappa laboratorio")
    ax.set_aspect("equal")
    ax.grid(True, color="0.85", lw=0.5)

    legend = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor="#1565ff",
               markersize=11, label="Spot (centro stanza)"),
        matplotlib.patches.Patch(facecolor=(1, 0, 0, 0.45), edgecolor="red",
                                 label="Zona di interesse"),
        matplotlib.patches.Patch(facecolor="white", edgecolor="0.6", label="libero"),
        matplotlib.patches.Patch(facecolor="black", label="ostacolo"),
        matplotlib.patches.Patch(facecolor="0.75", label="sconosciuto"),
    ]
    ax.legend(handles=legend, loc="upper right", fontsize=9, framealpha=0.9)
    fig.savefig(out_png, dpi=130, bbox_inches="tight")
    plt.close(fig)
    return (sx, sy)


def write_csv(zones, spot_xy, xmin, ymin, res, out_csv):
    import csv
    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "type", "x_m", "y_m", "area_m2",
                    "inscribed_radius_m", "n_cells",
                    "obstacle_border_frac", "unknown_frac"])
        w.writerow(["SPOT", "robot_start", round(spot_xy[0], 4),
                    round(spot_xy[1], 4), "", "", "", "", ""])
        for i, z in enumerate(zones, start=1):
            x, y = cell_to_world(z["row"], z["col"], xmin, ymin, res)
            w.writerow([i, "zone_of_interest", round(x, 4), round(y, 4),
                        round(z["area_m2"], 3), round(z["inscribed_r"], 3),
                        z["cells"], round(z["f_obst"], 3),
                        round(z["frac_unknown"], 3)])


# ----------------------------------------------------------------------------
def main():
    db_path = sys.argv[1] if len(sys.argv) > 1 else \
        "/mnt/user-data/uploads/rtabmap_lab_spot_moving.db"
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    os.makedirs(out_dir, exist_ok=True)

    grid, xmin, ymin, res, poses = load_occupancy_grid(db_path)
    print(f"Mappa {grid.shape}  res={res:.3f} m  "
          f"libero={int((grid==0).sum())} occ={int((grid==100).sum())} "
          f"unk={int((grid==-1).sum())}")

    zones, room_center_rc, masks = detect_zones(grid, res)
    print(f"Tasche interne sconosciute totali considerate; "
          f"zone di interesse trovate: {len(zones)}")

    out_png = os.path.join(out_dir, "zones_of_interest.png")
    out_csv = os.path.join(out_dir, "zones_of_interest.csv")
    spot_xy = render_png(grid, xmin, ymin, res, zones, room_center_rc, poses, out_png)
    write_csv(zones, spot_xy, xmin, ymin, res, out_csv)

    print(f"Spot (centro stanza): x={spot_xy[0]:.3f}  y={spot_xy[1]:.3f}")
    for i, z in enumerate(zones, start=1):
        x, y = cell_to_world(z["row"], z["col"], xmin, ymin, res)
        print(f"  Zona {i}: x={x:6.2f} y={y:6.2f}  area={z['area_m2']:.2f} m^2  "
              f"r_inscr={z['inscribed_r']:.2f} m  f_obst={z['f_obst']:.2f}")
    print(f"\nScritti:\n  {out_png}\n  {out_csv}")


if __name__ == "__main__":
    main()
