# Einkauf: optionales Nebelmodul

Aktuelle Produktzuordnung: [zentraler Produktkatalog](../web/products/) und
[Einkaufslinks mit Auswahlkriterien](Einkaufsliste-Links.md). Budgetwerte in dieser
Datei sind Planungswerte, keine aktuellen Shop-Angebote.

Stand 2026-09-10. Arbeitsbasis und Einbau:
[Schubduesen-Guide](../Documentation/Guides/Elektronik-Schubduesen.md).

Die folgenden EUR-Bereiche sind eigene Beschaffungsbudgets, keine verifizierten
Endpreise oder Waehrungsumrechnung. Der Hersteller zeigt das ausgewaehlte
[Cosplayer Bundle](https://pmigear.com/products/pmi-smoke-vest-on-body-smoke-system)
bei der Recherche mit 249 USD an; Lieferland, Variante, Steuern und Versand
sind beim konkreten Angebot abzugleichen. Vest Only enthaelt keinen Nebler.

| Position | Anzahl | Budget gesamt EUR | Auswahl |
| --- | ---: | ---: | --- |
| FOG01: SmokeNINJA Pro Cosplayer Bundle | 1 | 250-350 | Nebler, passende Schutzweste/Schlauchmaterial, Kammer, Originalfluid und Fernbedienung; Versionsumfang bestaetigen |
| FOG02: Abnehmbare Halterung und Servicezugang | 1 Satz | 25-50 | Nach Geraeteabmessungen und Waermeprobe fertigen |
| FOG03: LED-Ringe | 2 | 10-20 | Getrennt vom Fluidkanal; Anzahl je Ruestungsreferenz anpassen |
| FOG04: LED-Controller und Taster | 1 | 10-20 | Nur Lichtsteuerung; vorhandener Controller kann ausreichen |
| FOG05: Fertige USB-Versorgung fuer Licht | 1 | 20-35 | Strom nach LED-Datenblatt und Messung; kein Fogger-Netzteil |
| FOG06: Lichtverkabelung und Absicherung | 1 Satz | 15-30 | Querschnitt, Stecker und Sicherung nach realem Strom |
| **Zusatzmodul** | | **330-505** | Vor 20 Prozent Kostenreserve |
| **Mit Kostenreserve** | | **396-606** | Versand/Import und Werkzeug nicht pauschal enthalten |

Kein separater Wasserbehaelter, Heizdraht, Glyzerin-/PG-Rohstoff, MOSFET zum
Schalten der Heizung oder zusaetzlicher Druckluefter wird fuer diese Variante
bestellt. Im Bundle vorhandenes Fluid nicht nochmals als Startbedarf zaehlen.
Nachfuellfluid, Ersatzkammer und Vanishing Kit sind spaetere Zusatzposten.
Kammern und Fluide nur in den vom Hersteller vorgesehenen Paarungen einsetzen.

## Optionale technische Ausbaustufen

Diese Positionen sind **nicht** in den Summen oder der JSON-BOM enthalten.
Auswahl und Angebot folgen der [technischen Entscheidung](../Documentation/Guides/Mjolnir-Nebeltechnik.md).

| Option | Beschaffungsumfang | Vor Auswahl zu klaeren |
| --- | --- | --- |
| Kammer naeher an die Duese | [Original Chamber Extension Cable](https://pmigear.com/products/pmi-chamber-extension-cable), eigene warme Serviceaufnahme | Exakte Geraete-/Kammerkompatibilitaet; Kabellaenge und thermische Montage |
| Gemeinsamer Foto-Start | Passender OEM-Kabeltaster oder OEM-DMX-Modul mit Anleitung | Anschlussdaten, Stop-/Ausfallverhalten; Preis und lieferbare SKU offen |
| Je Duese eine Quelle | Zweites vollstaendiges OEM-Geraet mit Akku/Kammer und Befestigung | Masse, Energie und zwei separat stoppbare Kanaele; keine zwei Kammern an einem Ausgang |
| Kurzer sichtbarer Nebel | Vollstaendiges passendes Vanishing Kit | Eigene Kammer/Duese sowie Freigabe der konkreten Schlauch-/Vest-Kombination |
| Andere Steuerplattform | MicroFogger 5 Pro mit dafuer bestimmtem Steuerkabel oder Tiny FX | Ersetzt FOG01; eigener Halter, Fluid und Waermeauslegung statt PMI-Vest-Uebernahme |

Vor Bestellung aktuelle Montageanleitung der konkreten PRO-V2-/Vest-Version
und Sicherheitsdatenblatt sichern. Die alte frei abrufbare PRO-Anleitung ist
keine hinreichende Freigabe eines koerpernahen Sonderaufbaus.

Alle getragenen Massen sind in der [JSON-BOM](Mjolnir-Nebel-BOM.json) unbekannt.
Vor einer Gewichtsbewertung die komplette Baugruppe inklusive Fluidfuellung,
Akku, Schlaeuchen und Haltern wiegen. Doppelzaehlung von Weste/Traeger,
Beleuchtung und Stromversorgung beim Zusammenfuehren mit der Basisliste pruefen.

```bash
python3 tools/suit_budget.py --bom Materials/Mjolnir-Nebel-BOM.json --out build/Nebel-Budget.md
```

Alternativ im [Budgeteditor](../web/budget/) die vorhandene Projektliste laden
und das Modul hinzufuegen. Projektreserve und Massenziel bleiben unveraendert.
