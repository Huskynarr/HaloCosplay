// Helmet module: front shell and a rear shell that swings open sideways, one latch.
// Concept envelope only. No authentic helmet surface, visor, padding, real hinge,
// purchased latch, neck cover or impact protection.
include <Parameters.scad>

hinge_side = "l";
open_fraction = 0;
piece = "assembly";
$fn = 96;

assert(hinge_side == "l" || hinge_side == "r", "hinge_side must be l or r");
assert(piece == "assembly" || piece == "front" || piece == "rear", "piece must be assembly, front or rear");
assert(is_num(open_fraction) && open_fraction >= 0 && open_fraction <= 1, "open_fraction must be 0..1");
assert(is_num(wall_mm) && wall_mm > 0, "positive wall required");
assert(is_num(seam_gap_mm) && seam_gap_mm > 0, "positive seam gap required");
assert(is_num(hinge_offset_mm) && hinge_offset_mm >= 0, "nonnegative hinge offset required");
assert(is_num(helmet_opening_deg) && helmet_opening_deg > 0 && helmet_opening_deg <= 150, "helmet opening must be 0..150 degrees");
assert(len(helmet_mm) == 3, "helmet needs [width, depth, height]");
assert(is_num(helmet_split_fraction) && helmet_split_fraction > -0.3 && helmet_split_fraction < 0.3, "split must stay near the ears");
assert(len(latch_pad_mm) == 3, "latch pad needs [length, width, thickness]");
assert(is_num(latch_hole_d_mm) && latch_hole_d_mm >= 0, "nonnegative latch hole diameter required");
// Hole lists: [across, along] per hole. across = distance from the seam centre line on the
// land, along = offset along the seam from the middle of the land. Empty lists leave it blank.
function holes_fit(holes) = len([for (h = holes) if (!(len(h) == 2 && latch_hole_d_mm > 0 &&
    h[0] - latch_hole_d_mm / 2 >= seam_gap_mm / 2 && h[0] + latch_hole_d_mm / 2 <= seam_gap_mm / 2 + latch_pad_mm[1] &&
    abs(h[1]) + latch_hole_d_mm / 2 <= latch_pad_mm[0] / 2)) 1]) == 0;
assert(is_list(latch_holes_mm) && holes_fit(latch_holes_mm), "latch holes need a diameter and must lie on the land");
assert(is_list(keeper_holes_mm) && holes_fit(keeper_holes_mm), "keeper holes need a diameter and must lie on the land");

width = helmet_mm[0];
depth = helmet_mm[1];
height = helmet_mm[2];
assert(width > 8 * wall_mm && depth > 8 * wall_mm && height > 3 * latch_pad_mm[0], "helmet too small");

// Ellipsoid cut flat at the neck: centre at 45 % of the height, vertical half axis 55 %.
centre_z = height * 0.45;
half_z = height * 0.55;
split_y = depth * helmet_split_fraction;
pad_z = height * 0.22;
sign = hinge_side == "l" ? -1 : 1;
// Half width of the outer surface at the split and a given height.
function half_width(z) = width / 2 * sqrt(1 - pow(split_y / (depth / 2), 2) - pow((z - centre_z) / half_z, 2));
hinge_x = sign * (half_width(centre_z) + hinge_offset_mm);
swing = -sign * open_fraction * helmet_opening_deg;

module ellipsoid(inset) {
    translate([0, 0, centre_z]) scale([width / 2 - inset, depth / 2 - inset, half_z - inset]) sphere(r = 1);
}

module shell(rear) {
    intersection() {
        difference() {
            ellipsoid(0);
            ellipsoid(wall_mm);
        }
        translate([-width, rear ? split_y + seam_gap_mm / 2 : -2 * depth + split_y - seam_gap_mm / 2, 0])
            cube([2 * width, 2 * depth, height + 1]);
    }
}

// Flat land for the single purchased latch, on the side opposite the virtual hinge.
// The front shell carries the latch body (latch_holes_mm), the rear shell the keeper.
module latch_pad(rear) {
    x_surface = half_width(pad_z);
    pad_y = rear ? split_y + seam_gap_mm / 2 : split_y - seam_gap_mm / 2 - latch_pad_mm[1];
    difference() {
        translate([sign > 0 ? -x_surface - latch_pad_mm[2] : x_surface - 10, pad_y, pad_z - latch_pad_mm[0] / 2])
            cube([latch_pad_mm[2] + 10, latch_pad_mm[1], latch_pad_mm[0]]);
        ellipsoid(wall_mm);
        for (hole = rear ? keeper_holes_mm : latch_holes_mm)
                translate([-sign * x_surface, split_y + (rear ? 1 : -1) * hole[0], pad_z + hole[1]])
                    rotate([0, 90, 0]) cylinder(h = 2 * (latch_pad_mm[2] + wall_mm + 14), d = latch_hole_d_mm, center = true, $fn = 24);
    }
}

// Model axes: X to the wearer's right, negative Y front, Z up from the neck opening.
if (piece != "rear") color([0.45, 0.56, 0.28]) {
    difference() {
        shell(false);
        // Plain opening where the visor goes; the visor itself is not modelled.
        translate([-width * 0.4, -depth, height * 0.45]) cube([width * 0.8, depth * 0.72, height * 0.27]);
    }
    latch_pad(false);
}

if (piece != "front")
    translate([hinge_x, split_y, 0]) rotate([0, 0, swing]) translate([-hinge_x, -split_y, 0])
        color([0.19, 0.28, 0.20]) {
            shell(true);
            latch_pad(true);
        }

// Preview-only virtual pivot: excluded from render/STL, not a printed axle.
if ($preview && piece == "assembly")
    %translate([hinge_x, split_y, 0]) cylinder(h = height, r = 1.5);
