# Begleit-Roboter: Integration ins HUD (Konzept)

> **Level:** [P] Profi  |  **Varianten:** V3+ (Zukunft)  |  **Status:** Konzept/Skizze
> **Voraussetzungen:** HUD-Kette laeuft (`Documentation/Guides/Elektronik-HUD.md`),
> Modellwahl verstanden (`Design/Designs/IdeasReferences.md`, Abschnitt Begleit-Roboter).

Wie ein laufender Roboter (Unitree Go2 EDU, Xiaomi CyberDog 2) dem Spartan folgt
und seine Telemetrie ins Helm-HUD einspeist. Dies ist eine **Zukunfts-Skizze** -
die Software-Bruecke ist bereits vorhanden und hardwarefrei testbar, der Roboter
selbst ist (noch) nicht Teil des Builds.

## 1. Gesamtbild

Zwei voellig getrennte Systeme, lose ueber WLAN gekoppelt - exakt das
Entkopplungsprinzip aus `V3-Systemarchitektur.md`:

```
  ROBOTER (eigener Rechner, ROS 2 / Python-SDK)        HELM (Raspberry Pi)
  +------------------------------------+               +------------------------+
  | Follow-Logik (UWB-Tag am Koerper)  |               | hud_display.py         |
  | liest: Akku, Distanz, Peilung,     |   WLAN/UDP    |   liest hud_state.json  |
  | Zustand (follow/guard), Kontakte   | ============> | robot_bridge.py        |
  | sendet ~5x/s ein JSON-Datagramm    |   Port 9009   |   schreibt hud_state    |
  +------------------------------------+               +------------------------+
```

- Der **Roboter folgt per UWB-Tag** (Funk-Anhaenger am Guertel), nicht per
  Kameraerkennung - in Menschenmengen deutlich zuverlaessiger.
- Faellt das WLAN oder der Roboter aus, blendet `robot_bridge.py` den HUD-Marker
  nach ein paar Sekunden aus. Helm und Roboter funktionieren unabhaengig weiter.
- Es gibt **keine** Steuerung des Roboters aus dem Helm - nur Anzeige. Das haelt
  das sicherheitskritische Folgen beim Roboter selbst.

## 2. Datenvertrag (das einzige Bindeglied)

Der Roboter sendet pro Datagramm ein JSON-Objekt (UDP, Port 9009). Alle Felder
optional - was fehlt, wird einfach nicht angezeigt:

```json
{
  "robot_battery": 64,
  "robot_distance_m": 2.3,
  "robot_bearing": 130,
  "robot_state": "follow",
  "contacts": 2
}
```

| Feld | Bedeutung | HUD-Wirkung |
| --- | --- | --- |
| `robot_distance_m` | Abstand Roboter<->Traeger in Meter | Position des Markers auf dem Motion-Tracker (0-6 m -> Mitte bis Rand) |
| `robot_bearing` | Peilung 0-360 Grad (0 = voraus) | Richtung des Markers |
| `robot_battery` | Akku 0-100 % | < 20 % -> Marker blinkt |
| `robot_state` | `follow` oder `guard` | `guard` -> Marker mit Mittelpunkt |
| `contacts` | erkannte Personen (optional) | reserviert fuer spaeter |

`robot_bridge.py` schreibt diese Felder in `hud_state.json` und **bewahrt**
dabei `ammo`, `shield_percent`, `heading` anderer Module. So zeigt das HUD den
Roboter als freundliche Raute auf dem Motion-Tracker (vs. gefuellte Quadrate fuer
Kontakte).

## 3. Bausteine

### Auf dem Roboter (Go2 EDU)

Ein kleines Python-Skript nutzt das Unitree SDK2, liest Akku/Follow-Status und
sendet das Datagramm. Grobgeruest (nicht im Repo, geraetespezifisch):

```python
import socket, json, time
HELM = ("192.168.x.x", 9009)   # IP des Helm-Pi im gemeinsamen WLAN
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    msg = {
        "robot_battery": read_battery(),        # via unitree_sdk2
        "robot_distance_m": read_tag_distance(), # UWB-Companion
        "robot_bearing": read_tag_bearing(),
        "robot_state": current_mode(),           # "follow"/"guard"
    }
    sock.sendto(json.dumps(msg).encode(), HELM)
    time.sleep(0.2)
```

### Auf dem Helm (vorhanden, getestet)

- `Code/HelmetControl/robot_bridge.py` - UDP-Listener -> `hud_state.json`,
  mit Stale-Erkennung (Marker weg bei Signalverlust). Test:
  `python3 robot_bridge.py --selftest`
- `Code/HelmetControl/hud_display.py` - zeigt den Roboter als Raute auf dem
  Motion-Tracker, blinkt bei niedrigem Robo-Akku, Mittelpunkt im Guard-Modus.

Beide laufen wie `sensor_bridge.py` parallel zum HUD (eigener systemd-Service,
siehe `Elektronik-Autostart.md`).

## 4. "Watch Guard Mode" - was realistisch ist

- **Machbar:** Roboter wechselt per Knopf in `guard` (steht still, dreht Kamera
  auf Annaehernde, spielt Voicelines, Statuslicht). Das HUD zeigt den Wechsel.
- **Nicht realistisch / unsicher:** echte autonome Bewachung mit Eingriff. Dafuer
  sind die Geraete nicht gebaut, und in einer Menge ist es ein Sicherheitsrisiko.

## 5. Vor dem realen Einsatz klaeren

- **Con-Genehmigung einholen** - ein ~15-kg-Geraet faellt vermutlich unter
  "potenziell gefaehrlich". Handler + ggf. Versicherung. Siehe `Convention-Regeln.md`.
- **Toter Winkel** des Go2-LiDAR (seitlich/hinten) - in Mengen Kollisionsrisiko.
- **Security/Datenschutz** - dokumentierte Unitree-Firmware-Befunde (2025/26);
  kamerafuehrendes Geraet in der Oeffentlichkeit ist ein DSGVO-Thema. WLAN
  abschotten, Kamera-Uploads pruefen.

## Verwandte Dokumente

- Modellvergleich und Quellen: `Design/Designs/IdeasReferences.md` (Begleit-Roboter)
- HUD und Code: `Documentation/Guides/Elektronik-HUD.md`, `Code/README.md`
- Entkopplungsprinzip: `Documentation/Guides/V3-Systemarchitektur.md`
- Sensor-Bruecke (Vorbild): `Code/HelmetControl/sensor_bridge.py`
