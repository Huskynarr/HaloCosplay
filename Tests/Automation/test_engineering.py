"""Arithmetic, missing inputs, model boundaries and project isolation."""
import copy
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import suit_engineering as engineering


class EngineeringTests(unittest.TestCase):
    def setUp(self):
        self.demo = json.loads((ROOT / "Design/Engineering/Demo.json").read_text())

    def test_shared_battery_sums_converted_rails_and_separate_battery_is_independent(self):
        result = engineering.calculate(self.demo)
        rail = result["rails"][0]
        self.assertEqual(rail["average_output_w"], 7)
        self.assertEqual(rail["simultaneous_full_load_w"], 12)
        self.assertEqual(rail["specified_peak_w"], 15)
        self.assertAlmostEqual(rail["full_load_current_a"], 2.4)
        self.assertAlmostEqual(rail["specified_peak_current_a"], 3)
        self.assertAlmostEqual(rail["average_battery_input_w"], 9.25)
        b1, b2 = result["batteries"]
        self.assertAlmostEqual(b1["average_input_w"], 11.45)
        self.assertAlmostEqual(b1["estimated_runtime_h"], 40 / 11.45)
        self.assertAlmostEqual(b1["target_energy_wh"], 22.9)
        self.assertAlmostEqual(b1["energy_difference_wh"], 17.1)
        self.assertEqual(b2["estimated_runtime_h"], 8)
        self.assertAlmostEqual(result["estimated_system_runtime_h"], 40 / 11.45)
        self.assertEqual(result["input_status"], "synthetic")
        self.assertFalse(result["hardware_approved"])

    def test_empty_template_has_no_computed_capacity_or_static_pass(self):
        template = json.loads((ROOT / "Design/Engineering/Template.json").read_text())
        self.assertEqual(template, engineering.new_project())
        result = engineering.calculate(template)
        self.assertIsNone(result["estimated_system_runtime_h"])
        self.assertIsNone(result["hinges"][0]["static_gravity_moment_nm"])
        self.assertTrue(result["missing_inputs"])
        self.assertEqual({e["finding"] for e in result["stand_edges"]}, {"missing_inputs"})
        self.assertFalse(result["hardware_approved"])

    def test_one_unknown_load_is_not_silently_zero_and_peak_does_not_need_duty(self):
        self.demo["rails"][0]["consumers"][0]["duty_fraction"] = None
        result = engineering.calculate(self.demo)
        self.assertIsNone(result["rails"][0]["average_output_w"])
        self.assertEqual(result["rails"][0]["specified_peak_w"], 15)
        self.assertIsNone(result["batteries"][0]["estimated_runtime_h"])
        self.assertIsNone(result["estimated_system_runtime_h"])
        self.assertEqual(result["batteries"][1]["estimated_runtime_h"], 8)
        self.demo["rails"][0]["consumers"][0]["duty_fraction"] = 0.5
        self.demo["rails"][0]["consumers"][0]["peak_power_w"] = None
        result = engineering.calculate(self.demo)
        self.assertIsNone(result["rails"][0]["specified_peak_w"])
        self.assertIsNotNone(result["estimated_system_runtime_h"])

    def test_missing_voltage_does_not_invent_current_and_unknown_source_blocks_system_runtime(self):
        self.demo["rails"][0]["voltage_v"] = None
        self.demo["rails"][0]["battery_id"] = None
        result = engineering.calculate(self.demo)
        self.assertIsNone(result["rails"][0]["full_load_current_a"])
        self.assertIsNone(result["estimated_system_runtime_h"])
        self.assertIn("rails.R5V.battery_id", result["missing_inputs"])

    def test_static_moment_and_four_edges_include_offset_direction(self):
        result = engineering.calculate(self.demo)
        self.assertAlmostEqual(result["hinges"][0]["static_gravity_moment_nm"], 0.8 * 9.80665 * 0.12)
        self.demo["hinges"][0]["gravity_axis_factor"] = 0
        self.assertEqual(engineering.calculate(self.demo)["hinges"][0]["static_gravity_moment_nm"], 0)
        edges = {edge["edge"]: edge for edge in result["stand_edges"]}
        self.assertAlmostEqual(edges["+x"]["gravity_lever_m"], 0.35)
        self.assertAlmostEqual(edges["-x"]["gravity_lever_m"], 0.45)
        self.assertAlmostEqual(edges["+y"]["gravity_lever_m"], 0.33)
        self.assertAlmostEqual(edges["-y"]["gravity_lever_m"], 0.27)
        self.assertAlmostEqual(edges["+x"]["moment_difference_nm"], 30 * 9.80665 * 0.35 - 30)
        self.demo["stand"]["com_x_m"] = 0.5
        edges = engineering.calculate(self.demo)["stand_edges"]
        self.assertLess(edges[0]["restoring_moment_nm"], 0)
        self.assertEqual(edges[0]["finding"], "nonpositive_static_moment_difference")

    def test_no_load_does_not_produce_infinite_runtime(self):
        for rail in self.demo["rails"]:
            rail["idle_input_w"] = 0
            for consumer in rail["consumers"]:
                consumer["duty_fraction"] = 0
        result = engineering.calculate(self.demo)
        self.assertIsNone(result["estimated_system_runtime_h"])
        self.assertTrue(all(b["estimated_runtime_h"] is None for b in result["batteries"]))
        json.dumps(result, allow_nan=False)

    def test_absent_optional_hardware_is_explicitly_omitted(self):
        self.demo.update(batteries=[], rails=[], hinges=[], stand=None)
        result = engineering.calculate(self.demo)
        self.assertEqual(result["omitted_sections"], ["electrical_rails", "hinges", "stand"])
        self.assertIsNone(result["estimated_system_runtime_h"])
        self.assertFalse(result["hardware_approved"])
        self.assertEqual(result["stand_edges"], [])
        self.assertEqual(result["missing_inputs"], [])
        self.assertIn("stand", engineering.render(result))

    def test_invalid_units_schema_and_duplicate_ids_are_rejected(self):
        mutations = [
            lambda d: d.update(schema_version=True),
            lambda d: d.update(project="../../demo"),
            lambda d: d.update(status="approved"),
            lambda d: d.update(unknown=1),
            lambda d: d["batteries"].append(copy.deepcopy(d["batteries"][0])),
            lambda d: d["rails"][0].update(battery_id="unknown"),
            lambda d: d["rails"][0].update(voltage_v=0),
            lambda d: d["rails"][0].update(efficiency_fraction=0),
            lambda d: d["rails"][0].update(efficiency_fraction=1.1),
            lambda d: d["rails"][0]["consumers"][0].update(quantity=1.5),
            lambda d: d["rails"][0]["consumers"][0].update(quantity=True),
            lambda d: d["rails"][0]["consumers"][0].update(duty_fraction=-0.1),
            lambda d: d["rails"][0]["consumers"][0].update(power_w=float("nan")),
            lambda d: d["rails"][0]["consumers"][0].update(power_w=float("inf")),
            lambda d: d["rails"][0]["consumers"][0].update(peak_power_w=1),
            lambda d: d["stand"].update(force_height_m=-1),
            lambda d: d["stand"].update(base_width_x_m=0),
            lambda d: d["hinges"][0].update(gravity_axis_factor=1.1),
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                data = copy.deepcopy(self.demo)
                mutation(data)
                with self.assertRaises(ValueError):
                    engineering.calculate(data)

    def test_cli_rejects_hardlinked_source_before_writing_either_report(self):
        for filename in ("EngineeringReport.json", "EngineeringReport.md"):
            with self.subTest(filename=filename), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                source = root / "Input.json"
                source.write_text(json.dumps(self.demo))
                out = root / "reports"
                out.mkdir()
                os.link(source, out / filename)
                original = source.read_bytes()
                self.assertEqual(engineering.main(["--input", str(source), "--out", str(out)]), 2)
                self.assertEqual(source.read_bytes(), original)
                self.assertEqual((out / filename).read_bytes(), original)
                other = "EngineeringReport.md" if filename.endswith(".json") else "EngineeringReport.json"
                self.assertFalse((out / other).exists())

    def test_cli_init_reports_are_isolated_and_source_is_protected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in ("Suit-A", "Suit-B"):
                source = root / (name + ".json")
                self.assertEqual(engineering.main(["--init", str(source), "--name", name]), 0)
                original = source.read_bytes()
                self.assertEqual(engineering.main(["--init", str(source)]), 2)
                self.assertEqual(source.read_bytes(), original)
                self.assertEqual(engineering.main(["--input", str(source)]), 0)
                self.assertEqual(engineering.main(["--input", str(source), "--check"]), 0)
                report = json.loads((root / (name + "-engineering") / "EngineeringReport.json").read_text())
                self.assertEqual(report["project"], name)
            source = root / "EngineeringReport.json"
            source.write_text(json.dumps(self.demo))
            original = source.read_bytes()
            self.assertEqual(engineering.main(["--input", str(source), "--out", str(root)]), 2)
            self.assertEqual(source.read_bytes(), original)
            reportpath = root / "Suit-A-engineering" / "EngineeringReport.md"
            reportpath.write_text("stale")
            self.assertEqual(engineering.main(["--input", str(root / "Suit-A.json"), "--check"]), 2)


if __name__ == "__main__":
    unittest.main()
