#!/usr/bin/env python3
"""Render the actual OpenSCAD assembly meshes with optional matplotlib/numpy."""
import argparse
import json
from pathlib import Path
import re


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--meshes", type=Path, default=Path("build"))
    parser.add_argument("--out", type=Path, default=Path("Design/Parametric/Preview.png"))
    args = parser.parse_args()
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    root = Path(__file__).resolve().parents[1]
    report = json.loads((root/"Design/Parametric/Generated/fit-report.json").read_text())
    p = report["parameters_mm"]
    fig = plt.figure(figsize=(16, 10), facecolor="#0c151b")
    fig.text(.055, .94, "MJOLNIR / HUSKYNARR", color="#edf4e4", fontsize=25, weight="bold")
    fig.text(.055, .901, "Parametrisches Baugruppenmodell  |  mechanischer Front-Einstieg", color="#a9bbb7", fontsize=13)
    fig.text(.055, .858, "KONZEPT - 1660 mm angegeben; weitere Koerpermasse synthetisch", color="#ffca74", fontsize=12)
    for index, (name, title) in enumerate((("assembly-closed", "01  GESCHLOSSEN"), ("assembly-open", "02  AUSGEFAHREN + GEOEFFNET"))):
        text = (args.meshes/f"{name}.stl").read_text()
        values = re.findall(r"vertex\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)", text)
        if not values or len(values) % 3:
            raise ValueError("Expected non-empty ASCII STL")
        mesh = np.array(values, dtype=float).reshape(-1, 3, 3)
        if not np.isfinite(mesh).all():
            raise ValueError("Non-finite mesh")
        normals = np.cross(mesh[:, 1]-mesh[:, 0], mesh[:, 2]-mesh[:, 0])
        normals /= np.maximum(np.linalg.norm(normals, axis=1, keepdims=True), 1e-12)
        shade = .55 + .45*np.abs(normals @ np.array([.3, -.6, .74]))
        colors = np.tile(np.array([.43,.53,.31]), (len(mesh),1))*shade[:,None]
        centroid = mesh.mean(axis=1)
        frame = centroid[:,1] > p["torso_depth"]/2+12
        colors[frame] = np.array([.2,.61,.65])*shade[frame,None]
        # Approximate cosmetic colouring only; mesh itself comes directly from CAD.
        visor = (centroid[:,2] > p["body_height"]*.49+70+p["torso_height"]+45+p["helmet_height"]*.47) & (centroid[:,1] < -p["helmet_depth"]/2+2)
        colors[visor] = np.array([.85,.58,.22])*shade[visor,None]
        ax = fig.add_axes([.015+index*.49,.15,.49,.70], projection="3d", facecolor="#0c151b")
        ax.add_collection3d(Poly3DCollection(mesh, facecolors=colors, edgecolors="none", linewidths=0))
        ax.set(xlim=(-700,700), ylim=(-650,500), zlim=(0,1700))
        ax.set_box_aspect((1400,1150,1700))
        ax.set_proj_type("ortho")
        ax.view_init(elev=13, azim=-71)
        ax.set_axis_off()
        fig.text(.16+index*.49,.14,title,color="#edf4e4",fontsize=13,weight="bold")
    fig.text(.055,.077,"Originale Konzeptgeometrie aus MjolnirEntry.scad. Keine finale Halo-Oberflaeche oder Fertigungsfreigabe.", color="#b4c1bd",fontsize=11)
    fig.text(.055,.044,"Offen: persoenliche Masse, 3D-Kollisionen, echte Gelenke/Fuehrungen, Verschluesse und physische Last-/Passprobe.",color="#b4c1bd",fontsize=11)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out, dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(args.out)


if __name__ == "__main__":
    main()
