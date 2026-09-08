# HaloCosplay: konfigurierbare MJOLNIR-Projektmappe

Werkzeuge und Bauanleitungen fuer unterschiedliche Halo-Cosplays: eigene
Koerpermasse, getrennte linke/rechte Seiten, waehlbare Ruestungsreferenz,
Materialweg und Ausstattung. Ein Projektprofil haelt die Entscheidungen zusammen.
Es gibt keine vorgegebene Person, Koerpergroesse oder Schuhgroesse.

**Stand:** Parametrisches Bauraum-CAD, Mess- und Planungswerkzeuge sowie
Elektronikbeispiele. Vollstaendige Halo-Detailmodelle und nachgewiesene tragende
Mechanik fehlen weiterhin. Ein ausgefuelltes Profil erzeugt keine fertige
Druckruestung; reale Pass-, Last- und Funktionstests bleiben erforderlich.

## Eigenes Projekt starten

1. [Konfiguration und Mehrprofil-Workflow](Documentation/Guides/Mjolnir-Konfiguration.md)
   lesen oder den [Profil-Konfigurator](web/configurator/) oeffnen.
2. Ein leeres Profil anlegen; unbekannte Masse bleiben `null`.
3. Referenz, Material, Trage-/Ausstellungsbetrieb und optionale Technik auswaehlen.
4. [Messdefinitionen](Documentation/Guides/Mjolnir-Massanpassung.md) verwenden und
   jedes Projekt in ein eigenes Ausgabeverzeichnis rechnen.
5. [Prototypenfolge](BuildGuides/Armor/Mjolnir-Prototypen.md) am realen Aufbau pruefen.

Ab Repository-Wurzel mit Python 3.11+:

```bash
python3 tools/suit_fit.py --init build/MySuit.local.json --name "My Suit"
# Profil ausfuellen; danach ohne synthetische Ergaenzungen rechnen:
python3 tools/suit_fit.py --profile build/MySuit.local.json --out build/MySuit
```

Fuer die reine Demonstration ohne eigene Masse:

```bash
python3 tools/suit_fit.py --profile Design/Parametric/Profiles/Demo.json --concept --out build/Demo
```

`Template.json` enthaelt 32 leere Messfelder. `Demo.json` ist ausdruecklich
synthetisch. Mit `--concept` duerfen fehlende Masse fuer eine Konzeptansicht
ergaenzt werden; diese Herkunft bleibt sichtbar. Ohne die Option stoppt die
Berechnung bei fehlenden Werten. Private Profile und Berichte unter `build/`
halten; dieser Ordner wird nicht versioniert.

![Technische 2D-Draufsicht des synthetischen Oeffnungsbeispiels](Design/Parametric/Generated/OpeningEnvelope.svg)

## Konfigurierbare Entscheidungen

| Auswahl | Moeglichkeiten | Wirkung und Grenze |
| --- | --- | --- |
| Ruestungsreferenz | Chief / Infinite Mark VI GEN3, Mark VII, eigene Referenz | Eindeutiger Planungsbezug; keine automatische Detailmodellbeschaffung |
| Materialweg | Hybrid, Foam, 3D-Druck | Dokumentiert den Bauweg; Wandstaerke und Befestigungen separat auslegen |
| Einsatz | Getragen, Ausstellung, beides | Legt den Projektumfang fest; reale Abnahme je Einsatz erforderlich |
| Ausstattung | Exoskelett, HUD, Licht, Audio jeweils optional | Keine feste Elektronikpflicht; Aktivierung ersetzt keine Integration |
| Passform | Eigene mm-Werte und einstellbare Zuschlaege | Laenge, Breite, Tiefe und Seiten bleiben unabhaengig |

Das mechanische Basiskonzept verwendet vormontierte Baugruppen: Seitenfluegel
ausfahren, Frontschalen aufklappen, Einstieg und Handverschluesse. Die
Anziehstation haelt ausschliesslich ungetragene Ruestung. Der eigene Traeger
verteilt Ruestungsgewicht auf den Koerper; ein optionales Hueft-Exoskelett
ist ein separat anzupassendes System.

## Bau und Technik

- [Systementwurf und Baugruppen](Documentation/Guides/Mjolnir-Systementwurf.md)
- [Einstieg, Verriegelung und Anziehstation](Documentation/Guides/Mjolnir-Einstieg.md)
- [Parametrisches CAD und eigene Ausgabe](Design/Parametric/README.md)
- [Ruestungsreferenz und optische Abnahme](Documentation/Guides/Authentizitaet-Referenz.md)
- [Fertigungsplan und Schnittstellen](Documentation/Guides/Mjolnir-Fertigung.md)
- [Exoskelett und eigener Traeger](Documentation/Guides/Exoskelett.md)
- [Elektronik und optionale Aktorik](Documentation/Guides/Mjolnir-Elektronik.md)
- [Bezahlbare Hardware fuer einen ersten Prototyp](Materials/Mjolnir-Einkauf-Prototyp.md)
- [Budget-Editor mit JSON-Import/-Export](web/budget/) und [Beispiel-BOM](Materials/Mjolnir-BOM.md)
- [Messebetrieb](Documentation/Guides/Mjolnir-Messebetrieb.md) und [Zusatzbudget](Materials/Mjolnir-Messebudget.md)
- [Nachweisstatus](Progress/Mjolnir-Readiness.md) und [reale Abnahmeprotokolle](Tests/TestReports/Mjolnir-Abnahme.md)
- [Offline-Messeanzeige](Code/Exhibition/README.md)

Die mitgelieferte BOM ist ein editierbares Beispiel, kein automatisch passendes
Angebot fuer jedes Profil. Mengen, Ausstattung, Preise und Zielmassen nach dem
eigenen Entwurf anpassen. Testberichte gehoeren jeweils zum geprueften Projekt
und zur dokumentierten Revision. Softwarepruefungen sind keine Hardwarefreigabe.

## Web-Version und lokale Nutzung

[Web-Version](https://huskynarr.github.io/HaloCosplay/) mit Guides,
[Konfigurator](web/configurator/) und lokaler Fortschrittsverwaltung.
Der Konfigurator unterstuetzt mehrere Profile, JSON-Import/-Export und
optionales Speichern im Browser. Die Bedienung ist in
[Konfiguration](Documentation/Guides/Mjolnir-Konfiguration.md) beschrieben.
Technische Start-/Deploy-Hinweise: [web/README.md](web/README.md).

## Weitere Material- und Technikreferenzen

V1 (Foam), V2 (3D-Druck/Hybrid) und V3 (erweiterte Technik) sind historische
Guide-Kategorien. Sie sind keine Pflichtpakete und keine Garantie, dass Module
ohne Umbau kompatibel sind. Material, Referenz und Elektronik werden fuer jedes
Projekt getrennt entschieden.

- [Dokumentationshub](Documentation/README.md)
- [Varianten und Bauwege](Documentation/Guides/Varianten.md)
- [Komplett-Walkthrough](Documentation/Guides/Komplett-Walkthrough.md)
- [Projektaufgaben](Documentation/TODO.md)
- [STL-Quellen](Resources/STL-Quellen.md)
- [Materialsammlung](Materials/ShoppingList.md)
- [Sicherheit](Documentation/Guides/Sicherheit.md) und [Convention-Regeln](Documentation/Guides/Convention-Regeln.md)

## Projektstruktur und Pruefung

`Documentation/` enthaelt die Guides, `BuildGuides/` die Bauphasen, `Design/`
Profile und CAD, `Materials/` Budgetvorlagen, `Code/` Elektronikbeispiele,
`tools/` Generatoren und `Tests/` Softwaretests sowie physische Protokolle.

```bash
python3 tools/suit_budget.py --check
python3 -m unittest discover -s Tests/Automation -v
```

FAQ und Kontakt: [Support](Support/FAQ.md), [Kontakt](Support/Contact.md).
Community: [405th Infantry Division](https://www.405th.com/),
[RPF](https://www.therpf.com/).
