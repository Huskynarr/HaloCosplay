#!/usr/bin/env python3
"""Bridge: SensorFeeder (ESP32, serial JSON) -> hud_state.json / battery.json.

The SensorFeeder sketch sends one JSON line at ~10 Hz, e.g.
    {"heading":123,"battery":78,"temp":41}

This service reads those lines and writes them into the files the HUD polls,
so the compass shows real heading and the battery readout is live - without
coupling the HUD loop to the serial port. Run it alongside hud_display.py
(e.g. as a second systemd service, see Elektronik-Autostart.md).

Usage:
    python3 sensor_bridge.py --port /dev/ttyUSB0
    python3 sensor_bridge.py --port /dev/ttyUSB0 --baud 115200
    python3 sensor_bridge.py --selftest      # no hardware: feed sample lines

It is intentionally robust: a missing port, garbage lines, or a disconnected
ESP32 never crash it - it logs and keeps trying.
"""

import argparse
import json
import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_BAUD = 115200
DEFAULT_STATE = os.path.join(BASE_DIR, "hud_state.json")
DEFAULT_BATTERY = os.path.join(BASE_DIR, "battery.json")


def parse_line(line):
    """Parse one serial line into a dict, or None if it is not valid JSON."""
    line = line.strip()
    if not line.startswith("{"):
        return None
    try:
        return json.loads(line)
    except ValueError:
        return None


def atomic_write(path, payload):
    """Write JSON atomically so the HUD never reads a half-written file."""
    tmp = f"{path}.tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump(payload, handle)
        os.replace(tmp, path)
    except OSError as exc:
        print(f"sensor_bridge: Schreibfehler {path}: {exc}", file=sys.stderr)


def update_files(data, state_path, battery_path, keep_state=None):
    """Map a SensorFeeder reading onto hud_state.json and battery.json.

    keep_state preserves fields the sensor does not provide (e.g. ammo/shield
    set by another module) across writes.
    """
    state = dict(keep_state or {})
    if "heading" in data:
        state["heading"] = data["heading"]
    if state:
        atomic_write(state_path, state)

    battery = {}
    if "battery" in data:
        battery["battery_percent"] = data["battery"]
    if "voltage" in data:
        battery["voltage"] = data["voltage"]
    if battery:
        atomic_write(battery_path, battery)
    return state


def load_existing_state(state_path):
    """Read current hud_state.json so we don't clobber ammo/shield etc."""
    if not os.path.exists(state_path):
        return {}
    try:
        with open(state_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def run(port, baud, state_path, battery_path, reconnect_delay=2.0):
    try:
        import serial
    except ImportError:
        sys.exit("pyserial fehlt: pip install -r requirements.txt")

    print(f"sensor_bridge: lese {port} @ {baud} -> {os.path.basename(state_path)},"
          f" {os.path.basename(battery_path)}")
    while True:
        try:
            with serial.Serial(port, baud, timeout=1.0) as ser:
                print("sensor_bridge: verbunden")
                # keep ammo/shield that other modules may have written
                keep = {k: v for k, v in load_existing_state(state_path).items()
                        if k in ("ammo", "shield_percent")}
                while True:
                    raw = ser.readline().decode("utf-8", errors="ignore")
                    if not raw:
                        continue  # timeout, just keep waiting
                    data = parse_line(raw)
                    if data:
                        update_files(data, state_path, battery_path, keep)
        except serial.SerialException as exc:
            print(f"sensor_bridge: Port-Problem ({exc}), neuer Versuch in "
                  f"{reconnect_delay}s", file=sys.stderr)
            time.sleep(reconnect_delay)
        except KeyboardInterrupt:
            print("\nsensor_bridge: beendet")
            return


def run_selftest(state_path, battery_path):
    """Feed a few sample lines without any hardware and show the result."""
    samples = [
        '{"heading":0,"battery":100,"temp":35}',
        '{"heading":123,"battery":78,"temp":41}',
        'garbage line that should be ignored',
        '{"heading":270,"battery":55}',
    ]
    keep = {"ammo": 27, "shield_percent": 80}
    for line in samples:
        data = parse_line(line)
        status = "ignoriert" if data is None else "ok"
        print(f"  [{status}] {line}")
        if data:
            keep = update_files(data, state_path, battery_path, keep)
    print(f"\nGeschrieben: {state_path}")
    print(f"            {battery_path}")
    print("Hinweis: ammo/shield bleiben erhalten:", keep)


def main():
    parser = argparse.ArgumentParser(
        description="Bruecke SensorFeeder (Serial JSON) -> HUD-Dateien")
    parser.add_argument("--port", default="/dev/ttyUSB0",
                        help="serieller Port des ESP32 (Standard: /dev/ttyUSB0)")
    parser.add_argument("--baud", type=int, default=DEFAULT_BAUD,
                        help=f"Baudrate (Standard: {DEFAULT_BAUD})")
    parser.add_argument("--state", default=DEFAULT_STATE,
                        help="Ziel-Datei fuer Heading/Live-Werte")
    parser.add_argument("--battery", default=DEFAULT_BATTERY,
                        help="Ziel-Datei fuer Akkustatus")
    parser.add_argument("--selftest", action="store_true",
                        help="ohne Hardware: Beispielzeilen verarbeiten")
    args = parser.parse_args()

    if args.selftest:
        run_selftest(args.state, args.battery)
    else:
        run(args.port, args.baud, args.state, args.battery)


if __name__ == "__main__":
    main()
