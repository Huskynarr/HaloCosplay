# V3-Systemarchitektur: Alle Module im Zusammenspiel

> **Level:** [P] Profi  |  **Varianten:** V3 (einzelne Module auch fuer V2 nutzbar)
> **Voraussetzungen:** Strombudget verstanden (`Elektronik-Strombudget.md`), Einzelmodule
> bekannt (HUD, LEDs, Schubduesen, Audio, AR). Dieser Guide verdrahtet nichts neu -
> er ordnet die vorhandenen Module zu EINEM System.

Ein volles V3-Setup besteht aus sechs Subsystemen: AR-Display mit HUD, Visor-LEDs
mit Helm-Lueftung, Sensorik, Schubduesen mit Nebler, Voice Changer mit Lautsprecher
und (optional) einer POV-Kamera. Dieser Guide beschreibt, wie sie zusammenspielen,
ohne sich gegenseitig zu gefaehrden.

## 1. Grundprinzip: Entkoppeln statt zentralisieren

**Kein zentrales Hirn.** Jedes Subsystem laeuft autark mit eigenem Controller und
eigenem Taster. Es gibt bewusst KEINE Funk- oder Busvernetzung aller Module
(ESP-NOW, zentrale App o.ae.) - das klingt attraktiv, vervielfacht aber die
Fehlerquellen und macht Fehlersuche auf der Convention unmoeglich.

Was das konkret bringt:

- Faellt der AR-Rechner aus, laufen Luefter, Visor-LEDs, Duesen und Audio weiter.
- Jedes Modul wird einzeln gebaut, getestet und in Betrieb genommen.
- Ein defektes Modul wird auf der Con einfach abgeschaltet, der Rest laeuft.

Einzige erlaubte Kopplungen: der SensorFeeder speist den AR-Rechner per
USB/Serial (Heading, Akku, Temperatur), und der Pi darf dem Helm-Arduino per I2C
Kommandos geben (Helligkeit, Effekt). Beide Verbindungen sind so gebaut, dass ihr
Ausfall nichts lahmlegt.

## 2. Module und Verantwortlichkeiten

| Modul | Ort | Controller | Code/Guide |
| --- | --- | --- | --- |
| AR-Passthrough + HUD | Helm | Raspberry Pi 4/5 | `Code/HelmetControl/AR/`, `Elektronik-AR-Display.md` |
| Visor-LEDs + Helm-Luefter | Helm | Arduino Nano (I2C Slave 0x08) | `Code/HelmetControl/HelmetMultiEffects.ino` |
| Sensorik (IMU, Akku, Temp) | Helm | ESP32 | `Code/HelmetControl/AR/SensorFeeder/` |
| POV-Kamera | Helm | autarke Action-Cam | Abschnitt 4 |
| Schubduesen-LEDs + Nebler | Ruecken | Arduino/ESP32 | `Elektronik-Schubduesen.md` |
| Voice Changer + Lautsprecher | Brust/Helm | eigenes Modul | `Elektronik-Audio.md` |
| Armor-LEDs | Torso/Glieder | Arduino Nano | `Code/ArmorControl/MultiEffects.ino` |

```
        HELM                                RUECKEN / BACKPACK
+---------------------------+      +------------------------------------+
| Pi 4/5 (AR + HUD)         |<-USB-| (Akkus sitzen im Backpack)         |
| ESP32 SensorFeeder      --+      | Arduino: Duesen-LEDs + Nebler      |
| Nano: Visor-LED + Luefter |      |   [eigener Boost-Taster]           |
|   [eigener Effekt-Taster] |      |                                    |
| Action-Cam (autark, POV)  |      | Schiene 1: Powerbank/Step-Down Pi  |
+---------------------------+      | Schiene 2: LEDs + Nebler + Luefter |
        BRUST                      | Schiene 3: Audio                   |
+---------------------------+      +------------------------------------+
| Mikro (innen) -> Voice-   |
| Changer -> Lautsprecher   |
+---------------------------+
```

## 3. Stromverteilung: drei Schienen

Alle Akkus sitzen im Backpack/Torso (Gewicht, Hot-Swap, Kuehlung). Von dort gehen
drei getrennt abgesicherte 5V-Schienen ab:

| Schiene | Verbraucher | Spitzenlast ca. | Sicherung |
| --- | --- | --- | --- |
| 1: Rechner | Pi 4/5 + AR-Display + Kamera, SensorFeeder | 1.5-3.0 A | 3 A |
| 2: Effekte | Visor-/Armor-/Duesen-LEDs, Nebler, alle Luefter | 2.0-3.5 A (Boost) | 5-10 A |
| 3: Audio | Voice Changer + Verstaerker + Lautsprecher | 0.3-0.8 A | 2 A |

Warum getrennt: Der Nebler-Boost und LED-Spitzen erzeugen Spannungseinbrueche,
die einen Pi mitten im Passthrough rebooten wuerden (= ploetzliche Blindheit).
Der Rechner bekommt deshalb IMMER eine eigene Versorgung. Audio liegt getrennt,
weil Stoergeraeusche (Brummen/Zirpen) fast immer ueber gemeinsame
Versorgungsleitungen einstreuen.

- **Stromaufnahme Voll-V3: typisch 4-5 A im Betrieb, bis ~7-8 A in der Spitze**
  (alle Schienen-Maxima zusammen, z.B. Nebler-Boost gleichzeitig mit Pi-Last).
  Die Spitzen treten kurz und selten gleichzeitig auf - die getrennten Schienen
  fangen genau das ab. Rechne dein konkretes Setup mit `Elektronik-Strombudget.md`
  durch, plane 20-30% Reserve ein und MISS vor dem Einbau.
- Akku-Optionen: 2x 20.000 mAh Powerbanks (eine fuer Schiene 1, eine fuer 2+3)
  oder 3S LiPo mit zwei 5V/5A Step-Downs - siehe `Elektronik-Batterie.md`.
- Stufe-C-AR halbiert die Laufzeit gegenueber Stufe A. Fuer einen vollen Con-Tag
  Hot-Swap in der Mittagspause einplanen (Wechselakku in der Tasche).
- Pro Schiene ein eigener, von aussen erreichbarer Hauptschalter. Dickere
  Leitungen und Steckverbinder nach `Elektronik-Verdrahtung.md`.

## 4. POV-Kamera (Aufnahmen aus dem Helm)

**Empfehlung: autarke Mini-Action-Cam** (z.B. Insta360 Go, DJI Action Mini) hinter
einem kleinen Schlitz im Visor oder Helmrand.

- Eigener Akku, eigener Speicher, eigener Startknopf - null Software, null Risiko
  fuer die sicherheitskritische Passthrough-Kette.
- Position: mittig ueber oder unter dem Visor, Blickrichtung = Sichtachse.
  Vor dem Verkleben mit Klebeband testen (Bildausschnitt!).
- Waermequelle beachten: nicht direkt neben den Pi setzen.

**Variante fuer Spaeter: HUD-Mitschnitt ("Killcam").** Der Pi 5 kann den fertigen
Passthrough-Feed INKLUSIVE HUD-Overlay per Hardware-Encoder (H.264) mitschneiden -
fuer Analysen und Social Media einzigartig. Aber: Encoding kostet Latenz und
Waerme am Kopf. Regel: erst wenn der Passthrough stabil laeuft, als zuschaltbares
Feature einbauen, und der Pflicht-Latenztest (`Code/HelmetControl/AR/README.md`)
muss AUCH MIT laufender Aufnahme bestehen.

**Rechtlicher Hinweis:** Auf Conventions gelten Foto-/Filmregeln, und gefilmte
Personen haben Rechte am eigenen Bild. Versteckte Dauer-Aufnahmen in der Menge
sind tabu - Kamera sichtbar deklarieren (Hinweis am Kostuem oder auf Nachfrage)
und die Regeln der jeweiligen Con pruefen: `Convention-Regeln.md`.

## 5. Audio-Integration (Kurzfassung)

Details in `Elektronik-Audio.md` - hier nur die Integrationsregeln:

- **Nicht auf dem AR-Pi rechnen.** Der ist mit der Kamera ausgelastet; Audio-Latenz
  ueber 30-50 ms wirkt beim Sprechen sofort unnatuerlich. Dedizierten
  Arduino-Pitch-Shifter (Option B) oder fertiges Voice-Changer-Modul nutzen.
- **Rueckkopplung vermeiden:** Lautsprecher an die Brust (nach aussen), Mikro dicht
  vor den Mund im Helm. Nie Lautsprecher und Mikro zusammen in den Helm.
- Lautstaerke auf der Con erst moderat testen - Hallen verstaerken anders als die
  Werkstatt.

## 6. Inbetriebnahme: Modul fuer Modul

Grundsatz aus dem ElectronicsGuide gilt verschaerft: **Nie alle Module gleichzeitig
erstmals einschalten.**

1. Jedes Modul einzeln am Labornetzteil/USB testen (Strom messen, notieren)
2. Schiene 2 aufbauen: LEDs + Luefter + Nebler zusammen, Boost-Spitzenstrom messen
3. Schiene 1 aufbauen: Pi + Display + Kamera, Latenztest, Waermetest 30+ Minuten
4. Schiene 3 aufbauen: Audio, Rueckkopplungstest im geschlossenen Helm
5. Alles zusammen aus den finalen Akkus: Gesamtstrom messen, gegen Budget pruefen
6. Generalprobe in voller Montur 2+ Stunden (Hitze, Laufzeit) - Ergebnis als
   Testreport dokumentieren (`Tests/README.md`)

### Einschaltreihenfolge am Con-Morgen

1. Schiene 2 (Effekte) - Boot-Sequenzen pruefen
2. Schiene 1 (Rechner) - HUD da? Latenz-Anzeige gruen?
3. Schiene 3 (Audio) - kurzer Sprechtest
4. POV-Cam zuletzt (Akkulaufzeit sparen)

## 7. Ausfall-Matrix (was passiert wenn X stirbt)

| Ausfall | Effekt | Verhalten im Kostuem |
| --- | --- | --- |
| Pi / AR | HUD weg, Warnbanner bzw. schwarz | Visor hochklappen (Notausblick), Rest laeuft weiter |
| SensorFeeder | HUD ohne Heading/Akku-Anzeige | unkritisch, weiterlaufen |
| Helm-Arduino | Visor-LEDs + Luefter aus | Luefter-Ausfall ernst nehmen: Pausenraum, Helm ab |
| Duesen-Arduino | Ruecken-Effekte aus | unkritisch, Schiene 2 sonst unberuehrt |
| Audio | Stimme nur gedaempft hoerbar | unkritisch, lauter sprechen |
| Akku Schiene 1 | wie Pi-Ausfall | Hot-Swap oder auf Stufe A zurueckfallen |
| Akku Schiene 2 | alle Effekte + LUEFTER aus | wie Luefter-Ausfall behandeln |

Die zwei kritischen Faelle sind Passthrough-Ausfall (deshalb mechanischer
Notausblick, Pflicht-Regeln in `Elektronik-AR-Display.md` Abschnitt 3) und
Luefter-Ausfall im geschlossenen Helm (Hitzestau - siehe `Sicherheit.md`).

## Verwandte Guides

- AR-Display und Sicherheitsregeln: `Elektronik-AR-Display.md`
- Schubduesen + Nebler: `Elektronik-Schubduesen.md`
- Audio/Voice Changer: `Elektronik-Audio.md`
- Strombudget: `Elektronik-Strombudget.md` | Batterien: `Elektronik-Batterie.md`
- Verdrahtung: `Elektronik-Verdrahtung.md` | Luefter: `Elektronik-Luefter.md`
- Exoskelett (mechanischer V3-Teil): `Exoskelett.md`
