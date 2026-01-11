#!/usr/bin/env python3
"""Simple Halo-style HUD demo for a transparent OLED."""

import json
import os
import time
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1309
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

serial = i2c(port=CONFIG["i2c_port"], address=CONFIG["i2c_address"])
device = ssd1309(serial, width=WIDTH, height=HEIGHT)

def resolve_path(path_value):
    if not path_value:
        return ""
    if os.path.isabs(path_value):
        return path_value
    return os.path.join(BASE_DIR, path_value)


def read_battery(config):
    path_value = resolve_path(config.get("battery_path", ""))
    if not path_value or not os.path.exists(path_value):
        return None
    try:
        with open(path_value, "r", encoding="utf-8") as handle:
            raw = handle.read().strip()
        if not raw:
            return None
        if raw.startswith("{"):
            data = json.loads(raw)
            percent = data.get(config.get("battery_field", "battery_percent"))
            voltage = data.get(config.get("voltage_field", "voltage"))
        else:
            percent = float(raw)
            voltage = None
        return {"percent": percent, "voltage": voltage}
    except (OSError, ValueError, json.JSONDecodeError):
        return None


def write_log(log_path, battery):
    if not log_path:
        return
    path_value = resolve_path(log_path)
    if not path_value:
        return
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    percent = battery.get("percent") if battery else ""
    voltage = battery.get("voltage") if battery else ""
    line = f"{timestamp},percent={percent},voltage={voltage}\n"
    try:
        with open(path_value, "a", encoding="utf-8") as handle:
            handle.write(line)
    except OSError:
        return


def draw_hud(battery=None):
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    # Shield bar
    draw.rectangle((10, 5, 118, 15), outline=1, fill=0)
    draw.rectangle((12, 7, 90, 13), outline=0, fill=1)

    # Ammo count
    draw.text((90, 50), "32", fill=1)

    if CONFIG.get("show_battery") and battery:
        text = None
        if battery.get("percent") is not None:
            try:
                text = f"B{float(battery['percent']):.0f}%"
            except (ValueError, TypeError):
                text = None
        if text is None and battery.get("voltage") is not None:
            try:
                text = f"{float(battery['voltage']):.2f}V"
            except (ValueError, TypeError):
                text = None
        if text:
            draw.text((2, 50), text, fill=1)

    # Compass tick
    draw.line((64, 2, 64, 10), fill=1)

    # Motion tracker
    draw.ellipse((100, 40, 120, 60), outline=1)

    device.display(image)


def main():
    refresh = max(10, int(CONFIG.get("refresh_ms", 100))) / 1000.0
    log_interval = max(1, int(CONFIG.get("log_interval_s", 5)))
    last_log = 0.0
    while True:
        battery = read_battery(CONFIG)
        draw_hud(battery)
        now = time.time()
        if CONFIG.get("log_path") and now - last_log >= log_interval:
            write_log(CONFIG.get("log_path"), battery)
            last_log = now
        time.sleep(refresh)


if __name__ == "__main__":
    main()
