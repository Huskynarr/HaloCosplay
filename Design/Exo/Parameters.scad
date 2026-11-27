// X01 leg drive, mechanical concept. Millimetres and degrees. EDIT BEFORE USE:
// every body dimension below is a placeholder, not a measurement.

// Actuator interface, from the manufacturer's 2D drawing of the AK80-9 V3.0
// (see README). Check against the delivered part before drilling.
actuator_d_mm = 98;
actuator_h_mm = 38.5;            // overall, including the output flange
flange_d_mm = 48;
flange_protrusion_mm = 3;
flange_spigot_d_mm = 37;
housing_bolt_circle_mm = 85;     // 8 x M3 on the housing face
housing_bolt_count = 8;
housing_bolt_clear_mm = 3.4;
output_bolt_circle_mm = 28;      // 6 x M4 on the output flange
output_bolt_count = 6;
output_bolt_clear_mm = 4.5;

// Body placeholders: take all of them on the person (verification step P3).
pelvis_clear_width_mm = 380;     // free width between the two output arms
abduction_axis_z_mm = 90;        // abduction hinge above the hip flexion axis
back_offset_mm = 150;            // hip axis to the rear bar of the pelvis frame
hip_to_cuff_mm = 330;            // hip axis to the centre of the thigh cuff
thigh_cuff_d_mm = 150;           // thigh diameter at the cuff, without padding
hip_to_knee_mm = 430;            // only for the stage K placeholder

// Mechanical stops. They must lie outside the software fault limits of
// exo_core.h (-33 and +108 degrees with the defaults) and inside the
// pain-free range of the person.
stop_extension_deg = 36;
stop_flexion_deg = 112;

// Material placeholders. No part is sized for load.
plate_t_mm = 5;
arm_t_mm = 6;
arm_gap_mm = 4;                  // room for the housing screw heads
bar_w_mm = 30;
bar_t_mm = 5;
frame_bar_h_mm = 60;
hinge_bolt_d_mm = 8;
joint_bolt_d_mm = 6.4;           // M6 clearance
hole_pitch_mm = 25;
cuff_h_mm = 60;
cuff_padding_mm = 8;
strap_width_mm = 40;

// Test rig for one actuator (verification steps P1 and P2), see X01TestRig.scad.
rig_axis_h_mm = 90;              // output axis above the base board
rig_lever_mm = 250;              // output axis to the contact point on the scale
rig_foot_depth_mm = 70;
rig_board_screw_d_mm = 5;
rig_stop_gap_mm = 12;            // free lever travel above and below level, at the tip
