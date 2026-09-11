#!/usr/bin/env python3
"""Check evidence completeness; never certify hardware or event permission."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATES = {
    'REF': 'Referenzpaket', 'FIT': 'Koerpermasse und Passprobe',
    'CAD': 'Fertigungstaugliche Detailmodelle', 'MECH': 'Mechanischer Aufbau',
    'EXIT': 'Stromloser Ausstieg', 'VISION': 'Sicht und Beschlag',
    'THERMAL': 'Trage- und Waermeversuch', 'POWER': 'Elektrische Pruefung',
    'FINISH': 'Optische Abnahme', 'STAND': 'Ausstellungsstaender',
    'DEMO': 'Vorfuehrversuche', 'EVENT': 'Veranstaltung und Betriebsart',
}
SCOPES = {
    'wearable': ('REF', 'FIT', 'CAD', 'MECH', 'EXIT', 'VISION', 'THERMAL', 'POWER', 'FINISH'),
    'exhibition': tuple(GATES),
}


def evaluate(data, root=ROOT):
    if not isinstance(data, dict):
        raise ValueError('Register must be an object')
    if data.get('schema_version') != 1 or not isinstance(data.get('revision'), str) or not data['revision'].strip():
        raise ValueError('Invalid schema/revision')
    rows = data.get('gates')
    if not isinstance(rows, list) or len(rows) != len(GATES):
        raise ValueError('All gates required exactly once')
    if not all(isinstance(r, dict) for r in rows):
        raise ValueError('Gate must be an object')
    ids = [r.get('id') for r in rows]
    if len(set(ids)) != len(ids) or set(ids) != set(GATES):
        raise ValueError('Unknown, duplicate or missing gate')
    root = Path(root).resolve()
    binding_reasons = []
    binding = data.get('profile_binding')
    if binding is not None:
        try:
            rel = Path(binding['path'])
            source = (root / rel).resolve()
            if rel.is_absolute() or not source.is_relative_to(root):
                raise ValueError('Profil ausserhalb Nachweiswurzel')
            if hashlib.sha256(source.read_bytes()).hexdigest() != binding['sha256']:
                raise ValueError('Profil seit Registrierung geaendert; Nachweise neu bewerten')
        except (KeyError, TypeError, ValueError, OSError) as exc:
            binding_reasons.append(str(exc))
    results = []
    for row in rows:
        status = row.get('status')
        if status not in ('open', 'in_progress', 'passed', 'failed'):
            raise ValueError('Invalid gate status')
        reasons = list(binding_reasons)
        if status != 'passed':
            reasons.append('Status: ' + status)
        else:
            for key in ('reviewer', 'summary'):
                if not isinstance(row.get(key), str) or not row[key].strip():
                    reasons.append(key + ' fehlt')
            if row.get('revision') != data['revision']:
                reasons.append('Nachweis gehoert nicht zur aktuellen Revision')
            try:
                date = dt.date.fromisoformat(row.get('date', ''))
                if date > dt.datetime.now(dt.timezone.utc).date():
                    raise ValueError()
            except (ValueError, TypeError):
                reasons.append('Pruefdatum fehlt oder liegt in der Zukunft')
            evidence = row.get('evidence')
            if not isinstance(evidence, list) or not evidence:
                reasons.append('Nachweisdatei fehlt')
            else:
                for item in evidence:
                    try:
                        relative = Path(item['path'])
                        path = (root / relative).resolve()
                        if relative.is_absolute() or not path.is_relative_to(root):
                            raise ValueError('Nachweis ausserhalb Projekt')
                        if not path.is_file() or path.stat().st_size == 0:
                            raise ValueError('Nachweis fehlt oder ist leer')
                        if hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
                            raise ValueError('Nachweis-Hash stimmt nicht')
                    except (KeyError, TypeError, ValueError, OSError) as exc:
                        reasons.append(str(exc))
        results.append({'id': row['id'], 'name': GATES[row['id']],
                        'complete': not reasons, 'reasons': reasons})
    done = {r['id'] for r in results if r['complete']}
    return {'project': str(data.get('project', 'Allgemeines Musterregister')), 'revision': data['revision'], 'gates': results,
            'scopes': {scope: all(g in done for g in gates) for scope, gates in SCOPES.items()}}


def render(report):
    lines = ['# V4: Nachweisstatus', '', 'GENERATED: tools/suit_readiness.py.', '',
             'Prueft dokumentierte Nachweise, keine Sicherheit oder Veranstalterfreigabe.',
             'Ein Status passed ist eine menschliche Bewertung; Hash und Datum beweisen',
             'keine inhaltliche Richtigkeit. Vorlagen und Softwaretests zaehlen nicht als Hardwaretest.', '',
             'Projekt: ' + report['project'].replace('|', '/').replace('\n', ' '),
             'Revision: ' + report['revision'].replace('|', '/').replace('\n', ' '), '',
             '| Gate | Nachweis | Dokumentation |', '| --- | --- | --- |']
    for r in report['gates']:
        detail = 'vollstaendig registriert' if r['complete'] else '; '.join(r['reasons'])
        detail = detail.replace('|', '/').replace('\n', ' ')
        lines.append(f"| {r['id']} | {r['name']} | {detail} |")
    lines += ['', '## Dokumentationsumfang', '']
    for scope, complete in report['scopes'].items():
        lines.append(f"- {scope}: {'vollstaendig registriert' if complete else 'offene Nachweise'}")
    lines += ['', 'Exhibition umfasst hier den kombinierten getragenen und ungetragenen',
              'Messeauftritt. Eine reine statische Ausstellung braucht eine eigene',
              'bewertete Einsatzplanung und darf diese Gates nicht stillschweigend umgehen.', '']
    return '\n'.join(lines)


def input_paths(data, root):
    """Referenced files stay protected even for incomplete or failed gates."""
    root = Path(root).resolve()
    paths = set()
    binding = data.get('profile_binding')
    entries = [binding] if isinstance(binding, dict) else []
    for row in data['gates']:
        evidence = row.get('evidence')
        if isinstance(evidence, list):
            entries.extend(item for item in evidence if isinstance(item, dict))
    for item in entries:
        if isinstance(item.get('path'), str):
            paths.add((root / item['path']).resolve())
    return paths


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=ROOT / 'Progress/Mjolnir-Readiness.json')
    parser.add_argument('--out', type=Path)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--require', choices=SCOPES)
    parser.add_argument('--root', type=Path, default=ROOT, help='Root for evidence and optional bound profile')
    parser.add_argument('--init', type=Path, help='Create a blank evidence register; never overwrite')
    parser.add_argument('--project', default='My Suit')
    parser.add_argument('--revision', default='r1')
    parser.add_argument('--profile', type=Path, help='With --init: bind reviews to exact profile bytes')
    args = parser.parse_args()
    try:
        if args.init:
            if args.check or args.require or args.out:
                raise ValueError('--init cannot be combined with report/check options')
            if not args.project.strip() or not args.revision.strip():
                raise ValueError('Project and revision cannot be blank')
            data = {'schema_version': 1, 'project': args.project, 'revision': args.revision,
                    'gates': [{'id': key, 'status': 'open', 'evidence': []} for key in GATES]}
            if args.profile:
                source = args.profile.resolve()
                relative = source.relative_to(args.root.resolve())
                data['profile_binding'] = {'path': relative.as_posix(),
                                          'sha256': hashlib.sha256(source.read_bytes()).hexdigest()}
            args.init.parent.mkdir(parents=True, exist_ok=True)
            with args.init.open('x') as handle:
                json.dump(data, handle, indent=2, ensure_ascii=True)
                handle.write('\n')
            print('Created blank evidence register: ' + str(args.init))
            return 0
        if args.profile:
            raise ValueError('--profile is only valid with --init')
        data = json.loads(args.manifest.read_text())
        report = evaluate(data, args.root)
        target = args.out or (ROOT / 'Progress/Mjolnir-Readiness.md' if args.manifest.resolve() == ROOT / 'Progress/Mjolnir-Readiness.json' else None)
        protected = input_paths(data, args.root) | {args.manifest.resolve()}
        if target is not None and target.resolve() in protected:
            raise ValueError('Report must not overwrite evidence register, evidence files or bound profile')
        content = render(report)
        if args.check:
            if target is None or not target.exists() or target.read_text() != content:
                raise ValueError('Report missing/out of date; provide --out for custom manifests')
        elif target:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
        else:
            print(content)
        print(json.dumps(report['scopes'], sort_keys=True))
        return 2 if args.require and not report['scopes'][args.require] else 0
    except (OSError, ValueError, TypeError) as exc:
        parser.exit(1, f'Invalid evidence register: {exc}\n')


if __name__ == '__main__':
    raise SystemExit(main())
