#!/usr/bin/env python3
"""Simple Halo-style HUD demo for a transparent OLED."""

import json
import os
import time
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1309
from PIL import Image, ImageDraw

DEFAULTS = {
    "i2c_port": 1,
    "i2c_address": 0x3C,
    "width": 128,
    "height": 64,
    "refresh_ms": 100,
}


def load_config():
    config = DEFAULTS.copy()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "config.json")
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


def draw_hud():
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    # Shield bar
    draw.rectangle((10, 5, 118, 15), outline=1, fill=0)
    draw.rectangle((12, 7, 90, 13), outline=0, fill=1)

    # Ammo count
    draw.text((90, 50), "32", fill=1)

    # Compass tick
    draw.line((64, 2, 64, 10), fill=1)

    # Motion tracker
    draw.ellipse((100, 40, 120, 60), outline=1)

    device.display(image)


def main():
    refresh = max(10, int(CONFIG.get("refresh_ms", 100))) / 1000.0
    while True:
        draw_hud()
        time.sleep(refresh)


if __name__ == "__main__":
    main()
