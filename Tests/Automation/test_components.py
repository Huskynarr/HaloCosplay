import copy
import hashlib
import json
import math
from pathlib import Path
import re
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import suit_components as kit
import suit_fit


class ComponentTests(unittest.TestCase):
    def setUp(self):
        self.demo = json.loads(suit_fit.DEMO_PROFILE.read_text())
        self.fit = suit_fit.derive(self.demo, concept=True)

    def test_standalone_scad_defaults_match_editable_config(self):
        source = (kit.SOURCE / "Parameters.scad").read_text()
        parsed = {match.group(1): json.loads(match.group(2))
                  for match in re.finditer(r"^(\w+) = (.+);$", source, re.M)}
        self.assertEqual(parsed, kit.DEFAULTS)
        self.assertEqual(set(kit.BOUNDS) | {"clearances_mm"}, set(parsed))

    def test_hardware_dimensions_are_independent_from_stature(self):
        first = kit.parameters(self.fit)
        changed = copy.deepcopy(self.demo)
        changed["measurements_mm"]["height"] = 2000
        second = kit.parameters(suit_fit.derive(changed, concept=True))
        self.assertEqual(first, second)
        changed["measurements_mm"]["head_width"] = 180
        third = kit.parameters(suit_fit.derive(changed, concept=True))
        self.assertEqual(third["visor_radius_mm"] - first["visor_radius_mm"], 10)
        self.assertEqual(third["fan_hole_pitch_mm"], first["fan_hole_pitch_mm"])

    def test_impossible_geometry_is_rejected(self):
        cases = [({"fan_opening_mm": 40}, "Eckbohrungen"),
                 ({"fan_hole_pitch_mm": 70}, "Rand"),
                 ({"seam_tongue_height_mm": 3}, "Bodenmaterial"),
                 ({"joint_pitch_mm": 3, "joint_rib_width_mm": 4}, "ueberlappen"),
                 ({"hinge_pin_mm": 5, "hinge_barrel_mm": 8}, "Wand"),
                 ({"fastener_counterbore_mm": 4}, "Boden"),
                 ({"fastener_shaft_mm": 6, "fastener_head_mm": 5}, "Schraubenkopf")]
        for override, message in cases:
            with self.subTest(override=override), self.assertRaisesRegex(ValueError, message):
                kit.parameters(self.fit, override)

    def test_invalid_units_and_tolerance_order_are_rejected(self):
        for value in (True, "3", math.nan, math.inf, -2, 0):
            with self.subTest(value=value), self.assertRaises(ValueError):
                kit.parameters(self.fit, {"visor_sheet_mm": value})
        for gaps in ([0.4, 0.2, 0.6], [0.2, 0.2, 0.4], [0.2], [0.2, True, 0.4]):
            with self.subTest(gaps=gaps), self.assertRaises(ValueError):
                kit.parameters(self.fit, {"clearances_mm": gaps})
        with self.assertRaisesRegex(ValueError, "unbekannte"):
            kit.parameters(self.fit, {"fan_size_cm": 4})

    def test_generated_kit_is_portable_and_provenance_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "override.json"
            config.write_text('{"visor_radius_mm": 140}')
            out = Path(tmp) / "kit"
            result = kit.export(suit_fit.DEMO_PROFILE, out, concept=True, config_path=config)
            self.assertFalse(result["fabrication_approved"])
            self.assertEqual(result["fit_status"], "CONCEPT_NOT_MEASURED")
            self.assertEqual(result["profile_sha256"], hashlib.sha256(suit_fit.DEMO_PROFILE.read_bytes()).hexdigest())
            self.assertEqual(result["parameters"]["visor_radius_mm"], 140)
            self.assertEqual(result["parameter_origin"]["visor_radius_mm"], "explicit_config")
            self.assertEqual((out / "ComponentKit.scad").read_bytes(), (kit.SOURCE / "ComponentKit.scad").read_bytes())
            self.assertIn("include <Parameters.scad>", (out / "ComponentKit.scad").read_text())
            for component in kit.COMPONENTS:
                self.assertIn(component + '.stl', (out / (component + ".md")).read_text())
            bom = json.loads((out / "BOM.json").read_text())
            self.assertEqual(len(bom["components"]), 5)
            self.assertTrue(all(item["measured_mass_g"] is None and not item["physical_test_passed"]
                                for item in bom["components"]))

    def test_source_profile_and_existing_revision_cannot_be_overwritten(self):
        with self.assertRaisesRegex(ValueError, "Quellordner"):
            kit.export(suit_fit.DEMO_PROFILE, kit.SOURCE, concept=True)
        with tempfile.TemporaryDirectory() as tmp:
            profile = Path(tmp) / "Manifest.json"
            profile.write_text(json.dumps(self.demo))
            original = profile.read_bytes()
            with self.assertRaisesRegex(ValueError, "Profil"):
                kit.export(profile, Path(tmp), concept=True)
            self.assertEqual(profile.read_bytes(), original)
            out = Path(tmp) / "kit"
            kit.export(profile, out, concept=True)
            existing = (out / "Parameters.scad").read_bytes()
            with self.assertRaisesRegex(ValueError, "existiert"):
                kit.export(profile, out, concept=True)
            self.assertEqual((out / "Parameters.scad").read_bytes(), existing)

    def test_incomplete_or_synthetic_inputs_require_explicit_concept(self):
        with tempfile.TemporaryDirectory() as tmp:
            for profile in (suit_fit.DEFAULT_PROFILE, suit_fit.DEMO_PROFILE):
                out = Path(tmp) / profile.stem
                with self.subTest(profile=profile), self.assertRaises(ValueError):
                    kit.export(profile, out)
                self.assertFalse(out.exists())
            self.assertEqual(kit.main(["--demo", "--out", str(Path(tmp) / "cli")]), 2)
            self.assertFalse((Path(tmp) / "cli").exists())

    def test_two_profiles_get_separate_default_outputs(self):
        # Override only the root during this isolated workflow test.
        previous_root = kit.ROOT
        with tempfile.TemporaryDirectory() as tmp:
            kit.ROOT = Path(tmp)
            try:
                for name in ("Suit-A", "Suit-B"):
                    profile = copy.deepcopy(self.demo)
                    profile["profile"] = name
                    path = Path(tmp) / (name + ".json")
                    path.write_text(json.dumps(profile))
                    self.assertEqual(kit.main(["--profile", str(path), "--concept"]), 0)
                    self.assertTrue((Path(tmp) / "build" / name / "Components" / "Manifest.json").exists())
            finally:
                kit.ROOT = previous_root


if __name__ == "__main__":
    unittest.main()
