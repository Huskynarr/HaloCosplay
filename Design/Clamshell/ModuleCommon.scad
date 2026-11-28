// Shared building blocks of the limb modules (ArmModule.scad, LegModule.scad).
// Included after Parameters.scad. The including file defines handedness, angle,
// piece, want_front and want_rear. Concept envelopes only, nothing here is sized.
lug_margin = 6;
slot_height = 4;
lug_height = 2 * lug_margin + slot_height;
lug_overlap = 12;

assert(is_num(wall_mm) && wall_mm > 0, "positive wall required");
assert(is_num(seam_gap_mm) && seam_gap_mm > 0, "positive seam gap required");
assert(is_num(hinge_offset_mm) && hinge_offset_mm >= 0, "nonnegative hinge offset required");
assert(is_num(opening_deg) && opening_deg > 0 && opening_deg <= 150, "opening angle must be 0..150 degrees");
assert(len(limbs_mm) == 8, "eight independent limb dimension pairs required");
assert(is_num(strap_width_mm) && strap_width_mm > 0, "positive strap width required");
assert(len(latch_pad_mm) == 3, "latch pad needs [length, width, thickness]");
assert(is_num(latch_hole_d_mm) && latch_hole_d_mm >= 0, "nonnegative latch hole diameter required");
// Hole lists: [across, along] per hole. across = distance from the seam centre line on the
// land, along = offset along the seam from the middle of the land. Empty lists leave it blank.
function holes_fit(holes) = len([for (h = holes) if (!(len(h) == 2 && latch_hole_d_mm > 0 &&
    h[0] - latch_hole_d_mm / 2 >= seam_gap_mm / 2 && h[0] + latch_hole_d_mm / 2 <= seam_gap_mm / 2 + latch_pad_mm[1] &&
    abs(h[1]) + latch_hole_d_mm / 2 <= latch_pad_mm[0] / 2)) 1]) == 0;
assert(is_list(latch_holes_mm) && holes_fit(latch_holes_mm), "latch holes need a diameter and must lie on the land");
assert(is_list(keeper_holes_mm) && holes_fit(keeper_holes_mm), "keeper holes need a diameter and must lie on the land");

assert(is_num(hinge_pin_d_mm) && hinge_pin_d_mm > 0, "positive hinge pin diameter required");
assert(is_num(hinge_knuckle_mm) && hinge_knuckle_mm >= 8, "hinge knuckles need at least 8 mm");
assert(is_num(hinge_clearance_mm) && hinge_clearance_mm >= 0, "nonnegative hinge clearance required");
knuckle_r = hinge_pin_d_mm / 2 + 3;
assert(hinge_offset_mm >= knuckle_r + 1.5, "hinge offset too small for the knuckle barrel");
assert(is_num(split_lap_mm) && split_lap_mm > 0, "positive split lap required");
assert(is_num(split_z_mm) && split_z_mm >= 0, "split_z_mm must be 0 (off) or a height along the shell");
assert(split_keep == "all" || split_keep == "lower" || split_keep == "upper", "split_keep must be all, lower or upper");

// Keeps one side of a lap joint across a shell: the lower piece carries the inner half of
// the wall through the lap, the upper piece the outer half. split_z_mm = 0 or "all" keeps everything.
module split_region(radius) {
    if (split_z_mm <= 0 || split_keep == "all") children();
    else intersection() {
        children();
        if (split_keep == "lower") union() {
            translate([-2 * radius, -2 * radius, -1000]) cube([4 * radius, 4 * radius, 1000 + split_z_mm]);
            translate([0, 0, split_z_mm - 0.01]) cylinder(h = split_lap_mm, r = radius - wall_mm / 2 - 0.1);
        } else difference() {
            translate([-2 * radius, -2 * radius, split_z_mm + 0.1]) cube([4 * radius, 4 * radius, 2000]);
            translate([0, 0, split_z_mm]) cylinder(h = split_lap_mm + 0.1, r = radius - wall_mm / 2 + 0.1);
        }
    }
}

// One hinge knuckle on the outer side: a barrel around the pin axis, joined to the shell edge.
module knuckle(dims, front, z0, z1) {
    radius = dims[0] / 2;
    hinge_x = handedness * (radius + hinge_offset_mm);
    difference() {
        hull() {
            translate([hinge_x, 0, z0]) cylinder(h = z1 - z0, r = knuckle_r, $fn = 32);
            translate([handedness > 0 ? radius - 1 : -radius - 1, front ? -seam_gap_mm / 2 - 5 : seam_gap_mm / 2, z0])
                cube([2, 5, z1 - z0]);
        }
        translate([hinge_x, 0, z0 - 1]) cylinder(h = z1 - z0 + 2, d = hinge_pin_d_mm + 0.4, $fn = 24);
        translate([0, 0, z0 - 1]) cylinder(h = z1 - z0 + 2, r = radius - 0.5);
    }
}

// Alternating knuckles over the length both halves share: even ones on the rear half, odd ones on the front.
module knuckles(dims, front, low, high) {
    count = max(3, floor((high - low) / hinge_knuckle_mm));
    step = (high - low) / count;
    for (i = [0 : count - 1])
        if ((i % 2 == 1) == front)
            knuckle(dims, front, low + i * step + hinge_clearance_mm / 2, low + (i + 1) * step - hinge_clearance_mm / 2);
}

// Model axes: Z along the limb (far end at 0), negative Y towards the front.
// Each half covers low..high along Z so that a joint end can be cut back.
module half_shell(dims, front, low, high) {
    radius = dims[0] / 2;
    intersection() {
        difference() {
            cylinder(h = dims[1], r = radius);
            translate([0, 0, -1]) cylinder(h = dims[1] + 2, r = radius - wall_mm);
        }
        translate([-radius - 1, front ? -radius - 1 : seam_gap_mm / 2, low])
            cube([dims[0] + 2, radius + 1 - seam_gap_mm / 2, high - low]);
    }
}

// Flat mounting land for a purchased latch on the closing side, opposite the virtual hinge.
// The front half carries the latch body (latch_holes_mm), the rear half the keeper
// (keeper_holes_mm). Holes appear only once the lists are filled from the datasheet.
module latch_pad(dims, front) {
    radius = dims[0] / 2;
    pad_y = front ? -seam_gap_mm / 2 - latch_pad_mm[1] : seam_gap_mm / 2;
    difference() {
        translate([handedness > 0 ? -radius - latch_pad_mm[2] : radius - 6, pad_y, (dims[1] - latch_pad_mm[0]) / 2])
            cube([latch_pad_mm[2] + 6, latch_pad_mm[1], latch_pad_mm[0]]);
        translate([0, 0, -1]) cylinder(h = dims[1] + 2, r = radius - wall_mm);
        for (hole = front ? latch_holes_mm : keeper_holes_mm)
                translate([-handedness * (radius - wall_mm - 2), (front ? -1 : 1) * hole[0], dims[1] / 2 + hole[1]])
                    rotate([0, 90, 0]) cylinder(h = 2 * (latch_pad_mm[2] + wall_mm + 10), d = latch_hole_d_mm, center = true, $fn = 24);
    }
}

// Tab with a webbing slot on the rear half. direction 1 = beyond the upper end at z_end,
// -1 = beyond the lower end. azimuth turns the tab around the limb axis, 0 = straight back.
module strap_lug(dims, direction, z_end, azimuth = 0) {
    radius = dims[0] / 2;
    width = strap_width_mm + 2 * lug_margin;
    z_low = direction > 0 ? z_end - lug_overlap : z_end - lug_height;
    slot_z = direction > 0 ? z_end + lug_margin : z_end - lug_margin - slot_height;
    rotate([0, 0, azimuth]) difference() {
        translate([-width / 2, radius - wall_mm - 3, z_low]) cube([width, wall_mm + 3, lug_overlap + lug_height]);
        translate([0, 0, z_low - 1]) cylinder(h = lug_overlap + lug_height + 2, r = radius - wall_mm);
        translate([-strap_width_mm / 2 - 1, radius - wall_mm - 10, slot_z]) cube([strap_width_mm + 2, wall_mm + 20, slot_height]);
    }
}

// One opening shell. front_range and rear_range are [low, high] along Z.
module shell_segment(dims, lug_top, lug_bottom, front_range, rear_range, lug_azimuth = 0) {
    hinge_x = handedness * (dims[0] / 2 + hinge_offset_mm);
    hinge_low = max(front_range[0], rear_range[0]);
    hinge_high = min(front_range[1], rear_range[1]);
    if (want_rear) color([0.19, 0.28, 0.20]) split_region(dims[0] / 2) {
        half_shell(dims, false, rear_range[0], rear_range[1]);
        knuckles(dims, false, hinge_low, hinge_high);
        latch_pad(dims, false);
        if (lug_top) strap_lug(dims, 1, rear_range[1], lug_azimuth);
        if (lug_bottom) strap_lug(dims, -1, rear_range[0], lug_azimuth);
    }
    if (want_front)
        translate([hinge_x, 0, 0]) rotate([0, 0, angle]) translate([-hinge_x, 0, 0])
            color([0.45, 0.56, 0.28]) split_region(dims[0] / 2) {
                half_shell(dims, true, front_range[0], front_range[1]);
                knuckles(dims, true, hinge_low, hinge_high);
                latch_pad(dims, true);
            }
    // Preview-only hinge pin: a purchased rod, excluded from render/STL.
    if ($preview && piece == "assembly")
        %translate([hinge_x, 0, hinge_low - 3]) cylinder(h = hinge_high - hinge_low + 6, d = hinge_pin_d_mm, $fn = 16);
}
