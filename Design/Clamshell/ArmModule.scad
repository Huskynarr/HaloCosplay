// Arm module: upper-arm and forearm opening envelopes that stay together as one unit.
// Concept envelopes only. No authentic armor, real hinge, purchased latch or load approval.
include <Parameters.scad>
include <ModuleCommon.scad>

side = "l";
open_fraction = 0;
elbow_flex_deg = 0;
piece = "assembly";
segment = "both";
$fn = 96;

assert(side == "l" || side == "r", "side must be l or r");
assert(piece == "assembly" || piece == "rear" || piece == "front", "piece must be assembly, rear or front");
assert(segment == "both" || segment == "upperarm" || segment == "forearm", "segment must be both, upperarm or forearm");
assert(is_num(open_fraction) && open_fraction >= 0 && open_fraction <= 1, "open_fraction must be 0..1");
assert(is_num(elbow_flex_deg) && elbow_flex_deg >= 0 && elbow_flex_deg <= 150, "elbow_flex_deg must be 0..150");
assert(is_num(elbow_relief_mm) && elbow_relief_mm >= 0, "nonnegative elbow relief required");

handedness = side == "l" ? -1 : 1;
column = side == "l" ? 0 : 1;
upper = limbs_mm[column];
fore = limbs_mm[2 + column];
assert(is_num(elbow_gap_mm) && elbow_gap_mm > 2 * lug_height, "elbow gap must clear both strap lugs");
assert(upper[0] > 2 * wall_mm + seam_gap_mm && fore[0] > 2 * wall_mm + seam_gap_mm, "invalid diameter");
assert(elbow_relief_mm < upper[1] / 3 && elbow_relief_mm < fore[1] / 3, "elbow relief too long for the shell");
assert(latch_pad_mm[0] < fore[1] - 2 * elbow_relief_mm, "latch pad longer than the front shell");

elbow_z = fore[1] + elbow_gap_mm / 2;
angle = handedness * open_fraction * opening_deg;
want_front = piece != "rear";
want_rear = piece != "front";

// Upper arm: shoulder hang lug on top, elbow link lug below. The front half is cut back at the elbow.
if (segment != "forearm")
    translate([0, 0, fore[1] + elbow_gap_mm])
        shell_segment(upper, true, true, [elbow_relief_mm, upper[1]], [0, upper[1]]);

// Forearm: elbow link lug on top; the whole segment follows the elbow pose.
if (segment != "upperarm")
    translate([0, 0, elbow_z]) rotate([-elbow_flex_deg, 0, 0]) translate([0, 0, -elbow_z])
        shell_segment(fore, true, false, [0, fore[1] - elbow_relief_mm], [0, fore[1]]);

// Preview-only textile link across the elbow; the real link is webbing, not a printed part.
if ($preview && piece == "assembly" && segment == "both" && elbow_flex_deg == 0)
    %translate([-strap_width_mm / 2, max(upper[0], fore[0]) / 2, fore[1] + lug_margin])
        cube([strap_width_mm, 1.5, elbow_gap_mm - 2 * lug_margin]);
