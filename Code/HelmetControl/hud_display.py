#!/usr/bin/env python3
"""Halo-style HUD for a transparent OLED (SSD1309, 128x64).

Features:
  - boot sequence (MJOLNIR startup)
  - animated shield bar with recharge effect
  - scrolling compass (N/E/S/W) driven by live heading or demo rotation
  - motion tracker with sweep and blips
  - ammo counter, battery readout with low-battery flash
  - hydration reminder banner (blinking, driven by "hydration_due" flag)

Live values (all optional) are read from JSON files so other modules can
feed the HUD without coupling (see V3-Systemarchitektur.md):
  - battery_path: {"battery_percent": 78, "voltage": 7.4}
  - state_path:   {"shield_percent": 80, "ammo": 27, "heading": 123}
                  plus optional "vision_contacts"/"vision_ts" from vision_bridge.py
Missing files simply fall back to a self-running demo animation.

Hardware-free test (renders PNG frames instead of driving the OLED):
    python3 hud_display.py --selftest hud_test.png
"""

import argparse
import json
import math
import os
import sys
import time

from PIL import Image, ImageDraw

import hud_state

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
    # Akkuwerte aelter als dieser Wert gelten als unbekannt ("AKKU ?").
    # 0 schaltet die Pruefung ab (z.B. fuer eine von Hand gepflegte Datei).
    "battery_max_age_s": 30,
    "boot_animation": True,
    "log_path": "",
    "log_interval_s": 5,
    # Ab dieser Groesse wird das Log nach <name>.1 verschoben (eine Generation),
    # damit es die SD-Karte nicht fuellt. 0 = unbegrenzt.
    "log_max_kb": 512,
}


CONFIG_WARNING = ""   # set when config.json was unusable; shown on the HUD


def load_config(config_path=None):
    """Read config.json; a broken file must not stop the HUD from starting.

    Invalid JSON or wrong types fall back to DEFAULTS per key and set
    CONFIG_WARNING so the wearer sees "CFG?" instead of a crash loop.
    """
    global CONFIG_WARNING
    CONFIG_WARNING = ""
    config = DEFAULTS.copy()
    config_path = config_path or os.path.join(BASE_DIR, "config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
            if not isinstance(data, dict):
                raise ValueError("config.json muss ein JSON-Objekt sein")
            config.update(data)
        except (OSError, ValueError) as exc:
            CONFIG_WARNING = f"config.json unbrauchbar, nutze Standardwerte: {exc}"
    try:
        if isinstance(config.get("i2c_address"), str):
            config["i2c_address"] = int(config["i2c_address"], 0)
        for key in ("i2c_port", "i2c_address", "width", "height"):
            config[key] = int(config[key])
        if config["width"] <= 0 or config["height"] <= 0:
            raise ValueError("width/height muessen positiv sein")
    except (TypeError, ValueError) as exc:
        CONFIG_WARNING = f"config.json: ungueltiger Wert, nutze Standardwerte: {exc}"
        for key in ("i2c_port", "i2c_address", "width", "height"):
            config[key] = DEFAULTS[key]
    if CONFIG_WARNING:
        print("hud_display: " + CONFIG_WARNING, file=sys.stderr, flush=True)
    return config


CONFIG = load_config()
WIDTH = CONFIG["width"]
HEIGHT = CONFIG["height"]


def resolve_path(path_value):
    """Relative runtime files follow HUD_STATE_DIR (see hud_state.runtime_path)."""
    if not path_value:
        return ""
    if os.path.isabs(path_value):
        return path_value
    if os.path.basename(path_value) == path_value and path_value.endswith(".json"):
        return hud_state.runtime_path(path_value)
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
        data = json.loads(raw) if raw.startswith("{") else {"value": float(raw)}
        return data if isinstance(data, dict) else None
    except (OSError, ValueError, json.JSONDecodeError):
        return None


def read_battery(config, now=None):
    """Battery reading, or {"stale": True} when the source stopped updating.

    A dead SensorFeeder/bridge must not leave the last percentage on screen
    forever: data older than battery_max_age_s is reported as unknown. Age is
    the file mtime, or a "ts"/"timestamp" field (epoch seconds) if present.
    """
    path_value = resolve_path(config.get("battery_path", ""))
    data = read_json_file(path_value)
    if data is None:
        return None
    max_age = safe_float(config.get("battery_max_age_s"), 30.0)
    if max_age > 0:
        stamp = safe_float(data.get("ts"), safe_float(data.get("timestamp")))
        if stamp is None:
            try:
                stamp = os.path.getmtime(path_value)
            except OSError:
                stamp = None
        now = time.time() if now is None else now
        if stamp is None or now - stamp > max_age:
            return {"percent": None, "voltage": None, "stale": True}
    if "value" in data:
        return {"percent": data["value"], "voltage": None}
    return {
        "percent": data.get(config.get("battery_field", "battery_percent")),
        "voltage": data.get(config.get("voltage_field", "voltage")),
    }


def safe_float(value, default=None):
    """Parse value to a finite float; tolerate None, strings, junk, NaN, inf.

    json.load accepts NaN/Infinity and "1e999" parses to inf; both would
    raise later in int()/modulo and kill the HUD loop, so they count as junk.
    """
    if value is None or isinstance(value, bool):
        return default
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError):
        return default
    return number if math.isfinite(number) else default


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

    # Optional real contacts from vision_bridge.py (AI Camera). Only used while
    # fresh: if the camera stalls, the tracker falls back to the demo blips
    # instead of showing frozen contacts.
    vision_ts = safe_float(data.get("vision_ts"))
    contacts = data.get("vision_contacts")
    if vision_ts is not None and isinstance(contacts, list) and time.time() - vision_ts < 2.0:
        state["contacts"] = []
        for c in contacts[:6]:
            if not isinstance(c, dict):
                continue
            bearing = safe_float(c.get("bearing"))
            dist = safe_float(c.get("distance"))
            if bearing is None or dist is None:
                continue
            state["contacts"].append((bearing % 360.0, max(0.0, min(1.0, dist))))

    # Trink-Erinnerung (voice_control.py): Flag -> blinkendes Banner
    if data.get("hydration_due"):
        state["hydration_due"] = True
    return state


def write_log(log_path, battery, max_kb=512):
    if not log_path:
        return
    path_value = resolve_path(log_path)
    try:
        if max_kb and max_kb > 0 and os.path.getsize(path_value) > max_kb * 1024:
            os.replace(path_value, path_value + ".1")
    except OSError:
        pass  # no log yet, or not movable: keep appending
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


def draw_motion_tracker(draw, t, robot=None, contacts=None):
    cx, cy, r = 24, 48, 14
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=1)
    draw.ellipse((cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2), outline=1)
    # Rotating sweep line
    angle = (t * 2.0) % (2 * math.pi)
    draw.line((cx, cy, cx + int(r * math.cos(angle)),
               cy + int(r * math.sin(angle))), fill=1)
    if contacts is not None:
        # Real contacts (vision_bridge.py): bearing 0 = straight ahead = up
        for bearing, rel_dist in contacts:
            ca = math.radians(bearing)
            bx = cx + int(r * rel_dist * math.sin(ca))
            by = cy - int(r * rel_dist * math.cos(ca))
            draw.rectangle((bx - 1, by - 1, bx + 1, by + 1), fill=1)
    else:
        # Deterministic blips that drift inward (hostile contacts, demo)
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


def draw_battery(draw, battery, low_threshold, t, show_value=True):
    """Battery warnings are always drawn; the plain readout only if enabled.

    "AKKU!" (low) and "AKKU ?" (reading stale/unknown) are safety information
    and must not disappear because show_battery is off.
    """
    if not battery:
        return
    if battery.get("stale"):
        draw.rectangle((44, 38, 86, 48), outline=1, fill=0)
        draw.text((47, 40), "AKKU ?", fill=1)
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
    low = safe_float(low_threshold, 20.0)
    if percent is not None and percent <= low:
        if int(t * 2) % 2 == 0:  # flash
            draw.rectangle((44, 38, 86, 48), outline=1, fill=0)
            draw.text((48, 40), "AKKU!", fill=1)
    if show_value:
        # default font is ~8 px tall; y=54 keeps the glyph within the 64 px height
        draw.text((48, 54), text, fill=1)


def draw_hydration_banner(draw, t):
    """Blinkendes Banner ueber dem HUD, solange hydration_due gesetzt ist."""
    if int(t * 2) % 2 == 0:
        draw.rectangle((10, 30, 118, 46), outline=1, fill=0)
        draw.text((38, 34), "TRINKEN!", fill=1)


def draw_hud(t, battery, state, config):
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    draw_compass(draw, state["heading"])
    draw_shield(draw, state["shield"], t)
    draw_motion_tracker(draw, t, state.get("robot"), state.get("contacts"))
    draw_ammo(draw, state["ammo"])
    draw_battery(draw, battery, config.get("low_battery_percent", 20), t,
                 show_value=bool(config.get("show_battery")))
    if state.get("hydration_due"):
        draw_hydration_banner(draw, t)
    if CONFIG_WARNING:
        draw.text((100, 28), "CFG?", fill=1)
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
    state_h = read_state(CONFIG, 0.0)
    state_h["hydration_due"] = True
    frame = draw_hud(0.0, battery, state_h, dict(CONFIG, show_battery=True))
    frame.convert("L").save(f"{base}_2{ext}")
    banner = Image.open(f"{base}_2{ext}").convert("L")
    ok_banner = banner.getpixel((10, 30)) == 255   # Outline des Banners
    print(f"  [{'ok' if ok_banner else 'FEHLER'}] Hydration-Banner gerendert")
    if not ok_banner:
        sys.exit("Selftest fehlgeschlagen: Hydration-Banner fehlt")
    print(f"Selftest-Frames gespeichert: {base}_boot{ext}, {base}_0{ext}, {base}_1{ext}, {base}_2{ext}")
    run_robustness_selftest()


def run_robustness_selftest():
    """Bad inputs must degrade per field, never raise (no hardware needed)."""
    import tempfile
    global CONFIG_WARNING
    failures = []

    def check(name, ok):
        print(f"  [{'ok' if ok else 'FEHLER'}] {name}")
        if not ok:
            failures.append(name)

    with tempfile.TemporaryDirectory() as tmp:
        state_path = os.path.join(tmp, "hud_state.json")
        battery_path = os.path.join(tmp, "battery.json")
        cfg = dict(CONFIG, state_path=state_path, battery_path=battery_path, show_battery=False)
        # json.loads accepts NaN/Infinity; "1e999" becomes inf
        with open(state_path, "w", encoding="utf-8") as handle:
            handle.write('{"heading": NaN, "ammo": 1e999, "shield_percent": "1e999",'
                         ' "robot_distance_m": 2, "robot_bearing": NaN, "robot_battery": Infinity,'
                         ' "vision_ts": %r, "vision_contacts": [{"bearing": NaN, "distance": 0.5},'
                         ' {"bearing": 1e999, "distance": 1}, {"bearing": 30, "distance": 0.4}]}'
                         % time.time())
        try:
            state = read_state(cfg, 3.0)
            draw_hud(3.0, None, state, cfg)
            ok = (math.isfinite(state["heading"]) and state["ammo"] == 32
                  and state["contacts"] == [(30.0, 0.4)] and state["robot"]["bearing"] == 0.0)
        except Exception as exc:  # the point of the test: nothing may escape
            print(f"      {type(exc).__name__}: {exc}")
            ok = False
        check("NaN/inf in hud_state.json faellt pro Feld zurueck", ok)

        with open(battery_path, "w", encoding="utf-8") as handle:
            json.dump({"battery_percent": 12, "voltage": 6.5}, handle)
        fresh = read_battery(cfg)
        frame = draw_hud(0.0, fresh, read_state(cfg, 0.0), cfg).convert("L")
        check("Akku-Warnung auch ohne show_battery",
              fresh.get("percent") == 12 and frame.getpixel((44, 38)) == 255)
        stale = read_battery(cfg, now=time.time() + 120)
        frame = draw_hud(0.5, stale, read_state(cfg, 0.5), cfg).convert("L")
        check("Veralteter Akkustand wird als AKKU ? gezeigt",
              stale == {"percent": None, "voltage": None, "stale": True}
              and frame.getpixel((44, 38)) == 255)
        check("battery_max_age_s=0 schaltet die Alterspruefung ab",
              read_battery(dict(cfg, battery_max_age_s=0), now=time.time() + 1e6).get("percent") == 12)
        with open(battery_path, "w", encoding="utf-8") as handle:
            handle.write('{"battery_percent": NaN}')
        draw_hud(0.0, read_battery(cfg), read_state(cfg, 0.0), cfg)
        check("NaN im Akkustand zeichnet ohne Fehler", True)

        bad_config = os.path.join(tmp, "config.json")
        for raw in ("{kaputt", '["liste"]', '{"width": "breit", "i2c_address": "zz"}'):
            with open(bad_config, "w", encoding="utf-8") as handle:
                handle.write(raw)
            try:
                loaded = load_config(bad_config)
                ok = (bool(CONFIG_WARNING) and loaded["width"] == DEFAULTS["width"]
                      and loaded["i2c_address"] == DEFAULTS["i2c_address"])
            except Exception as exc:
                print(f"      {type(exc).__name__}: {exc}")
                ok = False
            check(f"Kaputte config.json ({raw[:10]}) -> Standardwerte + Warnung", ok)
        frame = draw_hud(0.0, None, read_state(cfg, 0.0), cfg).convert("L")
        check("CFG?-Hinweis sichtbar", any(frame.getpixel((x, y)) for x in range(100, 124) for y in range(28, 38)))
        CONFIG_WARNING = ""
        log_path = os.path.join(tmp, "hud_log.txt")
        for _ in range(60):
            write_log(log_path, {"percent": 50, "voltage": 3.9}, max_kb=1)
        check("Log wird ab log_max_kb rotiert",
              os.path.exists(log_path + ".1") and os.path.getsize(log_path) <= 2048)
    if failures:
        sys.exit("Selftest fehlgeschlagen: " + ", ".join(failures))


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

    def open_device():
        serial = i2c(port=CONFIG["i2c_port"], address=CONFIG["i2c_address"])
        return ssd1309(serial, width=WIDTH, height=HEIGHT)

    # A missing display at boot still exits (systemd restarts us); a glitch
    # while running is handled in the loop below without losing the process.
    device = open_device()

    start = time.time()
    if CONFIG.get("boot_animation", True):
        boot_duration = 2.5
        try:
            while time.time() - start < boot_duration:
                device.display(draw_boot_frame((time.time() - start) / boot_duration))
                time.sleep(0.05)
        except Exception as exc:  # boot animation is cosmetic
            print(f"hud_display: Boot-Animation abgebrochen: {exc}", file=sys.stderr, flush=True)

    refresh = max(10.0, safe_float(CONFIG.get("refresh_ms"), 100.0)) / 1000.0
    log_interval = max(1.0, safe_float(CONFIG.get("log_interval_s"), 5.0))
    last_log = 0.0
    failures = 0          # consecutive bad frames
    last_report = 0.0     # rate limit for the error line
    while True:
        frame_start = time.time()
        t = frame_start - start
        battery = None
        try:
            battery = read_battery(CONFIG)
            state = read_state(CONFIG, t)
            device.display(draw_hud(t, battery, state, CONFIG))
            failures = 0
        except Exception as exc:
            # One bad value or one I2C glitch costs a frame, not the HUD.
            failures += 1
            now = time.time()
            if now - last_report >= 5.0:
                print(f"hud_display: Frame uebersprungen ({failures}x in Folge): "
                      f"{type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
                last_report = now
            if failures >= 5:
                # Display probably lost its bus: back off and reopen it.
                time.sleep(min(5.0, 0.5 * (failures - 4)))
                try:
                    device = open_device()
                except Exception:
                    pass  # still gone; keep trying with the capped backoff
        now = time.time()
        if CONFIG.get("log_path") and now - last_log >= log_interval:
            write_log(CONFIG.get("log_path"), battery, safe_float(CONFIG.get("log_max_kb"), 512.0))
            last_log = now
        # refresh_ms is the frame period, not a pause on top of render + I2C time.
        time.sleep(max(0.005, refresh - (time.time() - frame_start)))


if __name__ == "__main__":
    main()
