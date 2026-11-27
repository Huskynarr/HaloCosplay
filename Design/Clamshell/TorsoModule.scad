// Torso module: two sliding rear wings, two front doors, belt band and the hang points
// for arm and leg modules. Concept envelopes only. No carrier, real hinge, slide rail,
// purchased latch or load approval; the fixed spine carrier is not modelled.
include <Parameters.scad>

side = "l";
open_fraction = 0;
piece = "assembly";
$fn = 48;

assert(side == "l" || side == "r", "side must be l or r");
assert(piece == "assembly" || piece == "rear" || piece == "door" || piece == "belt_rear" || piece == "belt_door",
       "piece must be assembly, rear, door, belt_rear or belt_door");
assert(is_num(open_fraction) && open_fraction >= 0 && open_fraction <= 1, "open_fraction must be 0..1");
assert(is_num(wall_mm) && wall_mm > 0, "positive wall required");
assert(is_num(seam_gap_mm) && seam_gap_mm > 0, "positive seam gap required");
assert(is_num(opening_deg) && opening_deg > 0 && opening_deg <= 150, "opening angle must be 0..150 degrees");
assert(len(torso_mm) == 3 && len(hip_mm) == 2, "torso needs [width, depth, height], hip [width, depth]");
assert(is_num(entry_slide_mm) && entry_slide_mm >= 0, "nonnegative entry slide required");
assert(is_num(belt_height_mm) && belt_height_mm > 0 && is_num(belt_gap_mm) && belt_gap_mm > 0, "invalid belt band");
assert(is_num(strap_width_mm) && strap_width_mm > 0, "positive strap width required");
assert(len(latch_pad_mm) == 3, "latch pad needs [length, width, thickness]");
assert(is_num(latch_hole_spacing_mm) && latch_hole_spacing_mm >= 0, "nonnegative latch hole spacing required");
assert(is_num(latch_hole_d_mm) && latch_hole_d_mm >= 0, "nonnegative latch hole diameter required");
assert(latch_hole_spacing_mm + latch_hole_d_mm < latch_pad_mm[0], "latch holes do not fit on the pad");
assert(latch_hole_d_mm < latch_pad_mm[1], "latch hole wider than the pad");

chamfer = 18;
lug_margin = 6;
slot_height = 4;
lug_width = strap_width_mm + 2 * lug_margin;
lug_height = 2 * lug_margin + slot_height;
torso_z = belt_height_mm + belt_gap_mm;
assert(torso_mm[0] > 4 * chamfer && torso_mm[1] > 4 * chamfer && torso_mm[2] > 3 * latch_pad_mm[0], "torso too small");
assert(hip_mm[0] > 4 * chamfer && hip_mm[1] > 4 * chamfer, "hip too small");

// The motion follows the entry concept: wings slide apart first, then the doors swing out.
slide = entry_slide_mm * min(1, open_fraction * 4);
swing = opening_deg * max(0, (open_fraction - 0.25) / 0.75);

// Model axes: X to the wearer's right (side l is negative X), negative Y front, Z up.
module outline(w, d) {
    polygon([[-w / 2 + chamfer, -d / 2], [w / 2 - chamfer, -d / 2], [w / 2, -d / 2 + chamfer],
             [w / 2, d / 2 - chamfer], [w / 2 - chamfer, d / 2], [-w / 2 + chamfer, d / 2],
             [-w / 2, d / 2 - chamfer], [-w / 2, -d / 2 + chamfer]]);
}

module quadrant(w, d, h, sign, front) {
    intersection() {
        linear_extrude(height = h) difference() {
            outline(w, d);
            offset(delta = -wall_mm) outline(w, d);
        }
        translate([sign > 0 ? seam_gap_mm / 2 : -w, front ? -d : seam_gap_mm / 2, -1])
            cube([w - seam_gap_mm / 2, d - seam_gap_mm / 2, h + 2]);
    }
}

// Flat land for a purchased latch on the front of a door or belt half, next to the centre seam.
module front_pad(d, sign, z) {
    x0 = sign > 0 ? seam_gap_mm / 2 : -seam_gap_mm / 2 - latch_pad_mm[1];
    difference() {
        translate([x0, -d / 2 - latch_pad_mm[2], z - latch_pad_mm[0] / 2])
            cube([latch_pad_mm[1], latch_pad_mm[2] + 1, latch_pad_mm[0]]);
        if (latch_hole_spacing_mm > 0 && latch_hole_d_mm > 0)
            for (offset = [-0.5, 0.5])
                translate([x0 + latch_pad_mm[1] / 2, -d / 2, z + offset * latch_hole_spacing_mm])
                    rotate([90, 0, 0]) cylinder(h = 2 * (latch_pad_mm[2] + wall_mm + 5), d = latch_hole_d_mm, center = true, $fn = 24);
    }
}

// Webbing tab; up = true stands above z, otherwise hangs below it.
module hang_lug(x, y, z, up) {
    translate([x - lug_width / 2, y - wall_mm - 3, up ? z - 12 : z - lug_height]) difference() {
        cube([lug_width, wall_mm + 3, 12 + lug_height]);
        translate([lug_margin - 1, -1, up ? 12 + lug_margin : lug_margin])
            cube([strap_width_mm + 2, wall_mm + 5, slot_height]);
    }
}

// Rear wing: carries the hang point of one arm module on top.
module rear_wing(sign) {
    color([0.19, 0.28, 0.20]) translate([0, 0, torso_z]) {
        quadrant(torso_mm[0], torso_mm[1], torso_mm[2], sign, false);
        hang_lug(sign * (torso_mm[0] / 2 - chamfer - lug_width / 2), torso_mm[1] / 2, torso_mm[2], true);
    }
}

// Front door with two latch lands at the centre seam.
module door(sign) {
    color([0.45, 0.56, 0.28]) translate([0, 0, torso_z]) {
        quadrant(torso_mm[0], torso_mm[1], torso_mm[2], sign, true);
        for (z = [torso_mm[2] * 0.3, torso_mm[2] * 0.75]) front_pad(torso_mm[1], sign, z);
    }
}

// Rear belt half: carries the hang point of one leg module below.
module belt_rear(sign) {
    color([0.19, 0.28, 0.20]) {
        quadrant(hip_mm[0], hip_mm[1], belt_height_mm, sign, false);
        hang_lug(sign * (hip_mm[0] / 2 - chamfer - lug_width / 2), hip_mm[1] / 2, 0, false);
    }
}

module belt_door(sign) {
    color([0.45, 0.56, 0.28]) {
        quadrant(hip_mm[0], hip_mm[1], belt_height_mm, sign, true);
        front_pad(hip_mm[1], sign, belt_height_mm / 2);
    }
}

module swung(sign, w) {
    translate([sign * (w / 2 + slide), 0, 0]) rotate([0, 0, sign * swing]) translate([-sign * w / 2, 0, 0]) children();
}

if (piece == "assembly") {
    for (sign = [-1, 1]) {
        translate([sign * slide, 0, 0]) { rear_wing(sign); belt_rear(sign); }
        swung(sign, torso_mm[0]) door(sign);
        swung(sign, hip_mm[0]) belt_door(sign);
        // Preview-only: virtual door pivot and the textile-mounted shoulder cap.
        if ($preview) {
            %translate([sign * (torso_mm[0] / 2 + slide), 0, 0]) cylinder(h = torso_z + torso_mm[2], r = 1.5);
            %translate([sign * (shoulder_span_mm / 2 + slide), 0, torso_z + torso_mm[2] - 40])
                cube([125, torso_mm[1] * 0.65, 125], center = true);
        }
    }
} else {
    sign = side == "l" ? -1 : 1;
    if (piece == "rear") rear_wing(sign);
    if (piece == "door") door(sign);
    if (piece == "belt_rear") belt_rear(sign);
    if (piece == "belt_door") belt_door(sign);
}
