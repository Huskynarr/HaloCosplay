#!/usr/bin/env python3
"""Halo-Style HUD-Overlay fuer den AR-Passthrough (V3).

Dieses Modul zeichnet das HUD auf einen Kamera-Frame (BGR numpy-Array).
Es haengt NUR von numpy und OpenCV ab und ist bewusst von der Kamera-/Display-
Pipeline (`ar_passthrough.py`) getrennt, damit man das Overlay auch ohne
Hardware testen kann (siehe `--selftest` in ar_passthrough.py).

Alle Funktionen arbeiten in-place auf dem uebergebenen Frame und geben ihn
zur Verkettung zurueck.
"""

import math

import cv2
import numpy as np

# Halo-Infinite-naher Gruenton (BGR fuer OpenCV). Hell genug fuer Lesbarkeit.
HUD_GREEN = (90, 240, 120)
HUD_DIM = (60, 140, 80)
WARN_RED = (60, 60, 235)
WARN_AMBER = (40, 190, 245)
WHITE = (235, 235, 235)

FONT = cv2.FONT_HERSHEY_SIMPLEX


def _text(frame, label, org, scale=0.6, color=HUD_GREEN, thickness=1):
    cv2.putText(frame, label, org, FONT, scale, color, thickness, cv2.LINE_AA)


def draw_shield_bar(frame, shield_percent):
    """Schild-Balken oben mittig, wie im Halo-HUD."""
    h, w = frame.shape[:2]
    pct = max(0.0, min(100.0, float(shield_percent)))
    bar_w = int(w * 0.5)
    x0 = (w - bar_w) // 2
    y0 = int(h * 0.06)
    x1 = x0 + bar_w
    y1 = y0 + max(8, int(h * 0.025))
    cv2.rectangle(frame, (x0, y0), (x1, y1), HUD_GREEN, 1, cv2.LINE_AA)
    fill_w = int((bar_w - 4) * pct / 100.0)
    if fill_w > 0:
        cv2.rectangle(frame, (x0 + 2, y0 + 2), (x0 + 2 + fill_w, y1 - 2),
                      HUD_GREEN, -1, cv2.LINE_AA)
    return frame


def draw_compass(frame, heading_deg):
    """Schmale Kompassleiste am oberen Rand."""
    h, w = frame.shape[:2]
    cx = w // 2
    y = int(h * 0.03)
    cv2.line(frame, (cx, y - 6), (cx, y + 6), HUD_GREEN, 2, cv2.LINE_AA)
    try:
        heading = int(heading_deg) % 360
    except (TypeError, ValueError):
        heading = 0
    _text(frame, f"{heading:03d}", (cx - 18, y - 10), 0.5, HUD_GREEN, 1)


def draw_motion_tracker(frame, contacts=None):
    """Bewegungsmelder unten rechts (kreisrundes Radar)."""
    h, w = frame.shape[:2]
    r = int(min(h, w) * 0.10)
    cx = w - r - 20
    cy = h - r - 20
    cv2.circle(frame, (cx, cy), r, HUD_GREEN, 1, cv2.LINE_AA)
    cv2.circle(frame, (cx, cy), r // 2, HUD_DIM, 1, cv2.LINE_AA)
    cv2.line(frame, (cx - r, cy), (cx + r, cy), HUD_DIM, 1, cv2.LINE_AA)
    cv2.line(frame, (cx, cy - r), (cx, cy + r), HUD_DIM, 1, cv2.LINE_AA)
    cv2.circle(frame, (cx, cy), 2, HUD_GREEN, -1, cv2.LINE_AA)
    for contact in contacts or []:
        # contact = (winkel_grad, distanz_0_bis_1)
        try:
            ang, dist = contact
            dist = max(0.0, min(1.0, float(dist)))
            px = int(cx + math.cos(math.radians(ang)) * r * dist)
            py = int(cy - math.sin(math.radians(ang)) * r * dist)
            cv2.circle(frame, (px, py), 3, WARN_RED, -1, cv2.LINE_AA)
        except (TypeError, ValueError):
            continue
    return frame


def draw_ammo(frame, ammo):
    # oben rechts, damit es nicht mit dem Bewegungsmelder (unten rechts) kollidiert
    h, w = frame.shape[:2]
    _text(frame, str(ammo), (w - 120, int(h * 0.14)), 1.1, HUD_GREEN, 2)


def draw_status(frame, battery_percent=None, fps=None, latency_ms=None):
    """Statuszeile unten links: Akku, FPS, Latenz (fuer den Pflicht-Latenztest)."""
    h = frame.shape[0]
    y = h - 22
    parts = []
    if battery_percent is not None:
        parts.append(f"AKKU {float(battery_percent):.0f}%")
    if fps is not None:
        parts.append(f"{float(fps):.0f} FPS")
    if latency_ms is not None:
        parts.append(f"{float(latency_ms):.0f} ms")
    if parts:
        _text(frame, "  ".join(parts), (20, y), 0.55, HUD_GREEN, 1)
    return frame


def draw_warning_banner(frame, message):
    """Grosser, nicht zu uebersehender Warnbalken. Sicherheitskritisch."""
    h, w = frame.shape[:2]
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, h // 2 - 40), (w, h // 2 + 40), WARN_RED, -1)
    cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)
    size = cv2.getTextSize(message, FONT, 1.0, 2)[0]
    org = ((w - size[0]) // 2, h // 2 + 10)
    _text(frame, message, org, 1.0, WHITE, 2)
    return frame


def draw_hud(frame, state):
    """Zeichnet das komplette HUD anhand eines state-dict.

    Erwartete Schluessel (alle optional):
      shield, ammo, battery_percent, heading_deg, fps, latency_ms,
      contacts (Liste von (winkel, distanz)), warning (str oder None).
    """
    draw_shield_bar(frame, state.get("shield", 100))
    draw_compass(frame, state.get("heading_deg", 0))
    draw_motion_tracker(frame, state.get("contacts"))
    draw_ammo(frame, state.get("ammo", 0))
    draw_status(frame,
                battery_percent=state.get("battery_percent"),
                fps=state.get("fps"),
                latency_ms=state.get("latency_ms"))

    # Latenz-Warnung (gelb): Bild zu traege -> Uebelkeit/Sturzgefahr
    latency_ms = state.get("latency_ms")
    latency_limit = state.get("latency_limit_ms", 40)
    if latency_ms is not None and latency_ms > latency_limit:
        h, w = frame.shape[:2]
        _text(frame, "LATENZ HOCH", (w // 2 - 80, int(h * 0.16)), 0.7, WARN_AMBER, 2)

    # Harte Warnung (rot) hat Vorrang und liegt obenauf
    warning = state.get("warning")
    if warning:
        draw_warning_banner(frame, warning)
    return frame


def make_test_frame(width=1280, height=720):
    """Synthetischer Frame fuer den Hardware-freien Selbsttest."""
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    # leichter Verlauf, damit man Overlay-Kontrast sieht
    for y in range(height):
        frame[y, :, 0] = int(20 + 30 * y / height)
        frame[y, :, 1] = int(25 + 20 * y / height)
    cv2.putText(frame, "SIM CAM", (width // 2 - 90, height // 2),
                FONT, 1.0, (70, 70, 70), 2, cv2.LINE_AA)
    return frame
