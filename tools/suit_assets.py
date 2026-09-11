#!/usr/bin/env python3
"""Inspect project model files and provenance; never certify shape, fit or strength."""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
import struct
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'Documentation/References/ArmorReferenceLibrary.json'
MAX_BYTES = 100 * 1024 * 1024
MAX_TRIANGLES = 300000


def reference(key):
    catalog = json.loads(CATALOG.read_text(encoding='utf-8'))
    found = [item for item in catalog['references'] if item['id'] == key]
    if len(found) != 1:
        raise ValueError('Unbekannte Ruestungsreferenz')
    return found[0]


def template(project, key):
    if not isinstance(project, str) or not project.strip() or len(project) > 64:
        raise ValueError('Projektname: 1-64 Zeichen erforderlich')
    return {'schema_version': 1, 'project': project, 'reference': key,
            'parts': [{'id': item['id'], 'revision': 'r1',
                       'kind': 'pattern' if item['id'] in ('undersuit', 'neck_seal') else 'mesh',
                       'source_url': None, 'license_note': None, 'reference_views': [],
                       'native_path': None, 'native_sha256': None,
                       'mesh_path': None, 'mesh_sha256': None, 'unit_scale_mm': None,
                       'notes': ''} for item in reference(key)['parts']]}


def positive(value, name):
    if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value) or value <= 0:
        raise ValueError(name + ': positive endliche Zahl erforderlich')
    return value


def local_file(root, value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('Dateipfad fehlt')
    rel = Path(value)
    p = (root / rel).resolve()
    if rel.is_absolute() or not p.is_relative_to(root):
        raise ValueError('Dateipfad ausserhalb Projektwurzel')
    if not p.is_file() or not 0 < p.stat().st_size <= MAX_BYTES:
        raise ValueError('Datei fehlt, ist leer oder groesser als 100 MiB')
    return p


def inspect_stl(data, scale):
    positive(scale, 'unit_scale_mm')
    triangles = []
    if len(data) >= 84 and len(data) == 84 + 50 * struct.unpack_from('<I', data, 80)[0]:
        count = struct.unpack_from('<I', data, 80)[0]
        if count > MAX_TRIANGLES:
            raise ValueError('STL ueber 300000 Dreiecke; Pruefexport vereinfachen oder segmentieren')
        for i in range(count):
            values = struct.unpack_from('<12f', data, 84 + 50*i)
            if not all(math.isfinite(v) for v in values):
                raise ValueError('STL enthaelt nichtendliche Zahlen')
            triangles.append(tuple(tuple(values[j:j+3]) for j in (3, 6, 9)))
    else:
        try:
            lines = [line.strip() for line in data.decode('ascii').splitlines() if line.strip()]
        except UnicodeDecodeError as exc:
            raise ValueError('STL weder gueltiges Binaerformat noch ASCII') from exc
        if len(lines) < 9 or not lines[0].startswith('solid') or not lines[-1].startswith('endsolid'):
            raise ValueError('ASCII-STL ohne vollstaendige solid-Huelle')
        body = lines[1:-1]
        if len(body) > MAX_TRIANGLES * 7:
            raise ValueError('STL ueber 300000 Dreiecke; Pruefexport vereinfachen oder segmentieren')
        if len(body) % 7:
            raise ValueError('Unvollstaendige ASCII-STL-Facette')
        for i in range(0, len(body), 7):
            block = body[i:i+7]
            if not block[0].startswith('facet normal ') or block[1] != 'outer loop' or block[5:] != ['endloop', 'endfacet']:
                raise ValueError('Ungueltige STL-Facette')
            try:
                normal = tuple(map(float, block[0].split()[2:]))
                vertices = tuple(tuple(map(float, line.split()[1:])) for line in block[2:5])
                if len(normal) != 3 or not all(line.startswith('vertex ') for line in block[2:5]) or any(len(v) != 3 for v in vertices):
                    raise ValueError()
                if not all(math.isfinite(x) for v in (normal, *vertices) for x in v):
                    raise ValueError()
            except ValueError as exc:
                raise ValueError('Ungueltige STL-Koordinaten') from exc
            triangles.append(vertices)
    if not triangles:
        raise ValueError('Leeres STL ohne Dreiecke')
    edges, direction = Counter(), Counter()
    low, high = [math.inf]*3, [-math.inf]*3
    area = 0.0
    for tri in triangles:
        a, b, c = [tuple(x*scale for x in v) for v in tri]
        u, v = [b[i]-a[i] for i in range(3)], [c[i]-a[i] for i in range(3)]
        cross = [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
        face_area = math.hypot(*cross)/2
        if not math.isfinite(face_area) or face_area <= 0:
            raise ValueError('Entartetes oder numerisch ungueltiges Dreieck')
        area += face_area
        for vertex in (a, b, c):
            for axis in range(3):
                low[axis] = min(low[axis], vertex[axis]); high[axis] = max(high[axis], vertex[axis])
        for edge in ((a,b), (b,c), (c,a)):
            edges[tuple(sorted(edge))] += 1
            direction[edge] += 1
    if not math.isfinite(area) or not all(math.isfinite(v) for v in (*low, *high)):
        raise ValueError('Geometrie numerisch ausserhalb Wertebereich')
    unmatched = sum(count != 2 for count in edges.values())
    winding = sum(direction[(a,b)] != 1 or direction[(b,a)] != 1 for a,b in edges)
    return {'triangles': len(triangles), 'bounds_mm': {'min': low, 'max': high},
            'size_mm': [high[i]-low[i] for i in range(3)], 'surface_area_mm2': area,
            'nonpaired_edges': unmatched, 'inconsistent_edges': winding,
            'edge_checks_complete': unmatched == 0 and winding == 0,
            'limits': 'Exakte Koordinaten; keine Reparatur, Selbstschnitt-, Wandstaerken- oder Formpruefung.'}


def evaluate(data, root):
    if not isinstance(data, dict) or type(data.get('schema_version')) is not int or data['schema_version'] != 1:
        raise ValueError('Ungueltiges Registerformat')
    ref = reference(data.get('reference'))
    if not isinstance(data.get('project'), str) or not data['project'].strip():
        raise ValueError('Projektname fehlt')
    rows = data.get('parts')
    required = {part['id'] for part in ref['parts']}
    required_views = {part['id']: set(part['required_views']) for part in ref['parts']}
    if not isinstance(rows, list) or not all(isinstance(r, dict) and isinstance(r.get('id'), str) for r in rows):
        raise ValueError('Teileliste fehlt oder ist ungueltig')
    ids = [r['id'] for r in rows]
    if len(ids) != len(set(ids)) or set(ids) != required:
        raise ValueError('Alle Referenzteile genau einmal erforderlich')
    results = []
    root = Path(root).resolve()
    for row in rows:
        reasons, details = [], {}
        if row.get('kind') not in ('mesh', 'pattern'):
            reasons.append('kind muss mesh oder pattern sein')
        if row['id'] not in ('undersuit', 'neck_seal') and row.get('kind') != 'mesh':
            reasons.append('Starres Ruestungsteil benoetigt Meshpruefung')
        for key in ('revision', 'license_note'):
            if not isinstance(row.get(key), str) or not row[key].strip(): reasons.append(key + ' fehlt')
        url = urlparse(row.get('source_url') if isinstance(row.get('source_url'), str) else '')
        if url.scheme not in ('http','https') or not url.netloc: reasons.append('Quelle als HTTP(S)-URL fehlt')
        views = row.get('reference_views')
        if not isinstance(views, list) or not views or not all(isinstance(v,str) and v.strip() for v in views):
            reasons.append('Konkrete Referenzansichten fehlen')
        else:
            missing_views = sorted(required_views[row['id']] - set(views))
            if missing_views:
                reasons.append('Referenzansichten fehlen: ' + ', '.join(missing_views))
        for kind in ('native', 'mesh') if row.get('kind') == 'mesh' else ('native',):
            try:
                p = local_file(root, row.get(kind+'_path'))
                raw = p.read_bytes(); sha = hashlib.sha256(raw).hexdigest()
                details[kind+'_sha256'] = sha
                if row.get(kind+'_sha256') != sha: reasons.append(kind + ': Hash fehlt oder weicht ab')
                if kind == 'mesh':
                    if p.suffix.lower() != '.stl': raise ValueError('Fuer Meshpruefung einen STL-Export ablegen')
                    details['mesh'] = inspect_stl(raw, row.get('unit_scale_mm'))
                    if not details['mesh']['edge_checks_complete']: reasons.append('Offene oder inkonsistente STL-Kanten')
                elif p.suffix.lower() not in ('.scad','.step','.stp','.fcstd','.blend','.f3d','.obj','.3mf','.svg','.dxf','.pdf'):
                    reasons.append('Editierbare CAD-/Musterquelle mit bekanntem Format erforderlich')
            except (ValueError, OSError, OverflowError) as exc:
                reasons.append(kind + ': ' + str(exc))
        results.append({'id':row['id'], 'file_checks_complete':not reasons, 'reasons':reasons, **details})
    return {'schema_version':1, 'project':data['project'], 'reference':data['reference'],
            'file_checks_complete':all(r['file_checks_complete'] for r in results),
            'fabrication_approved':False, 'authenticity_verified':False, 'parts':results,
            'limits':['Lizenznotiz und Referenzzuordnung sind Angaben, keine rechtliche/visuelle Pruefung.',
                      'Native Dateien werden auf Existenz und Hash geprueft, nicht interpretiert.',
                      'STL-Kantentest ersetzt weder Slicerpruefung noch Pass-, Last- oder Originaltreuetest.']}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--init', type=Path)
    mode.add_argument('--manifest', type=Path)
    parser.add_argument('--project', default='New-build')
    parser.add_argument('--reference', default='chief-infinite')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args(argv)
    try:
        if args.init:
            if args.report: raise ValueError('--report nicht mit --init kombinieren')
            data = template(args.project, args.reference)
            args.init.parent.mkdir(parents=True, exist_ok=True)
            with args.init.open('x', encoding='utf-8') as f: json.dump(data, f, indent=2, ensure_ascii=True); f.write('\n')
            print(args.init); return 0
        data = json.loads(args.manifest.read_text(encoding='utf-8'))
        root = args.manifest.resolve().parent
        result = evaluate(data, root)
        content = json.dumps(result, indent=2, ensure_ascii=True)+'\n'
        if args.report:
            protected = {args.manifest.resolve()}
            for row in data['parts']:
                for key in ('native_path','mesh_path'):
                    if isinstance(row.get(key), str): protected.add((root/row[key]).resolve())
            if args.report.resolve() in protected or (args.report.exists() and any(
                    path.exists() and args.report.samefile(path) for path in protected)):
                raise ValueError('Ausgabe darf keine Eingabe ueberschreiben')
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(content, encoding='utf-8')
        print(content, end='')
        return 0 if result['file_checks_complete'] else 2
    except (ValueError, OSError, TypeError, KeyError) as exc:
        print('Modelldatei-Fehler: '+str(exc), file=sys.stderr); return 2


if __name__ == '__main__':
    raise SystemExit(main())
