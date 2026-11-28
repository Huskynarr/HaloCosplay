// X01 control box: tray and lid for the ESP32 board and the CAN transceiver, clamped to the
// rear tube of the pelvis frame. Printed plastic, outside every load path. Board sizes are
// placeholders; no ingress protection, no strain relief design, not built.
include <Parameters.scad>

part = "assembly"; // assembly, tray, lid, clamp
$fn = 48;

assert(part == "assembly" || part == "tray" || part == "lid" || part == "clamp", "unknown part");
assert(len(box_board_mm) == 3 && len(box_transceiver_mm) == 3, "board sizes need [length, width, height]");
assert(box_wall_mm >= 1.2, "box wall too thin to print");

wall = box_wall_mm;
gap = 1.5;                                   // air around each board
inner = [box_board_mm[0] + 2 * gap,
         box_board_mm[1] + box_transceiver_mm[1] + 3 * gap,
         max(box_board_mm[2], box_transceiver_mm[2]) + 6];
outer = [inner[0] + 2 * wall, inner[1] + 2 * wall, inner[2] + wall];
tube = frame_tube_mm[0];
screw_d = 3.2;
post = 7;

module post_positions() {
    for (x = [post / 2 + 0.4, outer[0] - post / 2 - 0.4]) for (y = [post / 2 + 0.4, outer[1] - post / 2 - 0.4])
        translate([x, y, 0]) children();
}

// Tray: boards lie on low rails, cables leave through two openings in one end wall.
module tray() {
    difference() {
        union() {
            difference() {
                cube(outer);
                translate([wall, wall, wall]) cube([inner[0], inner[1], inner[2] + 1]);
            }
            intersection() {
                cube(outer);
                post_positions() cylinder(h = outer[2], d = post);
            }
        }
        post_positions() translate([0, 0, wall]) cylinder(h = outer[2], d = screw_d - 0.7, $fn = 16);
        for (y = [outer[1] * 0.3, outer[1] * 0.7])
            translate([-1, y, wall + inner[2] - box_cable_d_mm / 2 - 3]) rotate([0, 90, 0]) cylinder(h = wall + 2, d = box_cable_d_mm);
        // Vent slots along one side.
        for (i = [0 : 3]) translate([wall + 8 + i * 12, outer[1] - wall - 1, wall + 4]) cube([6, wall + 2, 3]);
    }
    // Rails keep solder joints off the floor and locate both boards.
    for (y = [wall + gap + 3, wall + gap + box_board_mm[1] - 5]) translate([wall + post, y, wall - 0.5]) cube([inner[0] - 2 * post, 2, 3]);
    translate([wall + post, wall + 2 * gap + box_board_mm[1] + 3, wall - 0.5]) cube([box_transceiver_mm[0], 2, 3]);
    // Two ears with holes for the clamp screws.
    for (x = [-10, outer[0] - 0.5]) translate([x, outer[1] / 2 - 8, 0]) difference() {
        cube([10.5, 16, wall + 1.6]);
        translate([x < 0 ? 5 : 5.5, 8, -1]) cylinder(h = wall + 4, d = screw_d + 1, $fn = 16);
    }
}

// Lid with holes for the push button and the status LED.
module lid() {
    difference() {
        union() {
            cube([outer[0], outer[1], wall]);
            translate([wall + 0.3, wall + 0.3, -2]) difference() {
                cube([inner[0] - 0.6, inner[1] - 0.6, 2]);
                translate([1.6, 1.6, -1]) cube([inner[0] - 3.8, inner[1] - 3.8, 4]);
                // Clear the corner posts.
                for (x = [-1, inner[0] - post - 0.6]) for (y = [-1, inner[1] - post - 0.6]) translate([x, y, -1]) cube([post + 1, post + 1, 4]);
            }
        }
        post_positions() translate([0, 0, -3]) cylinder(h = wall + 4, d = screw_d, $fn = 16);
        translate([outer[0] * 0.3, outer[1] / 2, -3]) cylinder(h = wall + 4, d = box_button_d_mm);
        translate([outer[0] * 0.7, outer[1] / 2, -3]) cylinder(h = wall + 4, d = box_led_d_mm);
    }
}

// Block under the tray with a slot for the square tube; two screws pull it against the tray ears.
module clamp() {
    span = outer[0] + 20;
    difference() {
        translate([-10, outer[1] / 2 - 8, -tube - wall - 0.4]) cube([span, 16, tube + wall + 0.4]);
        translate([(span - 20 - tube - 0.6) / 2, outer[1] / 2 - 9, -tube - 0.4]) cube([tube + 0.6, 18, tube + 1]);
        for (x = [-5, outer[0] + 5]) translate([x, outer[1] / 2, -tube - wall - 1]) cylinder(h = tube + wall + 3, d = screw_d - 0.7, $fn = 16);
    }
}

if (part == "tray") tray();
if (part == "lid") rotate([180, 0, 0]) lid();
if (part == "clamp") clamp();
if (part == "assembly") {
    color([0.25, 0.35, 0.40]) tray();
    color([0.45, 0.48, 0.50]) translate([0, 0, outer[2] + ($preview ? 12 : 0.2)]) lid();
    color([0.55, 0.60, 0.62]) translate([0, 0, -0.2]) clamp();
    if ($preview) {
        %translate([wall + gap, wall + gap, wall + 2.5]) cube(box_board_mm);
        %translate([wall + gap, wall + 2 * gap + box_board_mm[1], wall + 2.5]) cube(box_transceiver_mm);
        %translate([(outer[0] - tube) / 2, -40, -tube - 0.2]) cube([tube, outer[1] + 80, tube]);
    }
}
