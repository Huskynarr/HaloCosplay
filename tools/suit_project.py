#!/usr/bin/env python3
"""Create a complete, isolated digital workshop package from a project profile."""
import argparse
import csv
import hashlib
import html
import json
from pathlib import Path
import shlex
import sys

try:
    from . import suit_assets, suit_budget, suit_clamshell, suit_components, suit_engineering, suit_fit, suit_integration, suit_readiness, suit_thermal
except ImportError:
    import suit_assets, suit_budget, suit_clamshell, suit_components, suit_engineering, suit_fit, suit_integration, suit_readiness, suit_thermal

ROOT = Path(__file__).resolve().parents[1]


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True)+'\n', encoding='utf-8')


def finish_sheet(project):
    rows = ['<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" viewBox="0 0 210 297">',
            '<rect width="210" height="297" fill="white"/>',
            '<g fill="black" font-family="sans-serif" font-size="3.2">',
            '<text x="10" y="13" font-size="6">Finish-Musterprotokoll</text>',
            '<text x="10" y="21">Projekt: '+html.escape(project)+'</text>',
            '<text x="10" y="28">Reale Muster separat herstellen; Blatt bei 100 Prozent drucken.</text>']
    for i in range(6):
        y=35+i*35
        rows += [f'<rect x="10" y="{y}" width="190" height="31" fill="none" stroke="black" stroke-width="0.3"/>',
                 f'<text x="13" y="{y+6}">F{i+1:02d}: Untergrund / Vorbehandlung / Grundierung:</text>',
                 f'<text x="13" y="{y+14}">Farbcode / Schichten / Klarlack / Datum:</text>',
                 f'<text x="13" y="{y+22}">Referenzansicht / Licht / Haftung / Biegung / Freigabe:</text>']
    rows += ['<path d="M 10 260 H 60 M 10 258 V 262 M 60 258 V 262" fill="none" stroke="black" stroke-width="0.3"/>',
             '<text x="10" y="268">Kontrolllinie: 50 mm. Keine vorgegebenen RAL-/Herstellerfarben.</text>',
             '</g></svg>']
    return '\n'.join(rows)+'\n'


def generate(profile_path, out, concept=False, integration_path=None):
    profile_path=Path(profile_path).resolve(); out=Path(out).resolve()
    raw=profile_path.read_bytes(); profile=json.loads(raw)
    fit=suit_fit.derive(profile, concept)
    if fit['input_status'] == 'synthetic' and not concept:
        raise ValueError('Synthetisches Profil erfordert --concept')
    reference=suit_assets.reference(fit['build']['armor_reference'])
    integration=suit_integration.plan(fit, suit_integration.configure(fit, integration_path))
    engineering=suit_integration.engineering_inputs(integration)
    thermal=suit_integration.thermal_inputs(integration)
    assets=suit_assets.template(fit['profile'], reference['id'])
    bom=json.loads((ROOT/'Materials/Mjolnir-BOM.json').read_text())
    if fit['build']['fog_system']=='pmi-cloud':
        fog=json.loads((ROOT/'Materials/Mjolnir-Nebel-BOM.json').read_text())
        bom['items'].extend(fog['items'])
    # The BOM remains an explicit starting allowance, not an automatic material estimate.
    budget_text=suit_budget.render(bom, include_reference_notes=False)
    out.mkdir(parents=True, exist_ok=False)
    try:
        snapshot=out/'profile.local.json'; snapshot.write_bytes(raw)
        write_json(out/'Reference.json', reference)
        write_json(out/'assets.local.json', assets)
        write_json(out/'engineering.local.json', engineering)
        write_json(out/'thermal.local.json', thermal)
        write_json(out/'integration.local.json', integration['configuration'])
        integration['profile_sha256']=hashlib.sha256(raw).hexdigest()
        integration['configuration_sha256']=hashlib.sha256((out/'integration.local.json').read_bytes()).hexdigest()
        write_json(out/'Integration.json', integration)
        (out/'Integration.md').write_text(suit_integration.render(integration),encoding='utf-8')
        write_json(out/'BOM.local.json', bom)
        (out/'Budget.md').write_text(budget_text, encoding='utf-8')
        suit_fit.export(fit,out/'Fit')
        suit_components.export(snapshot, out/'Components', concept=concept)
        suit_clamshell.export(snapshot, out/'Clamshell', concept=concept)
        suit_thermal.export(out/'thermal.local.json', out/'Thermal')
        report=suit_engineering.calculate(engineering)
        report['input_sha256']=hashlib.sha256((out/'engineering.local.json').read_bytes()).hexdigest()
        (out/'Engineering').mkdir()
        write_json(out/'Engineering/EngineeringReport.json',report)
        (out/'Engineering/EngineeringReport.md').write_text(suit_engineering.render(report),encoding='utf-8')
        readiness={'schema_version':1, 'project':fit['profile'], 'revision':'prototype-r1',
                   'profile_binding':{'path':'profile.local.json','sha256':hashlib.sha256(raw).hexdigest()},
                   'gates':[{'id':key,'status':'open','evidence':[]} for key in suit_readiness.GATES]}
        write_json(out/'readiness.local.json',readiness)
        (out/'Readiness.md').write_text(suit_readiness.render(suit_readiness.evaluate(readiness,out)),encoding='utf-8')
        with (out/'Parts.csv').open('w',newline='',encoding='utf-8') as f:
            writer=csv.writer(f)
            writer.writerow(['part_id','label','revision','required_views','model_source_ids','native_path','mesh_path','measured_mass_g','status'])
            for part in reference['parts']:
                writer.writerow([part['id'],part['label'],'r1',';'.join(part['required_views']),';'.join(part['model_source_ids']),'','','','open'])
        with (out/'MovementTests.csv').open('w',newline='',encoding='utf-8') as f:
            writer=csv.writer(f); writer.writerow(['test_id','task','revision','observer','result','evidence','notes'])
            for key, task in [('MOVE01','Kopf links/rechts, Blick nach unten und freie Helm-Luftzufuhr'),('MOVE02','Arme heben, Greifen, Handruecken und Ellbogenfreiheit'),('MOVE03','Gehen, Abrollen, Wenden und freier Schritt'),('MOVE04','Sitzen und Wiederaufstehen, sofern geplanter Einsatz'),('MOVE05','Stromlos oeffnen, Helferzugang und Notausstieg'),('MOVE06','Klappern und Reiben lokalisieren, Gurte und Kabel kontrollieren'),('MOVE07','Waerme- und Laufzeitversuch unter dokumentierten Bedingungen')]:
                writer.writerow([key,task,'prototype-r1','','open','',''])
        (out/'FinishSheet.svg').write_text(finish_sheet(fit['profile']),encoding='utf-8')
        q=shlex.quote(str(out))
        lines=['# Digitales Baupaket: '+fit['profile'],'',
               'Status: **WORKSHOP_PACKAGE_NOT_PHYSICALLY_VALIDATED**. Keine fertige Gesamt-Druckruestung.',
               'Ruestungsreferenz: '+reference['title'],
               'Massherkunft: '+fit['status'], '',
               '## Dateien und Anwendung','',
               '| Datei | Anwendung |','| --- | --- |',
               '| profile.local.json / Fit/ | Profilsnapshot und getrennt berechnete Bauraumhuelle |',
               '| Reference.json / Parts.csv | Referenzansichten und kompletter Teileumfang |',
               '| assets.local.json | Eigene Modelldateien, Quellen, Lizenzen, Einheiten und Hashes eintragen |',
               '| Components/ | Fuenf parametrisierte Halter-/Passproben mit Stuecklisten und Montagehinweisen |',
               '| Clamshell/ | Acht aufklappbare Arm-/Beinhuellen, eigene Seiten und Selbstanzieh-Prueffolge |',
               '| integration.local.json / Integration.* | Ausgewaehlte Einbauzonen, zugaengliche Akkus und getrennte Stromkreise |',
               '| engineering.local.json / Engineering/ | Reale Verbraucher, Akkus, Tuergewicht und Staender-Geometrie eintragen und Berichte aktualisieren |',
               '| thermal.local.json / Thermal/ | Eigene LED-Waermewege und gemessene Luftkanaele auslegen |',
               '| BOM.local.json / Budget.md | Editierbare Budgetansaetze, keine profilberechneten Materialmengen |',
               '| FinishSheet.svg | Druckbares Protokoll fuer sechs reale Finishmuster |',
               '| MovementTests.csv | Bewegungs-, Geraeusch- und Ausstiegsproben dokumentieren |',
               '| readiness.local.json | Reale Nachweise an Projekt und Profilsnapshot binden |','',
               '## Baufolge','',
               '1. Referenzansichten und Detailmodellset zusammenstellen. Keine Modelle anderer Ruestungsversionen still vermischen.',
               '2. Helm, Torso und eine Schulter als leichte Passprobe abstimmen. Die Components-Geometrie dient lokalen Schnittstellen, nicht der originalgetreuen Aussenhaut.',
               '3. Visiermuster, Luefterhalter und Gelenkabdeckung am Tisch pruefen. Gekaufte Detaildateien segmentweise an reale Innenmasse anpassen.',
               '4. Tuerlagerung und Seitenfuehrung mit realen Massen bemessen; mechanischen Versuch ungetragen durchfuehren.',
               '5. Eine Arm-/Beinkassette bauen und korrigieren, zweite Seite separat anpassen. Unteranzug und Verbindungen im Rohbau testen.',
               '6. Rohbau wiegen; Strom-, Waerme-, Sprach- und Bewegungsversuche dokumentieren. Erst dann Finishmuster auf Gesamtteile uebertragen.',
               '7. Staender, Aufnahmen, Transport und Vorfuehrung getrennt proben. Nebel nur gemaess projektbezogenem Effekt- und Veranstaltungsplan.', '',
               '## Werkzeuge erneut ausfuehren','',
               'Folgende Befehle ab Repository-Wurzel. Nach Aenderung am Snapshot bleiben alte Nachweise ungueltig, bis sie neu bewertet wurden.', '',
               '```bash',
               f'python3 tools/suit_assets.py --manifest {q}/assets.local.json --report {q}/AssetReport.json',
               f'python3 tools/suit_engineering.py --input {q}/engineering.local.json --out {q}/Engineering',
               f'python3 tools/suit_thermal.py --input {q}/thermal.local.json --out {q}/Thermal',
               f'python3 tools/suit_budget.py --bom {q}/BOM.local.json --out {q}/Budget.md',
               f'python3 tools/suit_readiness.py --manifest {q}/readiness.local.json --root {q} --out {q}/Readiness.md',
               '```','',
               'Der Modelldateipruefer liefert Exitcode 2, solange Eingaben fehlen oder Datei-/Kantenpruefungen offen sind.',
               'Originalmodell-Dateien und reale Koerperdaten bleiben lokal. Bestehende Projektpakete werden bei Neuerzeugung nicht ueberschrieben.',
               'Engineering-Eingaben starten unbekannt; Demonstrationswerte werden dort nicht automatisch eingesetzt.',
               'Die Budgetvorlage bleibt an Materialweg, vorhandene Ausstattung und Angebote anzupassen. Komponenten-BOMs nicht pauschal nochmals aufaddieren.',
               'Integrationsauswahl aendert nicht automatisch die Budgetvorlage. Insbesondere Highpower-RGB, Treiber, Optik und PD-Versorgung separat erfassen.',
               'Aenderungen an integration.local.json gelten fuer eine neu erzeugte Revision via --integration; bestehende Berichte werden nicht still ueberschrieben.',
               'Ausgewaehlte HUD-, Audio-, Exoskelett- und Nebeltechnik benoetigt eigene Einbauraeume und Nachweise. Eine Profiloption bestaetigt diese nicht.', '']
        (out/'BuildPlan.md').write_text('\n'.join(lines),encoding='utf-8')
        write_json(out/'Package.json',{'schema_version':1,'project':fit['profile'],'reference':reference['id'],
                                      'status':'WORKSHOP_PACKAGE_NOT_PHYSICALLY_VALIDATED',
                                      'profile_sha256':hashlib.sha256(raw).hexdigest(),
                                      'fabrication_approved':False,'parts':len(reference['parts'])})
    except Exception:
        (out/'BUILD_INCOMPLETE.md').write_text('# Unvollstaendige Ausgabe\n\nErzeugung fehlgeschlagen; Fehler beheben und ein neues Ausgabeverzeichnis verwenden.\n',encoding='utf-8')
        raise
    return out


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--concept',action='store_true')
    parser.add_argument('--integration',type=Path,help='Partial equipment integration options JSON')
    args=parser.parse_args(argv)
    try:
        print(generate(args.profile,args.out,args.concept,args.integration)); return 0
    except (ValueError,OSError,TypeError,KeyError) as exc:
        print('Baupaket-Fehler: '+str(exc),file=sys.stderr); return 2


if __name__=='__main__':
    raise SystemExit(main())
