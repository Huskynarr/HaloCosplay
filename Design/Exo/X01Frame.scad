// X01 leg drive: mechanical concept of pelvis frame, hip module, thigh strut and cuff.
// NOT SIZED FOR LOAD, NOT BUILT, NOT TESTED. Shapes show interfaces and motion only.
// Stage K (knee) is a preview placeholder; its compensation mechanism is open.
include <Parameters.scad>

part = "assembly"; // assembly, motor_plate, output_arm, strut, cuff, pelvis_frame
side = "l";
hip_flex_deg = 0;      // assembly: positive swings the thigh forwards
abduction_deg = 0;     // assembly: positive swings the leg outwards
show_stage_k = false;  // assembly: knee actuator placeholder
$fn = 72;

assert(part == "assembly" || part == "motor_plate" || part == "output_arm" || part == "strut" ||
       part == "cuff" || part == "pelvis_frame", "unknown part");
assert(side == "l" || side == "r", "side must be l or r");
assert(is_num(abduction_deg) && abduction_deg >= 0 && abduction_deg <= 30, "abduction_deg must be 0..30");
assert(stop_extension_deg > 0 && stop_flexion_deg > 0, "stops must be positive angles");
assert(is_num(hip_flex_deg) && hip_flex_deg >= -stop_extension_deg && hip_flex_deg <= stop_flexion_deg,
       "hip_flex_deg lies beyond the mechanical stops");
assert(plate_t_mm > 0 && arm_t_mm > 0 && bar_t_mm > 0, "positive thickness required");
assert(arm_gap_mm >= 1, "arm gap too small");
assert(flange_d_mm < housing_bolt_circle_mm - 20, "no room for the stops between flange and housing screws");
assert(hip_to_cuff_mm > actuator_d_mm + 3 * hole_pitch_mm, "cuff too close to the hip axis");
assert(abduction_axis_z_mm > actuator_d_mm / 2 + 25, "abduction hinge too close to the actuator");

// Stack along the lateral direction, measured outwards from the body side of the output arm:
// output arm | gap | motor plate | actuator. The hub reaches the output flange through the plate.
hub_h = plate_t_mm + arm_gap_mm - flange_protrusion_mm;
assert(hub_h > 0, "plate and gap thinner than the flange protrusion");
housing_face_x = arm_t_mm + hub_h + flange_protrusion_mm;
plate_x = housing_face_x - plate_t_mm;
plate_centre_x = plate_x + plate_t_mm / 2;
plate_r = actuator_d_mm / 2 + 4;
centre_hole_r = flange_d_mm / 2 + 2;

// Stops: the bar of the output arm runs between two blocks on the motor plate.
stop_r_in = centre_hole_r + 2;
stop_r_out = housing_bolt_circle_mm / 2 - 5;
assert(stop_r_out - stop_r_in >= 6, "stop band too narrow");
assert(bar_w_mm / 2 < stop_r_in, "arm bar too wide for the stop band");
// Half angle of the bar where it first meets a block, at the inner radius of the stop band.
bar_half_deg = asin(bar_w_mm / 2 / stop_r_in);
block_deg = 14;
assert(stop_extension_deg + stop_flexion_deg + 2 * bar_half_deg + 2 * block_deg < 330, "stops overlap");
assert(frame_bar_h_mm >= strap_width_mm + 14, "frame bar too low for the belt slots");

arm_len = actuator_d_mm / 2 + 2 * hole_pitch_mm + 15;
strut_len = hip_to_cuff_mm - arm_len + 2 * hole_pitch_mm + 15 + cuff_h_mm / 2;
strut_holes = floor((strut_len - 30) / hole_pitch_mm) + 1;
cuff_r = thigh_cuff_d_mm / 2 + cuff_padding_mm;
// The cuff moves along the hole row in steps; it sits on the pair of holes nearest to hip_to_cuff_mm.
first_hole_z = -arm_len + 15 + hole_pitch_mm;
cuff_step = max(1, round((hip_to_cuff_mm + first_hole_z - hole_pitch_mm / 2) / hole_pitch_mm));
cuff_z = first_hole_z - cuff_step * hole_pitch_mm - hole_pitch_mm / 2;
assert(cuff_step + 1 <= strut_holes - 1, "cuff beyond the hole row");
hinge_block = [18, 30, 22];   // lateral, fore-aft, vertical
ear_t = 8;
frame_z = abduction_axis_z_mm + hinge_block[2] / 2 + 6;

// 2D sketch in the side view (x2 = backwards, y2 = up), thickness outwards.
module side_plate(t) { rotate([90, 0, 90]) linear_extrude(t) children(); }
module ring_holes(circle_d, count, hole_d, turn = 0) {
    for (i = [0 : count - 1]) rotate(turn + i * 360 / count) translate([circle_d / 2, 0]) circle(d = hole_d, $fn = 24);
}
// Annular sector between two angles measured from straight up towards the back.
module sector(r_in, r_out, from_deg, to_deg) {
    steps = 8;
    points = concat([for (i = [0 : steps]) let (a = from_deg + (to_deg - from_deg) * i / steps) [r_out * sin(a), r_out * cos(a)]],
                    [for (i = [steps : -1 : 0]) let (a = from_deg + (to_deg - from_deg) * i / steps) [r_in * sin(a), r_in * cos(a)]]);
    polygon(points);
}

// X01-H, fixed half: bolts to the housing face, carries the abduction hinge block and both stops.
module motor_plate() {
    translate([plate_x, 0, 0]) side_plate(plate_t_mm) difference() {
        union() {
            circle(r = plate_r);
            // Straight neck, no wider than the hinge block, so it passes between the fork ears.
            translate([-hinge_block[1] / 2, 0]) square([hinge_block[1], abduction_axis_z_mm + hinge_block[2] / 2]);
        }
        circle(r = centre_hole_r);
        ring_holes(housing_bolt_circle_mm, housing_bolt_count, housing_bolt_clear_mm, 22.5);
    }
    // Stop blocks stand on the body side of the plate, in the plane of the arm bar.
    // Angles run from straight up towards the back; the bar hangs at 180 and swings forwards.
    translate([plate_x - arm_gap_mm - arm_t_mm + 1, 0, 0]) side_plate(arm_gap_mm + arm_t_mm - 1) {
        sector(stop_r_in, stop_r_out, 180 + stop_flexion_deg + bar_half_deg, 180 + stop_flexion_deg + bar_half_deg + block_deg);
        sector(stop_r_in, stop_r_out, 180 - stop_extension_deg - bar_half_deg - block_deg, 180 - stop_extension_deg - bar_half_deg);
    }
    // Hinge block with a fore-aft bore: the free abduction joint.
    difference() {
        translate([plate_centre_x - hinge_block[0] / 2, -hinge_block[1] / 2, abduction_axis_z_mm - hinge_block[2] / 2]) cube(hinge_block);
        translate([plate_centre_x, 0, abduction_axis_z_mm]) rotate([90, 0, 0]) cylinder(h = hinge_block[1] + 2, d = hinge_bolt_d_mm, center = true);
    }
}

// X01-H, moving half: bolts to the output flange; its bar meets the stops and carries the strut.
module output_arm() {
    difference() {
        union() {
            side_plate(arm_t_mm) difference() {
                union() {
                    circle(r = centre_hole_r - 3);
                    translate([-bar_w_mm / 2, -arm_len]) square([bar_w_mm, arm_len]);
                }
                for (i = [0, 1]) translate([0, -arm_len + 15 + i * hole_pitch_mm]) circle(d = joint_bolt_d_mm, $fn = 24);
            }
            translate([arm_t_mm, 0, 0]) side_plate(hub_h) circle(r = centre_hole_r - 3);
        }
        translate([-1, 0, 0]) side_plate(arm_t_mm + hub_h + 2) ring_holes(output_bolt_circle_mm, output_bolt_count, output_bolt_clear_mm);
        // Shallow recess for the centring spigot of the flange; check depth and fit on the part.
        translate([arm_t_mm + hub_h - 1.5, 0, 0]) side_plate(2) circle(d = flange_spigot_d_mm + 0.4);
    }
}

// X01-O: flat bar with a hole row; the cuff moves along it in steps of hole_pitch_mm.
module strut() {
    side_plate(bar_t_mm) difference() {
        translate([-bar_w_mm / 2, -strut_len]) square([bar_w_mm, strut_len]);
        for (i = [0 : strut_holes - 1]) translate([0, -15 - i * hole_pitch_mm]) circle(d = joint_bolt_d_mm, $fn = 24);
    }
}

// Thigh cuff: half ring behind the thigh with two strap slots; the strap closes it at the front.
module cuff() {
    difference() {
        intersection() {
            difference() {
                cylinder(h = cuff_h_mm, r = cuff_r + bar_t_mm, center = true);
                cylinder(h = cuff_h_mm + 2, r = cuff_r, center = true);
            }
            translate([-cuff_r - bar_t_mm - 1, 0, -cuff_h_mm / 2 - 1]) cube([2 * (cuff_r + bar_t_mm + 1), cuff_r + bar_t_mm + 1, cuff_h_mm + 2]);
        }
        for (sign = [-1, 1]) translate([sign * cuff_r - (sign > 0 ? 1 : bar_t_mm + 1), 12, -strap_width_mm / 2 - 1])
            cube([bar_t_mm + 2, 5, strap_width_mm + 2]);
    }
    // Flat tab on the outer side for the strut, two holes on the strut pitch.
    tab_x = cuff_r + bar_t_mm - 2;
    difference() {
        translate([tab_x, -bar_w_mm / 2 + 30, -cuff_h_mm / 2]) cube([bar_t_mm + 2, bar_w_mm, cuff_h_mm]);
        cylinder(h = cuff_h_mm + 2, r = cuff_r + 1, center = true);
        for (i = [-0.5, 0.5]) translate([tab_x - 1, 30, i * hole_pitch_mm]) rotate([0, 90, 0]) cylinder(h = bar_t_mm + 4, d = joint_bolt_d_mm, $fn = 24);
    }
}

// X01-B: rear bar across the back, two side arms forwards, a fork at each end for the hinge block.
module pelvis_frame() {
    half = pelvis_clear_width_mm / 2 + plate_centre_x;
    difference() {
        translate([-half - bar_t_mm / 2, back_offset_mm, frame_z]) cube([2 * half + bar_t_mm, bar_t_mm, frame_bar_h_mm]);
        // Slots for the hip belt that carries the frame.
        for (x = [-half * 0.55, half * 0.55]) translate([x - 2.5, back_offset_mm - 1, frame_z + (frame_bar_h_mm - strap_width_mm - 2) / 2])
            cube([5, bar_t_mm + 2, strap_width_mm + 2]);
    }
    for (sign = [-1, 1]) {
        front = -hinge_block[1] / 2 - 1 - ear_t;
        translate([sign * half - bar_t_mm / 2, front, frame_z]) cube([bar_t_mm, back_offset_mm + bar_t_mm - front, frame_bar_h_mm]);
        for (y = [front, hinge_block[1] / 2 + 1]) difference() {
            translate([sign * half - hinge_block[0] / 2, y, abduction_axis_z_mm - hinge_block[2] / 2 - 2])
                cube([hinge_block[0], ear_t, frame_z - abduction_axis_z_mm + hinge_block[2] / 2 + 2 + frame_bar_h_mm]);
            translate([sign * half, y - 1, abduction_axis_z_mm]) rotate([-90, 0, 0]) cylinder(h = ear_t + 2, d = hinge_bolt_d_mm);
        }
    }
}

module actuator_envelope() {
    %translate([housing_face_x, 0, 0]) rotate([0, 90, 0]) cylinder(h = actuator_h_mm - flange_protrusion_mm, d = actuator_d_mm);
    %translate([housing_face_x - flange_protrusion_mm, 0, 0]) rotate([0, 90, 0]) cylinder(h = flange_protrusion_mm, d = flange_d_mm);
}

// One leg in its local frame: origin on the hip flexion axis at the body side of the output arm.
module leg_unit() {
    color([0.25, 0.35, 0.40]) motor_plate();
    if ($preview) actuator_envelope();
    rotate([-hip_flex_deg, 0, 0]) {
        color([0.80, 0.51, 0.15]) output_arm();
        color([0.55, 0.60, 0.62]) translate([-bar_t_mm, 0, first_hole_z + 15]) strut();
        // The cuff tab lies against the body side of the strut.
        color([0.30, 0.38, 0.23]) translate([-cuff_r - 3 * bar_t_mm, -30, cuff_z]) cuff();
        if ($preview && show_stage_k)
            %translate([0, 0, -hip_to_knee_mm]) rotate([0, 90, 0]) cylinder(h = actuator_h_mm, d = actuator_d_mm);
    }
}

if (part == "assembly") {
    color([0.45, 0.48, 0.50]) pelvis_frame();
    for (sign = [-1, 1])
        translate([sign * (pelvis_clear_width_mm / 2 + plate_centre_x), 0, abduction_axis_z_mm]) rotate([0, -sign * abduction_deg, 0])
            translate([-sign * plate_centre_x, 0, -abduction_axis_z_mm])
                mirror([sign < 0 ? 1 : 0, 0, 0]) leg_unit();
} else {
    mirror([side == "l" && part != "strut" && part != "pelvis_frame" ? 1 : 0, 0, 0]) {
        if (part == "motor_plate") motor_plate();
        if (part == "output_arm") output_arm();
        if (part == "cuff") cuff();
    }
    if (part == "strut") strut();
    if (part == "pelvis_frame") pelvis_frame();
}
