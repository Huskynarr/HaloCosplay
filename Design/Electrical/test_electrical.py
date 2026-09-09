"""Topologie-/Regressionspruefungen; absichtlich keine Hardware-Freigabe."""
import copy
import importlib.util
import itertools
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

PATH = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("halo_electrical_generator", PATH / "generate.py")
g = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(g)


class ElectricalTopologyTests(unittest.TestCase):
    def setUp(self):
        self.d = g.design()

    def test_reference_design_and_export_consistent(self):
        self.assertTrue(g.validate(self.d))
        self.assertTrue(g.validate(json.loads(g.outputs()["Netlist.json"])))

    def corrupt(self, ref, pin, net):
        d = copy.deepcopy(self.d)
        g.index(d)[ref]["pins"][str(pin)] = net
        with self.assertRaises(ValueError):
            g.validate(d)

    def test_led_return_must_not_be_grounded(self):
        for channel in self.d["channels"]:
            with self.subTest(channel=channel["id"]):
                self.corrupt(channel["driver"], 5, "E_GND")

    def test_wrong_led_polarity_or_crossed_color_rejected(self):
        self.corrupt("LED_HL_R", "A", "LED_H_R_MID")
        self.corrupt("LED_NR_B", "K", "LED_N_G_RET")
        self.corrupt("JHL", 2, "E_GND")

    def test_positive_feed_short_and_bypass_rejected(self):
        self.corrupt("J10", 1, "C_GND")
        self.corrupt("F20", 2, "E15_RAW")
        self.corrupt("S20", 2, "E15_FUSED")
        self.corrupt("K20", 3, "E15_SW")

    def test_domains_and_fan_voltage_remain_separate(self):
        self.corrupt("J11", 2, "E15_LED")
        self.corrupt("J10", 2, "E_GND")
        self.corrupt("U20", "VOUT", "C5_FAN")

    def test_reset_pulldowns_and_coil_diode_polarity(self):
        self.corrupt("R21", 2, "E5_CTRL")
        self.corrupt("R30", 2, "E5_CTRL")
        self.corrupt("Q20", 2, "COIL_LOW")
        self.corrupt("D20", "K", "COIL_LOW")

    def test_stationary_reset_and_disconnect_off_truth_table(self):
        for manual, fivev, connected, ready, thermal, pwm in itertools.product((False, True), repeat=6):
            state = g.steady_state(manual_on=manual, effects_5v_valid=fivev,
                controller_connected=connected, ready=ready,
                thermal_contact_closed=thermal, pwm=pwm)
            if not connected or not ready or not thermal or not fivev or not manual:
                self.assertFalse(state["led_on"])
                self.assertFalse(state["relay_energized"])
            self.assertTrue(state["comfort_fans_on"])
        self.assertTrue(g.steady_state(manual_on=True, effects_5v_valid=True,
            controller_connected=True, ready=True, thermal_contact_closed=True,
            pwm=True)["led_on"])

    def test_netlist_cache_mismatch_rejected(self):
        exported = json.loads(g.outputs()["Netlist.json"])
        exported["nets"]["E_GND"] = []
        with self.assertRaises(ValueError):
            g.validate(exported)

    def test_svg_pin_tags_match_netlist_and_five_sheets_parse(self):
        c = g.index(self.d)
        generated = g.outputs()
        svg_names = [name for name in generated if name.endswith(".svg")]
        self.assertEqual(len(svg_names), 5)
        for name in svg_names:
            root = ET.fromstring(generated[name])
            pins = [el for el in root.iter() if "data-pin" in el.attrib]
            self.assertGreater(len(pins), 5)
            for pin in pins:
                attr = pin.attrib
                self.assertEqual(attr["data-net"], c[attr["data-ref"]]["pins"][attr["data-pin"]] or "NC")

    def test_generated_files_are_current_and_ascii(self):
        for name, text in g.outputs().items():
            text.encode("ascii")
            self.assertEqual((PATH / name).read_text(encoding="utf-8"), text, name)


if __name__ == "__main__":
    unittest.main()
