import copy
import csv
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import suit_clamshell as clamshell
import suit_fit


class ClamshellTests(unittest.TestCase):
    def test_sides_use_independent_measurements_not_height_scaling(self):
        raw = json.loads(suit_fit.DEMO_PROFILE.read_text())
        before = clamshell.parameters(suit_fit.derive(raw, concept=True))
        changed = copy.deepcopy(raw)
        changed["measurements_mm"]["height"] = 2000
        self.assertEqual(before, clamshell.parameters(suit_fit.derive(changed, concept=True)))
        changed["measurements_mm"]["forearm_circumference_r"] += 30
        changed["measurements_mm"]["shin_length_l"] += 20
        after = clamshell.parameters(suit_fit.derive(changed, concept=True))
        for i in (0, 1, 2, 4, 5, 7):
            self.assertEqual(before["limbs_mm"][i], after["limbs_mm"][i])
        self.assertGreater(after["limbs_mm"][3][0], before["limbs_mm"][3][0])
        self.assertEqual(after["limbs_mm"][6][1] - before["limbs_mm"][6][1], 20)

    def test_opening_mirrors_sides_and_free_edges_move_forwards(self):
        # Independent quarter-turn result around x=+/-18 mm.
        left = clamshell.front_point(10, 0, 10, 8, 90, "l")
        right = clamshell.front_point(-10, 0, 10, 8, 90, "r")
        self.assertAlmostEqual(left[0], -18)
        self.assertAlmostEqual(right[0], 18)
        self.assertAlmostEqual(left[1], -28)
        self.assertAlmostEqual(right[1], -28)
        for side, pivot in (("l", -18), ("r", 18)):
            self.assertEqual(clamshell.front_point(pivot, 0, 10, 8, 110, side), (pivot, 0))
            self.assertEqual(clamshell.front_point(3, -4, 10, 8, 0, side), (3, -4))
        with self.assertRaises(ValueError):
            clamshell.front_point(0, 0, 10, 8, 90, "both")

    def test_portable_export_preserves_sources_and_never_marks_physical_checks_complete(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "kit"
            report = clamshell.export(suit_fit.DEMO_PROFILE, out, concept=True)
            self.assertEqual((out / "Profile.json").read_bytes(), suit_fit.DEMO_PROFILE.read_bytes())
            self.assertEqual((out / "LimbClamshell.scad").read_bytes(), (clamshell.SOURCE / "LimbClamshell.scad").read_bytes())
            for field, name in (("profile_sha256", "Profile.json"), ("source_sha256", "LimbClamshell.scad"),
                                ("parameters_sha256", "Parameters.scad")):
                self.assertEqual(report[field], hashlib.sha256((out / name).read_bytes()).hexdigest())
            self.assertEqual(report["fit_status"], "CONCEPT_NOT_MEASURED")
            self.assertFalse(report["fabrication_approved"])
            self.assertFalse(report["solo_donning_verified"])
            plan = json.loads((out / "ClamshellPlan.json").read_text())
            self.assertEqual(len(plan["parts"]), 8)
            self.assertEqual({part["id"] for part in plan["parts"]}, set(report["parts"]))
            self.assertTrue(all(part["hardware_model"] is None and part["measured_mass_g"] is None and
                                not part["physical_test_passed"] for part in plan["parts"]))
            with (out / "Checklists.csv").open() as handle:
                checks = list(csv.DictReader(handle))
            self.assertEqual(len(checks), 104)
            self.assertTrue(all(row["status"] == "open" for row in checks))
            self.assertEqual({row["part_id"] for row in checks},
                             set(report["parts"]) | set(report["modules"]) | {"complete_suit"})
            self.assertEqual(set(report["module_sources_sha256"]), set(clamshell.MODULE_SOURCES))
            for name, digest in report["module_sources_sha256"].items():
                self.assertEqual((out / name).read_bytes(), (clamshell.SOURCE / name).read_bytes())
                self.assertEqual(digest, hashlib.sha256((out / name).read_bytes()).hexdigest())
            self.assertEqual([module["id"] for module in plan["modules"]], report["modules"])
            self.assertTrue(all(module["hardware_model"] is None and module["measured_mass_g"] is None and
                                not module["physical_test_passed"] for module in plan["modules"]))
            # Every generated parameter is declared with its origin and is defined in the static example.
            self.assertEqual(set(report["parameters"]), set(report["parameter_origin"]))
            static = (clamshell.SOURCE / "Parameters.scad").read_text()
            for key in report["parameters"]:
                self.assertIn(f"\n{key} = ", static)
            self.assertEqual(report["parameters"]["latch_hole_spacing_mm"], 0)
            self.assertEqual(report["parameters"]["latch_hole_d_mm"], 0)

    def test_six_modules_match_the_target_and_report_geometric_estimates_only(self):
        values = clamshell.parameters(suit_fit.derive(json.loads(suit_fit.DEMO_PROFILE.read_text()), concept=True))
        result = clamshell.modules(values)
        self.assertEqual([module["module"] for module in result], ["M1", "M2", "M3", "M4", "M5", "M6"])
        self.assertEqual([module["kind"] for module in result], ["leg", "leg", "torso", "arm", "arm", "helmet"])
        # Target from the donning guide: 3 + 3 + 3 + 2 + 2 + 1 hand latches.
        self.assertEqual(sum(module["target_hand_latches"] for module in result), 14)
        self.assertTrue(all(module["source"] in clamshell.MODULE_SOURCES for module in result))
        leg, _, torso, left, right, helmet = result
        self.assertEqual(left["segments"], ["upperarm_l", "forearm_l"])
        self.assertEqual(right["segments"], ["upperarm_r", "forearm_r"])
        upper, fore = values["limbs_mm"][0], values["limbs_mm"][2]
        self.assertAlmostEqual(left["overall_length_mm"], upper[1] + fore[1] + values["elbow_gap_mm"])
        thigh, shin = values["limbs_mm"][4], values["limbs_mm"][6]
        self.assertAlmostEqual(leg["overall_length_mm"], thigh[1] + shin[1] + values["knee_gap_mm"] +
                               values["ankle_gap_mm"] + values["boot_height_mm"])
        self.assertEqual(leg["knee_free_flex_estimate_deg"],
                         clamshell.free_flex_deg(thigh[0], values["knee_gap_mm"], values["knee_relief_mm"]))
        self.assertIsNone(leg["measured_knee_flex_deg"])
        self.assertAlmostEqual(torso["clear_entry_width_mm"],
                               values["torso_mm"][0] - 2 * values["wall_mm"] + 2 * values["entry_slide_mm"])
        # The neck opening is smaller than the shell, which is why the rear shell opens.
        self.assertLess(helmet["neck_opening_mm"][0], values["helmet_mm"][0] * 0.7)
        self.assertLess(helmet["neck_opening_mm"][1], values["helmet_mm"][1] * 0.7)
        # Gap and relief equal to the radius give exactly a right angle.
        self.assertEqual(clamshell.free_flex_deg(120, 60, 30), 90.0)
        self.assertLess(clamshell.free_flex_deg(120, 60, 0), clamshell.free_flex_deg(120, 60, 30))
        self.assertLess(clamshell.free_flex_deg(160, 60, 30), 90.0)
        self.assertEqual([key for key, _ in clamshell.module_checks("leg")],
                         ["MOD01", "MOD02", "MOD03", "MOD04", "MOD05", "MOD06", "MOD07"])

    def test_incomplete_and_synthetic_profiles_need_explicit_concept(self):
        with tempfile.TemporaryDirectory() as tmp:
            for profile in (suit_fit.DEFAULT_PROFILE, suit_fit.DEMO_PROFILE):
                out = Path(tmp) / profile.stem
                with self.subTest(profile=profile), self.assertRaises(ValueError):
                    clamshell.export(profile, out)
                self.assertFalse(out.exists())
            measured = json.loads(suit_fit.DEMO_PROFILE.read_text())
            measured["status"] = "measured"
            source = Path(tmp) / "measured.json"
            source.write_text(json.dumps(measured))
            result = clamshell.export(source, Path(tmp) / "measured")
            self.assertEqual(result["fit_status"], "MEASURED_ENVELOPE_NOT_VALIDATED")
            self.assertFalse(result["solo_donning_verified"])

    def test_existing_outputs_and_native_source_are_not_overwritten(self):
        with self.assertRaisesRegex(ValueError, "Quellordner"):
            clamshell.export(suit_fit.DEMO_PROFILE, clamshell.SOURCE / "generated", concept=True)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "revision"
            clamshell.export(suit_fit.DEMO_PROFILE, out, concept=True)
            original = (out / "Parameters.scad").read_bytes()
            with self.assertRaisesRegex(ValueError, "existiert"):
                clamshell.export(suit_fit.DEMO_PROFILE, out, concept=True)
            self.assertEqual((out / "Parameters.scad").read_bytes(), original)
            link = Path(tmp) / "link"
            link.symlink_to(Path(tmp) / "missing")
            with self.assertRaisesRegex(ValueError, "existiert"):
                clamshell.export(suit_fit.DEMO_PROFILE, link, concept=True)


if __name__ == "__main__":
    unittest.main()
