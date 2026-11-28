import json
import math
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import suit_loads as loads


class LoadEstimateTests(unittest.TestCase):
    def setUp(self):
        self.parameters = loads.scad_parameters(loads.PARAMETERS.read_text(encoding="ascii"))
        self.case = json.loads(loads.LOAD_CASE.read_text(encoding="utf-8"))
        checks, self.info, self.lugs = loads.estimate(self.parameters, self.case)
        self.checks = {check["id"]: check for check in checks}

    def test_hand_calculations(self):
        torque = 22000.0  # Nmm
        # Arm 6 x 30 mm: sigma = 6 M / (t w^2)
        self.assertAlmostEqual(self.checks["E01"]["stress_mpa"], 6 * torque / (6 * 30 ** 2), places=1)
        # Thin-walled square tube 30 x 2: tau = T / (2 A t) with A = 28^2
        self.assertAlmostEqual(self.checks["E13"]["stress_mpa"], torque / (2 * 28 ** 2 * 2), places=1)
        # Six M4 on a 28 mm circle
        self.assertAlmostEqual(self.checks["E05"]["stress_mpa"], torque / (6 * 14) / 8.78, places=1)
        # Utilisation: stress times safety factor over yield, shear at 0.58 of it
        self.assertAlmostEqual(self.checks["E01"]["utilisation"]["EN AW-6061-T6"], 24.4 * 3 / 240, places=2)
        self.assertAlmostEqual(self.checks["E13"]["utilisation"]["S235"], 7.0 * 3 / (0.58 * 235), places=2)
        twist = {row["material"]: row["value"] for row in self.info if row["id"] == "I01"}
        self.assertAlmostEqual(twist["EN AW-6061-T6"], math.degrees(torque * 380 / (26000 * 28 ** 3 * 2)), places=2)

    def test_tube_is_far_stiffer_than_a_flat_bar_and_print_fails_everywhere(self):
        by = {(row["id"], row["material"]): row["value"] for row in self.info}
        for material in self.case["materials"]:
            self.assertGreater(by[("I02", material)], 10 * by[("I01", material)])
        printed = [name for name in self.case["materials"] if name.startswith("PETG")][0]
        section = [check for check in self.checks.values() if not check["bolt"]]
        self.assertTrue(all(check["utilisation"][printed] > 1 for check in section))
        self.assertTrue(all(check["utilisation"]["EN AW-6061-T6"] < 1 for check in section))
        self.assertTrue(all(check["utilisation"]["Schraube 8.8"] < 1 for check in self.checks.values() if check["bolt"]))

    def test_load_scales_and_committed_outputs_are_current(self):
        doubled = dict(self.case, peak_torque_nm=44.0)
        checks, _, _ = loads.estimate(self.parameters, doubled)
        self.assertAlmostEqual(checks[0]["stress_mpa"], 2 * self.checks["E01"]["stress_mpa"], places=0)
        self.assertEqual(loads.main(["--check"]), 0)
        text = loads.OUT_MD.read_text(encoding="utf-8")
        self.assertIn("ROUGH_ESTIMATE_NOT_A_STRENGTH_APPROVAL", text)
        self.assertTrue(text.isascii())

    def test_stop_radius_matches_the_cad_formula(self):
        # X01Frame.scad: stop_r_in = flange_d / 2 + 2 + 2, stop_r_out = housing circle / 2 - 5
        frame = (ROOT / "Design/Exo/X01Frame.scad").read_text(encoding="ascii")
        self.assertIn("centre_hole_r = flange_d_mm / 2 + 2;", frame)
        self.assertIn("stop_r_in = centre_hole_r + 2;", frame)
        self.assertIn("stop_r_out = housing_bolt_circle_mm / 2 - 5;", frame)
        self.assertEqual(loads.stop_geometry(self.parameters), (28.0, 37.5))


if __name__ == "__main__":
    unittest.main()
