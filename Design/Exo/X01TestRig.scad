// X01 test rig: holds ONE actuator on a base board and lets a lever press on a scale.
// For verification steps P1 and P2 only, without a person. NOT SIZED FOR LOAD: the
// bracket, the lever and above all the travel limiter must be checked before power-up.
include <Parameters.scad>

part = "assembly"; // assembly, bracket, lever, limiter
$fn = 72;

assert(part == "assembly" || part == "bracket" || part == "lever" || part == "limiter", "unknown part");
assert(rig_axis_h_mm > actuator_d_mm / 2 + plate_t_mm + 5, "axis too low for the actuator");
assert(rig_lever_mm > actuator_d_mm, "lever too short");
assert(rig_stop_gap_mm > 0 && rig_stop_gap_mm < rig_axis_h_mm / 2, "invalid limiter gap");

plate_r = actuator_d_mm / 2 + 4;
centre_hole_r = flange_d_mm / 2 + 2;
foot_w = 2 * plate_r + 40;
hub_r = centre_hole_r - 3;
limiter_w = 30;

module ring_holes(circle_d, count, hole_d, turn = 0) {
    for (i = [0 : count - 1]) rotate(turn + i * 360 / count) translate([circle_d / 2, 0]) circle(d = hole_d, $fn = 24);
}

// Upright plate on a foot. The actuator bolts on with its output towards the lever side (-Y).
// Model axes: X along the lever, Y along the output axis, Z up from the board.
module bracket() {
    // Upright: sketch in X/Z, thickness along Y.
    translate([0, plate_t_mm, 0]) rotate([90, 0, 0]) linear_extrude(plate_t_mm) difference() {
        union() {
            translate([0, rig_axis_h_mm]) circle(r = plate_r);
            translate([-plate_r, 0]) square([2 * plate_r, rig_axis_h_mm]);
        }
        translate([0, rig_axis_h_mm]) {
            circle(r = centre_hole_r);
            ring_holes(housing_bolt_circle_mm, housing_bolt_count, housing_bolt_clear_mm, 22.5);
        }
    }
    // Foot behind the upright, under the actuator, with four holes for the board.
    difference() {
        translate([-foot_w / 2, 0, 0]) cube([foot_w, rig_foot_depth_mm, plate_t_mm]);
        for (x = [-foot_w / 2 + 12, foot_w / 2 - 12]) for (y = [18, rig_foot_depth_mm - 12])
            translate([x, y, -1]) cylinder(h = plate_t_mm + 2, d = rig_board_screw_d_mm, $fn = 24);
    }
    // Two gussets outside the actuator.
    for (x = [-plate_r, plate_r - plate_t_mm])
        translate([x, plate_t_mm, plate_t_mm]) rotate([90, 0, 90]) linear_extrude(plate_t_mm)
            polygon([[0, 0], [rig_foot_depth_mm - plate_t_mm - 5, 0], [0, rig_axis_h_mm * 0.6]]);
}

// Lever on the output flange. The tip hole takes a bolt whose head rests on the scale;
// its centre is exactly rig_lever_mm from the axis, which is the lever arm of the measurement.
module lever() {
    hub_h = plate_t_mm + arm_gap_mm - flange_protrusion_mm;
    rotate([90, 0, 0]) difference() {
        union() {
            linear_extrude(arm_t_mm) {
                circle(r = hub_r);
                translate([0, -bar_w_mm / 2]) square([rig_lever_mm, bar_w_mm]);
                translate([rig_lever_mm, 0]) circle(d = bar_w_mm);
            }
            translate([0, 0, -hub_h]) linear_extrude(hub_h) circle(r = hub_r);
        }
        translate([0, 0, -hub_h - 1]) linear_extrude(arm_t_mm + hub_h + 2) {
            ring_holes(output_bolt_circle_mm, output_bolt_count, output_bolt_clear_mm);
            translate([rig_lever_mm, 0]) circle(d = joint_bolt_d_mm, $fn = 24);
        }
        translate([0, 0, -hub_h - 1]) linear_extrude(2.5) circle(d = flange_spigot_d_mm + 0.4);
    }
}

// Fork around the lever near its tip: limits the travel in both directions if the
// actuator runs away. Screws to the board; the scale stands beside it under the tip.
module limiter() {
    slot = bar_w_mm + 2 * rig_stop_gap_mm;
    height = rig_axis_h_mm + slot / 2 + 15;
    difference() {
        union() {
            translate([-limiter_w / 2, -25, 0]) cube([limiter_w, 50, height]);
            translate([-limiter_w / 2 - 25, -25, 0]) cube([limiter_w + 50, 50, plate_t_mm]);
        }
        translate([-limiter_w / 2 - 1, -12, rig_axis_h_mm - slot / 2]) cube([limiter_w + 2, 24, slot]);
        for (x = [-limiter_w / 2 - 13, limiter_w / 2 + 13]) for (y = [-13, 13])
            translate([x, y, -1]) cylinder(h = plate_t_mm + 2, d = rig_board_screw_d_mm, $fn = 24);
    }
}

lever_y = -(arm_gap_mm + arm_t_mm);
if (part == "assembly") {
    color([0.25, 0.35, 0.40]) bracket();
    color([0.80, 0.51, 0.15]) translate([0, lever_y + arm_t_mm, rig_axis_h_mm]) lever();
    color([0.55, 0.60, 0.62]) translate([rig_lever_mm * 0.8, lever_y + arm_t_mm / 2, 0]) limiter();
    if ($preview) {
        // Actuator behind the upright, base board and the place of the scale.
        %translate([0, plate_t_mm, rig_axis_h_mm]) rotate([-90, 0, 0]) cylinder(h = actuator_h_mm - flange_protrusion_mm, d = actuator_d_mm);
        %translate([-foot_w / 2 - 20, -80, -18]) cube([rig_lever_mm + foot_w / 2 + 80, 80 + rig_foot_depth_mm + 20, 18]);
        %translate([rig_lever_mm - 40, lever_y - 40, 0]) cube([80, 80, rig_axis_h_mm - bar_w_mm / 2 - 8]);
    }
}
if (part == "bracket") bracket();
if (part == "lever") lever();
if (part == "limiter") limiter();
