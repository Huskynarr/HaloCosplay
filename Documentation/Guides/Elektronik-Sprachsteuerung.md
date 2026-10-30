# Elektronik: Sprachsteuerung, Helmfunk und Kamera-Erkennung (Pi 5)

> **Level:** [F] Fortgeschritten | [P] Profi  |  **Varianten:** V2/V3 (optional)
> **Voraussetzungen:** HUD laeuft (`Elektronik-HUD.md`), Helm-Arduino mit `HelmetMultiEffects.ino`,
> Grundprinzip aus `V3-Systemarchitektur.md` verstanden, Grundlagen Linux/systemd (`Elektronik-Autostart.md`).

Dieses optionale Modul macht aus dem Helm-Pi eine Sprachzentrale: Taster halten,
"visier rot" oder "nebel" sagen, loslassen. Dazu kommen ein Helmfunk-Effekt fuer
die Stimme nach aussen (Audio Option C) und eine Objekterkennung, die echte
Kontakte auf den Bewegungsmelder des HUD bringt.

## 1. Was das Modul macht - und was bewusst nicht

| Funktion | Programm | Weg zum Ziel |
| --- | --- | --- |
| Sprachbefehle (offline, Deutsch) | `voice_control.py` | Push-to-Talk-Taster, Vosk-Spracherkennung |
| Visor-Farbe, -Effekt, -Helligkeit, Helm-Luefter | `voice_control.py` | I2C 0x08 an den Helm-Arduino (vorhandenes Protokoll + neues `0x04` Farbe) |
| Schubduesen-Boost (LEDs + Nebel) | `voice_control.py` | Optokoppler parallel zum Boost-Taster |
| Naechster Ruestungs-Effekt | `voice_control.py` | Optokoppler parallel zum Effekt-Taster |
| Helmfunk-Stimme nach aussen | `voice_control.py` | I2S-Verstaerker + Lautsprecher an der Brust |
| Rueckmeldung innen (Piepen, Ansagen) | `voice_control.py` | USB-Soundkarte + 2 kleine Lautsprecher am Ohr |
| Objekterkennung -> Bewegungsmelder | `vision_bridge.py` | AI Camera (IMX500) -> `hud_state.json` -> `hud_display.py` |

**Bewusst nicht:** Der Pi wird kein zentrales Hirn. Er "drueckt" nur die Taster der
anderen Module. Faellt er aus, funktionieren Schubduesen, Ruestungs-LEDs und
Visor/Luefter exakt wie vorher - mit ihren eigenen Tastern. Die Sicherheitslogik
(z.B. die 5-Sekunden-Grenze des Boosts) bleibt in den jeweiligen Arduinos.

## 2. Einordnung in die Systemarchitektur

```
   HELM                                         RUECKEN / TORSO
+------------------------------------+       +-------------------------------+
| Pi 5                               |       | Schubduesen-Arduino           |
|  voice_control.py --- GPIO27 --[Opto]----->|  D2 (Boost-Taster parallel)   |
|                   --- GPIO22 --[Opto]--+   +-------------------------------+
|                   --- I2C 0x08 ---+    |   +-------------------------------+
|  vision_bridge.py                 |    +-->| Ruestungs-Arduino D2 (Effekt) |
|      | hud_state.json             |        +-------------------------------+
|  hud_display.py -> OLED (I2C 0x3C)|
|  AI Camera (CAM0)                 v        BRUST
| Helm-Nano: Visor-LEDs + Luefter          +-------------------------------+
| Mikro (Mund) + 2 Ohr-Lautsprecher  |---->| MAX98357A + Lautsprecher (I2S)|
+------------------------------------+     +-------------------------------+
```

Der Optokoppler trennt die Stromkreise vollstaendig: Der Rueckenteil braucht nicht
einmal eine gemeinsame Masse mit dem Pi. Das ist dieselbe "Taster druecken"-Idee,
die `Elektronik-Schubduesen.md` schon fuer die Fogger-Fernbedienung nutzt.

**Nicht mit AR-Stufe C auf demselben Pi:** `ar_passthrough.py` braucht die Kamera
und jede Millisekunde Rechenzeit (Abschnitt 5 in `V3-Systemarchitektur.md`). Wer
Stufe C faehrt, nutzt fuer die Stimme Audio Option A/B und laesst `vision_bridge.py`
weg. Fuer Stufe A/B (OLED-HUD) ist ein Pi 5 dagegen kaum ausgelastet: Die AI Camera
rechnet das Erkennungsnetz selbst, der Helmfunk-Effekt kostet nur wenige Prozent CPU.

## 3. Hardware

| Teil | Empfehlung | Preis ca. | Zweck |
| --- | --- | --- | --- |
| Rechner | Raspberry Pi 5 (4 GB) + Active Cooler | 70 EUR | ersetzt den Pi Zero 2 W |
| Kamera | Raspberry Pi AI Camera (IMX500) | 75 EUR | Erkennung auf dem Kamerachip |
| Soundkarte | USB-Soundkarte mit Mic-In + Kopfhoerer-Out | 8 EUR | Mikro rein, Ansagen innen raus |
| Mikrofon | Lavalier (3.5 mm, Plug-in-Power) | 10 EUR | dicht vor dem Mund |
| Innen-Verstaerker | PAM8403 | 3 EUR | 2 Ohr-Lautsprecher |
| Innen-Lautsprecher | 2x 8 Ohm, 0.5-1 W, ca. 28 mm | 6 EUR | Rueckmeldungen |
| Aussen-Verstaerker | MAX98357A (I2S, 3 W) | 6 EUR | Helmfunk (Option C) |
| Aussen-Lautsprecher | 4 Ohm, 3 W, 40-50 mm | 5 EUR | an der Brust, nach aussen |
| PTT-Taster | Mikrotaster, z.B. im Handschuh | 2 EUR | Sprechen = Befehl |
| Optokoppler | 2x PC817 + 2x 330 Ohm | 2 EUR | Taster der anderen Module druecken |

## 4. Verdrahtung

### Pi 5 GPIO

| Pi-Pin | GPIO | Verbunden mit | Hinweis |
| --- | --- | --- | --- |
| 3 / 5 | GPIO2 / GPIO3 | I2C: OLED (0x3C) + Helm-Nano (0x08) | unveraendert |
| 11 | GPIO17 | PTT-Taster, andere Seite GND (Pin 9) | interner Pull-Up |
| 13 | GPIO27 | 330 Ohm -> PC817 #1 Anode | Boost Schubduesen |
| 15 | GPIO22 | 330 Ohm -> PC817 #2 Anode | Effekt Ruestung |
| 12 | GPIO18 | MAX98357A BCLK | I2S |
| 35 | GPIO19 | MAX98357A LRC | I2S |
| 40 | GPIO21 | MAX98357A DIN | I2S |
| 14 / 20 | GND | PC817 Kathoden, MAX98357A GND | |
| CAM/DISP 0 | - | AI Camera | 22-auf-15-Pin-Kabel |
| USB | - | USB-Soundkarte | |

### Optokoppler ("Taster druecken")

```
Pi GPIO27 --[330R]--> PC817 Pin 1 (Anode)       PC817 Pin 4 (Kollektor) --> Schubduesen-Arduino D2
Pi GND -------------> PC817 Pin 2 (Kathode)     PC817 Pin 3 (Emitter)   --> Schubduesen-Arduino GND
```

Der Original-Taster bleibt parallel angeschlossen. `voice_control.py` haelt den
Ausgang 200 ms (`pulse_ms`) - fuer den Arduino sieht das aus wie ein Tastendruck.
Fuer den Ruestungs-Arduino dasselbe mit GPIO22 und PC817 #2 an dessen Pin 2.

### Audio

- **Innen:** Kopfhoerer-Ausgang der USB-Soundkarte -> PAM8403 (L/R) -> 2 Lautsprecher
  am Ohr. PAM8403 aus 5V des Pi (Pin 4). Hinweise aus `Elektronik-Audio.md` gelten
  (Lautsprecher-Minus nie an GND, L/R nie zusammenschliessen).
- **Aussen:** MAX98357A auf **Schiene 3 (Audio)**, Lautsprecher an die Brust. SD und
  GAIN offen lassen. Nie Lautsprecher und Mikro zusammen in den Helm
  (`V3-Systemarchitektur.md`, Abschnitt 5).
- Die Ohr-Lautsprecher spielen nur Pieptoene und Ansagen, nie das Mikrofon - deshalb
  koppelt hier nichts zurueck, obwohl Mikro und Ohr-Lautsprecher im Helm sitzen.

### Strom

Der Pi 5 haengt an **Schiene 1**. An einer normalen 5V/3A-Powerbank meldet er "kein
5-A-Netzteil" und begrenzt USB auf 600 mA - das reicht, die Soundkarte zieht ca. 50 mA.
Zusatzlast gegenueber dem Pi Zero 2 W: ca. 3-6 W. In `Elektronik-Strombudget.md`
nachrechnen.

## 5. Software einrichten

Raspberry Pi OS Lite (64-bit) auf dem Pi 5, Repo nach `~/HaloCosplay` klonen:

```bash
sudo apt update
sudo apt install -y --no-install-recommends python3-venv python3-numpy python3-scipy \
  python3-gpiozero python3-lgpio python3-smbus2 python3-picamera2 imx500-all \
  libportaudio2 alsa-utils espeak-ng unzip wget

# I2C (HUD + Helm-Nano) und I2S-Verstaerker aktivieren, dann neu starten
echo "dtparam=i2c_arm=on"  | sudo tee -a /boot/firmware/config.txt
echo "dtoverlay=max98357a" | sudo tee -a /boot/firmware/config.txt

cd ~/HaloCosplay/Code/HelmetControl
python3 -m venv --system-site-packages venv
venv/bin/pip install -r requirements.txt -r requirements-voice.txt

# Deutsches Sprachmodell (ca. 45 MB) und COCO-Labels fuer die Kamera
mkdir -p models
wget -O /tmp/vosk-de.zip https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip
unzip /tmp/vosk-de.zip -d models
wget -O coco_labels.txt https://raw.githubusercontent.com/raspberrypi/picamera2-examples/main/examples/imx500/assets/coco_labels.txt

cp voice_config.example.json voice_config.json
```

Dann Geraetenamen pruefen und in `voice_config.json` eintragen:

```bash
venv/bin/python -m sounddevice   # Teilstring fuer mic_device / outer_device
aplay -L | grep plughw            # Wert fuer inner_alsa
```

Optional eine natuerlichere Stimme innen (statt espeak-ng):

```bash
venv/bin/pip install piper-tts
venv/bin/python -m piper.download_voices de_DE-kerstin-low --download-dir voices
```

### Autostart

Analog zu `Elektronik-Autostart.md` je eine Unit fuer Sprachsteuerung und Kamera
(Pfade und Benutzer anpassen):

```ini
# /etc/systemd/system/voice.service
[Unit]
Description=Halo Sprachsteuerung + Helmfunk
After=sound.target

[Service]
User=pi
WorkingDirectory=/home/pi/HaloCosplay/Code/HelmetControl
ExecStart=/home/pi/HaloCosplay/Code/HelmetControl/venv/bin/python -u voice_control.py
Restart=on-failure
RestartSec=3

[Install]
WantedBy=multi-user.target
```

`vision.service` genauso, nur mit `vision_bridge.py`. Danach
`sudo systemctl enable --now voice.service vision.service`.

## 6. Sprachbefehle

PTT-Taster halten, sprechen, loslassen. Ein hoher Ton = verstanden, ein tiefer = nicht verstanden.

| Gesagt | Wirkung |
| --- | --- |
| "visier rot" / "gold" / "blau" / ... | Visor-Farbe (I2C `0x04`) |
| "visier atmen" / "herzschlag" / "lauflicht" / "flackern" / "statisch" | Visor-Effekt (`0x03`) |
| "visier heller" / "dunkler" / "aus" / "an" | Helligkeit (`0x01`) |
| "nebel" / "boost" / "schub" | Boost-Taster der Schubduesen druecken |
| "ruestung weiter" / "licht weiter" | Effekt-Taster der Ruestung druecken |
| "show" | Visor-Lauflicht + Boost, danach zurueck |
| "alarm" | Visor rot im Herzschlag-Takt |
| "stopp" / "ruhe" | Visor zurueck auf Gold, Atmen |
| "luefter voll" / "leise" / "staerker" / "schwaecher" / "normal" / "aus" | Helm-Luefter (`0x02`) |
| "scanner an" / "aus" | Ansagen wie "Person links" aus der Kamera-Erkennung |
| "stimme aus" / "an" | Helmfunk nach aussen stumm/aktiv |
| "status" | Temperatur, Helm-Verbindung, Kamera ansagen |
| "wasser" / "spaeter" / "trinken aus" / "trinken an" | Trink-Erinnerung: getrunken / 10 min Snooze / aus / an |

Farben: gold, rot, gruen, blau, gelb, orange, weiss, lila, tuerkis. Neue Woerter in
`WORDS`/`COLORS` von `voice_control.py` eintragen; die Erkennung lernt sie automatisch.

## 7. Testreihenfolge

1. `python3 voice_control.py --selftest` und `python3 vision_bridge.py --selftest` (laeuft ueberall, auch in der CI)
2. `venv/bin/python voice_control.py --keyboard` - Befehle tippen, Visor/Luefter reagieren?
3. Optokoppler einzeln testen: "nebel" -> Boost am Schubduesen-Arduino, eigener Taster geht weiterhin
4. PTT + Mikro im offenen Helm, dann im geschlossenen Helm (Atem, Daempfung)
5. Helmfunk: Lautstaerke langsam hoch, Rueckkopplungstest in voller Montur
6. `vision_bridge.py` starten, durch den Raum gehen - Kontakte auf dem Bewegungsmelder?
7. Ausfalltest: `voice.service` stoppen - alle anderen Module muessen normal weiterlaufen

## 8. Grenzen und Sicherheit

- **Luefter:** "luefter aus" ist moeglich, wird aber mit Warnung angesagt. Im
  geschlossenen Helm nie dauerhaft ohne Lueftung (`Sicherheit.md`).
- **Boost/Nebel:** Die Zeitbegrenzung sitzt im Schubduesen-Arduino, nicht im Pi. Ein
  haengender Pi kann den Nebel deshalb nicht dauerhaft einschalten.
- **Kamera:** `vision_bridge.py` speichert keine Bilder, es gehen nur Kontakt-Positionen
  in `hud_state.json`. Eine sichtbare Kamera am Helm trotzdem auf Nachfrage erklaeren
  und die Regeln der Con beachten (`Convention-Regeln.md`).
- **Erkennung ist Show, keine Sicherheitsfunktion:** Der Bewegungsmelder zeigt nur, was
  die Kamera vorne sieht (ca. 66 Grad). Er ersetzt keinen Blick und keinen Handler.
- **Laute Hallen:** Vosk mit eingeschraenktem Wortschatz ist robust, aber nicht
  unfehlbar. Deshalb gibt es fuer alles weiterhin die physischen Taster.

## Verwandte Guides

- Gesamtsystem: [V3-Systemarchitektur.md](V3-Systemarchitektur.md)
- Audio-Optionen: [Elektronik-Audio.md](Elektronik-Audio.md)
- Schubduesen + Nebler: [Elektronik-Schubduesen.md](Elektronik-Schubduesen.md)
- HUD: [Elektronik-HUD.md](Elektronik-HUD.md) | Autostart: [Elektronik-Autostart.md](Elektronik-Autostart.md)
- Code-Uebersicht: [Code/README.md](../../Code/README.md)
