"""Shared-sink heat, channel energy balance, missing inputs and file protection."""
import copy
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import suit_thermal as thermal


class ThermalTests(unittest.TestCase):
    def setUp(self):
        self.demo = json.loads((ROOT / "Design/Thermal/Demo.json").read_text())

    def test_shared_sink_and_independent_junction_paths_do_not_double_count_heat(self):
        report = thermal.calculate(self.demo)
        sink = report["modules"][0]
        self.assertEqual(sink["sink_temperature_c"], 40)
        self.assertEqual([path["junction_temperature_c"] for path in sink["junction_paths"]], [43, 43.75, 45])
        self.assertEqual(sink["heat_not_assigned_to_junctions_w"], 0)
        self.assertIsNone(sink["surface_headroom_k"])
        self.assertTrue(all(path["finding"] == "missing_inputs" for path in sink["junction_paths"]))
        self.assertFalse(report["hardware_approved"])
        self.assertFalse(report["fabrication_approved"])

    def test_surface_and_chip_limits_are_separate_and_resistance_bound_is_conditional(self):
        module = self.demo["modules"][0]
        module["surface_limit_c"] = 50
        module["junction_paths"][0]["junction_limit_c"] = 42
        sink = thermal.calculate(self.demo)["modules"][0]
        self.assertEqual(sink["surface_headroom_k"], 10)
        self.assertEqual(sink["surface_max_sink_ambient_k_per_w"], 7.5)
        self.assertEqual(sink["finding"], "positive_model_headroom")
        self.assertEqual(sink["junction_paths"][0]["junction_headroom_k"], -1)
        self.assertEqual(sink["junction_paths"][0]["finding"], "nonpositive_model_headroom")
        module["surface_limit_c"] = 20
        sink = thermal.calculate(self.demo)["modules"][0]
        self.assertIsNone(sink["surface_max_sink_ambient_k_per_w"])
        self.assertEqual(sink["surface_resistance_bound_note"], "ambient_at_or_above_limit_no_positive_resistance_possible")

    def test_known_chip_heat_must_fit_total_even_if_another_chip_is_unknown(self):
        self.demo["modules"][0]["junction_paths"][2]["heat_w"] = None
        self.demo["modules"][0]["heat_load_w"] = 2
        with self.assertRaisesRegex(ValueError, "exceeds total"):
            thermal.calculate(self.demo)
        self.demo["modules"][0]["heat_load_w"] = 4
        sink = thermal.calculate(self.demo)["modules"][0]
        self.assertEqual(sink["sink_temperature_c"], 40)
        self.assertIsNone(sink["heat_not_assigned_to_junctions_w"])
        self.assertIsNone(sink["junction_paths"][2]["junction_temperature_c"])
        self.demo["modules"][0]["heat_load_w"] = None
        sink = thermal.calculate(self.demo)["modules"][0]
        self.assertIsNone(sink["sink_temperature_c"])
        self.assertTrue(all(path["junction_temperature_c"] is None for path in sink["junction_paths"]))

    def test_airflow_balance_uses_cubic_metres_per_hour_and_preserves_missing_inputs(self):
        vent = thermal.calculate(self.demo)["vents"][0]
        self.assertAlmostEqual(vent["air_temperature_rise_k"], 6)
        self.assertAlmostEqual(vent["model_outlet_temperature_c"], 26)
        self.demo["vents"][0]["ambient_c"] = None
        vent = thermal.calculate(self.demo)["vents"][0]
        self.assertAlmostEqual(vent["air_temperature_rise_k"], 6)
        self.assertIsNone(vent["model_outlet_temperature_c"])
        self.demo["vents"][0]["measured_flow_m3_h"] = None
        vent = thermal.calculate(self.demo)["vents"][0]
        self.assertIsNone(vent["air_temperature_rise_k"])
        self.assertEqual(vent["finding"], "missing_inputs")

    def test_zero_flow_has_no_false_finite_solution_and_zero_heat_has_no_resistance_bound(self):
        self.demo["vents"][0]["measured_flow_m3_h"] = 0
        report = thermal.calculate(self.demo)
        self.assertIsNone(report["vents"][0]["air_temperature_rise_k"])
        self.assertEqual(report["vents"][0]["finding"], "zero_flow_unbounded_in_this_model")
        self.demo["vents"][0]["heat_w"] = 0
        self.demo["modules"][0].update(heat_load_w=0, surface_limit_c=50, junction_paths=[])
        report = thermal.calculate(self.demo)
        self.assertEqual(report["modules"][0]["sink_temperature_c"], 20)
        self.assertIsNone(report["modules"][0]["surface_max_sink_ambient_k_per_w"])
        self.assertEqual(report["modules"][0]["surface_resistance_bound_note"], "zero_heat_no_resistance_bound")
        self.assertEqual(report["vents"][0]["finding"], "zero_flow_no_advective_solution")
        json.dumps(report, allow_nan=False)

    def test_template_has_no_guessed_airflow_temperature_or_limits_and_empty_sections_are_explicit(self):
        template = json.loads((ROOT / "Design/Thermal/Template.json").read_text())
        self.assertEqual(template, thermal.new_project())
        report = thermal.calculate(template)
        self.assertIsNone(report["modules"][0]["sink_temperature_c"])
        self.assertIsNone(report["vents"][0]["air_temperature_rise_k"])
        self.assertEqual(len(report["missing_inputs"]), 12)
        template.update(modules=[], vents=[])
        report = thermal.calculate(template)
        self.assertEqual(report["omitted_sections"], ["modules", "vents"])
        self.assertFalse(report["hardware_approved"])
        self.assertIn("Explizit ausgelassene Bereiche: modules, vents", thermal.render(report))

    def test_invalid_units_nonfinite_inputs_duplicate_ids_and_overflow_are_rejected(self):
        mutations = [
            lambda d: d.update(schema_version=True),
            lambda d: d.update(project="../../example"),
            lambda d: d.update(status="approved"),
            lambda d: d.update(unexpected=0),
            lambda d: d["modules"].append(copy.deepcopy(d["modules"][0])),
            lambda d: d["modules"][0]["junction_paths"].append(copy.deepcopy(d["modules"][0]["junction_paths"][0])),
            lambda d: d["modules"][0].update(heat_load_w=-1),
            lambda d: d["modules"][0].update(heat_load_w=True),
            lambda d: d["modules"][0].update(heat_load_w=float("nan")),
            lambda d: d["modules"][0].update(heat_load_w=float("inf")),
            lambda d: d["modules"][0].update(heat_load_w=10 ** 1000),
            lambda d: d["modules"][0].update(heat_load_w=1e308, sink_ambient_k_per_w=1e308),
            lambda d: d["modules"][0].update(ambient_c=-273.15),
            lambda d: d["modules"][0].update(sink_ambient_k_per_w=0),
            lambda d: d["modules"][0]["junction_paths"][0].update(junction_to_sink_k_per_w=-1),
            lambda d: d["vents"][0].update(measured_flow_m3_h=-1),
            lambda d: d["vents"][0].update(rho_kg_m3=0),
            lambda d: d["vents"][0].update(cp_j_kg_k=0),
            lambda d: d["vents"][0].update(measured_flow_m3_h=1e-300, rho_kg_m3=1e-300),
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                data = copy.deepcopy(self.demo)
                mutation(data)
                with self.assertRaises(ValueError):
                    thermal.calculate(data)

    def test_export_hash_check_and_project_isolation_preserve_source(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for project in ("Suit-A", "Suit-B"):
                source = root / (project + ".json")
                self.assertEqual(thermal.main(["--init", str(source), "--name", project]), 0)
                original = source.read_bytes()
                self.assertEqual(thermal.main(["--init", str(source)]), 2)
                report = thermal.export(source)
                self.assertEqual(report["project"], project)
                self.assertEqual(report["input_sha256"], hashlib.sha256(original).hexdigest())
                self.assertEqual(thermal.main(["--input", str(source), "--check"]), 0)
                self.assertEqual(source.read_bytes(), original)
            stale = root / "Suit-A-thermal/ThermalReport.md"
            stale.write_text("stale")
            self.assertEqual(thermal.main(["--input", str(root / "Suit-A.json"), "--check"]), 2)
            self.assertEqual(stale.read_text(), "stale")

    def test_output_aliases_cannot_overwrite_input_or_each_other(self):
        for filename in ("ThermalReport.json", "ThermalReport.md"):
            for alias in ("same_path", "hardlink", "symlink"):
                with self.subTest(filename=filename, alias=alias), tempfile.TemporaryDirectory() as temp:
                    root = Path(temp)
                    source = root / (filename if alias == "same_path" else "Input.json")
                    source.write_text(json.dumps(self.demo))
                    original = source.read_bytes()
                    if alias == "hardlink":
                        os.link(source, root / filename)
                    elif alias == "symlink":
                        (root / filename).symlink_to(source)
                    self.assertEqual(thermal.main(["--input", str(source), "--out", str(root)]), 2)
                    self.assertEqual(source.read_bytes(), original)
                    other = "ThermalReport.md" if filename.endswith(".json") else "ThermalReport.json"
                    self.assertFalse((root / other).exists())
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "Input.json"
            source.write_text(json.dumps(self.demo))
            first, second = root / "ThermalReport.json", root / "ThermalReport.md"
            first.write_text("original")
            os.link(first, second)
            with self.assertRaisesRegex(ValueError, "hardlinked together"):
                thermal.export(source, root)
            self.assertEqual(first.read_text(), "original")


if __name__ == "__main__":
    unittest.main()
