// Overview of the six donning modules as plain bodies in one figure.
// Solid stand-ins built from Parameters.scad, not the module geometry itself: no halves,
// tabs or latch lands. Heights follow the module stack; the sideways positions of legs
// and arms and the height of belt and helmet are DISPLAY ASSUMPTIONS, not body measurements.
// Red marks where two stand-ins overlap with these assumptions.
include <Parameters.scad>

leg_spread_mm = -1;   // distance between the leg axes; -1 = half the hip width
arm_gap_mm = 10;      // air between torso side and upper arm
neck_gap_mm = 30;     // torso top to helmet bottom
$fn = 64;

assert(len(limbs_mm) == 8 && len(boots_mm) == 2, "limb and shoe dimensions required");
assert(len(torso_mm) == 3 && len(hip_mm) == 2 && len(helmet_mm) == 3, "torso, hip and helmet dimensions required");
assert(leg_spread_mm == -1 || leg_spread_mm > 0, "leg_spread_mm must be -1 or positive");

spread = leg_spread_mm < 0 ? hip_mm[0] / 2 : leg_spread_mm;
olive = [0.30, 0.38, 0.23];

function leg_x(column) = (column == 0 ? -1 : 1) * spread / 2;
function shin_z(column) = boot_height_mm + ankle_gap_mm;
function thigh_z(column) = shin_z(column) + limbs_mm[6 + column][1] + knee_gap_mm;
function thigh_top(column) = thigh_z(column) + limbs_mm[4 + column][1];
// The belt starts one joint gap above the higher thigh shell.
belt_z = max(thigh_top(0), thigh_top(1)) + knee_gap_mm;
torso_z = belt_z + belt_height_mm + belt_gap_mm;
shoulder_z = torso_z + torso_mm[2];
function arm_x(column) = (column == 0 ? -1 : 1) * (torso_mm[0] / 2 + arm_gap_mm + limbs_mm[column][0] / 2);

module tube(dims) { cylinder(h = dims[1], d = dims[0]); }
module box(w, d, h) { translate([-w / 2, -d / 2, 0]) cube([w, d, h]); }

module thigh(column) { translate([leg_x(column), 0, thigh_z(column)]) tube(limbs_mm[4 + column]); }
module shin(column) { translate([leg_x(column), 0, shin_z(column)]) tube(limbs_mm[6 + column]); }
module shoe(column) {
    translate([leg_x(column) - boots_mm[column][0] / 2, -boots_mm[column][1] * 0.73, 0])
        cube([boots_mm[column][0], boots_mm[column][1], boot_height_mm]);
}
module leg(column) { thigh(column); shin(column); shoe(column); }
module arm(column) {
    fore = limbs_mm[2 + column];
    upper = limbs_mm[column];
    translate([arm_x(column), 0, shoulder_z - 40 - upper[1]]) {
        tube(upper);
        translate([0, 0, -elbow_gap_mm - fore[1]]) tube(fore);
    }
}
module belt() { translate([0, 0, belt_z]) box(hip_mm[0], hip_mm[1], belt_height_mm); }
module torso() { translate([0, 0, torso_z]) box(torso_mm[0], torso_mm[1], torso_mm[2]); }
module helmet() {
    translate([0, 0, shoulder_z + neck_gap_mm]) intersection() {
        translate([0, 0, helmet_mm[2] * 0.45]) scale([helmet_mm[0] / 2, helmet_mm[1] / 2, helmet_mm[2] * 0.55]) sphere(r = 1);
        box(helmet_mm[0], helmet_mm[1], helmet_mm[2]);
    }
}

color(olive) { leg(0); leg(1); belt(); torso(); arm(0); arm(1); helmet(); }
// Overlaps between neighbours, enlarged slightly so they stay visible.
color("red") {
    scale([1.01, 1.01, 1]) intersection() { leg(0); leg(1); }
    for (column = [0, 1]) scale([1.01, 1.01, 1]) intersection() { leg(column); belt(); }
    for (column = [0, 1]) intersection() { arm(column); union() { torso(); belt(); } }
    intersection() { torso(); helmet(); }
}

echo(overall_height_mm = shoulder_z + neck_gap_mm + helmet_mm[2]);
echo(thigh_overlap_mm = (limbs_mm[4][0] + limbs_mm[5][0]) / 2 - spread);
