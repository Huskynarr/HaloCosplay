#!/usr/bin/env python3
"""Gemeinsamer, sicherer Zugriff auf hud_state.json fuer alle Bruecken.

Mehrere Module schreiben Live-Werte in dieselbe Datei (sensor_bridge: heading,
robot_bridge: robot_*, vision_bridge: vision_*). Wuerde jedes Modul seinen
eigenen Stand komplett zurueckschreiben, ueberschreiben sie sich gegenseitig.
merge() liest deshalb unter einer Dateisperre den aktuellen Stand, aendert nur
die eigenen Schluessel und ersetzt die Datei atomar. Der HUD liest ohne Sperre
und sieht dank os.replace() nie eine halb geschriebene Datei.
"""

import fcntl
import json
import os
import sys


def load(path):
    """Aktuellen Stand lesen; fehlende oder kaputte Datei ergibt {}."""
    if not path or not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def merge(path, updates=None, remove=()):
    """Schluessel setzen bzw. entfernen, alle anderen Module bleiben unberuehrt.

    Gibt den neuen Gesamtstand zurueck. Schreibfehler werden gemeldet, aber
    nie als Exception weitergereicht - ein volles Dateisystem darf keine
    Bruecke abstuerzen lassen.
    """
    updates = updates or {}
    try:
        with open(f"{path}.lock", "a", encoding="utf-8") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            try:
                state = load(path)
                state.update(updates)
                for key in remove:
                    state.pop(key, None)
                tmp = f"{path}.tmp"
                with open(tmp, "w", encoding="utf-8") as handle:
                    json.dump(state, handle)
                os.replace(tmp, path)
                return state
            finally:
                fcntl.flock(lock, fcntl.LOCK_UN)
    except OSError as exc:
        print(f"hud_state: Schreibfehler {path}: {exc}", file=sys.stderr)
        return load(path)
