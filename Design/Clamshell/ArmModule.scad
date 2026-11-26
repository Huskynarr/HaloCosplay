// Arm module: upper-arm and forearm opening envelopes that stay together as one unit.
// Concept envelopes only. No authentic armor, real hinge, purchased latch or load approval.
include <Parameters.scad>

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
assert(is_num(wall_mm) && wall_mm > 0, "positive wall required");
assert(is_num(seam_gap_mm) && seam_gap_mm > 0, "positive seam gap required");
assert(is_num(hinge_offset_mm) && hinge_offset_mm >= 0, "nonnegative hinge offset required");
assert(is_num(opening_deg) && opening_deg > 0 && opening_deg <= 150, "opening angle must be 0..150 degrees");
assert(len(limbs_mm) == 8, "eight independent limb dimension pairs required");
assert(is_num(strap_width_mm) && strap_width_mm > 0, "positive strap width required");
assert(is_num(elbow_relief_mm) && elbow_relief_mm >= 0, "nonnegative elbow relief required");
assert(len(latch_pad_mm) == 3, "latch pad needs [length, width, thickness]");

handedness = side == "l" ? -1 : 1;
column = side == "l" ? 0 : 1;
upper = limbs_mm[column];
fore = limbs_mm[2 + column];
lug_margin = 6;
slot_height = 4;
lug_height = 2 * lug_margin + slot_height;
lug_overlap = 12;
assert(is_num(elbow_gap_mm) && elbow_gap_mm > 2 * lug_height, "elbow gap must clear both strap lugs");
assert(upper[0] > 2 * wall_mm + seam_gap_mm && fore[0] > 2 * wall_mm + seam_gap_mm, "invalid diameter");
assert(elbow_relief_mm < upper[1] / 3 && elbow_relief_mm < fore[1] / 3, "elbow relief too long for the shell");
assert(latch_pad_mm[0] < fore[1] - 2 * elbow_relief_mm, "latch pad longer than the front shell");

elbow_z = fore[1] + elbow_gap_mm / 2;
angle = handedness * open_fraction * opening_deg;
want_front = piece != "rear";
want_rear = piece != "front";

// Model axes: Z along the arm (hand end at 0), negative Y towards the front.
// The front half is shortened by elbow_relief_mm at the elbow end.
module half_shell(dims, front, low, high) {
    radius = dims[0] / 2;
    intersection() {
        difference() {
            cylinder(h = dims[1], r = radius);
            translate([0, 0, -1]) cylinder(h = dims[1] + 2, r = radius - wall_mm);
        }
        translate([-radius - 1, front ? -radius - 1 : seam_gap_mm / 2, front ? low : -1])
            cube([dims[0] + 2, radius + 1 - seam_gap_mm / 2, front ? high - low : dims[1] + 2]);
    }
}

// Flat mounting land for a purchased latch on the closing side, opposite the virtual hinge.
module latch_pad(dims, front) {
    radius = dims[0] / 2;
    difference() {
        translate([handedness > 0 ? -radius - latch_pad_mm[2] : radius - 6,
                   front ? -seam_gap_mm / 2 - latch_pad_mm[1] : seam_gap_mm / 2,
                   (dims[1] - latch_pad_mm[0]) / 2])
            cube([latch_pad_mm[2] + 6, latch_pad_mm[1], latch_pad_mm[0]]);
        translate([0, 0, -1]) cylinder(h = dims[1] + 2, r = radius - wall_mm);
    }
}

// Tab with a webbing slot at the rear of a shell end. direction 1 = beyond the upper end.
module strap_lug(dims, direction) {
    radius = dims[0] / 2;
    width = strap_width_mm + 2 * lug_margin;
    z_low = direction > 0 ? dims[1] - lug_overlap : -lug_height;
    slot_z = direction > 0 ? dims[1] + lug_margin : -lug_margin - slot_height;
    difference() {
        translate([-width / 2, radius - wall_mm - 3, z_low]) cube([width, wall_mm + 3, lug_overlap + lug_height]);
        translate([0, 0, z_low - 1]) cylinder(h = lug_overlap + lug_height + 2, r = radius - wall_mm);
        translate([-strap_width_mm / 2 - 1, radius - wall_mm - 10, slot_z]) cube([strap_width_mm + 2, wall_mm + 20, slot_height]);
    }
}

module shell_segment(dims, lug_top, lug_bottom, front_low, front_high) {
    hinge_x = handedness * (dims[0] / 2 + hinge_offset_mm);
    if (want_rear) color([0.19, 0.28, 0.20]) {
        half_shell(dims, false, 0, dims[1]);
        latch_pad(dims, false);
        if (lug_top) strap_lug(dims, 1);
        if (lug_bottom) strap_lug(dims, -1);
    }
    if (want_front)
        translate([hinge_x, 0, 0]) rotate([0, 0, angle]) translate([-hinge_x, 0, 0])
            color([0.45, 0.56, 0.28]) {
                half_shell(dims, true, front_low, front_high);
                latch_pad(dims, true);
            }
    // Preview-only virtual pivot: excluded from render/STL, not a printed axle.
    if ($preview && piece == "assembly")
        %translate([hinge_x, 0, -5]) cylinder(h = dims[1] + 10, r = 1.5);
}

// Upper arm: shoulder hang lug on top, elbow link lug below.
if (segment != "forearm")
    translate([0, 0, fore[1] + elbow_gap_mm])
        shell_segment(upper, true, true, elbow_relief_mm, upper[1]);

// Forearm: elbow link lug on top; the whole segment follows the elbow pose.
if (segment != "upperarm")
    translate([0, 0, elbow_z]) rotate([-elbow_flex_deg, 0, 0]) translate([0, 0, -elbow_z])
        shell_segment(fore, true, false, 0, fore[1] - elbow_relief_mm);

// Preview-only textile link across the elbow; the real link is webbing, not a printed part.
if ($preview && piece == "assembly" && segment == "both" && elbow_flex_deg == 0)
    %translate([-strap_width_mm / 2, max(upper[0], fore[0]) / 2, fore[1] + lug_margin])
        cube([strap_width_mm, 1.5, elbow_gap_mm - 2 * lug_margin]);
