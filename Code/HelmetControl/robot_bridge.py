#!/usr/bin/env python3
"""Display-only companion telemetry -> hud_state.json; no motion commands.

CONCEPT: no manufacturer SDK adapter or following controller is implemented.
See Documentation/Guides/Begleitroboter-Integration.md. Each valid UDP message
is a complete snapshot, for example:

    {"robot_battery": 64, "robot_distance_m": 2.3, "robot_bearing": 130,
     "robot_state": "follow"}

Bearing is relative to the wearer: 0 degrees ahead, 90 degrees right.
The sender must perform that conversion; UWB range alone cannot.
Missing robot fields are cleared. Foreign HUD fields are preserved in each
read/modify/write, but this is NOT a concurrent-writer protocol. sensor_bridge
can still replace these fields; a future live integration needs a coordinated
writer. Atomic rename prevents partial JSON reads, not concurrent lost updates.

Loopback is the default. --source-ip is only an IP filter, NOT authentication
or replay protection. Stale removal works while this process runs; the existing
HUD has no independent freshness check after a bridge crash. This display is
not a robot safety system.

Selftest (always uses temporary files, --state is ignored):
    python3 robot_bridge.py --selftest
Local development listener:
    python3 robot_bridge.py --listen 127.0.0.1 --port 9009
"""

import argparse
import ipaddress
import json
import math
import os
import socket
import sys
import tempfile
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_STATE = os.path.join(BASE_DIR, "hud_state.json")
DEFAULT_PORT = 9009
DEFAULT_LISTEN = "127.0.0.1"
ROBOT_KEYS = ("robot_distance_m", "robot_bearing", "robot_battery", "robot_state")
ROBOT_STATES = ("idle", "follow", "hold", "guard", "stopped", "lost", "fault",
                "emergency_stop")


def validate_snapshot(data):
    """Return known valid fields; reject malformed or empty robot snapshots."""
    if not isinstance(data, dict):
        return None
    snapshot = {key: data[key] for key in ROBOT_KEYS if key in data}
    if not snapshot:
        return None
    for key, value in snapshot.items():
        if key == "robot_state":
            if not isinstance(value, str) or value not in ROBOT_STATES:
                return None
            continue
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return None
        try:
            if not math.isfinite(value) or value < 0:
                return None
        except OverflowError:
            return None
        if key == "robot_battery" and value > 100:
            return None
        if key == "robot_bearing" and value >= 360:
            return None
    return snapshot


def parse_datagram(raw):
    """Strict UTF-8 JSON -> validated snapshot; invalid messages are ignored."""
    if isinstance(raw, bytes):
        try:
            raw = raw.decode("utf-8")
        except UnicodeDecodeError:
            return None
    if not isinstance(raw, str):
        return None
    try:
        return validate_snapshot(json.loads(raw))
    except (ValueError, RecursionError):
        return None


def load_state(state_path):
    try:
        with open(state_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def atomic_write(path, payload):
    """Publish complete JSON through a unique temp file; not a writer lock."""
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=os.path.dirname(os.path.abspath(path)),
                prefix=".robot-state-", suffix=".tmp", delete=False) as handle:
            tmp = handle.name
            json.dump(payload, handle, allow_nan=False)
        os.replace(tmp, path)
        return True
    except (OSError, TypeError, ValueError) as exc:
        print(f"robot_bridge: Schreibfehler {path}: {exc}", file=sys.stderr)
        return False
    finally:
        if tmp is not None:
            try:
                os.remove(tmp)
            except OSError:
                pass


def merge_into_state(data, state_path):
    """Replace the robot snapshot, retaining all foreign fields read at entry."""
    snapshot = validate_snapshot(data)
    if snapshot is None:
        raise ValueError("ungueltiger Roboter-Snapshot")
    updated = {key: value for key, value in load_state(state_path).items()
               if key not in ROBOT_KEYS}
    updated.update(snapshot)
    if not atomic_write(state_path, updated):
        raise OSError("Roboter-Snapshot konnte nicht geschrieben werden")
    return updated


def clear_robot_state(state_path):
    """Return success if robot fields are absent or were successfully removed."""
    state = load_state(state_path)
    if not any(key in state for key in ROBOT_KEYS):
        return True
    return atomic_write(state_path, {key: value for key, value in state.items()
                                     if key not in ROBOT_KEYS})


def run(listen, port, state_path, stale_after=3.0, source_ip=None):
    if not math.isfinite(stale_after) or stale_after <= 0:
        raise ValueError("stale_after muss positiv und endlich sein")
    if source_ip is not None:
        source_ip = str(ipaddress.IPv4Address(source_ip))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind((listen, port))
    except OSError as exc:
        sock.close()
        sys.exit(f"robot_bridge: kann {listen}:{port} nicht binden ({exc})")
    sock.settimeout(min(1.0, stale_after))
    if not clear_robot_state(state_path):  # Never revive a previous snapshot.
        sock.close()
        raise OSError("Alter Roboter-Snapshot konnte nicht entfernt werden")
    print(f"robot_bridge: Telemetrie {listen}:{port} "
          f"-> {os.path.basename(state_path)} (nur Anzeige)")
    last_seen = None
    try:
        while True:
            # Check every iteration, including during invalid packet floods.
            if last_seen is not None and time.monotonic() - last_seen >= stale_after:
                if clear_robot_state(state_path):
                    last_seen = None
                    print("robot_bridge: Signal verloren - Snapshot entfernt")
            try:
                raw, addr = sock.recvfrom(2048)
            except socket.timeout:
                continue
            if source_ip is not None and addr[0] != source_ip:
                continue
            data = parse_datagram(raw)
            if data is not None:
                try:
                    merge_into_state(data, state_path)
                except OSError:
                    continue  # A failed publication must not refresh freshness.
                last_seen = time.monotonic()
    except KeyboardInterrupt:
        print("\nrobot_bridge: beendet")
    finally:
        sock.close()
        clear_robot_state(state_path)


def run_selftest(state_path=None):
    """Keep the legacy argument, but never touch the supplied or live path."""
    with tempfile.TemporaryDirectory(prefix="halo-robot-selftest-") as tmp:
        test_path = os.path.join(tmp, "hud_state.json")
        atomic_write(test_path, {"ammo": 27, "shield_percent": 80, "heading": 90})
        samples = [
            '{"robot_battery":64,"robot_distance_m":2.3,"robot_bearing":130,"robot_state":"follow"}',
            'not json - ignored',
            '{"robot_battery":18,"robot_distance_m":1.1,"robot_bearing":200,"robot_state":"guard"}',
        ]
        for line in samples:
            data = parse_datagram(line)
            print(f"  [{'ignoriert' if data is None else 'ok'}] {line}")
            if data is not None:
                result = merge_into_state(data, test_path)
        assert result["ammo"] == 27 and result["robot_battery"] == 18
        print("Selftest in temporaeren Dateien erfolgreich:", result)
        return result


def main():
    parser = argparse.ArgumentParser(
        description="Begleit-Roboter-Telemetrie -> HUD; keine Bewegungssteuerung")
    parser.add_argument("--listen", default=DEFAULT_LISTEN,
                        help="Bind-Adresse (Standard: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT,
                        help=f"UDP-Port (Standard: {DEFAULT_PORT})")
    parser.add_argument("--state", default=DEFAULT_STATE,
                        help="Ziel-Datei; wird beim Selftest nicht verwendet")
    parser.add_argument("--source-ip", type=ipaddress.IPv4Address,
                        help="Optionale Sender-IPv4; nur Filter, keine Authentifizierung")
    parser.add_argument("--stale-after", type=float, default=3.0,
                        help="Snapshot nach dieser Zahl Sekunden entfernen (Standard: 3)")
    parser.add_argument("--selftest", action="store_true",
                        help="ohne Netzwerk ausschliesslich temporaere Dateien testen")
    args = parser.parse_args()
    if args.selftest:
        run_selftest(args.state)
    else:
        run(args.listen, args.port, args.state, args.stale_after, args.source_ip)


if __name__ == "__main__":
    main()
