# Elektronik-Guide

> **Level:** [A] Anfaenger | [F] Fortgeschritten | [P] Profi  ·  **Varianten:** alle

Diese Seite ist die zentrale Uebersicht ueber die gesamte Elektronik im MJOLNIR-Suit
(Master Chief, HALO INFINITE, GEN3-Proportionen). Sie ordnet die Einzel-Guides ein,
zeigt welches Modul fuer welche Variante sinnvoll ist und gibt eine empfohlene
Aufbau-Reihenfolge vor.

## Was die Elektronik leistet

Elektronik macht aus einem statischen Cosplay einen lebendigen Suit:

- Beleuchtung: gruenes Glimmen an Brustplatte, Schultern, Armmodulen (Authentizitaet zu GEN3).
- Visor/HUD: Statusanzeige im Helm, von dezenter Beleuchtung bis zu echtem Mini-Display.
- Klima: Luefter gegen Beschlag und Hitze im Helm.
- Sound: Voice-Changer/Funkstimme, Bootsounds, ambiente Effekte.
- Komfort/Show: Bootsequenzen, schaltbare Effekte, bei V3 AR-Passthrough und Sensorik.

Wichtigstes Designprinzip: **modular halten**. Jedes Modul (LEDs, Luefter, HUD, Audio)
soll eigenstaendig stromversorgt, einzeln steckbar und einzeln testbar sein. So kannst
du Module nachruesten, im Fehlerfall einzeln tauschen und den Suit ohne Loetkolben
auf der Convention zerlegen und packen (siehe `Documentation/Guides/Transport.md`).

## Modul-Matrix nach Variante

V1 = Einsteiger (Foam, Batterie, einfache LEDs).
V2 = Fortgeschritten (3D-Druck/TPU mit Bambulab H2C, HUD).
V3 = Profi (Exoskelett, AR, Premium).

Legende: **Pflicht** = gehoert zwingend dazu, **Empfohlen** = stark zu empfehlen,
**Optional** = nice-to-have, **Nicht noetig** = fuer diese Variante uebertrieben/unpassend.

| Modul | V1 | V2 | V3 |
| --- | --- | --- | --- |
| Einfache LEDs (5V/12V, gemeinsam geschaltet) | Pflicht | Optional | Nicht noetig |
| WS2812B-LEDs mit Effekten (adressierbar) | Optional | Pflicht | Pflicht |
| Helm-Luefter (Beschlag/Hitze) | Empfohlen | Pflicht | Pflicht |
| Transparentes OLED-HUD (SSD1309) | Nicht noetig | Empfohlen | Empfohlen |
| Pi-HUD-Software (hud_display.py) | Nicht noetig | Empfohlen | Pflicht |
| Audio / Voice-Changer | Optional | Empfohlen | Empfohlen |
| Autostart / systemd (kabelloser Start) | Nicht noetig | Empfohlen | Pflicht |
| AR-Passthrough (Kamera + Display) | Nicht noetig | Nicht noetig | Optional |
| Sensorik (IMU, Abstand, Akkustand, Temperatur) | Nicht noetig | Optional | Empfohlen |

Hinweise:
- V1 setzt bewusst auf wenige, robuste, gemeinsam geschaltete LEDs an einer Batterie.
  Ein Mikrocontroller ist nicht noetig; ein einfacher Schalter reicht.
- V2 ist der "Sweet Spot": adressierbare LEDs mit Effekten, OLED-HUD, Luefter, optional
  Voice-Changer. Pi Zero 2 W treibt das HUD, Arduino/ESP32 treibt die LEDs.
- V3 nutzt zusaetzlich Sensorik (z. B. Akkustand auf dem HUD, Bewegung fuer Effekte) und
  optional AR-Passthrough. AR ist aufwendig und nur fuer ambitionierte Builds sinnvoll.

## Mikrocontroller- und SBC-Wahl

Die richtige Recheneinheit pro Modul:

| Plattform | Stark fuer | Eher nicht fuer | Typische Rolle |
| --- | --- | --- | --- |
| Arduino Nano (ATmega328) | Einfache, robuste LED-Effekte, Tasterabfrage, Luefter-PWM, I2C-Slave | Display-Grafik, Audio, Netzwerk | LED-Controller in Ruestung/Helm, Luefterregelung |
| ESP32 | WS2812B mit vielen LEDs/Effekten, WiFi/BLE-Steuerung, mehr RAM/Kerne als Nano | aufwendige Grafik-Stacks/Linux-Software | "smarter" LED- und Sensor-Hub, ferngesteuerte Effekte |
| Raspberry Pi Zero 2 W | OLED-HUD-Software (Python/luma.oled), Autostart per systemd, leichte Logik | rechenintensive Bildverarbeitung, niedriger Stromverbrauch | HUD-Rechner im Helm (`hud_display.py`) |
| Raspberry Pi 4/5 | AR-Passthrough (Kamera + Display), Bildverarbeitung, mehrere Tasks parallel | kompakte/sparsame Builds (heiss, hungrig) | nur V3 AR; sonst ueberdimensioniert |

Faustregeln:
- LEDs und Luefter: Arduino Nano (V1/V2 simpel) oder ESP32 (viele LEDs, Funksteuerung).
- HUD-Display: Pi Zero 2 W. Klein, sparsam genug, treibt das OLED stabil ueber I2C.
- AR/Vision: erst ab Pi 4/5. Vorher Hitze- und Strombudget pruefen
  (`Documentation/Guides/Elektronik-Strombudget.md`).
- Mische ruhig: Pi fuers HUD + Arduino/ESP32 fuer LEDs ueber I2C ist die Standard-Aufteilung
  in V2/V3.

## Empfohlene Aufbau-Reihenfolge

Reihenfolge so, dass du nie auf einer unsicheren Stromversorgung aufbaust:

1. **Strombudget rechnen.** Bevor irgendetwas verloetet wird: erwarteten Verbrauch und
   Laufzeit kalkulieren. Siehe `Documentation/Guides/Elektronik-Strombudget.md`.
2. **Batterie und Stromverteilung waehlen.** Akku, Buck-Converter, Sicherung und
   Verteilung festlegen. Siehe `Documentation/Guides/Elektronik-Batterie.md` und
   `Documentation/Guides/Elektronik-Verdrahtung.md`.
3. **Power leer testen.** Verteilung ohne Module unter Last messen (Multimeter):
   stimmen 5V/12V stabil, haelt die Sicherung, wird etwas heiss?
4. **Steckverbinder/Backbone verlegen.** Steckbare Verbindungen (JST/XT) und Kabelfuehrung
   im Suit, sodass jedes Modul abnehmbar bleibt (Transport, Wartung).
5. **Modul fuer Modul aufstecken und einzeln testen** - immer eines nach dem anderen:
   1. Luefter (`Documentation/Guides/Elektronik-Luefter.md`)
   2. LEDs / Effekte (`Documentation/Guides/LED-Effekte.md`)
   3. OLED-HUD-Hardware + Pi (`Documentation/Guides/Elektronik-HUD.md`)
   4. Audio / Voice-Changer (`Documentation/Guides/Elektronik-Audio.md`)
   5. Autostart einrichten, damit alles ohne Tastatur hochfaehrt
      (`Documentation/Guides/Elektronik-Autostart.md`)
   6. nur V3: AR-Passthrough und Sensorik zuletzt
6. **Gesamttest unter realer Last.** Alle Module gleichzeitig, Laufzeit messen, mit dem
   Budget aus Schritt 1 abgleichen. Erst dann fest verbauen und Kabel sichern.

Grundsatz: Nie alle Module gleichzeitig erstmals einschalten. Fehler sind nur isolierbar,
wenn du jedes Modul einzeln in Betrieb genommen hast.

## Alle Elektronik-Guides

- HUD und Systemuebersicht: `Documentation/Guides/Elektronik-HUD.md`
- LED-Effekte (Muster, Code-Bezug): `Documentation/Guides/LED-Effekte.md`
- Pi-Einrichtung und Autostart: `Documentation/Guides/Elektronik-Autostart.md`
- Strombudget und Laufzeit: `Documentation/Guides/Elektronik-Strombudget.md`
- Batterieloesungen (8+ Stunden): `Documentation/Guides/Elektronik-Batterie.md`
- Verdrahtung und Power-Verteilung: `Documentation/Guides/Elektronik-Verdrahtung.md`
- Helm-Belueftung (Luefter): `Documentation/Guides/Elektronik-Luefter.md`
- Audio und Voice Changer: `Documentation/Guides/Elektronik-Audio.md`
- AR-Display und Kamera-Passthrough (V3): `Documentation/Guides/Elektronik-AR-Display.md`

## Code

- HUD-Display: `Code/HelmetControl/hud_display.py`
- Konfig: `Code/HelmetControl/config.example.json`
- Batterie-Input: `Code/HelmetControl/battery.example.json`
- Arduino Helm: `Code/HelmetControl/MainControlCode.ino`
- Arduino LEDs Helm: `Code/HelmetControl/LightingEffectsCode.ino`
- Arduino Helm (erweitert, Effekte + Luefter): `Code/HelmetControl/HelmetMultiEffects.ino`
- Arduino Ruestung: `Code/ArmorControl/MainControlCode.ino`
- Arduino LEDs Ruestung: `Code/ArmorControl/LightingEffectsCode.ino`
- Arduino Ruestung (erweitert, Effekte + Bootsequenz): `Code/ArmorControl/MultiEffects.ino`
