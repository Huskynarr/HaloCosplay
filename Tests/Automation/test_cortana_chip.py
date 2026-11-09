#!/usr/bin/env python3
"""Tests fuer das Cortana-Chip-Modul: Dateien, JSON, Geometrie-Marker."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHIP = ROOT / 'Design/Props/CortanaChip'
FIRMWARE = ROOT / 'Code/CortanaChip/cortana_chip.ino'
WEBAPP = ROOT / 'web/cortana/index.html'


class TestCortanaChip(unittest.TestCase):
    def test_stl_files_exist_and_nonempty(self):
        for name in ('cortana-assembly.stl', 'cortana-back.stl',
                     'cortana-frame.stl', 'cortana-front.stl'):
            path = CHIP / 'STL' / name
            self.assertTrue(path.exists(), 'Fehlt: ' + name)
            self.assertGreater(path.stat().st_size, 1000, 'Zu klein: ' + name)

    def test_scad_has_electronics_cutouts(self):
        scad = (CHIP / 'CortanaChip.scad').read_text()
        for marker in ('esp_w', 'st60_w', 'antenna_free', 'usb_w', 'strap_slot'):
            self.assertIn(marker, scad, 'SCAD fehlt Marker: ' + marker)

    def test_firmware_has_ble_and_display(self):
        fw = FIRMWARE.read_text()
        for marker in ('BLEDevice', 'SSD1306', 'LittleFS',
                       'SERVICE_UUID', 'CHAR_DATA_UUID'):
            self.assertIn(marker, fw, 'Firmware fehlt Marker: ' + marker)

    def test_character_json_valid(self):
        for name in ('cortana_v1.json', 'husky_v1.json'):
            data = json.loads((ROOT / 'Code/CortanaChip/characters' / name).read_text())
            for key in ('id', 'name', 'status', 'shield', 'energy', 'mode'):
                self.assertIn(key, data, name + ' fehlt Feld: ' + key)
            self.assertIsInstance(data['shield'], int)
            self.assertIsInstance(data['energy'], int)

    def test_webapp_has_web_ble(self):
        html = WEBAPP.read_text()
        for marker in ('navigator.bluetooth', SERVICE_UUID_MARKER,
                       CHAR_DATA_UUID_MARKER):
            self.assertIn(marker, html, 'Web-App fehlt Marker: ' + marker)

    def test_uuids_match_between_firmware_and_webapp(self):
        fw = FIRMWARE.read_text()
        html = WEBAPP.read_text()
        fw_uuids = set(re.findall(r'"([0-9a-f-]{36})"', fw))
        html_uuids = set(re.findall(r'"([0-9a-f-]{36})"', html))
        self.assertTrue(fw_uuids & html_uuids,
                        'Firmware und Web-App teilen keine UUID')


SERVICE_UUID_MARKER = '4fafc201-1fb5-459e-8fcc-c5c9c331914b'
CHAR_DATA_UUID_MARKER = 'beb5483f-36e1-4688-b7f5-ea07361b26a8'

if __name__ == '__main__':
    unittest.main()
