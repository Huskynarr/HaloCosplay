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
    if data.get('schema_version') != 1 or not isinstance(data.get('revision'), str) or not data['revision'].strip():
        raise ValueError('Invalid schema/revision')
    rows = data.get('gates')
    if not isinstance(rows, list) or len(rows) != len(GATES):
        raise ValueError('All gates required exactly once')
    ids = [r.get('id') for r in rows]
    if len(set(ids)) != len(ids) or set(ids) != set(GATES):
        raise ValueError('Unknown, duplicate or missing gate')
    root = Path(root).resolve()
    results = []
    for row in rows:
        status = row.get('status')
        if status not in ('open', 'in_progress', 'passed', 'failed'):
            raise ValueError('Invalid gate status')
        reasons = []
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
    return {'revision': data['revision'], 'gates': results,
            'scopes': {scope: all(g in done for g in gates) for scope, gates in SCOPES.items()}}


def render(report):
    lines = ['# V4: Nachweisstatus', '', 'GENERATED: tools/suit_readiness.py.', '',
             'Prueft dokumentierte Nachweise, keine Sicherheit oder Veranstalterfreigabe.',
             'Ein Status passed ist eine menschliche Bewertung; Hash und Datum beweisen',
             'keine inhaltliche Richtigkeit. Vorlagen und Softwaretests zaehlen nicht als Hardwaretest.', '',
             'Revision: ' + report['revision'], '',
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=ROOT / 'Progress/Mjolnir-Readiness.json')
    parser.add_argument('--out', type=Path)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--require', choices=SCOPES)
    args = parser.parse_args()
    try:
        report = evaluate(json.loads(args.manifest.read_text()))
        target = args.out or (ROOT / 'Progress/Mjolnir-Readiness.md' if args.manifest.resolve() == ROOT / 'Progress/Mjolnir-Readiness.json' else None)
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
