// Parametrische Passproben. Keine tragenden Bauteile oder fertigen Ruestungsschalen.
// Komponenten: visor_retainer, fan_bracket, seam_coupon, joint_cover, hinge_coupon, magnet_mount.
include <Parameters.scad>
component = "layout";
magnet_part = "layout"; // base, base_lid, mate, mate_lid, assembly, layout
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
assert(bounded(magnet_diameter_mm, 8, 16));
assert(bounded(magnet_thickness_mm, 2, 5));
assert(bounded(magnet_clearance_mm, 0.1, 0.8));
assert(bounded(magnet_axial_clearance_mm, 0.1, 0.5));
assert(bounded(magnet_pitch_mm, 20, 50));
assert(bounded(magnet_wall_mm, 1.5, 4));
assert(bounded(magnet_floor_mm, 1.5, 4));
assert(bounded(magnet_lid_mm, 0.8, 2));
assert(bounded(magnet_lip_mm, 0.6, 2));
assert(bounded(magnet_guide_mm, 3, 6));
assert(bounded(magnet_guide_height_mm, 2, 5));
assert(bounded(magnet_guide_clearance_mm, 0.2, 0.8));
assert(bounded(magnet_mount_hole_mm, 3, 5));
assert(bounded(magnet_strap_width_mm, 8, 20));

magnet_length = magnet_pitch_mm + magnet_diameter_mm + magnet_clearance_mm + 2*magnet_wall_mm;
magnet_width = max(magnet_diameter_mm + magnet_clearance_mm + 2*magnet_wall_mm,
                   2*magnet_guide_mm + 4*magnet_wall_mm + 6);
magnet_height = magnet_floor_mm + magnet_thickness_mm + magnet_axial_clearance_mm;
magnet_guide_y = magnet_width/2 - magnet_wall_mm - (magnet_guide_mm+magnet_guide_clearance_mm)/2;
magnet_socket_depth = max(0, magnet_guide_height_mm - magnet_lid_mm + magnet_guide_clearance_mm);
magnet_ear_radius = max(6, magnet_mount_hole_mm/2 + magnet_wall_mm + 1);
assert(magnet_pitch_mm >= magnet_diameter_mm + magnet_clearance_mm + 2*magnet_wall_mm,
       "Magnettaschen haben zu wenig Zwischenwand");
assert(sqrt(pow(magnet_pitch_mm/2,2) + pow(magnet_guide_y,2)) >=
       (magnet_diameter_mm + magnet_clearance_mm + magnet_guide_mm + magnet_guide_clearance_mm)/2
       + magnet_wall_mm, "Magnettasche und Fuehrungsaufnahme ueberschneiden sich");
assert(magnet_socket_depth <= magnet_thickness_mm + magnet_axial_clearance_mm,
       "Fuehrungsaufnahme durchbricht den Boden");
assert(magnet_length/2 + 2 - (magnet_strap_width_mm+0.4)/2 >=
       magnet_mount_hole_mm/2 + magnet_wall_mm, "Zuglasche schneidet Montagebohrung");

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

// Vier flach druckbare Einzelteile. Zwei Magnete je Traeger; Schrauben und
// Muttern halten die Lochdeckel und befestigen zugleich das Muster am Aufbau.
// Die kleineren Deckelfenster halten die Magnete formschluessig in den Taschen.
module magnet_outline(mate, height) {
    union() {
        hull() for (x=[-1,1], y=[-1,1])
            translate([x*(magnet_length/2-2),y*(magnet_width/2-2),0])
                cylinder(r=2,h=height);
        for (side=[-1,1]) {
            if (mate) {
                translate([-magnet_ear_radius,side > 0 ? magnet_width/2-2 :
                          -magnet_width/2-magnet_ear_radius+1,0])
                    cube([2*magnet_ear_radius,magnet_ear_radius+1,height]);
                translate([0,side*(magnet_width/2+magnet_ear_radius-1),0])
                    cylinder(r=magnet_ear_radius,h=height);
            } else {
                translate([side > 0 ? magnet_length/2-2 :
                          -magnet_length/2-magnet_ear_radius+1,-magnet_ear_radius,0])
                    cube([magnet_ear_radius+1,2*magnet_ear_radius,height]);
                translate([side*(magnet_length/2+magnet_ear_radius-1),0,0])
                    cylinder(r=magnet_ear_radius,h=height);
            }
        }
        if (mate) hull() for (x=[-1,1], y=[-1,1])
            translate([magnet_length/2+2 + x*((magnet_strap_width_mm+6)/2-2),
                       magnet_width/2+6+y*6,0]) cylinder(r=2,h=height);
    }
}

module magnet_mounting_holes(mate, height) {
    for (side=[-1,1])
        translate([mate ? 0 : side*(magnet_length/2+magnet_ear_radius-1),
                   mate ? side*(magnet_width/2+magnet_ear_radius-1) : 0,-eps])
            cylinder(d=magnet_mount_hole_mm,h=height+2*eps);
    if (mate)
        translate([magnet_length/2+2,magnet_width/2+6,-eps])
            slot(magnet_strap_width_mm+0.4-3.4,3.4,height+2*eps);
}

module magnet_carrier(mate=false) {
    difference() {
        magnet_outline(mate,magnet_height);
        magnet_mounting_holes(mate,magnet_height);
        for (side=[-1,1])
            translate([side*magnet_pitch_mm/2,0,magnet_floor_mm])
                cylinder(d=magnet_diameter_mm+magnet_clearance_mm,
                         h=magnet_thickness_mm+magnet_axial_clearance_mm+eps);
        if (mate && magnet_socket_depth > 0)
            for (side=[-1,1]) translate([0,side*magnet_guide_y,magnet_height-magnet_socket_depth])
                cylinder(d=magnet_guide_mm+magnet_guide_clearance_mm,h=magnet_socket_depth+eps);
    }
}

module magnet_lid(mate=false) {
    difference() {
        union() {
            magnet_outline(mate,magnet_lid_mm);
            if (!mate) for (side=[-1,1])
                translate([0,side*magnet_guide_y,magnet_lid_mm-eps])
                    cylinder(d1=magnet_guide_mm,d2=magnet_guide_mm-1,
                             h=magnet_guide_height_mm+eps);
        }
        magnet_mounting_holes(mate,magnet_lid_mm);
        for (side=[-1,1]) translate([side*magnet_pitch_mm/2,0,-eps])
            cylinder(d=magnet_diameter_mm-2*magnet_lip_mm,h=magnet_lid_mm+2*eps);
        if (mate) for (side=[-1,1]) translate([0,side*magnet_guide_y,-eps])
            cylinder(d=magnet_guide_mm+magnet_guide_clearance_mm,h=magnet_lid_mm+2*eps);
    }
}

module magnet_half(mate=false) {
    magnet_carrier(mate);
    translate([0,0,magnet_height]) magnet_lid(mate);
}

module magnet_mount() {
    assert(magnet_part == "layout" || magnet_part == "base" || magnet_part == "base_lid"
           || magnet_part == "mate" || magnet_part == "mate_lid" || magnet_part == "assembly",
           "Unbekanntes Magnetteil");
    if (magnet_part == "base") magnet_carrier(false);
    else if (magnet_part == "base_lid") magnet_lid(false);
    else if (magnet_part == "mate") magnet_carrier(true);
    else if (magnet_part == "mate_lid") magnet_lid(true);
    else if (magnet_part == "assembly") {
        color("SteelBlue") magnet_half(false);
        color("DarkOrange") translate([0,0,2*(magnet_height+magnet_lid_mm)])
            rotate([180,0,0]) magnet_half(true);
    } else {
        step_x = magnet_length+2*magnet_ear_radius+12;
        step_y = magnet_width+2*magnet_ear_radius+28;
        magnet_carrier(false);
        translate([step_x,0,0]) magnet_lid(false);
        translate([0,step_y,0]) magnet_carrier(true);
        translate([step_x,step_y,0]) magnet_lid(true);
    }
}

module layout() {
    visor_retainer();
    translate([95,35,0]) fan_bracket();
    translate([150,0,0]) seam_coupon();
    translate([300,0,0]) joint_cover();
    translate([300,joint_width_mm+20,0]) hinge_coupon();
    translate([430,0,0]) magnet_mount();
}

assert(component == "layout" || component == "visor_retainer" || component == "fan_bracket"
       || component == "seam_coupon" || component == "joint_cover" || component == "hinge_coupon"
       || component == "magnet_mount",
       "Unbekannte Komponente");
if (component == "layout") layout();
else if (component == "visor_retainer") visor_retainer();
else if (component == "fan_bracket") fan_bracket();
else if (component == "seam_coupon") seam_coupon();
else if (component == "joint_cover") joint_cover();
else if (component == "hinge_coupon") hinge_coupon();
else if (component == "magnet_mount") magnet_mount();
