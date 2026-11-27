import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
PARAMETERS = ROOT / "Design/Exo/Parameters.scad"
CORE = ROOT / "Code/ExoControl/LegAssist/exo_core.h"
SKETCH = ROOT / "Code/ExoControl/LegAssist/LegAssist.ino"


def scad_values(text):
    return {name: float(value) for name, value in re.findall(r"^(\w+) = (-?[\d.]+);", text, re.M)}


def core_value(text, name):
    match = re.search(r"\b%s = (-?[\d.]+)f" % name, text)
    if not match:
        raise AssertionError("exo_core.h: %s nicht gefunden" % name)
    return float(match.group(1))


class ExoMechanicsTests(unittest.TestCase):
    """Text-level consistency between the concept CAD and the controller; no hardware claim."""

    def setUp(self):
        self.scad = scad_values(PARAMETERS.read_text(encoding="ascii"))
        self.core = CORE.read_text(encoding="ascii")

    def test_mechanical_stops_lie_outside_the_software_fault_limits(self):
        margin = core_value(self.core, "rangeMarginDeg")
        fault_extension = -core_value(self.core, "hipMinDeg") + margin
        fault_flexion = core_value(self.core, "hipMaxDeg") + margin
        # The controller must trip before the bar reaches a stop, with some room for overshoot.
        self.assertGreaterEqual(self.scad["stop_extension_deg"], fault_extension + 2)
        self.assertGreaterEqual(self.scad["stop_flexion_deg"], fault_flexion + 2)
        # A stop far outside the software range would no longer protect the joint.
        self.assertLessEqual(self.scad["stop_extension_deg"], fault_extension + 10)
        self.assertLessEqual(self.scad["stop_flexion_deg"], fault_flexion + 10)

    def test_readme_quotes_the_current_limits(self):
        readme = (ROOT / "Design/Exo/README.md").read_text(encoding="ascii")
        margin = core_value(self.core, "rangeMarginDeg")
        low = core_value(self.core, "hipMinDeg") - margin
        high = core_value(self.core, "hipMaxDeg") + margin
        self.assertIn("%d und +%d Grad" % (low, high), readme)
        self.assertIn("%d Grad Streckung, %d Grad Beugung" % (self.scad["stop_extension_deg"],
                                                              self.scad["stop_flexion_deg"]), readme)

    def test_actuator_interface_matches_the_selected_drive(self):
        # The sketch packs frames for the AK80-9; the CAD carries that actuator's drawing values.
        self.assertIn("#define MOTOR_RANGE exo::RANGE_AK80_9", SKETCH.read_text(encoding="ascii"))
        self.assertEqual((self.scad["actuator_d_mm"], self.scad["actuator_h_mm"]), (98, 38.5))
        self.assertEqual((self.scad["housing_bolt_circle_mm"], self.scad["housing_bolt_count"]), (85, 8))
        self.assertEqual((self.scad["output_bolt_circle_mm"], self.scad["output_bolt_count"]), (28, 6))

    def test_bench_limit_stays_below_the_fixed_torque_cap(self):
        sketch = SKETCH.read_text(encoding="ascii")
        bench = float(re.search(r"#define BENCH_LIMIT_NM ([\d.]+)f", sketch).group(1))
        self.assertLessEqual(bench, core_value(self.core, "ABS_TORQUE_LIMIT_NM"))
        self.assertRegex(sketch, r"#define BENCH_TEST 0\b")


if __name__ == "__main__":
    unittest.main()
