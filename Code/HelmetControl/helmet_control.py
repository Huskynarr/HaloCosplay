#!/usr/bin/env python3
"""Pi-side controller for the helmet Arduino (HelmetMultiEffects.ino).

The Arduino listens as I2C slave (default address 0x08) and understands:
    0x01 <0-255>  visor brightness
    0x02 <0-255>  fan speed (PWM)
    0x03 <0-4>    effect select

Usage examples:
    python3 helmet_control.py brightness 128
    python3 helmet_control.py fan 180
    python3 helmet_control.py effect heartbeat
    python3 helmet_control.py effect 3
    python3 helmet_control.py demo

Wiring and protocol: see Code/README.md and
Documentation/Guides/Elektronik-Verdrahtung.md.
"""

import argparse
import sys
import time

CMD_BRIGHTNESS = 0x01
CMD_FAN = 0x02
CMD_EFFECT = 0x03

# Must match the mode order in HelmetMultiEffects.ino
EFFECTS = {
    "static": 0,
    "breathing": 1,
    "heartbeat": 2,
    "chase": 3,
    "flicker": 4,
}


def open_bus(bus_num):
    try:
        from smbus2 import SMBus
    except ImportError:
        sys.exit("smbus2 fehlt: pip install -r requirements.txt")
    try:
        return SMBus(bus_num)
    except OSError as exc:
        sys.exit(f"I2C-Bus {bus_num} nicht verfuegbar ({exc}). "
                 "I2C aktiviert? (sudo raspi-config -> Interface Options)")


def send(bus, addr, cmd, value, retries=3):
    for attempt in range(retries):
        try:
            bus.write_i2c_block_data(addr, cmd, [value & 0xFF])
            return
        except OSError as exc:
            if attempt == retries - 1:
                sys.exit(f"Arduino auf 0x{addr:02X} antwortet nicht ({exc}). "
                         "Verkabelung SDA/SCL/GND pruefen, i2cdetect -y 1")
            time.sleep(0.05)


def parse_effect(value):
    if value.lower() in EFFECTS:
        return EFFECTS[value.lower()]
    try:
        num = int(value)
    except ValueError:
        sys.exit(f"Unbekannter Effekt '{value}'. "
                 f"Namen: {', '.join(EFFECTS)} oder Nummer 0-4.")
    if not 0 <= num <= max(EFFECTS.values()):
        sys.exit("Effekt-Nummer muss 0-4 sein.")
    return num


def parse_byte(value, what):
    try:
        num = int(value)
    except ValueError:
        sys.exit(f"{what} muss eine Zahl 0-255 sein.")
    if not 0 <= num <= 255:
        sys.exit(f"{what} muss 0-255 sein.")
    return num


def run_demo(bus, addr):
    """Cycle through all effects, then settle on breathing."""
    print("Demo: alle Effekte durchschalten (Ctrl+C zum Abbrechen)")
    send(bus, addr, CMD_BRIGHTNESS, 160)
    for name, num in EFFECTS.items():
        print(f"  Effekt {num}: {name}")
        send(bus, addr, CMD_EFFECT, num)
        time.sleep(5)
    print("  zurueck zu: breathing")
    send(bus, addr, CMD_EFFECT, EFFECTS["breathing"])


def main():
    parser = argparse.ArgumentParser(
        description="Steuert den Helm-Arduino (HelmetMultiEffects.ino) per I2C.")
    parser.add_argument("--bus", type=int, default=1,
                        help="I2C-Busnummer (Standard: 1)")
    parser.add_argument("--addr", type=lambda v: int(v, 0), default=0x08,
                        help="I2C-Adresse des Arduinos (Standard: 0x08)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_bright = sub.add_parser("brightness", help="Visor-Helligkeit 0-255")
    p_bright.add_argument("value")
    p_fan = sub.add_parser("fan", help="Luefter-Speed 0-255")
    p_fan.add_argument("value")
    p_effect = sub.add_parser("effect",
                              help="Effekt: " + ", ".join(EFFECTS) + " oder 0-4")
    p_effect.add_argument("value")
    sub.add_parser("demo", help="Alle Effekte nacheinander vorfuehren")

    args = parser.parse_args()

    # Werte VOR dem Bus-Open validieren (Fehlermeldung auch ohne Hardware)
    action = None
    if args.command == "brightness":
        action = (CMD_BRIGHTNESS, parse_byte(args.value, "Helligkeit"))
    elif args.command == "fan":
        action = (CMD_FAN, parse_byte(args.value, "Luefter-Speed"))
    elif args.command == "effect":
        action = (CMD_EFFECT, parse_effect(args.value))

    bus = open_bus(args.bus)
    try:
        if action:
            send(bus, args.addr, action[0], action[1])
        else:
            run_demo(bus, args.addr)
    finally:
        bus.close()


if __name__ == "__main__":
    main()
