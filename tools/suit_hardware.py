#!/usr/bin/env python3
"""Export independent accessory CAD and electrical references, optionally STL."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

try:
    from . import suit_assets
except ImportError:
    import suit_assets

ROOT = Path(__file__).resolve().parents[1]
CAD_SOURCE = ROOT / 'Design/HardwareKit'
ELECTRICAL_SOURCE = ROOT / 'Design/Electrical'
STATUS = 'HARDWARE_PROTOTYPES_NOT_VALIDATED'
SUFFIXES = {'.scad', '.json', '.md', '.svg', '.png', '.py', '.sch', '.kicad_sch', '.kicad_pro', '.lib'}


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True, allow_nan=False)+'\n', encoding='utf-8')


def configuration(config_path=None):
    defaults = json.loads((CAD_SOURCE / 'ExampleConfig.json').read_text(encoding='utf-8'))
    overrides = json.loads(Path(config_path).read_text(encoding='utf-8')) if config_path else {}
    if not isinstance(overrides, dict) or set(overrides)-set(defaults):
        raise ValueError('Hardware-Konfiguration: unbekannte Felder oder kein Objekt')
    values = {**defaults, **overrides}
    for key, value in values.items():
        if not re.fullmatch(r'[a-z][a-z0-9_]*', key):
            raise ValueError('Ungueltiger Parametername')
        if isinstance(value, bool) or not isinstance(value, (float, int)):
            raise ValueError(key+': endliche Zahl erforderlich')
        try:
            finite = math.isfinite(value)
        except OverflowError:
            finite = False
        if not finite or abs(value) > 10000:
            raise ValueError(key+': Zahl ausserhalb des Geometriebereichs')
    return values, {key: 'explicit_config' if key in overrides else 'generic_example' for key in values}


def parts():
    data = json.loads((CAD_SOURCE / 'Manifest.json').read_text(encoding='utf-8'))
    result = data['parts']
    names, ids = set(), set()
    for row in result:
        if not re.fullmatch(r'[A-Za-z0-9_-]+\.stl', row['file']):
            raise ValueError('STL-Dateiname muss ein einfacher Dateiname sein')
        if row['file'] in names or row['id'] in ids:
            raise ValueError('Doppelte Hardware-Teil-ID oder Ausgabedatei')
        names.add(row['file']); ids.add(row['id'])
        for key in ('component', 'part'):
            if not re.fullmatch(r'[a-z][a-z0-9_]*', row[key]):
                raise ValueError('Ungueltiger CAD-Selector')
    if not result:
        raise ValueError('Keine Hardwareteile im Manifest')
    return result


def export(out, config_path=None, render_stl=False, openscad='openscad'):
    out = Path(out)
    if out.exists() or out.is_symlink():
        raise ValueError('Ausgabe existiert; neuen Revisionsordner waehlen')
    for source in (CAD_SOURCE, ELECTRICAL_SOURCE):
        if out.resolve().is_relative_to(source.resolve()):
            raise ValueError('Ausgabe darf nicht im Quellordner liegen')
    values, origins = configuration(config_path)
    selected = parts()
    executable = shutil.which(openscad) if render_stl else None
    if render_stl and executable is None:
        raise ValueError('OpenSCAD fehlt; Quellenexport ohne --render-stl moeglich')
    snapshots = {}
    for folder, source in (('CAD', CAD_SOURCE), ('Electrical', ELECTRICAL_SOURCE)):
        for file in sorted(source.rglob('*')):
            if file.is_file() and file.suffix in SUFFIXES and '__pycache__' not in file.parts:
                if file.is_symlink():
                    raise ValueError('Symlink als Paketquelle nicht unterstuetzt')
                snapshots[Path(folder) / file.relative_to(source)] = file.read_bytes()
    if not any(p.parts[0] == 'Electrical' for p in snapshots):
        raise ValueError('Elektrische Referenzdateien fehlen')
    report = {'schema_version': 1, 'status': STATUS, 'fabrication_approved': False,
              'hardware_approved': False, 'parameters': values, 'parameter_origin': origins,
              'body_scaling': 'none; hardware dimensions are independent of wearer',
              'configuration_sha256': hashlib.sha256(Path(config_path).read_bytes()).hexdigest() if config_path else None,
              'sources_sha256': {p.as_posix(): hashlib.sha256(b).hexdigest() for p, b in snapshots.items()},
              'geometry_check': 'not_run', 'electrical_check': 'not_run_in_this_export', 'parts': []}
    out.mkdir(parents=True, exist_ok=False)
    try:
        for path, content in snapshots.items():
            dest = out/path; dest.parent.mkdir(parents=True, exist_ok=True); dest.write_bytes(content)
        # Repository examples must never look like evidence for overridden dimensions.
        for name in ('GeometryCheck.json', 'Preview.png'):
            (out/'CAD'/name).rename(out/'CAD'/('Baseline'+name))
        baseline_path = out/'CAD/BaselineGeometryCheck.json'
        baseline = json.loads(baseline_path.read_text(encoding='utf-8'))
        baseline['original_status'] = baseline['status']
        baseline['status'] = 'BASELINE_ONLY_NOT_THIS_EXPORT'
        baseline['scope'] = 'Unchanged repository example geometry; not the exported configuration.'
        write_json(baseline_path, baseline)
        cad_readme = out/'CAD/README.md'
        readme = cad_readme.read_text(encoding='utf-8')
        readme = readme.replace('GeometryCheck.json', 'BaselineGeometryCheck.json').replace('Preview.png', 'BaselinePreview.png')
        title, remainder = readme.split('\n', 1)
        cad_readme.write_text(title+'\n\n**EXPORT-HINWEIS:** BaselineGeometryCheck.json und BaselinePreview.png zeigen\n'
                              'ausschliesslich den urspruenglichen Repository-Beispielstand. Ihre Masse und\n'
                              'Quellhashes gelten nicht fuer diese Exportkonfiguration. Der aktuelle\n'
                              'Pruefstatus steht in ../HardwarePackage.json; ohne STL-Export ist er not_run.\n'+remainder,
                              encoding='utf-8')
        (out/'CAD/Parameters.scad').write_text(
            '// GENERATED independent example dimensions; mm/degrees. No hardware approval.\n'+
            '\n'.join(f'{key} = {json.dumps(value, allow_nan=False)};' for key, value in values.items())+'\n', encoding='ascii')
        write_json(out/'Config.json', values)
        if render_stl:
            (out/'STL').mkdir(); (out/'Logs').mkdir()
            version = subprocess.run([executable, '--version'], capture_output=True, text=True, check=True, timeout=20)
            report['openscad_version'] = (version.stdout+version.stderr).strip()
        for row in selected:
            entry = dict(row)
            entry.update({'physical_test_passed': False, 'mesh_sha256': None, 'mesh_check': None})
            if render_stl:
                dest = out/'STL'/row['file']
                command = [executable, '--hardwarnings', '--export-format', 'asciistl',
                           '-D', 'component='+json.dumps(row['component']),
                           '-D', 'part='+json.dumps(row['part']), '-o', str(dest.resolve()),
                           str((out/'CAD/HardwareKit.scad').resolve())]
                result = subprocess.run(command, capture_output=True, text=True, timeout=180,
                                        env={**os.environ, 'QT_QPA_PLATFORM': 'offscreen'})
                log = result.stdout+result.stderr
                (out/'Logs'/Path(row['file']).with_suffix('.log')).write_text(log, encoding='utf-8')
                if result.returncode or 'ERROR:' in log or not dest.is_file():
                    raise ValueError('OpenSCAD fehlgeschlagen: '+row['id'])
                mesh = dest.read_bytes(); check = suit_assets.inspect_stl(mesh, 1)
                if not check['edge_checks_complete']:
                    raise ValueError('STL-Kantenpruefung fehlgeschlagen: '+row['id'])
                entry.update({'mesh_sha256': hashlib.sha256(mesh).hexdigest(), 'mesh_check': check})
            report['parts'].append(entry)
        if render_stl:
            report['geometry_check'] = 'openscad_and_closed_consistently_oriented_edges_passed'
        (out/'README.md').write_text(
            '# CAD- und Schaltplanpaket\n\nStatus: **'+STATUS+'**. Keine Hardwarefreigabe.\n\n'
            'CAD/ enthaelt sechs einstellbare Einbaumodelle; Einzelteile stehen im Manifest.\n'
            'Electrical/ enthaelt Schaltblaetter, Verbindungen, Quellen und offene Auslegungswerte.\n'
            'Config.json enthaelt Geraete-/Befestigermasse als generische Beispiele. Koerpermasse\n'
            'werden nicht auf Kaufteile uebertragen. Die Modelle sind keine Halo-Detailruestung.\n\n'
            'Bei --render-stl enthaelt STL/ gepruefte Mesh-Exporte in mm. Kantenpruefungen\n'
            'belegen keine Wandstaerke, Selbstschnittfreiheit, Last, Passform oder Temperatur.\n'
            'HardwarePackage.json dokumentiert Parameterherkunft, Quellenhashes und Einzelpruefungen.\n'
            'Anschliessende manuelle Dateiaenderungen benoetigen einen neuen Export fuer passende Hashes.\n\n'
            'Schaltplaene sind Referenzentwuerfe. Bauteilrevision, Sicherungen, Leitungen,\n'
            'Versorgung und reales Einschalt-/Ausfallverhalten vor Aufbau pruefen.\n\n'
            'Aus dem Repository mit neuer Revision exportieren:\n\n```bash\n'
            'python3 tools/suit_hardware.py --config build/Hardware.local.json --out build/Hardware-r2 --render-stl\n'
            '```\n\nOhne --render-stl ist kein OpenSCAD erforderlich; geometrische Assertions\n'
            'werden dann noch nicht ausgefuehrt. CAD/README.md und Electrical/README.md enthalten Details.\n', encoding='ascii')
        report['outputs_sha256'] = {
            p.relative_to(out).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(out.rglob('*')) if p.is_file()}
        write_json(out/'HardwarePackage.json', report)
    except Exception:
        (out/'BUILD_INCOMPLETE.md').write_text('# Unvollstaendiger Export\n\nKeine vollstaendige Ausgabe. Fehler beheben und neuen Ordner verwenden.\n', encoding='ascii')
        raise
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--config', type=Path)
    parser.add_argument('--render-stl', action='store_true')
    parser.add_argument('--openscad', default='openscad')
    args = parser.parse_args(argv)
    try:
        result = export(args.out, args.config, args.render_stl, args.openscad)
    except (ValueError, OSError, TypeError, KeyError, subprocess.SubprocessError) as exc:
        print('Hardware-Export: '+str(exc), file=sys.stderr); return 2
    print(f"{result['status']}: {len(result['parts'])} Teile; {args.out}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
