#!/usr/bin/env python3
"""Render every ASCII STL of a directory as an overview grid; requires matplotlib/numpy.

Beispiele:
  python3 Design/Armor/RenderPreview.py --stl-dir Design/Armor/STL \
      --output Design/Armor/Preview.png --title "MJOLNIR / RUESTUNGSHUELLEN"
  python3 Design/Armor/RenderPreview.py --stl-dir Design/Props/CortanaChip/STL \
      --output Design/Props/CortanaChip/Preview.png --title "CORTANA-CHIP" --columns 2
"""
import argparse
import math
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

BACKGROUND, MUTED, TEXT, ACCENT = '#101923', '#96adbb', '#e7f0f4', '#edbb5f'
COLOR = np.array([.47, .58, .40])
ELEVATION, AZIMUTH = 24, -58


def load(path):
    vertices = [list(map(float, line.split()[1:])) for line in path.read_text('ascii').splitlines()
                if line.lstrip().startswith('vertex ')]
    faces = np.asarray(vertices).reshape((-1, 3, 3))
    if not len(faces):
        raise ValueError('Empty STL: ' + str(path))
    return faces


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--stl-dir', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--title', default='MJOLNIR / RUESTUNGSHUELLEN')
    parser.add_argument('--columns', type=int, default=6)
    args = parser.parse_args()
    files = sorted(args.stl_dir.glob('*.stl'))
    if not files:
        raise SystemExit('No STL files in ' + str(args.stl_dir))
    columns = max(1, min(args.columns, len(files)))
    rows = math.ceil(len(files) / columns)
    fig = plt.figure(figsize=(3.2 * columns, 3.6 * rows + 1.6), facecolor=BACKGROUND)
    head = 1.1 / fig.get_figheight()
    foot = .5 / fig.get_figheight()
    fig.text(.03, 1 - head * .5, args.title, color=TEXT, size=22, weight='bold', va='center')
    fig.text(.97, 1 - head * .5, 'KONSTRUKTIONSMODELL / KEINE PASSFREIGABE', color=ACCENT, size=9,
             ha='right', va='center')
    fig.text(.03, foot * .4, f'{len(files)} Teile aus {args.stl_dir.as_posix()}  |  '
             'Ansichten haben unterschiedliche Massstaebe', color=MUTED, size=9)
    light = np.array([-.4, -.5, .9])
    light /= np.linalg.norm(light)
    elevation, azimuth = np.deg2rad(ELEVATION), np.deg2rad(AZIMUTH)
    view = np.array([np.cos(elevation) * np.cos(azimuth), np.cos(elevation) * np.sin(azimuth), np.sin(elevation)])
    cell_w = .94 / columns
    cell_h = (1 - head - foot) / rows
    for index, path in enumerate(files):
        faces = load(path)
        normal = np.cross(faces[:, 1] - faces[:, 0], faces[:, 2] - faces[:, 0])
        lengths = np.linalg.norm(normal, axis=1)
        keep = lengths > 0
        faces, normal = faces[keep], normal[keep] / lengths[keep][:, None]
        # Shells are open: draw both sides, inner faces darker.
        facing = normal @ view
        shade = .30 + .70 * np.abs(normal @ light)
        shade = np.where(facing > 0, shade, shade * .55)
        # No depth buffer: back faces first, then front faces, each far to near.
        order = np.lexsort((faces.mean(axis=1) @ view, facing > 0))
        row, col = divmod(index, columns)
        x = .03 + col * cell_w
        y = 1 - head - (row + 1) * cell_h
        ax = fig.add_axes([x, y + cell_h * .12, cell_w, cell_h * .76], projection='3d', facecolor=BACKGROUND)
        ax.add_collection3d(Poly3DCollection(faces[order], facecolors=np.clip(shade[order, None] * COLOR, 0, 1),
                                             linewidths=0, edgecolors='none', antialiased=False))
        points = faces.reshape((-1, 3))
        low, high = points.min(axis=0), points.max(axis=0)
        span, center, radius = high - low, (low + high) / 2, max(high - low) * .54
        ax.set_xlim(center[0] - radius, center[0] + radius)
        ax.set_ylim(center[1] - radius, center[1] + radius)
        ax.set_zlim(center[2] - radius, center[2] + radius)
        ax.set_box_aspect((1, 1, 1))
        ax.view_init(elev=ELEVATION, azim=AZIMUTH)
        ax.set_proj_type('ortho')
        ax.set_axis_off()
        fig.text(x + .008, y + cell_h * .92, f'{index + 1:02d}  {path.stem.upper()}', color=TEXT, size=9.5,
                 weight='bold')
        fig.text(x + .008, y + cell_h * .05, ' x '.join(f'{value:.0f}' for value in span) + ' mm',
                 color=MUTED, size=8)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=110, facecolor=BACKGROUND)
    plt.close(fig)


if __name__ == '__main__':
    main()
