#!/usr/bin/env python3
"""Bridge: companion robot (WLAN/UDP telemetry) -> hud_state.json.

CONCEPT / future extension. See Documentation/Guides/Begleitroboter-Integration.md.

A Unitree Go2 EDU (or CyberDog 2) runs its own computer (ROS 2 / Python SDK).
A small script ON THE ROBOT sends one UDP JSON datagram per ~0.2 s to the
helmet Pi over the shared WLAN, e.g.:

    {"robot_battery": 64, "robot_distance_m": 2.3, "robot_bearing": 130,
     "robot_state": "follow", "contacts": 2}

This service receives those datagrams and merges them into hud_state.json, so
the HUD shows the robot as a friendly marker on the motion tracker (and can
warn on low robot battery). It mirrors sensor_bridge.py but listens on the
network instead of a serial port.

Fields written to hud_state.json: robot_distance_m, robot_bearing,
robot_battery, robot_state. Fields from other modules (ammo, shield_percent,
heading) are preserved.

Hardware-free test (feeds sample datagrams locally):
    python3 robot_bridge.py --selftest
Live:
    python3 robot_bridge.py --listen 0.0.0.0 --port 9009
"""

import argparse
import json
import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_STATE = os.path.join(BASE_DIR, "hud_state.json")
DEFAULT_PORT = 9009

# Telemetry keys the robot may send -> kept as-is in hud_state.json
ROBOT_KEYS = ("robot_distance_m", "robot_bearing", "robot_battery", "robot_state")
# Keys owned by other modules that must survive a robot update
PRESERVE_KEYS = ("ammo", "shield_percent", "heading")


def parse_datagram(raw):
    """Bytes/str -> dict, or None if it is not a valid JSON object."""
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8", errors="ignore")
    raw = raw.strip()
    if not raw.startswith("{"):
        return None
    try:
        data = json.loads(raw)
        return data if isinstance(data, dict) else None
    except ValueError:
        return None


def load_state(state_path):
    if not os.path.exists(state_path):
        return {}
    try:
        with open(state_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def atomic_write(path, payload):
    tmp = f"{path}.tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump(payload, handle)
        os.replace(tmp, path)
    except OSError as exc:
        print(f"robot_bridge: Schreibfehler {path}: {exc}", file=sys.stderr)


def merge_into_state(data, state_path):
    """Write robot fields into hud_state.json, preserving other modules' keys."""
    state = load_state(state_path)
    updated = {k: v for k, v in state.items() if k in PRESERVE_KEYS}
    # carry over any previous robot fields, then apply the new datagram
    for k in ROBOT_KEYS:
        if k in state:
            updated[k] = state[k]
    for k in ROBOT_KEYS:
        if k in data:
            updated[k] = data[k]
    atomic_write(state_path, updated)
    return updated


def run(listen, port, state_path, stale_after=3.0):
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind((listen, port))
    except OSError as exc:
        sys.exit(f"robot_bridge: kann {listen}:{port} nicht binden ({exc})")
    sock.settimeout(1.0)
    print(f"robot_bridge: warte auf Robo-Telemetrie auf {listen}:{port} "
          f"-> {os.path.basename(state_path)}")
    last_seen = None
    try:
        while True:
            try:
                raw, _addr = sock.recvfrom(2048)
            except socket.timeout:
                # No packet: mark robot as lost so the HUD can drop the marker
                if last_seen and time.time() - last_seen > stale_after:
                    state = load_state(state_path)
                    if "robot_distance_m" in state:
                        for k in ROBOT_KEYS:
                            state.pop(k, None)
                        atomic_write(state_path, state)
                        print("robot_bridge: Robo-Signal verloren - Marker entfernt")
                    last_seen = None
                continue
            data = parse_datagram(raw)
            if data:
                merge_into_state(data, state_path)
                last_seen = time.time()
    except KeyboardInterrupt:
        print("\nrobot_bridge: beendet")
    finally:
        sock.close()


def run_selftest(state_path):
    """Feed sample datagrams without any network, show the merged result."""
    # Pretend another module already set ammo/shield/heading
    atomic_write(state_path, {"ammo": 27, "shield_percent": 80, "heading": 90})
    samples = [
        '{"robot_battery": 64, "robot_distance_m": 2.3, "robot_bearing": 130, "robot_state": "follow"}',
        'not json - ignored',
        '{"robot_battery": 18, "robot_distance_m": 1.1, "robot_bearing": 200, "robot_state": "guard"}',
    ]
    for line in samples:
        data = parse_datagram(line)
        status = "ignoriert" if data is None else "ok"
        print(f"  [{status}] {line}")
        if data:
            result = merge_into_state(data, state_path)
    print(f"\nGeschrieben: {state_path}")
    print("Ergebnis (ammo/shield/heading bleiben erhalten):", result)
    os.remove(state_path)


def main():
    parser = argparse.ArgumentParser(
        description="Bruecke Begleit-Roboter (WLAN/UDP) -> HUD (hud_state.json)")
    parser.add_argument("--listen", default="0.0.0.0",
                        help="Bind-Adresse (Standard: 0.0.0.0 = alle)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT,
                        help=f"UDP-Port (Standard: {DEFAULT_PORT})")
    parser.add_argument("--state", default=DEFAULT_STATE,
                        help="Ziel-Datei (Standard: hud_state.json)")
    parser.add_argument("--selftest", action="store_true",
                        help="ohne Netzwerk: Beispiel-Telemetrie verarbeiten")
    args = parser.parse_args()
    if args.selftest:
        run_selftest(args.state)
    else:
        run(args.listen, args.port, args.state)


if __name__ == "__main__":
    main()
