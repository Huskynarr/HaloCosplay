// Parametrische Passproben. Keine tragenden Bauteile oder fertigen Ruestungsschalen.
// Komponenten: visor_retainer, fan_bracket, seam_coupon, joint_cover, hinge_coupon.
include <Parameters.scad>
component = "layout";
$fn = 72;
eps = 0.02;

function bounded(v, low, high) = is_num(v) && v >= low && v <= high;
assert(bounded(visor_radius_mm, 40, 250), "visor_radius_mm ausserhalb der Modellgrenzen");
assert(bounded(visor_angle_deg, 10, 60), "visor_angle_deg ausserhalb der Modellgrenzen");
assert(bounded(visor_sheet_mm, 0.4, 3), "visor_sheet_mm ausserhalb der Modellgrenzen");
assert(bounded(visor_lip_mm, 1, 4), "visor_lip_mm ausserhalb der Modellgrenzen");
assert(bounded(visor_base_mm, 1, 4), "visor_base_mm ausserhalb der Modellgrenzen");
assert(bounded(visor_depth_mm, 3, 15), "visor_depth_mm ausserhalb der Modellgrenzen");
assert(bounded(fan_size_mm, 25, 80), "fan_size_mm ausserhalb der Modellgrenzen");
assert(bounded(fan_hole_pitch_mm, 15, 75), "fan_hole_pitch_mm ausserhalb der Modellgrenzen");
assert(bounded(fan_hole_mm, 2, 5), "fan_hole_mm ausserhalb der Modellgrenzen");
assert(bounded(fan_opening_mm, 15, 75), "fan_opening_mm ausserhalb der Modellgrenzen");
assert(bounded(bracket_edge_mm, 3, 10), "bracket_edge_mm ausserhalb der Modellgrenzen");
assert(bounded(bracket_thickness_mm, 2, 6), "bracket_thickness_mm ausserhalb der Modellgrenzen");
assert(bounded(bracket_mount_hole_mm, 2, 5), "bracket_mount_hole_mm ausserhalb der Modellgrenzen");
assert(bounded(seam_tile_mm, 25, 60), "seam_tile_mm ausserhalb der Modellgrenzen");
assert(bounded(seam_thickness_mm, 2.5, 8), "seam_thickness_mm ausserhalb der Modellgrenzen");
assert(bounded(seam_tongue_width_mm, 4, 20), "seam_tongue_width_mm ausserhalb der Modellgrenzen");
assert(bounded(seam_tongue_height_mm, 0.8, 4), "seam_tongue_height_mm ausserhalb der Modellgrenzen");
assert(bounded(seam_tongue_length_mm, 2, 8), "seam_tongue_length_mm ausserhalb der Modellgrenzen");
assert(bounded(joint_length_mm, 40, 120), "joint_length_mm ausserhalb der Modellgrenzen");
assert(bounded(joint_width_mm, 25, 80), "joint_width_mm ausserhalb der Modellgrenzen");
assert(bounded(joint_base_mm, 0.6, 3), "joint_base_mm ausserhalb der Modellgrenzen");
assert(bounded(joint_rib_width_mm, 1, 4), "joint_rib_width_mm ausserhalb der Modellgrenzen");
assert(bounded(joint_pitch_mm, 3, 12), "joint_pitch_mm ausserhalb der Modellgrenzen");
assert(bounded(joint_rib_height_mm, 0.5, 5), "joint_rib_height_mm ausserhalb der Modellgrenzen");
assert(bounded(hinge_pin_mm, 2, 5), "hinge_pin_mm ausserhalb der Modellgrenzen");
assert(bounded(hinge_barrel_mm, 8, 14), "hinge_barrel_mm ausserhalb der Modellgrenzen");
assert(bounded(hinge_barrel_height_mm, 5, 20), "hinge_barrel_height_mm ausserhalb der Modellgrenzen");
assert(bounded(hinge_plate_mm, 3, 8), "hinge_plate_mm ausserhalb der Modellgrenzen");
assert(bounded(fastener_shaft_mm, 2, 6), "fastener_shaft_mm ausserhalb der Modellgrenzen");
assert(bounded(fastener_head_mm, 5, 12), "fastener_head_mm ausserhalb der Modellgrenzen");
assert(bounded(fastener_counterbore_mm, 1, 4), "fastener_counterbore_mm ausserhalb der Modellgrenzen");
assert(is_list(clearances_mm) && len(clearances_mm) == 3, "Genau drei Spiele erforderlich");
assert(bounded(clearances_mm[0],0.1,1.2) && bounded(clearances_mm[1],0.1,1.2)
       && bounded(clearances_mm[2],0.1,1.2)
       && clearances_mm[0] < clearances_mm[1] && clearances_mm[1] < clearances_mm[2],
       "Spiele muessen verschieden und aufsteigend sein");
assert(fan_opening_mm + 2*fan_hole_mm + 2 <= sqrt(2)*fan_hole_pitch_mm,
       "Luefteroeffnung und Eckbohrungen ueberschneiden sich");
assert(fan_opening_mm + 4 <= fan_size_mm, "Luefteroeffnung laesst zu wenig Rahmen");
assert(fan_hole_pitch_mm + fan_hole_mm + 4 <= fan_size_mm + 2*bracket_edge_mm,
       "Zu wenig Rand um Luefterbohrungen");
assert(seam_tongue_height_mm + max(clearances_mm) + 1 <= seam_thickness_mm);
assert(seam_tongue_width_mm + max(clearances_mm) + 4 < seam_tile_mm);
assert(joint_rib_width_mm < joint_pitch_mm && joint_base_mm > 0);
assert(hinge_pin_mm + max(clearances_mm) + 3 < hinge_barrel_mm);
assert(fastener_head_mm + max(clearances_mm) + 2 < 20);
assert(fastener_head_mm >= fastener_shaft_mm + 1, "Schraubenkopf zu klein");
assert(fastener_counterbore_mm + 1 <= hinge_plate_mm);

module slot(travel, diameter, height) {
    hull() for (x=[-travel/2,travel/2])
        translate([x,0,0]) cylinder(d=diameter,h=height);
}

module visor_strip(clearance) {
    // U-Profil in radialer Richtung; Nutbreite = Scheibendicke + Gesamtspiel.
    groove = visor_sheet_mm + clearance;
    rotate([0,0,-visor_angle_deg/2])
    rotate_extrude(angle=visor_angle_deg, convexity=6)
    translate([visor_radius_mm,0,0])
    union() {
        square([2*visor_lip_mm+groove,visor_base_mm]);
        square([visor_lip_mm,visor_depth_mm+visor_base_mm]);
        translate([visor_lip_mm+groove,0])
            square([visor_lip_mm,visor_depth_mm+visor_base_mm]);
    }
}

module visor_retainer() {
    // Drei unabhaengige Segmente, Spiele in der Reihenfolge der Parameterliste.
    spacing = 2*(visor_radius_mm+2*visor_lip_mm+visor_sheet_mm+max(clearances_mm))
              *sin(visor_angle_deg/2)+12;
    for (i=[0:len(clearances_mm)-1])
        translate([-visor_radius_mm,i*spacing,0]) visor_strip(clearances_mm[i]);
}

module fan_bracket() {
    outer = fan_size_mm + 2*bracket_edge_mm;
    difference() {
        union() {
            translate([-outer/2,-outer/2,0]) cube([outer,outer,bracket_thickness_mm]);
            for (side=[-1,1])
                translate([side*(outer/2+8)-8,-6,0]) cube([16,12,bracket_thickness_mm]);
        }
        translate([0,0,-eps]) cylinder(d=fan_opening_mm,h=bracket_thickness_mm+2*eps);
        for (x=[-1,1], y=[-1,1])
            translate([x*fan_hole_pitch_mm/2,y*fan_hole_pitch_mm/2,-eps])
                cylinder(d=fan_hole_mm,h=bracket_thickness_mm+2*eps);
        for (side=[-1,1])
            translate([side*(outer/2+8),0,-eps])
                slot(6,bracket_mount_hole_mm,bracket_thickness_mm+2*eps);
    }
}

module seam_male() {
    union() {
        cube([seam_tile_mm,seam_tile_mm,seam_thickness_mm]);
        translate([seam_tile_mm-eps,(seam_tile_mm-seam_tongue_width_mm)/2,
                   (seam_thickness_mm-seam_tongue_height_mm)/2])
            cube([seam_tongue_length_mm+eps,seam_tongue_width_mm,seam_tongue_height_mm]);
    }
}

module seam_female(clearance) {
    difference() {
        cube([seam_tile_mm,seam_tile_mm,seam_thickness_mm]);
        translate([-eps,(seam_tile_mm-seam_tongue_width_mm-clearance)/2,
                   (seam_thickness_mm-seam_tongue_height_mm-clearance)/2])
            cube([seam_tongue_length_mm+clearance+eps,
                  seam_tongue_width_mm+clearance,seam_tongue_height_mm+clearance]);
    }
}

module seam_coupon() {
    for (i=[0:len(clearances_mm)-1]) translate([0,i*(seam_tile_mm+10),0]) {
        seam_male();
        translate([seam_tile_mm+seam_tongue_length_mm+10,0,0])
            seam_female(clearances_mm[i]);
    }
}

module joint_cover() {
    // Flache, nicht tragende Materialprobe. TPU-Verhalten separat messen.
    union() {
        cube([joint_length_mm,joint_width_mm,joint_base_mm]);
        for (x=[joint_pitch_mm:joint_pitch_mm:joint_length_mm-joint_pitch_mm])
            translate([x-joint_rib_width_mm/2,0,joint_base_mm-eps])
                cube([joint_rib_width_mm,joint_width_mm,joint_rib_height_mm+eps]);
    }
}

module hinge_coupon() {
    count = len(clearances_mm);
    difference() {
        union() {
            cube([count*20,40,hinge_plate_mm]);
            for (i=[0:count-1]) translate([10+i*20,10,hinge_plate_mm-eps])
                cylinder(d=hinge_barrel_mm,h=hinge_barrel_height_mm+eps);
        }
        for (i=[0:count-1]) {
            translate([10+i*20,10,-eps])
                cylinder(d=hinge_pin_mm+clearances_mm[i],
                         h=hinge_plate_mm+hinge_barrel_height_mm+2*eps);
            translate([10+i*20,30,-eps])
                cylinder(d=fastener_shaft_mm+clearances_mm[i],h=hinge_plate_mm+2*eps);
            translate([10+i*20,30,hinge_plate_mm-fastener_counterbore_mm])
                cylinder(d=fastener_head_mm+clearances_mm[i],h=fastener_counterbore_mm+eps);
        }
    }
    // Separater gedruckter Vergleichsstift; ein realer Stift bleibt erforderlich.
    translate([count*20+12,10,0]) union() {
        cylinder(d=8,h=3);
        translate([0,0,3-eps]) cylinder(d=hinge_pin_mm,h=hinge_barrel_height_mm+hinge_plate_mm+3);
    }
}

module layout() {
    visor_retainer();
    translate([95,35,0]) fan_bracket();
    translate([150,0,0]) seam_coupon();
    translate([300,0,0]) joint_cover();
    translate([300,joint_width_mm+20,0]) hinge_coupon();
}

assert(component == "layout" || component == "visor_retainer" || component == "fan_bracket"
       || component == "seam_coupon" || component == "joint_cover" || component == "hinge_coupon",
       "Unbekannte Komponente");
if (component == "layout") layout();
else if (component == "visor_retainer") visor_retainer();
else if (component == "fan_bracket") fan_bracket();
else if (component == "seam_coupon") seam_coupon();
else if (component == "joint_cover") joint_cover();
else if (component == "hinge_coupon") hinge_coupon();
