# Einkauf: RGB-Power-Licht und trockene Duesenluefter

Aktuelle Produktzuordnung: [zentraler Produktkatalog](../web/products/) und
[Einkaufslinks mit Auswahlkriterien](Einkaufsliste-Links.md). Budgetwerte in dieser
Datei sind Planungswerte, keine aktuellen Shop-Angebote.

Stand: 2026-09-09. Beschaffungsplan fuer zwei Helmlampen und zwei beleuchtete
Duesen. Die [Lichtauslegung](../Documentation/Guides/Mjolnir-Lichtmodule.md)
ist massgeblich fuer Verschaltung und Messungen. Es wurde nichts bestellt.

## Verifizierte Produktkandidaten

| Komponente | Konkreter Kandidat und Quelle | Abrufstand und Auswahl |
| --- | --- | --- |
| RGB-Power-LED auf fertiger Metallkernplatine | [LEDSupply CREEXPE2-RGB, Cree XP-E2 auf 20-mm-Star](https://www.ledsupply.com/leds/cree-xpe2-rgb-high-power-led) | Detailseite zeigt 16,85 USD. Bestand und Optionsmeldung widersprechen sich; Lieferbarkeit und Chiprevision bestaetigen |
| RGB-Alternative | [LEDSupply J036-L1C1RGB00, LUXEON C 3-Up 20 mm](https://www.ledsupply.com/leds/luxeon-c-rgb-led) | 18,95 USD auf Detailseite; andere LED-Daten erfordern Anpassung der Auslegung |
| RGBW-Alternative | [LEDSupply CREEXML-RGBW, Cree XM-L Color](https://www.ledsupply.com/leds/cree-xml-rgbw-star-led) | 25,49 USD, beim Abruf ausverkauft; Weisskanal und Revision separat auslegen |
| Konstantstromtreiber | [MEAN WELL LDD-350L, Herstellerdatenblatt](https://www.meanwell.com/Upload/PDF/LDD-L/LDD-L-SPEC.PDF) | Sechs Stueck fuer zwei RGB-Paare in Reihenschaltung; genaue Bauform L, nicht ungeprueft LW/LS/1000L bestellen |
| Optik fuer XP-E2-3-Up | [Carclo 10508/10509 im Modulzubehoer](https://www.ledsupply.com/leds/cree-xpe2-rgb-high-power-led) | 2,93 USD je aufgefuehrter Optik; 10509 als nicht verfuegbar angezeigt. Eine mittlere und breite Streuung zuerst vergleichen |
| Trockener Effektluefter | [Noctua NF-A4x10 5V PWM](https://www.noctua.at/en/products/nf-a4x10-5v-pwm/specifications) | 40 x 40 x 10 mm, maximal 0,35 W und 0,07 A bei 5 V. Nur im separaten trockenen Luftkanal |

USD-Werte sind Momentaufnahmen der Originalangebote, keine umgerechneten
deutschen Endpreise. Steuern, Versand und Importkosten sind damit nicht
abgedeckt. Eine Kategorieseite zeigte einen anderen XP-E2-Preis; massgeblich
ist ein konkretes Angebot fuer die ausgewaehlte Ausfuehrung. Die folgenden
EUR-Betraege sind **Budgetansaetze**, keine Lieferantenzusagen.

## Mengen und Budget fuer den kompletten Zusatzaufbau

| ID | Position | Menge | Ansatz je Einheit | Summe EUR |
| --- | --- | --- | --- | --- |
| LIGHT01 | XP-E2 RGB-Star oder gleichartig dokumentiertes Fertigmodul | 4 | 20-30 EUR | 80-120 |
| LIGHT02 | LDD-350L-Konstantstromtreiber | 6 | 6-10 EUR | 36-60 |
| LIGHT03 | Aluminiumkuehlkoerper mit bekannter Kennlinie | 4 | 8-18 EUR | 32-72 |
| LIGHT04 | Passende Optik, Halter und wechselbare Schutzscheibe | 4 | 5-10 EUR | 20-40 |
| LIGHT05 | Waermeleitmaterial, Schrauben und offene Schutzgitter | 1 Satz | 20-35 EUR | 20-35 |
| LIGHT06 | 5-V-Pegelstufe, Treibertraeger und Controller-Anpassung | 1 Satz | 15-35 EUR | 15-35 |
| LIGHT07 | Temperaturfuehler und hardwareseitige Lichtabschaltung | 1 Satz | 20-40 EUR | 20-40 |
| LIGHT08 | Vorhandene oder neue PD-Versorgung mit gepruefter 15-V-Ausgabe und passendem Ausgangsmodul | 1 Satz | 40-75 EUR | 40-75 |
| LIGHT09 | 5-V-PWM-Effektluefter, beispielsweise NF-A4x10 5V PWM | 2 | 15-25 EUR | 30-50 |
| LIGHT10 | Trockene Luftkanaele, Lueftergitter und entkoppelte Halter | 1 Satz | 10-25 EUR | 10-25 |
| LIGHT11 | Abgesicherte Verteilung, Kabel, kodierte Stecker und Zugentlastung | 1 Satz | 20-40 EUR | 20-40 |
| | **Gesamter Planungsrahmen** | | | **323-592** |
| | **Mit 20 % Projektreserve** | | | **387,60-710,40** |

Nicht enthalten: Nebelgeraet und Fluid, komplette Ruestung, Haupt-Comfortlueftung,
CAD-Arbeit, Arbeitszeit, Messgeraete, Versand/Import und mehrfache Gehaeuseproben.
Diese Liste ist bewusst eine vollstaendige Zusatzkalkulation, kein
automatisch eingespielter Warenkorb.

## Bezahlbarer Einstieg und Abgleich vorhandener Teile

Zuerst entsteht ein symmetrisches Paar am Tisch: zwei gleiche RGB-Stars, drei
Treiber, zwei Kuehlkoerper und zwei Optiken. Bestehende geeignete Versorgung
und Steuerung werden nachgemessen. Nach erfolgreicher Probe wird das zweite
Paar ergaenzt. Der kostensparende Punkt ist die Reihenschaltung gleicher Farben,
nicht der Verzicht auf Kuehlung oder auf Konstantstromregelung.

Bei bereits vorhandenem Nebelmodul werden die Positionen der
[Nebel-BOM](Mjolnir-Nebel-BOM.json) einzeln abgeglichen:

| Bestehende Position | Behandlung beim Power-Licht-Ausbau |
| --- | --- |
| FOG01, Neblerbundle | Bleibt separat; kein neuer Nebler in dieser Liste |
| FOG02, Halter/Schlauchfuehrung | Nur tatsaechlich zusaetzliche Licht- und Trockenluftteile ergaenzen |
| FOG03, zwei kleine LED-Ringe | Durch das Duesen-Power-Licht ersetzen oder als zusaetzliche Dekoration bewusst behalten |
| FOG04, Controller/Taster | Auf Eignung pruefen; keine doppelte Pauschale bei Wiederverwendung |
| FOG05, 5-V-Lichtversorgung | Reicht fuer den 15-V-Konstantstromaufbau nicht automatisch. Vorhandene 5 V koennen nach Lastpruefung die Effektluefter speisen |
| FOG06, Kabel/Absicherung | Vorhandene geeignete Teile gegen LIGHT11 verrechnen |

Dasselbe gilt fuer die Basis-BOM: vorhandene Powerbanks, Kabel und Controller
werden nur einmal budgetiert. Die Budgetdatei des konkreten Projekts wird nach
diesem Abgleich angepasst; die generischen Listen bleiben getrennte Vorlagen.

## Bestellbare Spezifikation fuer offene Teile

- Kuehlkoerper: Metall, dokumentierte Abmessungen und thermische Kennlinie,
  plane Kontaktflaeche fuer den gewaehlten Star, verschraubbar. Eine pauschale
  Bezeichnung wie "fuer 10 W" reicht fuer den Helmeinbau nicht.
- Treibertraeger: sechs einzeln zugaengliche Kanaele, kein gemeinsames Verbinden
  der LED-Rueckleitungen mit Masse; 5-V-DIM-Pegel und abgeschalteter Reset-Zustand.
- Temperaturschutz: Sensorposition und Abschaltpfad am echten Kuehlmodul,
  festgelegte Fehlerreaktion auch bei geloestem Sensor. Ausloesewerte werden aus
  Bauteil-, Beruehrungs- und Einbaumessungen abgeleitet.
- Versorgung: im Betrieb tatsaechlich anliegende 15 V fuer Licht und separat
  5 V fuer die ausgewaehlten Luefter; dokumentiertes Leistungsverhalten bei
  mehreren Anschluessen. Keine unbekannte Powerbank-Revision einplanen.
- Kabel und Stecker: Nennspannung/Strom passend zu Last und Sicherung,
  mechanisch kodiert, mit Zugentlastung. Ein geeigneter Steckverbinder hat
  getrennte Kontakte fuer getrennte LED-Strange.

Ohne verifizierte Masse bleiben Gewichtsfelder unbekannt. Das Waerme- und
Leistungsbudget wird nach dem ersten Modulversuch mit Messwerten aktualisiert.
