#!/usr/bin/env python3
"""AR-Passthrough-Demo fuer den V3-Helm (Stufe C).

Pipeline:  Kamera -> (optional entzerren) -> HUD-Overlay -> Display
Zielschleife: moeglichst unter 20-30 ms pro Frame (siehe
`Documentation/Guides/Elektronik-AR-Display.md`, Abschnitt 2).

SICHERHEIT (zwingend lesen): Dieses Programm ersetzt bei Stufe C die direkte
Sicht. Ein Ausfall = Blindheit mitten in der Bewegung. Darum:
  - Watchdog: bleibt ein frischer Frame aus oder steigt die Latenz, wird ein
    grosser Warnbanner eingeblendet ("VISOR HOCH"). Das Bild wird NIE einfach
    schwarz, ohne zu warnen.
  - Mechanischer Notausblick (hochklappbarer/absetzbarer Visor) und ein Handler
    sind PFLICHT. Software ersetzt das nicht.
  - Luefter und Notbeleuchtung muessen unabhaengig von diesem Rechner laufen.
Details: `Documentation/Guides/Elektronik-AR-Display.md` Abschnitt 3.

Plattform: Raspberry Pi 4/5 oder Jetson. Auf Pi mit CSI-Kamera wird picamera2
genutzt, sonst faellt das Programm auf eine OpenCV-VideoCapture zurueck.

Aufruf:
  python3 ar_passthrough.py                 # normaler Betrieb
  python3 ar_passthrough.py --selftest out.png   # ohne Kamera/Display, schreibt ein PNG
"""

import argparse
import json
import os
import sys
import time
from collections import deque

import cv2

import hud_overlay

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULTS = {
    "camera_backend": "auto",     # auto | picamera2 | opencv
    "camera_index": 0,            # nur fuer OpenCV-Backend
    "width": 1280,
    "height": 720,
    "target_fps": 60,
    "fullscreen": True,
    "flip_horizontal": False,
    "flip_vertical": False,
    "latency_limit_ms": 40,       # darueber: gelbe Latenz-Warnung
    "frame_timeout_ms": 250,      # kein frischer Frame -> roter Warnbanner
    "low_battery_percent": 15,    # darunter: Warnbanner
    "sensor_serial_port": "",     # z.B. "/dev/ttyUSB0" fuer ESP32-Feeder; leer = aus
    "sensor_baud": 115200,
    "default_shield": 100,
    "default_ammo": 32,
    "window_name": "MJOLNIR AR",
}


def load_config():
    config = DEFAULTS.copy()
    path = os.path.join(BASE_DIR, "ar_config.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as handle:
            config.update(json.load(handle))
    return config


# --------------------------------------------------------------------------
# Kameraquelle: picamera2 (Pi/CSI) mit Fallback auf OpenCV-VideoCapture
# --------------------------------------------------------------------------
class CameraSource:
    def __init__(self, config):
        self.config = config
        self.backend = None
        self._picam = None
        self._cap = None

    def open(self):
        backend = self.config.get("camera_backend", "auto")
        if backend in ("auto", "picamera2"):
            if self._open_picamera2():
                self.backend = "picamera2"
                return True
            if backend == "picamera2":
                return False
        # OpenCV-Fallback
        if self._open_opencv():
            self.backend = "opencv"
            return True
        return False

    def _open_picamera2(self):
        try:
            from picamera2 import Picamera2  # nur auf dem Pi vorhanden
        except Exception:
            return False
        try:
            self._picam = Picamera2()
            cfg = self._picam.create_preview_configuration(
                main={"size": (self.config["width"], self.config["height"]),
                      "format": "RGB888"})
            self._picam.configure(cfg)
            self._picam.start()
            return True
        except Exception:
            self._picam = None
            return False

    def _open_opencv(self):
        try:
            cap = cv2.VideoCapture(int(self.config.get("camera_index", 0)))
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config["width"])
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config["height"])
            cap.set(cv2.CAP_PROP_FPS, self.config["target_fps"])
            if not cap.isOpened():
                return False
            self._cap = cap
            return True
        except Exception:
            return False

    def read(self):
        """Gibt (ok, frame_bgr) zurueck. frame ist None bei Fehlschlag."""
        if self.backend == "picamera2":
            try:
                rgb = self._picam.capture_array()
                return True, cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
            except Exception:
                return False, None
        if self.backend == "opencv":
            ok, frame = self._cap.read()
            return bool(ok), frame if ok else None
        return False, None

    def close(self):
        try:
            if self._picam is not None:
                self._picam.stop()
            if self._cap is not None:
                self._cap.release()
        except Exception:
            pass


# --------------------------------------------------------------------------
# Optionaler Sensor-Feeder (ESP32) ueber serielle Schnittstelle.
# Erwartet JSON-Zeilen, z.B. {"heading":123,"battery":78,"temp":41}
# Laeuft bewusst getrennt: faellt der Feeder aus, laeuft das Passthrough weiter.
# --------------------------------------------------------------------------
class SensorReader:
    def __init__(self, config):
        self.config = config
        self._serial = None
        self._buf = b""
        self.latest = {}

    def open(self):
        port = self.config.get("sensor_serial_port", "")
        if not port:
            return False
        try:
            import serial  # pyserial
            self._serial = serial.Serial(port, int(self.config.get("sensor_baud", 115200)),
                                         timeout=0)
            return True
        except Exception:
            self._serial = None
            return False

    def poll(self):
        if self._serial is None:
            return
        try:
            self._buf += self._serial.read(256)
            while b"\n" in self._buf:
                line, self._buf = self._buf.split(b"\n", 1)
                line = line.strip()
                if line.startswith(b"{"):
                    try:
                        self.latest = json.loads(line.decode("utf-8", "ignore"))
                    except ValueError:
                        pass
        except Exception:
            return

    def close(self):
        try:
            if self._serial is not None:
                self._serial.close()
        except Exception:
            pass


def apply_flips(frame, config):
    if config.get("flip_horizontal"):
        frame = cv2.flip(frame, 1)
    if config.get("flip_vertical"):
        frame = cv2.flip(frame, 0)
    return frame


def run_selftest(config, out_path):
    """Rendert das HUD auf einen synthetischen Frame und schreibt ein PNG.
    Braucht weder Kamera noch Display. Gut fuer CI / schnellen Sichttest."""
    frame = hud_overlay.make_test_frame(config["width"], config["height"])
    state = {
        "shield": 72, "ammo": config["default_ammo"], "battery_percent": 84,
        "heading_deg": 137, "fps": 58, "latency_ms": 22,
        "latency_limit_ms": config["latency_limit_ms"],
        "contacts": [(45, 0.6), (200, 0.3)], "warning": None,
    }
    hud_overlay.draw_hud(frame, state)
    ok = cv2.imwrite(out_path, frame)
    print(f"Selbsttest {'OK' if ok else 'FEHLGESCHLAGEN'}: {out_path}")
    return 0 if ok else 1


def main():
    parser = argparse.ArgumentParser(description="MJOLNIR AR-Passthrough-Demo")
    parser.add_argument("--selftest", metavar="OUT.png", default=None,
                        help="HUD ohne Hardware rendern und als PNG speichern")
    args = parser.parse_args()

    config = load_config()

    if args.selftest:
        return run_selftest(config, args.selftest)

    camera = CameraSource(config)
    if not camera.open():
        print("FEHLER: keine Kamera gefunden (picamera2 und OpenCV fehlgeschlagen).",
              file=sys.stderr)
        return 2
    print(f"Kamera-Backend: {camera.backend}")

    sensors = SensorReader(config)
    if sensors.open():
        print(f"Sensor-Feeder: {config['sensor_serial_port']}")
    else:
        print("Sensor-Feeder: aus (kein Port konfiguriert oder nicht erreichbar)")

    window = config.get("window_name", "MJOLNIR AR")
    cv2.namedWindow(window, cv2.WINDOW_NORMAL)
    if config.get("fullscreen"):
        cv2.setWindowProperty(window, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    target_dt = 1.0 / max(1, int(config.get("target_fps", 60)))
    frame_timeout = float(config.get("frame_timeout_ms", 250)) / 1000.0
    low_batt = float(config.get("low_battery_percent", 15))

    latencies = deque(maxlen=30)
    last_good_frame = None
    last_good_time = time.monotonic()

    try:
        while True:
            loop_start = time.monotonic()
            ok, frame = camera.read()
            now = time.monotonic()

            warning = None
            if ok and frame is not None:
                frame = apply_flips(frame, config)
                last_good_frame = frame
                last_good_time = now
            else:
                # Kein frischer Frame: letzten zeigen, aber warnen sobald zu alt
                frame = last_good_frame
                if frame is None:
                    # noch nie ein Frame bekommen -> leeres Warnbild
                    frame = hud_overlay.make_test_frame(config["width"], config["height"])
                if now - last_good_time > frame_timeout:
                    warning = "SICHT PRUEFEN - VISOR HOCH"

            sensors.poll()
            s = sensors.latest

            # Latenz (Schleifenzeit) gleitend mitteln -> Pflicht-Latenztest
            dt_ms = (now - loop_start) * 1000.0
            latencies.append(dt_ms)
            avg_latency = sum(latencies) / len(latencies)
            fps = 1000.0 / avg_latency if avg_latency > 0 else 0.0

            battery = s.get("battery")
            if battery is not None and float(battery) <= low_batt and warning is None:
                warning = "AKKU SCHWACH - VISOR HOCH"

            state = {
                "shield": s.get("shield", config["default_shield"]),
                "ammo": s.get("ammo", config["default_ammo"]),
                "battery_percent": battery,
                "heading_deg": s.get("heading", 0),
                "fps": fps,
                "latency_ms": avg_latency,
                "latency_limit_ms": config["latency_limit_ms"],
                "contacts": s.get("contacts"),
                "warning": warning,
            }
            hud_overlay.draw_hud(frame, state)
            cv2.imshow(window, frame)

            # auf Zielbildrate einregeln (nicht heisslaufen lassen)
            spent = time.monotonic() - loop_start
            if spent < target_dt:
                wait_ms = max(1, int((target_dt - spent) * 1000))
            else:
                wait_ms = 1
            key = cv2.waitKey(wait_ms) & 0xFF
            if key in (27, ord("q")):  # ESC oder q
                break
    finally:
        camera.close()
        sensors.close()
        cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    sys.exit(main())
