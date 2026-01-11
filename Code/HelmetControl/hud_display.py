#!/usr/bin/env python3
"""Simple Halo-style HUD demo for a transparent OLED."""

import time
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1309
from PIL import Image, ImageDraw

I2C_PORT = 1
I2C_ADDRESS = 0x3C
WIDTH = 128
HEIGHT = 64

serial = i2c(port=I2C_PORT, address=I2C_ADDRESS)
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
    while True:
        draw_hud()
        time.sleep(0.1)


if __name__ == "__main__":
    main()
