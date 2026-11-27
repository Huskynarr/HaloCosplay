// Leg module: thigh, knee pad, shin and shoe cover of one side as one unit.
// Concept envelopes only. No authentic armor, real hinge, purchased latch or load approval.
// Not a load-bearing leg strut and not part of the X01 drive.
include <Parameters.scad>
include <ModuleCommon.scad>

side = "l";
open_fraction = 0;
knee_flex_deg = 0;
piece = "assembly";
segment = "all";
$fn = 96;

assert(side == "l" || side == "r", "side must be l or r");
assert(piece == "assembly" || piece == "rear" || piece == "front", "piece must be assembly, rear or front");
assert(segment == "all" || segment == "thigh" || segment == "shin" || segment == "kneepad" || segment == "shoe",
       "segment must be all, thigh, shin, kneepad or shoe");
assert(is_num(open_fraction) && open_fraction >= 0 && open_fraction <= 1, "open_fraction must be 0..1");
assert(is_num(knee_flex_deg) && knee_flex_deg >= 0 && knee_flex_deg <= 150, "knee_flex_deg must be 0..150");
assert(len(boots_mm) == 2, "two shoe dimension pairs required");
assert(is_num(boot_height_mm) && boot_height_mm > 2 * wall_mm, "invalid shoe cover height");
assert(is_num(knee_relief_mm) && knee_relief_mm >= 0, "nonnegative knee relief required");
assert(is_num(ankle_gap_mm) && ankle_gap_mm > lug_height, "ankle gap must clear the strap lug");

handedness = side == "l" ? -1 : 1;
column = side == "l" ? 0 : 1;
thigh = limbs_mm[4 + column];
shin = limbs_mm[6 + column];
boot = boots_mm[column];
assert(is_num(knee_gap_mm) && knee_gap_mm > 0, "positive knee gap required");
assert(thigh[0] > 2 * wall_mm + seam_gap_mm && shin[0] > 2 * wall_mm + seam_gap_mm, "invalid diameter");
assert(knee_relief_mm < thigh[1] / 3 && knee_relief_mm < shin[1] / 3, "knee relief too long for the shell");
assert(boot[0] > 4 * wall_mm && boot[1] > boot[0], "invalid shoe cover dimensions");

shin_z = boot_height_mm + ankle_gap_mm;
knee_z = shin_z + shin[1] + knee_gap_mm / 2;
thigh_z = shin_z + shin[1] + knee_gap_mm;
angle = handedness * open_fraction * opening_deg;
want_front = piece != "rear";
want_rear = piece != "front";
// Strap tabs sit on the outer rear quarter, away from the back of the knee.
lug_azimuth = -handedness * 50;
pad_radius = max(thigh[0], shin[0]) / 2 + 6;
pad_height = knee_gap_mm + 80;
heel_y = boot[1] * 0.27;
toe_y = -boot[1] * 0.73;

// Arc over the front of the knee. It hangs on textile; no strap points are modelled.
module knee_pad() {
    color([0.45, 0.56, 0.28]) intersection() {
        translate([0, 0, -pad_height / 2]) difference() {
            cylinder(h = pad_height, r = pad_radius + wall_mm);
            translate([0, 0, -1]) cylinder(h = pad_height + 2, r = pad_radius);
        }
        translate([0, 0, -pad_height / 2 - 1]) linear_extrude(pad_height + 2)
            polygon([[0, 0], [-2 * pad_radius, -2 * pad_radius], [2 * pad_radius, -2 * pad_radius]]);
    }
}

module shoe_body(width, height, toe_inset, rear_extra) {
    hull() {
        translate([0, toe_y + boot[0] / 2, 0]) cylinder(h = height * 0.55, d = width - 2 * toe_inset);
        translate([-width / 2, -boot[1] * 0.2, 0]) cube([width, heel_y + boot[1] * 0.2 + rear_extra, height]);
    }
}

// Cap over the worn shoe: open below, open at the heel and slotted above the ankle,
// so it is set onto the shoe from the front. A heel strap through the two side slots closes it.
module shoe_cover() {
    ankle_d = min(boot[0] - 4 * wall_mm, shin[0] * 0.8);
    color([0.19, 0.28, 0.20]) difference() {
        shoe_body(boot[0], boot_height_mm, 0, 0);
        translate([0, 0, -wall_mm]) shoe_body(boot[0] - 2 * wall_mm, boot_height_mm, wall_mm, 1);
        translate([0, 0, boot_height_mm - wall_mm - 1]) cylinder(h = wall_mm + 2, d = ankle_d);
        translate([-ankle_d / 2, 0, boot_height_mm - wall_mm - 1]) cube([ankle_d, heel_y + 1, wall_mm + 2]);
        translate([-boot[0] / 2 - 1, heel_y - lug_margin - slot_height, boot_height_mm * 0.3])
            cube([boot[0] + 2, slot_height, strap_width_mm + 2]);
    }
}

// Thigh: hang lug to the hip belt on top, knee link lug below. The rear half is cut back at the knee.
if (segment == "all" || segment == "thigh")
    translate([0, 0, thigh_z])
        shell_segment(thigh, true, true, [0, thigh[1]], [knee_relief_mm, thigh[1]], lug_azimuth);

if ((segment == "all" && piece == "assembly") || segment == "kneepad")
    translate([0, 0, knee_z]) rotate([knee_flex_deg / 2, 0, 0]) knee_pad();

// Shin and shoe cover follow the knee pose; the knee bends backwards.
translate([0, 0, knee_z]) rotate([knee_flex_deg, 0, 0]) translate([0, 0, -knee_z]) {
    if (segment == "all" || segment == "shin")
        translate([0, 0, shin_z])
            shell_segment(shin, true, true, [0, shin[1]], [0, shin[1] - knee_relief_mm], lug_azimuth);
    if ((segment == "all" && piece == "assembly") || segment == "shoe")
        shoe_cover();
}
