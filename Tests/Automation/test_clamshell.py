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
            self.assertEqual(len(checks), 66)
            self.assertTrue(all(row["status"] == "open" for row in checks))
            self.assertEqual({row["part_id"] for row in checks}, set(report["parts"]) | {"complete_suit"})

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
