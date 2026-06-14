# Sicherheit

> **Level:** [A] Anfaenger | [F] Fortgeschritten | [P] Profi  |  **Varianten:** alle  |  **Voraussetzungen:** keine, vor dem ersten Tragen lesen

Sicherheit hat Prioritaet. Teste jede Baugruppe einzeln und plane immer einen schnellen Ausstieg.

## Bauphase

- Atemschutz beim Schleifen und Lackieren (besonders Filler Primer, XTC-3D, 2K-Lacke)
- Handschuhe bei Klebern/Harzen (CA-Kleber, Epoxy, Kontaktkleber)
- Gute Belueftung bei Sprays und Plasti-Dip
- Schutzbrille beim Dremel-Einsatz und Schleifen

## Elektronik

- Nur Akkus mit Schutzschaltung/BMS nutzen
- Akkus nie im Kostuem laden, immer extern
- Kabel gegen Zug sichern (Klett, Kabelkanaele)
- Not-Aus-Schalter oder Schnelltrennung vorsehen
- Sicherungen nahe der Batterie (2-3 A fuer Logik, 5-10 A fuer LEDs)
- Strom vor Einbau mit Multimeter messen

## Hitze-Management (Convention)

- Volle Ruestung staut Waerme - Koerpertemperatur kann gefaehrlich steigen
- **Helm-Luefter:** 2x 40 mm Luefter (Intake unten, Exhaust oben) - fast Pflicht
- **Kuehlweste:** unter der Ruestung mit Kuehlakku-Taschen tragen, mehrere Kuehlakkus zum Wechseln mitbringen
- **Material:** leichte EVA-Foam/3D-Druck mit Belueftungsspalten zwischen Ruestungsteilen
- **Unteranzug:** feuchtigkeitsableitendes Sportmaterial, KEIN Baumwoll-T-Shirt
- **Zeitplan:** Outdoor-Shoots fruehmorgens oder spaetabends, Mittagshitze vermeiden

## Hydrierung

- **CamelBak/Trinkblase:** Schlauch innen in der Ruestung zum Helm fuer freies Trinken - essentiell bei Voll-Ruestung
- Bei jeder Gelegenheit trinken, nicht auf Durst warten
- Elektrolyt-Ergaenzung, nicht nur Wasser
- Pausen alle 30-45 Minuten einplanen

## Sichtfeld und Mobilitaet

- Helm-Sichtfeld testen fuer Treppen, Bordsteine, Tuerrahmen, niedrige Decken
- Peripheres Sehen pruefen - Convention-Boeden sind voll
- Sitzen, Hocken, Treppen, Tueren vorher testen
- Ruestung sollte Toilettengang ohne Komplett-Demontage ermoeglichen
- Gewicht auf die Huefte, nicht auf die Schultern
- Mindestens 30 Minuten im vollen Anzug zu Hause ueben

## Handler (Buddy-System)

- **Essentiell bei voller Halo-Ruestung** - Handler hilft navigieren, haelt Sachen bei Fotos, warnt vor Hindernissen
- Handler traegt Wasser, Handy, Geldboerse, Reparatur-Kit
- Handler managed Fotoanfragen und Crowd-Kontrolle
- Handler hilft bei Notfall-Entfernung der Ruestung
- Handler angemessen danken - Ticket, Essen, etc.

## Tragen

- Gewicht auf die Huefte, nicht auf die Schultern
- Quick-Release fuer Brust/Beine einplanen
- Helm nie ohne Lueftung bei langen Sessions

## Conventions

- Regeln vorher pruefen (siehe `Convention-Regeln.md`)
- Prop-Waffen deklarieren
- Kein Metall an Kanten/Spitzen
- Props in geschlossenen Taschen transportieren (Waffengesetz)

## Hitze- und Belastungsmanagement

Dieser Abschnitt ist kein optionaler Komfort-Tipp, sondern Pflichtlektuere. Ein
geschlossener MJOLNIR-Helm plus Voll-Ruestung wirkt wie eine Sauna: Du atmest
warme Luft, der Koerper kann Schweiss kaum verdunsten und die Hitze staut sich.
Kombiniert man das mit einer Sommer-Con (Halle mit 28-32 Grad, kaum Luftzug) und
koerperlicher Anstrengung (Posen, Laufen, Treppen, Foto-Sessions), entsteht
schnell ein gefaehrlicher Hitzestau. Die Folge sind Dehydrierung, Kreislauf-
Kollaps und im schlimmsten Fall ein Hitzschlag mit Ohnmacht - und in einem Helm
mit Quick-Release, das nur jemand von aussen kennt, ist eine bewusstlose Person
ein echter Notfall. Das gilt fuer alle drei Varianten: V1 (Foam) heizt langsamer
auf als V2/V3, aber kein Material schuetzt vor Hitzestau, wenn keine Luft zirkuliert.

### Warum es kritisch ist

- Der Helm faengt Atemluft und Koerperwaerme ein - die Innentemperatur liegt oft
  5-10 Grad ueber der Hallentemperatur.
- Schweiss kann unter der Ruestung nicht verdunsten, die natuerliche Kuehlung faellt aus.
- Adrenalin und Konzentration auf die Performance maskieren Warnsignale - viele
  merken die Ueberhitzung erst, wenn es schon spaet ist.
- V3 mit Exoskelett und voller AR-Elektronik fuegt zusaetzliche Waermequellen
  (Motoren, Akkus, Rechner) direkt am Koerper hinzu.

### Warnsignale erkennen (Schwellen)

Brich die Session SOFORT ab und nimm den Helm ab, wenn eines dieser Anzeichen auftritt:

| Stufe | Anzeichen | Handlung |
|-------|-----------|----------|
| Fruehwarnung | Starkes Schwitzen, Durst, leichte Mattigkeit | Trinken, in den Schatten, Tempo raus |
| Ernst | Schwindel, Kopfschmerz, Herzrasen/Puls fuehlbar im Kopf, Uebelkeit | **Helm sofort ab**, hinsetzen, kuehlen |
| Notfall | Verwirrtheit, kein Schwitzen mehr trotz Hitze, trockene heisse Haut, Sehstoerungen, drohende Ohnmacht | **Komplett ausziehen**, kuehlen, Notruf 112 |

Faustregel: **Im Zweifel Helm ab.** Ein paar Minuten ohne Helm kosten nichts, ein
Kreislaufkollaps in der Crowd kann gefaehrlich werden. Wer sich "komisch" fuehlt,
hat schon zu lange gewartet.

### Massnahmen

1. **Aktive Belueftung einbauen.** Helm-Luefter sind bei Voll-Ruestung praktisch
   Pflicht: ein Intake-Luefter unten, ein Exhaust oben, sodass ein Luftstrom am
   Gesicht vorbeizieht. Dimensionierung, Verkabelung und Strombudget stehen in
   `Documentation/Guides/Elektronik-Luefter.md`. Teste vor der Con, dass die
   Luefter bei voller Akkulaufzeit durchhalten.
2. **Trinkblase/CamelBak.** Schlauch von der Trinkblase im Ruecken nach innen zum
   Mund fuehren, sodass du ohne Helm-Abnahme trinken kannst. Vor der Con mit
   geschlossenem Helm ueben, damit der Schlauch sicher in Mundnaehe sitzt.
   Mindestens 2 Liter, plus Elektrolyte (nicht nur reines Wasser).
3. **Pausenzyklen.** Plane feste Helm-ab-Pausen: alle 60-90 Minuten raus aus der
   Crowd, in den Schatten oder einen kuehlen Raum, Helm ab, 5-10 Minuten
   abkuehlen und trinken. Bei grosser Hitze die Intervalle verkuerzen. Setze dir
   einen Timer (Handy beim Handler) - Adrenalin laesst die Zeit verschwimmen.
4. **Kuehlweste/Eispacks.** Eine Kuehlweste mit Kuehlakku-Taschen unter der
   Ruestung tragen, mehrere Kuehlakkus zum Wechseln im Cooler deponieren. Eispacks
   an Nacken, Handgelenken und Leiste kuehlen das Blut effektiv. Eispacks nie
   direkt auf die Haut (Erfrierungsgefahr) - immer mit duennem Stoff dazwischen.
5. **Atemwege frei halten.** Nichts darf die Atmung oder den Luftstrom zum Mund
   blockieren. Halsmanschette, Unteranzug-Kragen und Polster so anpassen, dass du
   tief durchatmen kannst. Bei Bartmasken/Polstern darauf achten, dass sie nicht
   verrutschen und Nase/Mund verdecken.
6. **Unteranzug und Timing.** Feuchtigkeitsableitendes Sportmaterial statt
   Baumwolle, Outdoor-Shoots in die kuehlen Tageszeiten legen (siehe auch den
   Abschnitt Hitze-Management oben).

### Sichtfeld-Sicherheit

Eingeschraenktes Sehen ist neben der Hitze die zweite grosse Gefahr - besonders
bei V3 mit AR/Passthrough-Display, wo du die Umgebung nur ueber Kamera und Bild
siehst.

- **Handler-Pflicht.** Bei Voll-Ruestung mit Helm immer ein Handler dabei (siehe
  Abschnitt Handler oben). Der Handler fuehrt an Treppen, Bordsteinen,
  Engstellen und durch die Crowd. Vereinbart Handzeichen fuer "Stopp", "Stufe",
  "rechts/links".
- **Treppen und Hoehenunterschiede.** Niemals blind eine Treppe nehmen. Handler
  ansagen lassen, Gelaender suchen, langsam. Bordsteine und Rampen sind im Helm
  schwer abzuschaetzen.
- **Engstellen und Tueren.** Tuerrahmen, niedrige Decken, Standwaende und
  Crowd-Gassen vorher mental durchgehen. Schulterplatten und Helm machen dich
  breiter und hoeher, als du es gewohnt bist.
- **AR/Passthrough besonders kritisch.** Latenz, Bildausfall oder ein leerer Akku
  koennen das Bild von einer Sekunde auf die andere abschalten. Plane immer eine
  direkte Sichtmoeglichkeit (klappbares Visier, schneller Helm-Release) und teste
  das System lange vor der Con. Setup und Failsafes siehe
  `Documentation/Guides/Elektronik-HUD.md`.

### Elektrik-Sicherheit (kurz)

- **LiPo-Handling:** Nur Akkus mit BMS/Schutzschaltung verwenden, nie geblaehte
  oder beschaedigte Zellen einsetzen. Akkus extern laden, nie im Kostuem (siehe
  Abschnitt Elektronik oben).
- **Keine ueberhitzenden Akkus am Koerper:** Akkupacks gut belueftet und vom
  Koerper entkoppelt montieren. Im Betrieb regelmaessig die Temperatur pruefen -
  wird ein Pack heiss, sofort trennen und abkuehlen lassen.
- **Quick-Disconnect:** Eine zentrale Schnelltrennung/Not-Aus vorsehen, die du und
  dein Handler im Notfall blind finden und in Sekunden loesen koennt. Bei Hitze-
  oder Elektriknotfall: erst stromlos, dann Helm/Ruestung ab.
