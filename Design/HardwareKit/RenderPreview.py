#!/usr/bin/env python3
"""Render the actual ASCII-STL parts as an overview; requires matplotlib/numpy."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stl-dir', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    manifest = json.loads((Path(__file__).parent / 'Manifest.json').read_text())
    background = '#101923'
    muted = '#96adbb'
    text = '#e7f0f4'
    accent = '#edbb5f'
    colors = {'powerbank': '#67b8c4', 'transmitter': '#9abe78',
              'camera': '#90b7dd', 'hud': '#edbb5f', 'nozzle': '#77c5bb',
              'controller': '#7b9ecd'}
    titles = {'powerbank_base': ('POWERBANK', 'Offener Gurttraeger'),
              'transmitter_base': ('ORIGINALSENDER', 'Offenes Tasten- und Antennenfeld'),
              'camera_base': ('KAMERA / GEHAEUSE', 'Optische Achse an der Stirnseite'),
              'camera_lid': ('KAMERA / DECKEL', 'Vier M3-Durchgaenge'),
              'hud_base': ('HUD / SCHARNIERBASIS', 'Metallachse und zwei Langloecher'),
              'hud_arm': ('HUD / KLAPPARM', 'Modulplatte mit Laengsjustage'),
              'nozzle_shroud': ('DUESENLICHT / BLENDE', 'Freie Mitte fuer separaten OEM-Auslass'),
              'nozzle_diffuser': ('DUESENLICHT / DIFFUSOR', 'Geometrie fuer separate Platte'),
              'nozzle_fan_bracket': ('DUESENLICHT / LUEFTER', 'Separater trockener Halter'),
              'controller_base': ('CONTROLLER / WANNE', 'Platinenauflagen und Luftschlitze'),
              'controller_lid': ('CONTROLLER / DECKEL', 'Verschraubt und abnehmbar')}
    fig = plt.figure(figsize=(16, 18), facecolor=background)
    fig.text(.055, .968, 'MJOLNIR  /  HARDWARE-KIT', color=text, size=25, weight='bold')
    fig.text(.055, .944, '11 parametrische Einzelteile  |  Tatsaechliche STL-Geometrie',
             color=muted, size=12)
    fig.text(.945, .971, 'KONSTRUKTIONSSTAND 01', color=accent, size=10, ha='right')
    fig.text(.945, .951, 'BEISPIELMASSE / KEINE PASSFREIGABE', color=muted, size=9, ha='right')
    light = np.array([-.4, -.5, .9]); light /= np.linalg.norm(light)
    elevation, azimuth = np.deg2rad(38), np.deg2rad(-62)
    view = np.array([np.cos(elevation)*np.cos(azimuth),
                     np.cos(elevation)*np.sin(azimuth), np.sin(elevation)])
    for index, part in enumerate(manifest['parts']):
        path = args.stl_dir / part['file']
        vertices = [list(map(float, line.split()[1:])) for line in path.read_text('ascii').splitlines()
                    if line.lstrip().startswith('vertex ')]
        faces = np.asarray(vertices).reshape((-1, 3, 3))
        if not len(faces):
            raise ValueError('Empty STL: ' + str(path))
        normal = np.cross(faces[:, 1] - faces[:, 0], faces[:, 2] - faces[:, 0])
        lengths = np.linalg.norm(normal, axis=1)
        if np.any(lengths == 0):
            raise ValueError('Degenerate triangle: ' + str(path))
        normal /= lengths[:, None]
        # Matplotlib has no depth buffer: backface culling prevents hidden
        # bottom triangles being drawn over their coplanar top counterparts.
        visible = normal @ view > 1e-8
        shade = .46 + .54 * np.maximum(0, normal @ light)
        rgb = np.asarray(to_rgb(colors[part['component']]))
        facecolors = np.clip(shade[:, None] * rgb, 0, 1)
        row, col = divmod(index, 3)
        x = .045 + col * .317
        y = .726 - row * .218
        ax = fig.add_axes([x, y+.006, .294, .164], projection='3d', facecolor=background)
        ax.add_collection3d(Poly3DCollection(faces[visible], facecolors=facecolors[visible], linewidths=0,
                                            edgecolors='none', antialiased=False))
        low = faces.reshape((-1, 3)).min(axis=0)
        high = faces.reshape((-1, 3)).max(axis=0)
        span = high - low
        center = (low + high) / 2
        radius = max(span) * .54
        ax.set_xlim(center[0]-radius, center[0]+radius)
        ax.set_ylim(center[1]-radius, center[1]+radius)
        ax.set_zlim(center[2]-radius, center[2]+radius)
        ax.set_box_aspect((1, 1, 1))
        ax.view_init(elev=38, azim=-62)
        ax.set_proj_type('ortho')
        ax.set_axis_off()
        title, subtitle = titles[part['id']]
        fig.text(x+.012, y+.183, f'{index+1:02d}  {title}', color=text, size=10, weight='bold')
        fig.text(x+.012, y+.168, subtitle, color=muted, size=8.4)
        fig.text(x+.012, y+.009,
                 ' x '.join(f'{value:.1f}' for value in span) + ' mm  |  ' + part['file'],
                 color=muted, size=7.3)
    x, y = .045 + 2*.317, .726 - 3*.218
    fig.text(x+.012, y+.168, 'VOM PARAMETER ZUM BAUTEIL', color=accent, size=11, weight='bold')
    notes = ('CAD: OpenSCAD, getrennte Einzelteil-Exporte\n'
             'Masse: frei anpassbare synthetische Beispiele\n'
             'Verschraubung: Metallachse, M3 / M4\n'
             'Druckorientierung: im Teilemanifest\n\n'
             'Noch offen: konkrete Geraetepassung,\n'
             'Tragstruktur, Last und Temperatur.\n'
             'Die Ansichten haben unterschiedliche Massstaebe.\n'
             'Keine gedruckten Kuehlkoerper oder Heizer.')
    fig.text(x+.012, y+.146, notes, color=text, size=10, va='top', linespacing=1.8)
    fig.text(.055, .033, 'Design/HardwareKit  |  Editierbare Konstruktion + Manifest + Geometriepruefung',
             color=muted, size=10)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=160, facecolor=background)
    plt.close(fig)


if __name__ == '__main__':
    main()
