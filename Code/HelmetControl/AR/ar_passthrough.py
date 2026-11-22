#!/usr/bin/env python3
"""AR-Passthrough-Demo fuer den V3-Helm (Stufe C).

Pipeline:  Kamera -> (optional entzerren) -> HUD-Overlay -> Display
Zielschleife: moeglichst unter 20-30 ms pro Frame (siehe
`Documentation/Guides/Elektronik-AR-Display.md`, Abschnitt 2).

SICHERHEIT (zwingend lesen): Dieses Programm ersetzt bei Stufe C die direkte
Sicht. Ein Ausfall = Blindheit mitten in der Bewegung. Darum:
  - Watchdog: Die Kamera wird in einem eigenen Thread gelesen. Ist der letzte
    Frame aelter als frame_timeout_ms (Kamera liefert Fehler ODER haengt), wird
    ein grosser Warnbanner eingeblendet ("VISOR HOCH"). Grenzen: Der Banner
    setzt voraus, dass dieser Prozess, die Grafikausgabe und das Display noch
    laufen. Haengt der Rechner selbst oder faellt das Display aus, warnt
    niemand - dagegen hilft nur der mechanische Notausblick.
  - Mechanischer Notausblick (hochklappbarer/absetzbarer Visor) und ein Handler
    sind PFLICHT. Software ersetzt das nicht.
  - Luefter und Notbeleuchtung muessen unabhaengig von diesem Rechner laufen.
Details: `Documentation/Guides/Elektronik-AR-Display.md` Abschnitt 3.

Plattform: Raspberry Pi 4/5 oder Jetson. Auf Pi mit CSI-Kamera wird picamera2
genutzt, sonst faellt das Programm auf eine OpenCV-VideoCapture zurueck.

Aufruf:
  python3 ar_passthrough.py                 # normaler Betrieb
  python3 ar_passthrough.py --selftest out.png   # ohne Kamera/Display, schreibt ein PNG
  python3 ar_passthrough.py --selftest-logic     # Watchdog/Sensor-Logik, ohne OpenCV
"""

import argparse
import json
import math
import os
import sys
import threading
import time

try:
    import cv2
    import hud_overlay
except ImportError:  # --selftest-logic laeuft auch ohne OpenCV
    cv2 = None
    hud_overlay = None

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
    "sensor_timeout_ms": 3000,    # aeltere Feeder-Werte gelten als unbekannt
    "default_shield": 100,
    "default_ammo": 32,
    "window_name": "MJOLNIR AR",
}


def load_config():
    config = DEFAULTS.copy()
    path = os.path.join(BASE_DIR, "ar_config.json")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
            if not isinstance(data, dict):
                raise ValueError("kein JSON-Objekt")
            config.update(data)
        except (OSError, ValueError) as exc:
            print(f"WARNUNG: ar_config.json unbrauchbar ({exc}), nutze Standardwerte.",
                  file=sys.stderr)
    return config


def finite(value, default=None):
    """Zahl als endlicher float, sonst default (None, Text, NaN, inf)."""
    if value is None or isinstance(value, bool):
        return default
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError):
        return default
    return number if math.isfinite(number) else default


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
# Kamera-Thread: camera.read() kann blockieren (haengende CSI-Pipeline, USB-
# Kamera abgezogen). Laeuft das Lesen im Hauptthread, friert die Anzeige ohne
# Warnung ein. Darum liest ein eigener Thread, der Hauptthread prueft nur das
# Alter des letzten Frames und kann so auch bei haengender Kamera warnen.
# --------------------------------------------------------------------------
class FrameGrabber:
    def __init__(self, camera, clock=time.monotonic):
        self._camera = camera
        self._clock = clock
        self._lock = threading.Lock()
        self._frame = None
        self._stamp = None
        self._seq = 0
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, name="camera", daemon=True)

    def start(self):
        self._thread.start()
        return self

    def _run(self):
        while not self._stop.is_set():
            try:
                ok, frame = self._camera.read()
            except Exception:
                ok, frame = False, None
            if ok and frame is not None:
                with self._lock:
                    self._frame, self._stamp = frame, self._clock()
                    self._seq += 1
            else:
                self._stop.wait(0.01)  # Fehlerfall: nicht heisslaufen

    def latest(self):
        """(frame, alter_in_s, laufende_nummer); frame None = noch kein Bild."""
        with self._lock:
            if self._frame is None:
                return None, None, 0
            return self._frame, self._clock() - self._stamp, self._seq

    def stop(self):
        # Daemon-Thread: haengt read() fuer immer, endet er mit dem Prozess.
        self._stop.set()
        self._thread.join(timeout=0.5)


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
        self.latest_time = None   # time.monotonic() der letzten gueltigen Zeile

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
                    self.feed(line)
            if len(self._buf) > 4096:   # Datenmuell ohne Zeilenende
                self._buf = b""
        except Exception:
            return

    def feed(self, line, now=None):
        """Eine JSON-Zeile uebernehmen (auch fuer den Selbsttest)."""
        try:
            data = json.loads(line.decode("utf-8", "ignore"))
        except ValueError:
            return
        if isinstance(data, dict):
            self.latest = data
            self.latest_time = time.monotonic() if now is None else now

    def fresh(self, now=None):
        """Letzte Werte, oder {} wenn der Feeder zu lange schweigt.

        Ein ausgefallener ESP32 darf nicht ewig "Akku 78 %" anzeigen lassen.
        """
        if self.latest_time is None:
            return {}
        now = time.monotonic() if now is None else now
        limit = finite(self.config.get("sensor_timeout_ms"), 3000.0) / 1000.0
        return self.latest if now - self.latest_time <= limit else {}

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


def frame_warning(age_s, frame_timeout_s):
    """Warntext, wenn es kein ausreichend frisches Kamerabild gibt."""
    if age_s is None or age_s > frame_timeout_s:
        return "SICHT PRUEFEN - VISOR HOCH"
    return None


def battery_warning(battery, low_percent):
    return "AKKU SCHWACH - VISOR HOCH" if battery is not None and battery <= low_percent else None


def run_logic_selftest():
    """Watchdog- und Sensorlogik ohne Kamera, Display und OpenCV pruefen."""
    failures = []

    def check(name, ok):
        print(f"  [{'ok' if ok else 'FEHLER'}] {name}")
        if not ok:
            failures.append(name)

    class HangingCamera:
        """Liefert zwei Frames und blockiert dann wie eine haengende Pipeline."""
        def __init__(self):
            self.calls = 0
            self.release = threading.Event()

        def read(self):
            self.calls += 1
            if self.calls <= 2:
                return True, f"frame{self.calls}"
            self.release.wait(5)
            return False, None

    cam = HangingCamera()
    grabber = FrameGrabber(cam).start()
    deadline = time.monotonic() + 1.0
    while grabber.latest()[2] < 2 and time.monotonic() < deadline:
        time.sleep(0.005)
    frame, age, seq = grabber.latest()
    check("Grabber liefert Frames", frame == "frame2" and seq == 2 and frame_warning(age, 0.25) is None)
    time.sleep(0.12)   # Kamera haengt jetzt in read(); Hauptthread laeuft weiter
    frame, age, seq = grabber.latest()
    check("Haengende Kamera: Hauptthread blockiert nicht, Warnung nach Timeout",
          seq == 2 and age > 0.1 and frame_warning(age, 0.1) is not None)
    cam.release.set()
    grabber.stop()
    check("Noch kein Bild -> Warnung", frame_warning(None, 0.25) is not None)

    sensors = SensorReader({"sensor_timeout_ms": 3000})
    check("Ohne Feeder keine Werte", sensors.fresh(now=0.0) == {})
    sensors.feed(b'{"heading":123,"battery":12}', now=100.0)
    check("Frische Feeder-Werte werden genutzt", sensors.fresh(now=101.0).get("battery") == 12)
    check("Veraltete Feeder-Werte gelten als unbekannt", sensors.fresh(now=104.5) == {})
    sensors.feed(b'[1,2,3]', now=200.0)
    check("Nicht-Objekt-Zeilen werden ignoriert", sensors.latest.get("battery") == 12)
    check("Akkuwarnung nur bei gueltiger Zahl",
          battery_warning(finite(12), 15.0) is not None
          and battery_warning(finite("leer"), 15.0) is None
          and battery_warning(finite(float("nan")), 15.0) is None
          and battery_warning(finite(80), 15.0) is None)
    if failures:
        print("Logik-Selbsttest FEHLGESCHLAGEN: " + ", ".join(failures))
        return 1
    print("Logik-Selbsttest OK")
    return 0


def main():
    parser = argparse.ArgumentParser(description="MJOLNIR AR-Passthrough-Demo")
    parser.add_argument("--selftest", metavar="OUT.png", default=None,
                        help="HUD ohne Hardware rendern und als PNG speichern")
    parser.add_argument("--selftest-logic", action="store_true",
                        help="Watchdog-/Sensorlogik pruefen (ohne OpenCV)")
    args = parser.parse_args()

    if args.selftest_logic:
        return run_logic_selftest()
    if cv2 is None:
        print("FEHLER: OpenCV (cv2) fehlt. Installation: siehe README.md.", file=sys.stderr)
        return 2

    config = load_config()

    if args.selftest:
        return run_logic_selftest() or run_selftest(config, args.selftest)

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

    target_dt = 1.0 / max(1.0, finite(config.get("target_fps"), 60.0))
    frame_timeout = finite(config.get("frame_timeout_ms"), 250.0) / 1000.0
    low_batt = finite(config.get("low_battery_percent"), 15.0)

    grabber = FrameGrabber(camera).start()
    startup = time.monotonic()
    last_seq = 0
    fps = 0.0
    fps_window_start = startup
    fps_frames = 0

    try:
        while True:
            loop_start = time.monotonic()
            raw, age, seq = grabber.latest()

            if raw is None:
                # noch nie ein Frame bekommen -> leeres Warnbild (nach Anlaufzeit)
                frame = hud_overlay.make_test_frame(config["width"], config["height"])
                age = None if loop_start - startup > frame_timeout else 0.0
            else:
                # Kopie: der Grabber-Frame wird sonst bei stehender Kamera
                # mehrfach uebermalt
                frame = apply_flips(raw.copy(), config)
            warning = frame_warning(age, frame_timeout)

            if seq != last_seq:
                fps_frames += seq - last_seq
                last_seq = seq
            if loop_start - fps_window_start >= 1.0:
                fps = fps_frames / (loop_start - fps_window_start)
                fps_window_start, fps_frames = loop_start, 0

            sensors.poll()
            s = sensors.fresh()

            # Anzeige-Latenz = Alter des gezeigten Kamerabilds (Aufnahme fertig
            # bis Anzeige), nicht nur die Schleifenzeit. Glas-zu-Glas kommt
            # noch Sensor- und Displayzeit dazu (Pflicht-Latenztest im Guide).
            latency_ms = age * 1000.0 if age is not None else None

            battery = finite(s.get("battery"))
            if warning is None:
                warning = battery_warning(battery, low_batt)

            contacts = s.get("contacts")
            state = {
                "shield": finite(s.get("shield"), config["default_shield"]),
                "ammo": int(finite(s.get("ammo"), config["default_ammo"])),
                "battery_percent": battery,
                "heading_deg": finite(s.get("heading"), 0.0),
                "fps": fps,
                "latency_ms": latency_ms,
                "latency_limit_ms": config["latency_limit_ms"],
                "contacts": contacts if isinstance(contacts, list) else None,
                "warning": warning,
            }
            try:
                hud_overlay.draw_hud(frame, state)
            except Exception as exc:
                # HUD-Fehler duerfen das Kamerabild nicht kosten
                print(f"HUD-Overlay uebersprungen: {type(exc).__name__}: {exc}", file=sys.stderr)
                if warning:   # der Warnbanner hat Vorrang vor allem anderen
                    try:
                        hud_overlay.draw_warning_banner(frame, warning)
                    except Exception:
                        pass
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
        grabber.stop()
        camera.close()
        sensors.close()
        cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    sys.exit(main())
