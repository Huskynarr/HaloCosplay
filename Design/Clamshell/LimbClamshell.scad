// Opening limb envelopes only. No authentic armor, real hinge or load approval.
include <Parameters.scad>

part = "forearm";
side = "l";
open_fraction = 0;
piece = "assembly";
$fn = 96;

part_index = part == "upperarm" ? 0 : part == "forearm" ? 1 : part == "thigh" ? 2 : part == "shin" ? 3 : -1;
assert(part_index >= 0, "part must be upperarm, forearm, thigh or shin");
assert(side == "l" || side == "r", "side must be l or r");
assert(piece == "assembly" || piece == "rear" || piece == "front", "piece must be assembly, rear or front");
assert(is_num(open_fraction) && open_fraction >= 0 && open_fraction <= 1, "open_fraction must be 0..1");
assert(is_num(wall_mm) && wall_mm > 0, "positive wall required");
assert(is_num(seam_gap_mm) && seam_gap_mm > 0, "positive seam gap required");
assert(is_num(hinge_offset_mm) && hinge_offset_mm >= 0, "nonnegative hinge offset required");
assert(is_num(opening_deg) && opening_deg > 0 && opening_deg <= 150, "opening angle must be 0..150 degrees");
assert(len(limbs_mm) == 8, "eight independent limb dimension pairs required");
index = 2 * part_index + (side == "l" ? 0 : 1);
diameter = limbs_mm[index][0];
length_mm = limbs_mm[index][1];
assert(is_num(diameter) && diameter > 2 * wall_mm + seam_gap_mm, "invalid diameter");
assert(is_num(length_mm) && length_mm > 0, "positive length required");
radius = diameter / 2;
handedness = side == "l" ? -1 : 1;
hinge_x = handedness * (radius + hinge_offset_mm);
angle = handedness * open_fraction * opening_deg;

// Model axes: Z along limb, negative Y towards front. Half shells remain open at both ends.
module half_shell(front = false) {
    intersection() {
        difference() {
            cylinder(h = length_mm, r = radius);
            translate([0, 0, -1]) cylinder(h = length_mm + 2, r = radius - wall_mm);
        }
        translate([-radius - 1, front ? -radius - 1 : seam_gap_mm / 2, -1])
            cube([diameter + 2, radius + 1 - seam_gap_mm / 2, length_mm + 2]);
    }
}

if (piece == "assembly" || piece == "rear") color([0.19, 0.28, 0.20]) half_shell();
if (piece == "assembly" || piece == "front")
    translate([hinge_x, 0, 0]) rotate([0, 0, angle]) translate([-hinge_x, 0, 0])
        color([0.45, 0.56, 0.28]) half_shell(true);

// Preview-only virtual pivot: excluded from render/STL, not a printed axle.
if ($preview && piece == "assembly")
    %translate([hinge_x, 0, -5]) cylinder(h = length_mm + 10, r = 1.5);
