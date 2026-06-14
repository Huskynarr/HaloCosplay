#!/usr/bin/env python3
"""Halo-style HUD for a transparent OLED (SSD1309, 128x64).

Features:
  - boot sequence (MJOLNIR startup)
  - animated shield bar with recharge effect
  - scrolling compass (N/E/S/W) driven by live heading or demo rotation
  - motion tracker with sweep and blips
  - ammo counter, battery readout with low-battery flash

Live values (all optional) are read from JSON files so other modules can
feed the HUD without coupling (see V3-Systemarchitektur.md):
  - battery_path: {"battery_percent": 78, "voltage": 7.4}
  - state_path:   {"shield_percent": 80, "ammo": 27, "heading": 123}
Missing files simply fall back to a self-running demo animation.

Hardware-free test (renders PNG frames instead of driving the OLED):
    python3 hud_display.py --selftest hud_test.png
"""

import argparse
import json
import math
import os
import time

from PIL import Image, ImageDraw

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULTS = {
    "i2c_port": 1,
    "i2c_address": 0x3C,
    "width": 128,
    "height": 64,
    "refresh_ms": 100,
    "show_battery": False,
    "battery_path": "battery.json",
    "battery_field": "battery_percent",
    "voltage_field": "voltage",
    "state_path": "hud_state.json",
    "low_battery_percent": 20,
    "boot_animation": True,
    "log_path": "",
    "log_interval_s": 5,
}


def load_config():
    config = DEFAULTS.copy()
    config_path = os.path.join(BASE_DIR, "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        config.update(data)
    if isinstance(config.get("i2c_address"), str):
        config["i2c_address"] = int(config["i2c_address"], 0)
    return config


CONFIG = load_config()
WIDTH = CONFIG["width"]
HEIGHT = CONFIG["height"]


def resolve_path(path_value):
    if not path_value:
        return ""
    if os.path.isabs(path_value):
        return path_value
    return os.path.join(BASE_DIR, path_value)


def read_json_file(path_value):
    path_value = resolve_path(path_value)
    if not path_value or not os.path.exists(path_value):
        return None
    try:
        with open(path_value, "r", encoding="utf-8") as handle:
            raw = handle.read().strip()
        if not raw:
            return None
        return json.loads(raw) if raw.startswith("{") else {"value": float(raw)}
    except (OSError, ValueError, json.JSONDecodeError):
        return None


def read_battery(config):
    data = read_json_file(config.get("battery_path", ""))
    if data is None:
        return None
    if "value" in data:
        return {"percent": data["value"], "voltage": None}
    return {
        "percent": data.get(config.get("battery_field", "battery_percent")),
        "voltage": data.get(config.get("voltage_field", "voltage")),
    }


def safe_float(value, default=None):
    """Parse value to float; tolerate None, strings, junk."""
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def read_state(config, t):
    """Live state from file, with demo animation as fallback.

    Tolerant against missing keys, null, and string values so a malformed
    hud_state.json never crashes the HUD - it just falls back per field.
    """
    data = read_json_file(config.get("state_path", "")) or {}
    state = {}
    shield = safe_float(data.get("shield_percent"))
    if shield is not None:
        state["shield"] = max(0.0, min(100.0, shield))
    else:
        # Demo: shield takes a "hit" every 12 s, then recharges
        cycle = t % 12.0
        state["shield"] = 100.0 if cycle < 8.0 else min(100.0, (cycle - 8.0) * 25.0)
    ammo = safe_float(data.get("ammo"), 32.0)
    state["ammo"] = max(0, min(999, int(ammo)))
    heading = safe_float(data.get("heading"))
    if heading is not None:
        state["heading"] = heading % 360.0
    else:
        state["heading"] = (t * 12.0) % 360.0  # Demo: slow rotation

    # Optional companion robot (see Begleitroboter-Integration.md). Only shown
    # when robot telemetry is present; absent -> HUD behaves exactly as before.
    dist = safe_float(data.get("robot_distance_m"))
    if dist is not None:
        state["robot"] = {
            "distance": max(0.0, dist),
            "bearing": (safe_float(data.get("robot_bearing"), 0.0)) % 360.0,
            "battery": safe_float(data.get("robot_battery")),
            "guard": str(data.get("robot_state", "")).lower() == "guard",
        }
    return state


def write_log(log_path, battery):
    if not log_path:
        return
    path_value = resolve_path(log_path)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    percent = battery.get("percent") if battery else ""
    voltage = battery.get("voltage") if battery else ""
    try:
        with open(path_value, "a", encoding="utf-8") as handle:
            handle.write(f"{timestamp},percent={percent},voltage={voltage}\n")
    except OSError:
        return


# --- drawing -----------------------------------------------------------

COMPASS_POINTS = {0: "N", 90: "E", 180: "S", 270: "W"}


def draw_compass(draw, heading):
    """Scrolling compass strip across the top, current heading centered."""
    draw.line((14, 10, 114, 10), fill=1)
    for deg in range(0, 360, 15):
        # Position of this tick relative to the heading, wrapped to +-180
        rel = (deg - heading + 540) % 360 - 180
        if abs(rel) > 50:
            continue
        x = 64 + int(rel)
        if 14 <= x <= 114:
            label = COMPASS_POINTS.get(deg)
            if label:
                draw.text((x - 2, 0), label, fill=1)
                draw.line((x, 7, x, 10), fill=1)
            else:
                draw.line((x, 9, x, 10), fill=1)
    # Center marker
    draw.polygon([(62, 14), (66, 14), (64, 11)], fill=1)


def draw_shield(draw, shield, t):
    draw.rectangle((10, 18, 118, 26), outline=1, fill=0)
    fill_w = int(106 * shield / 100.0)
    if fill_w > 0:
        draw.rectangle((11, 19, 11 + fill_w, 25), outline=0, fill=1)
    if shield < 100 and int(t * 4) % 2 == 0:
        draw.text((40, 28), "RECHARGE", fill=1)


def draw_motion_tracker(draw, t, robot=None):
    cx, cy, r = 24, 48, 14
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=1)
    draw.ellipse((cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2), outline=1)
    # Rotating sweep line
    angle = (t * 2.0) % (2 * math.pi)
    draw.line((cx, cy, cx + int(r * math.cos(angle)),
               cy + int(r * math.sin(angle))), fill=1)
    # Deterministic blips that drift inward (hostile contacts)
    for i in range(2):
        blip_t = (t * 0.4 + i * 0.5) % 1.0
        blip_a = (i * 2.4 + t * 0.1) % (2 * math.pi)
        dist = r * (1.0 - blip_t * 0.8)
        bx = cx + int(dist * math.cos(blip_a))
        by = cy + int(dist * math.sin(blip_a))
        draw.rectangle((bx - 1, by - 1, bx + 1, by + 1), fill=1)
    # Companion robot as a friendly hollow diamond (vs filled hostile squares).
    # Maps 0-6 m to tracker radius; low battery makes it blink.
    if robot:
        low_batt = robot.get("battery") is not None and robot["battery"] <= 20
        if not (low_batt and int(t * 2) % 2 == 0):
            rd = min(1.0, robot["distance"] / 6.0)
            ra = math.radians(robot["bearing"])
            kx = cx + int(r * rd * math.sin(ra))
            ky = cy - int(r * rd * math.cos(ra))
            draw.polygon([(kx, ky - 2), (kx + 2, ky), (kx, ky + 2), (kx - 2, ky)],
                         outline=1, fill=0)
            if robot.get("guard"):  # guard mode: center dot
                draw.point((kx, ky), fill=1)


def draw_ammo(draw, ammo):
    draw.text((92, 38), "AMMO", fill=1)
    draw.text((92, 48), f"{ammo:02d}", fill=1)


def draw_battery(draw, battery, low_threshold, t):
    if not battery:
        return
    text = None
    percent = safe_float(battery.get("percent"))
    if percent is not None:
        percent = max(0.0, min(100.0, percent))  # clamp away "B150%"/"B-10%"
        text = f"B{percent:.0f}%"
    else:
        voltage = safe_float(battery.get("voltage"))
        if voltage is not None:
            text = f"{voltage:.2f}V"
    if text is None:
        return
    if percent is not None and percent <= low_threshold:
        if int(t * 2) % 2 == 0:  # flash
            draw.rectangle((44, 38, 86, 48), outline=1)
            draw.text((48, 40), "AKKU!", fill=1)
    # default font is ~8 px tall; y=54 keeps the glyph within the 64 px height
    draw.text((48, 54), text, fill=1)


def draw_hud(t, battery, state, config):
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    draw_compass(draw, state["heading"])
    draw_shield(draw, state["shield"], t)
    draw_motion_tracker(draw, t, state.get("robot"))
    draw_ammo(draw, state["ammo"])
    if config.get("show_battery"):
        draw_battery(draw, battery, config.get("low_battery_percent", 20), t)
    return image


def draw_boot_frame(progress):
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    draw.text((28, 14), "MJOLNIR MARK VI", fill=1)
    draw.text((34, 26), "UNSC BOOT v6.1", fill=1)
    draw.rectangle((14, 42, 114, 50), outline=1)
    fill_w = int(98 * progress)
    if fill_w > 0:
        draw.rectangle((15, 43, 15 + fill_w, 49), fill=1)
    return image


# --- main loops --------------------------------------------------------

def run_selftest(out_path):
    """Render boot + HUD frames as PNGs, no display hardware needed."""
    base, ext = os.path.splitext(out_path)
    draw_boot_frame(0.7).convert("L").save(f"{base}_boot{ext}")
    for i, t in enumerate((0.0, 9.0)):  # full shield / recharge moment
        state = read_state(CONFIG, t)
        battery = {"percent": 78, "voltage": 7.4}
        frame = draw_hud(t, battery, state, dict(CONFIG, show_battery=True))
        frame.convert("L").save(f"{base}_{i}{ext}")
    print(f"Selftest-Frames gespeichert: {base}_boot{ext}, {base}_0{ext}, {base}_1{ext}")


def main():
    parser = argparse.ArgumentParser(description="Halo HUD fuer transparentes OLED")
    parser.add_argument("--selftest", metavar="PNG",
                        help="rendert Testframes als PNG statt aufs Display")
    args = parser.parse_args()

    if args.selftest:
        run_selftest(args.selftest)
        return

    # Import only when real hardware is used, so --selftest runs anywhere
    from luma.core.interface.serial import i2c
    from luma.oled.device import ssd1309

    serial = i2c(port=CONFIG["i2c_port"], address=CONFIG["i2c_address"])
    device = ssd1309(serial, width=WIDTH, height=HEIGHT)

    start = time.time()
    if CONFIG.get("boot_animation", True):
        boot_duration = 2.5
        while time.time() - start < boot_duration:
            device.display(draw_boot_frame((time.time() - start) / boot_duration))
            time.sleep(0.05)

    refresh = max(10, int(CONFIG.get("refresh_ms", 100))) / 1000.0
    log_interval = max(1, int(CONFIG.get("log_interval_s", 5)))
    last_log = 0.0
    while True:
        t = time.time() - start
        battery = read_battery(CONFIG)
        state = read_state(CONFIG, t)
        device.display(draw_hud(t, battery, state, CONFIG))
        now = time.time()
        if CONFIG.get("log_path") and now - last_log >= log_interval:
            write_log(CONFIG.get("log_path"), battery)
            last_log = now
        time.sleep(refresh)


if __name__ == "__main__":
    main()
