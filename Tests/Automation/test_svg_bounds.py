"""A large valid envelope must remain visible in the exported diagram."""
import copy
import re
import unittest
import xml.etree.ElementTree as ET

from tools.suit_fit import derive, layout_svg, new_profile


class DiagramBoundsTests(unittest.TestCase):
    def test_broad_deep_profile_stays_inside_pose_panels(self):
        profile = copy.deepcopy(new_profile("Broad-demo"))
        profile["measurements_mm"].update({"shoulder_width": 700, "chest_width": 700,
                                           "chest_depth": 700, "abdomen_depth": 700})
        svg = ET.fromstring(layout_svg(derive(profile, concept=True)))
        groups = svg.findall("{http://www.w3.org/2000/svg}g")[1:]
        for group, (left, right) in zip(groups, ((60, 660), (730, 1330))):
            for shape in group:
                if "d" in shape.attrib or "points" in shape.attrib:
                    coordinates = re.findall(r"(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)",
                                             shape.get("d", shape.get("points", "")))
                    self.assertTrue(coordinates)
                    for x, y in coordinates:
                        self.assertTrue(left - 0.01 <= float(x) <= right + 0.01)
                        self.assertTrue(189.99 <= float(y) <= 610.01)


if __name__ == "__main__":
    unittest.main()
