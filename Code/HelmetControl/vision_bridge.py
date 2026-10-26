#!/usr/bin/env python3
"""Bruecke: Raspberry Pi AI Camera (IMX500) -> hud_state.json.

Die AI Camera rechnet das Erkennungsnetz direkt auf dem Kamerachip, der Pi
liest nur die Ergebnisse aus (kaum CPU-Last). Diese Bruecke uebersetzt jede
Erkennung in einen Kontakt fuer den Bewegungsmelder des HUD:

    "vision_contacts": [{"label": "person", "score": 0.91,
                         "bearing": -12.5, "distance": 0.42}, ...],
    "vision_ts": 1730000000.0

bearing  = Winkel in Grad relativ zur Blickrichtung (negativ = links)
distance = 0.0 (direkt vor dir) bis 1.0 (Rand des Trackers), geschaetzt aus
           der Groesse des Objekts im Bild
vision_ts = Zeitstempel; hud_display.py ignoriert Kontakte, die aelter als
           2 s sind (Kamera abgestuerzt -> keine eingefrorenen Blips)

Nur fuer AR-Stufe A/B (OLED-HUD). Bei Stufe C belegt ar_passthrough.py die
Kamera - dort gehoert die Erkennung in die Passthrough-Pipeline.

Hardwarefreier Test:
    python3 vision_bridge.py --selftest --state /tmp/vision_state.json
Live (Pi 5 + AI Camera, Pakete siehe Elektronik-Sprachsteuerung.md):
    python3 vision_bridge.py
"""

import argparse
import math
import os
import sys
import time

import hud_state

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_STATE = os.path.join(BASE_DIR, "hud_state.json")
DEFAULT_MODEL = ("/usr/share/imx500-models/"
                 "imx500_network_ssd_mobilenetv2_fpnlite_320x320_pp.rpk")
DEFAULT_LABELS = os.path.join(BASE_DIR, "coco_labels.txt")

THRESHOLD = 0.55          # Mindest-Konfidenz
MAX_CONTACTS = 6          # mehr passt auf 128x64 nicht sinnvoll
HFOV_DEG = 66.0           # horizontaler Bildwinkel der AI Camera
WRITE_INTERVAL = 0.2      # s - HUD liest alle 100 ms, oefter schreiben bringt nichts
VISION_KEYS = ("vision_contacts", "vision_ts")


def detection_to_contact(label, score, box, flip_x=False):
    """Normierte Box (y0, x0, y1, x1) -> Kontakt fuer den Bewegungsmelder."""
    y0, x0, y1, x1 = (float(v) for v in box)
    xc = min(1.0, max(0.0, (x0 + x1) / 2.0))
    if flip_x:
        xc = 1.0 - xc
    area = max(0.0, (x1 - x0) * (y1 - y0))
    # Grosses Objekt = nah. Wurzel, weil die Flaeche quadratisch mit der Naehe waechst.
    distance = min(1.0, max(0.15, 1.1 - math.sqrt(area) * 1.4))
    return {
        "label": str(label),
        "score": round(float(score), 2),
        "bearing": round((xc - 0.5) * HFOV_DEG, 1),
        "distance": round(distance, 2),
    }


def build_contacts(detections, labels, flip_x=False):
    """[(class_id, score, box), ...] -> sortierte Kontaktliste."""
    contacts = []
    for cls, score, box in detections:
        if score < THRESHOLD:
            continue
        idx = int(cls)
        label = labels[idx] if 0 <= idx < len(labels) else f"#{idx}"
        if label in ("", "-"):
            continue
        contacts.append(detection_to_contact(label, score, box, flip_x))
    contacts.sort(key=lambda c: -c["score"])
    return contacts[:MAX_CONTACTS]


def publish(state_path, contacts):
    hud_state.merge(state_path, {"vision_contacts": contacts, "vision_ts": round(time.time(), 2)})


def run(state_path, model, labels_path, flip_x):
    try:
        from picamera2 import Picamera2
        from picamera2.devices import IMX500
        from picamera2.devices.imx500 import NetworkIntrinsics
    except ImportError:
        sys.exit("picamera2 fehlt: sudo apt install python3-picamera2 imx500-all")

    imx = IMX500(model)                       # muss VOR Picamera2() passieren
    intr = imx.network_intrinsics or NetworkIntrinsics()
    if not intr.task:
        intr.task = "object detection"
    if intr.labels is None:
        try:
            with open(labels_path, "r", encoding="utf-8") as handle:
                intr.labels = handle.read().splitlines()
        except OSError:
            sys.exit(f"Label-Datei fehlt: {labels_path} (siehe Elektronik-Sprachsteuerung.md)")
    intr.update_with_defaults()

    cam = Picamera2(imx.camera_num)
    cfg = cam.create_preview_configuration(controls={"FrameRate": intr.inference_rate},
                                           buffer_count=12)
    cam.start(cfg, show_preview=False)
    print(f"vision_bridge: AI Camera laeuft -> {os.path.basename(state_path)}")

    last_write = 0.0
    try:
        while True:
            out = imx.get_outputs(cam.capture_metadata(), add_batch=True)
            if out is None:
                continue
            boxes, scores, classes = out[0][0], out[1][0], out[2][0]
            if intr.bbox_normalization:
                boxes = boxes / imx.get_input_size()[1]
            if intr.bbox_order == "xy":
                boxes = boxes[:, [1, 0, 3, 2]]
            now = time.time()
            if now - last_write >= WRITE_INTERVAL:
                publish(state_path, build_contacts(zip(classes, scores, boxes), intr.labels, flip_x))
                last_write = now
    except KeyboardInterrupt:
        print("\nvision_bridge: beendet")
    finally:
        cam.stop()
        hud_state.merge(state_path, remove=VISION_KEYS)   # HUD faellt auf Demo zurueck


def run_selftest(state_path):
    """Kuenstliche Erkennungen verarbeiten, ohne Kamera."""
    labels = ["person", "bicycle", "-", "dog"]
    hud_state.merge(state_path, {"ammo": 27, "heading": 90})   # Werte anderer Module
    detections = [
        (0, 0.91, (0.10, 0.15, 0.95, 0.45)),   # Person links, nah
        (3, 0.72, (0.60, 0.70, 0.80, 0.80)),   # Hund rechts, weiter weg
        (2, 0.99, (0.0, 0.0, 1.0, 1.0)),       # "-" Platzhalter -> ignoriert
        (1, 0.30, (0.4, 0.4, 0.6, 0.6)),       # zu unsicher -> ignoriert
    ]
    contacts = build_contacts(detections, labels)
    for c in contacts:
        print(f"  {c['label']:<8} {c['score']:.2f}  {c['bearing']:+6.1f} Grad  Distanz {c['distance']:.2f}")
    publish(state_path, contacts)
    state = hud_state.load(state_path)
    assert state.get("ammo") == 27 and len(state["vision_contacts"]) == 2, state
    print(f"\nGeschrieben: {state_path} (ammo/heading bleiben erhalten)")


def main():
    parser = argparse.ArgumentParser(description="Bruecke AI Camera (IMX500) -> HUD-Bewegungsmelder")
    parser.add_argument("--state", default=DEFAULT_STATE, help="Ziel-Datei (Standard: hud_state.json)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="IMX500-Netz (.rpk)")
    parser.add_argument("--labels", default=DEFAULT_LABELS, help="Label-Datei (coco_labels.txt)")
    parser.add_argument("--flip-x", action="store_true", help="Kamera kopfueber eingebaut")
    parser.add_argument("--selftest", action="store_true", help="ohne Kamera: Beispieldaten verarbeiten")
    args = parser.parse_args()
    if args.selftest:
        run_selftest(args.state)
    else:
        run(args.state, args.model, args.labels, args.flip_x)


if __name__ == "__main__":
    main()
