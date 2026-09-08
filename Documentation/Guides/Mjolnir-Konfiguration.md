# Eigenes Projekt konfigurieren

Ein Profil beschreibt eine konkrete Person und einen konkreten Aufbau. Mehrere
Profile koennen parallel verwendet werden, etwa fuer verschiedene Personen,
Unteranzuege oder Ausstattungen. Kein Koerpermass wird von einem anderen Profil
uebernommen. Ein Wechsel des Materialwegs oder der Ausstattung erfordert eine
erneute Pruefung der betroffenen Bauteile.

## Browser-Workflow

Den [Konfigurator](../../web/configurator/) ueber die Web-Version oder den lokalen
Webserver oeffnen. Ein neues leeres Profil anlegen und eindeutig benennen.
Messwerte in Millimetern eintragen, links und rechts getrennt. Leere Felder
bleiben unbekannt. Referenz, Materialweg, Einsatz und optionale Ausstattung
werden im selben Profil festgehalten.

Profile lassen sich als JSON exportieren und wieder importieren. Mehrere
Projekte erhalten eigene Profile; die optionale Browserspeicherung dient dem
bequemen Wiederaufruf. Ein Export ist die uebertragbare Sicherung. Private
Messdaten werden nicht als Teil einer GitHub-Veroeffentlichung benoetigt.

## Kommandozeile

Ab Repository-Wurzel, Python 3.11+:

```bash
python3 tools/suit_fit.py --init build/MySuit.local.json --name "My Suit"
```

Das angelegte Profil enthaelt 32 unbekannte Messfelder. Die
[Messanleitung](Mjolnir-Massanpassung.md) definiert die Endpunkte und
[Messprotokoll.csv](../../Design/Parametric/Profiles/Messprotokoll.csv) dient der
handschriftlichen oder tabellarischen Aufnahme. Der Generator nutzt JSON;
das Messblatt ist kein automatischer Import ungepruefter Messreihen.

Nach dem Ausfuellen:

```bash
python3 tools/suit_fit.py --profile build/MySuit.local.json --out build/MySuit
```

Ohne `--concept` muessen alle erforderlichen Messwerte vorliegen. Das erzeugte
`build/MySuit/MjolnirEntry.scad` verwendet die Parameter genau dieser Ausgabe;
es ist keine manuelle Aenderung der zentralen Include-Datei noetig. Der
Fit-Bericht zeigt Eingaben, Herkunft und abgeleitete Bauraummasse.

Ein zweites Projekt bleibt unabhaengig:

```bash
python3 tools/suit_fit.py --init build/SecondSuit.local.json --name "Second Suit"
# Zweites Profil ausfuellen:
python3 tools/suit_fit.py --profile build/SecondSuit.local.json --out build/SecondSuit
```

## Konzepte ohne vollstaendige Masse

```bash
python3 tools/suit_fit.py --profile Design/Parametric/Profiles/Demo.json --concept --out build/Demo
```

`Demo.json` enthaelt synthetische Beispielwerte. `Template.json` enthaelt keine
Personendaten. Die Option `--concept` erlaubt synthetische Ergaenzungen und
kennzeichnet die Ausgabe als Konzept. Beispielwerte sind weder Durchschnitts-
noch empfohlene Zielmasse. Aus einer Konzeptausgabe darf keine persoenlich
passende Druckdatei oder bestandene Passprobe abgeleitet werden.

## Auswahlfelder und reale Wirkung

| Feld unter build | Auswahl | Wofuer die Auswahl dient |
| --- | --- | --- |
| armor_reference | chief-infinite / mark-vii / custom | Referenzpaket fuer genau diese Ruestung festlegen |
| material | hybrid / foam / printed | Materialweg dokumentieren und passende Technik-Guides waehlen |
| operating_mode | wearable / exhibition / both | Tragebetrieb und/oder Ausstellung planen |
| features.exoskeleton | ein / aus | Separates Integrationsvorhaben einplanen |
| features.hud | ein / aus | Sicht-/Displayprobe und Strombedarf einplanen |
| features.lighting | ein / aus | Lichtpositionen, Kabel und Leistung einplanen |
| features.audio | ein / aus | Sprachverstaendlichkeit, Halter und Leistung einplanen |

Die Auswahlfelder stehen im Bereich `build`. Referenzwahl erzeugt keine
originalgetreuen Detailoberflaechen. Materialwahl bemisst weder Wandaufbau noch
Verbindungen. Ein gesetztes Exoskelett-Merkmal ist keine Herstellerfreigabe
und erzeugt keine passenden Motor-/Gurtvolumina. Die Optionen beschreiben den
Planungsumfang; die hier verlinkten Arbeitsschritte bleiben erforderlich.

## Budget und Nachweise je Projekt

Der [Budget-Editor](../../web/budget/) bearbeitet Mengen, Einzelpreise,
Zielmassen und Reserve einer eigenen BOM. Import und Export verwenden das
gleiche JSON-Format wie die Kommandozeile. Es gibt dort keine automatische
Browserspeicherung; die Datei nach Aenderungen explizit exportieren.

Die [Basis-BOM](../../Materials/Mjolnir-BOM.md) ist ein Beispiel fuer einen
vollstaendigen Aufbau. Eine eigene Kopie der JSON-BOM anpassen und getrennt
auswerten:

```bash
cp Materials/Mjolnir-BOM.json build/MySuit-BOM.local.json
python3 tools/suit_budget.py --bom build/MySuit-BOM.local.json --out build/MySuit-Budget.md
```

Mengen, vorhandene Teile, Material- und Finishkosten sowie optionale Systeme
muessen dem tatsaechlichen Entwurf entsprechen. Konfigurator-Auswahl und
Budgetdatei sind keine automatisch belastbare Einkaufs- oder Gewichtsermittlung.
Reale Bauteilmasse und aktuelle Angebote ersetzen spaeter die Planwerte.

Fuer das konkrete Projekt einen leeren Nachweisdatensatz anlegen:

```bash
python3 tools/suit_readiness.py --init build/MySuit-readiness.local.json --project "My Suit" --revision "prototype-01"
```

Die [Nachweisanleitung](../../Tests/TestReports/Mjolnir-Abnahme.md) beschreibt
Pruefungen und Belege. Ein neuer Name oder ein ausgefuelltes Profil setzt
keinen Test auf bestanden. Aenderungen an Profil, Material, Hardware oder
Schnittstellen muessen bei der Bewertung der vorhandenen Nachweise beruecksichtigt werden.

## Eingabegrenzen

Die gemeinsamen Felddefinitionen begrenzen plausible Eingaben, zum Beispiel
Koerpergroesse auf 1200-2200 mm. Diese Softwaregrenzen sind kein nachgewiesener
Passbereich und keine Eignungsaussage fuer Kinder oder eine bestimmte Person.
Ein Wert ausserhalb des Bereichs darf nicht durch einen passenden Ersatzwert
verfaelscht werden: Rechenmodell und Grenzen muessen dann gesondert ueberarbeitet
und geprueft werden. Auch innerhalb des Bereichs bleibt die Passprobe erforderlich.

## Was weiterhin konstruiert werden muss

Vor einem tragbaren Endteil werden Referenzmodell, segmentierte Innenkonturen,
Verbindungen, Lastpfade, Visier, Luftfuehrung und Fertigungsparameter benoetigt.
Danach folgen reale Pass-, Bewegungs-, Ausstiegs- und Belastungsproben.
Fuer Ausstellungen kommen gepruefter Staender, Transport und Vorfuehrablauf hinzu.
Ein generisches Profil macht den Entwicklungsablauf wiederverwendbar; es
ersetzt diese Arbeit nicht.

Weiter: [Systementwurf](Mjolnir-Systementwurf.md),
[Fertigung](Mjolnir-Fertigung.md), [Parametrisches CAD](../../Design/Parametric/README.md).
