import copy
import json
import math
from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import suit_fit
import suit_budget


class FitTests(unittest.TestCase):
    def setUp(self):
        self.profile = json.loads(suit_fit.DEFAULT_PROFILE.read_text())

    def complete(self):
        result = copy.deepcopy(self.profile)
        result["measurements_mm"] = dict(suit_fit.DEMO)
        return result

    def test_unknown_measurements_block_normal_export(self):
        with self.assertRaisesRegex(ValueError, "Fehlende Masse"):
            suit_fit.derive(self.profile)

    def test_concept_preserves_height_and_labels_every_estimate(self):
        r = suit_fit.derive(self.profile, concept=True)
        self.assertEqual(r["measurements_mm"]["height"], 1660)
        self.assertEqual(len(r["missing_measurements"]), 31)
        self.assertFalse(r["fabrication_approved"])
        self.assertEqual(r["measurement_sources"]["height"], "profile_input")
        for key in r["missing_measurements"]:
            self.assertEqual(r["measurement_sources"][key], "synthetic_concept")

    def test_complete_values_never_imply_fabrication_approval(self):
        r = suit_fit.derive(self.complete())
        self.assertEqual(r["status"], "MEASURED_ENVELOPE_NOT_VALIDATED")
        self.assertFalse(r["fabrication_approved"])

    def test_stature_does_not_shrink_broad_shoulders(self):
        p = self.complete()
        a = suit_fit.derive(p)["parameters_mm"]
        p["measurements_mm"]["height"] = 1800
        b = suit_fit.derive(p)["parameters_mm"]
        self.assertEqual(a["shoulder_span"], b["shoulder_span"])
        self.assertEqual(a["torso_height"], b["torso_height"])

    def test_left_and_right_are_independent(self):
        p = self.complete()
        p["measurements_mm"]["forearm_length_l"] = 235
        r = suit_fit.derive(p)["parameters_mm"]
        self.assertEqual(r["forearm_length_l"], 195)
        self.assertEqual(r["forearm_length_r"], 205)

    def test_radial_allowance_is_not_circumference_allowance(self):
        r = suit_fit.derive(self.complete())["parameters_mm"]
        self.assertAlmostEqual(r["forearm_diameter_l"], 310/math.pi+46, places=3)
        self.assertEqual(r["torso_width"], 466)

    def test_entry_slide_fills_missing_aperture(self):
        r = suit_fit.derive(self.complete())["parameters_mm"]
        self.assertEqual(r["entry_width_required"], 550)
        self.assertEqual(r["entry_slide_each_side"], 45)
        self.assertEqual(r["torso_width"]-2*r["wall"]+2*r["entry_slide_each_side"], 550)

    def test_zero_slide_is_valid(self):
        p = self.complete()
        p["allowances_mm"]["entry_clearance_each_side"] = 10
        p["measurements_mm"]["shoulder_width"] = 420
        r = suit_fit.derive(p)["parameters_mm"]
        self.assertEqual(r["entry_slide_each_side"], 0)

    def test_invalid_measurements_rejected(self):
        for value in (True, "1660", math.nan, math.inf, -1, 166):
            with self.subTest(value=value):
                p = self.complete()
                p["measurements_mm"]["height"] = value
                with self.assertRaises(ValueError):
                    suit_fit.derive(p)

    def test_typos_and_missing_height_rejected(self):
        p = self.complete()
        p["measurements_mm"]["hieght"] = 1660
        with self.assertRaises(ValueError):
            suit_fit.derive(p)
        p = self.complete()
        p["measurements_mm"]["height"] = None
        with self.assertRaises(ValueError):
            suit_fit.derive(p, concept=True)

    def test_invalid_allowances_rejected(self):
        p = self.complete()
        p["allowances_mm"]["shell_wall"] = -1
        with self.assertRaises(ValueError):
            suit_fit.derive(p)
        p = self.complete()
        p["measurements_mm"]["torso_length"] = 100
        p["allowances_mm"]["edge_clearance"] = 60
        with self.assertRaises(ValueError):
            suit_fit.derive(p)

    def test_opening_geometry_against_orthogonal_cases(self):
        a = suit_fit.opening_envelope(400, 300, 0)
        self.assertAlmostEqual(a["outer_width_mm"], 400)
        self.assertAlmostEqual(a["forward_reach_mm"], 150)
        b = suit_fit.opening_envelope(400, 300, 90, 40)
        self.assertAlmostEqual(b["outer_width_mm"], 780)
        self.assertAlmostEqual(b["forward_reach_mm"], 200)
        with self.assertRaises(ValueError):
            suit_fit.opening_envelope(400, 300, 180)

    def test_generated_files_match_source_and_svg_parses(self):
        report = suit_fit.derive(self.profile, concept=True)
        with tempfile.TemporaryDirectory() as tmp:
            suit_fit.export(report, Path(tmp))
            for name in ("fit-report.json", "FitReport.md", "parameters.scad", "OpeningEnvelope.svg"):
                self.assertEqual((Path(tmp)/name).read_bytes(),
                                 (ROOT/"Design/Parametric/Generated"/name).read_bytes(), name)
            ET.parse(Path(tmp)/"OpeningEnvelope.svg")

    def test_cli_refuses_unknowns_without_creating_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)/"absent"
            self.assertEqual(suit_fit.main(["--out", str(out)]), 2)
            self.assertFalse(out.exists())


class BudgetTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT/"Materials/Mjolnir-BOM.json").read_text())

    def test_budget_has_explicit_reserve_and_no_station_mass(self):
        r = suit_budget.calculate(self.data)
        self.assertEqual(r["base_eur"], [1663, 3540])
        self.assertEqual(r["with_reserve_eur"], [2161.9, 4602.0])
        self.assertEqual(r["planned_worn_g"], 11460)
        self.assertTrue(r["mass_target_met_in_plan"])

    def test_unknown_mass_cannot_pass_target(self):
        self.data["items"][0]["unit_mass_target_g"] = None
        r = suit_budget.calculate(self.data)
        self.assertFalse(r["mass_target_met_in_plan"])
        self.assertIn("T01", r["unknown_worn_mass_ids"])

    def test_bad_budget_values_rejected(self):
        for field, value in (("qty", -1), ("qty", True), ("unit_budget_eur", [30, 10]),
                             ("unit_mass_target_g", math.nan)):
            with self.subTest(field=field, value=value):
                data = copy.deepcopy(self.data)
                data["items"][0][field] = value
                with self.assertRaises(ValueError):
                    suit_budget.calculate(data)

    def test_budget_document_matches_source(self):
        self.assertEqual(suit_budget.render(self.data), (ROOT/"Materials/Mjolnir-BOM.md").read_text())


if __name__ == "__main__":
    unittest.main()
