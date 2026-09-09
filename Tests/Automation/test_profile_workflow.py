"""Independent profiles, explicit provenance and isolated output directories."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import suit_fit
import suit_budget


class ProfileWorkflowTests(unittest.TestCase):
    def test_default_outputs_are_per_profile_and_sources_are_protected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ("Project-A", "Project-B"):
                p = suit_fit.new_profile(name)
                source = root / (name + ".json")
                source.write_text(json.dumps(p))
                with mock.patch.object(suit_fit, "ROOT", root):
                    self.assertEqual(suit_fit.main(["--profile", str(source), "--concept"]), 0)
                self.assertEqual(json.loads((root / "build" / name / "fit-report.json").read_text())["profile"], name)
            source = root / "fit-report.json"
            original = json.dumps(suit_fit.new_profile())
            source.write_text(original)
            self.assertEqual(suit_fit.main(["--profile", str(source), "--concept", "--out", str(root)]), 2)
            self.assertEqual(source.read_text(), original)
            report = suit_fit.derive(suit_fit.new_profile(), concept=True)
            with self.assertRaisesRegex(ValueError, "CAD-Quelldatei"):
                suit_fit.export(report, suit_fit.MODEL_PATH.parent)

    def test_shared_schema_template_and_demo_cover_same_fields(self):
        template = json.loads(suit_fit.DEFAULT_PROFILE.read_text())
        self.assertEqual(template, suit_fit.new_profile())
        self.assertEqual(set(suit_fit.SCHEMA["measurements"]), set(suit_fit.DEMO))
        self.assertEqual(set(suit_fit.SCHEMA["allowances"]), set(template["allowances_mm"]))
        report = suit_fit.derive(json.loads(suit_fit.DEMO_PROFILE.read_text()))
        self.assertEqual(report["status"], "CONCEPT_NOT_MEASURED")
        self.assertEqual(set(report["measurement_sources"].values()), {"synthetic_concept"})

    def test_init_roundtrip_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "profiles" / "Studio.local.json"
            self.assertEqual(suit_fit.main(["--init", str(path), "--name", "Studio-01"]), 0)
            original = path.read_bytes()
            self.assertEqual(suit_fit.main(["--init", str(path)]), 2)
            self.assertEqual(path.read_bytes(), original)
            p = json.loads(original)
            p["measurements_mm"] = dict(suit_fit.DEMO)
            # Completing numbers never silently turns pending into measured.
            self.assertEqual(suit_fit.derive(p)["status"], "INPUT_ENVELOPE_NOT_VALIDATED")
            p["status"] = "measured"
            p["build"] = {"armor_reference": "custom", "material": "foam", "operating_mode": "exhibition",
                          "features": {"exoskeleton": False, "hud": True, "lighting": False, "audio": True}}
            path.write_text(json.dumps(p))
            out = Path(tmp) / "project-export"
            self.assertEqual(suit_fit.main(["--profile", str(path), "--out", str(out)]), 0)
            report = json.loads((out / "fit-report.json").read_text())
            self.assertEqual(report["build"], {**p["build"], "fog_system": "none"})
            self.assertEqual(report["profile"], "Studio-01")
            self.assertFalse(report["fabrication_approved"])

    def test_profiles_export_independent_portable_cad(self):
        a = suit_fit.new_profile("Project-A")
        b = suit_fit.new_profile("Project-B")
        a["measurements_mm"].update(height=1720, boot_width_l=130, boot_length_l=270)
        b["measurements_mm"].update(height=1920, shoulder_width=525, boot_width_l=100, boot_length_l=310)
        b["allowances_mm"]["padding_radial"] = 10
        b["build"] = {"armor_reference": "mark-vii", "features": {"hud": True}}
        ar, br = suit_fit.derive(a, True), suit_fit.derive(b, True)
        self.assertNotEqual(ar["parameters_mm"]["boot_width_l"], br["parameters_mm"]["boot_width_l"])
        self.assertLess(ar["parameters_mm"]["boot_length_l"], br["parameters_mm"]["boot_length_l"])
        self.assertEqual(br["build"]["material"], "hybrid")
        with tempfile.TemporaryDirectory() as tmp:
            pa, pb = Path(tmp) / "a", Path(tmp) / "b"
            suit_fit.export(ar, pa)
            old = (pa / "parameters.scad").read_bytes()
            suit_fit.export(br, pb)
            self.assertEqual((pa / "parameters.scad").read_bytes(), old)
            self.assertNotEqual(old, (pb / "parameters.scad").read_bytes())
            cad = (pb / "MjolnirEntry.scad").read_text()
            self.assertIn("include <parameters.scad>", cad)
            self.assertNotIn("include <Generated/parameters.scad>", cad)
            self.assertNotIn(str(ROOT), cad)
            moved = Path(tmp) / "moved-export"
            pb.rename(moved)
            self.assertTrue((moved / "parameters.scad").exists())
            self.assertEqual((moved / "MjolnirEntry.scad").read_text(), cad)

    def test_invalid_config_and_metadata_cannot_silently_select_defaults(self):
        base = suit_fit.new_profile()
        invalid = [
            ("profile", "../person"), ("profile", "a" * 65), ("profile", " name"),
            ("profile", "name|table"), ("profile", True), ("schema_version", True),
            ("status", "ready"), ("status", []), ("build", None),
            ("build", {"material": "metal"}), ("build", {"armor_reference": []}),
            ("build", {"operating_mode": "automatic"}), ("build", {"unknown": True}),
            ("build", {"features": {"hud": 1}}), ("build", {"features": {"motors": True}}),
            ("allowances_mm", []),
        ]
        for key, value in invalid:
            with self.subTest(key=key, value=value):
                p = copy.deepcopy(base)
                p[key] = value
                with self.assertRaises(ValueError):
                    suit_fit.derive(p, concept=True)

    def test_old_profile_without_build_uses_explicit_schema_defaults(self):
        p = suit_fit.new_profile()
        del p["build"]
        r = suit_fit.derive(p, concept=True)
        self.assertEqual(r["build"], suit_fit.build_config())

    def test_synthetic_status_survives_fully_populated_and_edited_profile(self):
        p = json.loads(suit_fit.DEMO_PROFILE.read_text())
        p["measurements_mm"]["height"] = 1900
        r = suit_fit.derive(p)
        self.assertEqual(r["input_status"], "synthetic")
        self.assertEqual(r["measurement_sources"]["height"], "synthetic_concept")
        p["measurements_mm"]["height"] = None
        p["status"] = "measured"
        with self.assertRaises(ValueError):
            suit_fit.derive(p, concept=True)


class CustomBudgetTests(unittest.TestCase):
    def test_custom_bom_stays_beside_custom_source_and_checks_output(self):
        reference = (ROOT / "Materials/Mjolnir-BOM.md").read_bytes()
        data = json.loads(suit_budget.DEFAULT_BOM.read_text())
        data["items"] = data["items"][:1]
        data["items"][0]["qty"] = 2
        with tempfile.TemporaryDirectory() as tmp:
            bom = Path(tmp) / "Custom.json"
            bom.write_text(json.dumps(data))
            self.assertEqual(suit_budget.main(["--bom", str(bom)]), 0)
            self.assertEqual((ROOT / "Materials/Mjolnir-BOM.md").read_bytes(), reference)
            target = bom.with_suffix(".md")
            self.assertTrue(target.exists())
            self.assertNotIn("P01 zuerst", target.read_text())
            self.assertEqual(suit_budget.main(["--bom", str(bom), "--check"]), 0)
            target.write_text("stale")
            self.assertEqual(suit_budget.main(["--bom", str(bom), "--check"]), 2)
            out = Path(tmp) / "separate" / "Report.md"
            self.assertEqual(suit_budget.main(["--bom", str(bom), "--out", str(out)]), 0)
            self.assertTrue(out.exists())
            original = bom.read_bytes()
            self.assertEqual(suit_budget.main(["--bom", str(bom), "--out", str(bom)]), 2)
            self.assertEqual(bom.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
