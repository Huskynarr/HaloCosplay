// MJOLNIR Mark VI Ruestung - Master-Chief-inspirierte Schalen.
// Konstruktionsmodell: alle Teile sind einzeln druckbar und parametrisch.
// Keine Lastfreigabe, keine Passfreigabe, keine Original-Halo-Oberflaeche.
// Einheit mm. OpenSCAD 2021.01+.

include <Parameters.scad>;

part = "assembly"; // assembly|helmet|visor|chest|back|shoulder_l|shoulder_r|
                   // upperarm_l|upperarm_r|forearm_l|forearm_r|gauntlet_l|
                   // gauntlet_r|thigh_l|thigh_r|shin_l|shin_r|boot_l|boot_r
show_mannequin = false; // Referenzkoerper nur in der Vorschau

assert(part != "assembly" || show_mannequin || true, "part unbekannt");

// ---------- Farben ----------
c_armor = [0.30, 0.34, 0.28];
c_dark  = [0.10, 0.13, 0.15];
c_gold  = [0.82, 0.55, 0.16];
c_glow  = [0.20, 0.75, 0.80];
c_body  = [0.45, 0.45, 0.48];

// ---------- Hilfsbausteine ----------
module shell_half(len, dia, wall=shell_wall) {
    // Halboffene Schale: Zylinder mit Wandstaerke, entlang Z, unten/oben offen.
    difference() {
        cylinder(h=len, d=dia, center=true);
        translate([0, 0, -0.1]) cylinder(h=len+0.2, d=dia-2*wall, center=true);
    }
}

module rounded_box(w, d, h, r) {
    hull() for(x=[-w/2+r, w/2-r], y=[-d/2+r, d/2-r], z=[-h/2+r, h/2-r])
        translate([x, y, z]) sphere(r);
}

module strap_slot(len) {
    // Gurtschlitz: rechteckige Oeffnung mit abgerundeten Enden
    hull() for(x=[-len/2+strap_slot_w/2, len/2-strap_slot_w/2])
        translate([x, 0]) cylinder(h=strap_slot_h*3, d=strap_slot_w, center=true);
}

module m3_hole(depth) {
    cylinder(h=depth*3, d=m3_clear, center=true);
}

// ---------- Helm ----------
module helmet() {
    hw = helmet_width * helmet_scale_w;
    hd = helmet_depth * helmet_scale_w;
    hh = helmet_height * helmet_scale_h;
    color(c_armor) difference() {
        union() {
            // Grundform: abgeflachte Kugel mit verbreiterter Krone
            scale([hw/2, hd/2, hh/2]) sphere(1);
            // Nackenverlaengerung (Mark VI typisch)
            translate([0, -hd*0.28, -hh*0.18])
                scale([hw*0.34, hd*0.30, hh*0.26]) sphere(1);
        }
        // Aushoehlen (Wandstaerke)
        translate([0, 0, hh*0.04])
            scale([(hw-2*shell_wall)/2, (hd-2*shell_wall)/2, (hh-2*shell_wall)/2])
                sphere(1);
        // Gesichtsffnung (Visier-Ausschnitt)
        translate([0, hd*0.42, hh*0.10])
            scale([hw*0.38, hd*0.35, hh*0.30]) sphere(1);
    }
    // Visierrahmen
    color(c_dark) difference() {
        translate([0, hd*0.30, hh*0.08])
            scale([hw*0.42, hd*0.20, hh*0.34]) sphere(1);
        translate([0, hd*0.36, hh*0.10])
            scale([hw*0.36, hd*0.25, hh*0.28]) sphere(1);
    }
}

module visor() {
    hw = helmet_width * helmet_scale_w;
    hd = helmet_depth * helmet_scale_w;
    hh = helmet_height * helmet_scale_h;
    color(c_gold) intersection() {
        translate([0, hd*0.34, hh*0.09])
            scale([hw*0.40, hd*0.24, hh*0.31]) sphere(1);
        translate([0, hd*0.34, hh*0.09])
            scale([hw*0.37, hd*0.30, hh*0.29]) sphere(1);
    }
}

// ---------- Torso ----------
module chest() {
    cw = torso_width * chest_scale_w;
    cd = torso_depth * chest_scale_d;
    ch = torso_height;
    color(c_armor) difference() {
        union() {
            rounded_box(cw, cd, ch, 30);
            // Brustbein-Platte (Mark VI typisch ueberlagert)
            translate([0, cd*0.32, ch*0.10])
                rounded_box(cw*0.62, cd*0.22, ch*0.42, 14);
        }
        translate([0, 0, 0]) rounded_box(cw-2*shell_wall, cd-2*shell_wall, ch+2, 28);
        // Halsdurchlass
        translate([0, 0, ch/2]) cylinder(h=60, d=helmet_width*0.62, center=true);
    }
    // Schultergurt-Schlitze
    color(c_dark) for(sx=[-1, 1])
        translate([sx*cw*0.30, 0, ch*0.30]) rotate([0, 90, 0])
            strap_slot(cd*0.55);
}

module back_plate() {
    cw = torso_width * chest_scale_w;
    cd = torso_depth * chest_scale_d;
    ch = torso_height;
    color(c_dark) difference() {
        union() {
            rounded_box(cw*0.85, cd*0.30, ch*0.85, 24);
            // Rucksack-Aufnahme (Powerbank/Controller, siehe HardwareKit)
            translate([0, -cd*0.10, 0])
                rounded_box(cw*0.55, cd*0.22, ch*0.55, 18);
        }
        // Lueftungsschlitze
        for(zy=[-1, 0, 1]) for(sx=[-1, 1])
            translate([sx*cw*0.18, -cd*0.18, zy*ch*0.20])
                rotate([90, 0, 0]) cylinder(h=cd, d=10, center=true);
    }
}

// ---------- Schultern ----------
module shoulder(side=1) {
    sd = upperarm_diameter_l * shoulder_scale;
    color(c_armor) difference() {
        union() {
            // Mark VI Pauldron: abgeflachte Halbkugel, nach aussen gezogen
            scale([sd*0.75, sd*0.62, sd*0.55]) sphere(1);
            translate([0, 0, -sd*0.10])
                scale([sd*0.68, sd*0.55, sd*0.30]) sphere(1);
        }
        translate([0, 0, sd*0.05])
            scale([sd*0.70, sd*0.56, sd*0.48]) sphere(1);
        // Armdurchlass
        cylinder(h=sd, d=upperarm_diameter_l + 4, center=true);
    }
}

// ---------- Arme ----------
module upper_arm(side=1) {
    len = upperarm_length_l;
    dia = upperarm_diameter_l;
    color(c_armor) difference() {
        shell_half(len, dia+2*shell_wall);
        // Split-Fuge fuer Einstieg
        translate([0, 0, 0]) cube([dia+10, split_gap, len+2], center=true);
    }
    // Bizeps-Platte
    color(c_dark) translate([0, side*dia*0.30, len*0.15])
        rounded_box(dia*0.55, plate_wall, len*0.35, 6);
}

module forearm(side=1) {
    len = forearm_length_l;
    dia = forearm_diameter_l;
    color(c_armor) difference() {
        shell_half(len, dia+2*shell_wall);
        translate([0, 0, 0]) cube([dia+10, split_gap, len+2], center=true);
    }
}

module gauntlet(side=1) {
    len = forearm_length_l * 0.55;
    dia = forearm_diameter_l * 1.12;
    color(c_dark) difference() {
        shell_half(len, dia);
        translate([0, 0, 0]) cube([dia+10, split_gap, len+2], center=true);
    }
}

// ---------- Beine ----------
module thigh(side=1) {
    len = thigh_length_l;
    dia = thigh_diameter_l;
    color(c_armor) difference() {
        shell_half(len, dia+2*shell_wall);
        translate([0, 0, 0]) cube([dia+10, split_gap, len+2], center=true);
    }
    // Oberschenkel-Panzerplatte
    color(c_dark) translate([0, side*dia*0.28, 0])
        rounded_box(dia*0.50, plate_wall, len*0.55, 8);
}

module shin(side=1) {
    len = shin_length_l;
    dia = shin_diameter_l;
    color(c_armor) difference() {
        shell_half(len, dia+2*shell_wall);
        translate([0, 0, 0]) cube([dia+10, split_gap, len+2], center=true);
    }
    // Schienbeinschutz (Mark VI typisch vorgezogen)
    color(c_dark) translate([0, dia*0.34, len*0.10])
        rounded_box(dia*0.45, plate_wall, len*0.65, 8);
}

module boot(side=1) {
    bw = boot_width_l;
    bl = boot_length_l;
    bh = 110; // Stiefelhoehe (Konzept)
    color(c_armor) difference() {
        union() {
            rounded_box(bw, bl, bh, 22);
            // Sohle
            translate([0, 0, -bh/2+8]) rounded_box(bw+8, bl+10, 16, 8);
        }
        rounded_box(bw-2*shell_wall, bl-2*shell_wall, bh+2, 20);
        // Kniedurchlass
        translate([0, 0, bh/2]) cylinder(h=40, d=shin_diameter_l*0.7, center=true);
    }
}

// ---------- Referenzkoerper (nur Vorschau) ----------
module mannequin() {
    color(c_body, 0.25) union() {
        cylinder(h=torso_height, d=torso_width*0.55, center=true); // Torso
        translate([0, 0, torso_height/2+helmet_height/2])
            sphere(helmet_width*0.35);                               // Kopf
        for(s=[-1, 1]) {
            translate([s*shoulder_span*0.45, 0, torso_height/2-20])
                rotate([0, 0, 0]) cylinder(h=upperarm_length_l, d=upperarm_diameter_l*0.6, center=true);
            translate([s*shoulder_span*0.45, 0, torso_height/2-upperarm_length_l-forearm_length_l/2])
                cylinder(h=forearm_length_l, d=forearm_diameter_l*0.6, center=true);
            translate([s*hip_width*0.30, 0, -torso_height/2-thigh_length_l/2])
                cylinder(h=thigh_length_l, d=thigh_diameter_l*0.6, center=true);
            translate([s*hip_width*0.30, 0, -torso_height/2-thigh_length_l-shin_length_l/2])
                cylinder(h=shin_length_l, d=shin_diameter_l*0.6, center=true);
        }
    }
}

// ---------- Montage ----------
module assembly() {
    hip_z = body_height * 0.49;
    torso_z = hip_z + 70;
    shoulder_z = torso_z + torso_height/2;
    if (show_mannequin) mannequin();
    // Helm
    translate([0, 0, shoulder_z + torso_height/2 + helmet_height*0.55]) helmet();
    // Brust und Ruecken
    translate([0, torso_depth*0.10, torso_z]) chest();
    translate([0, -torso_depth*0.28, torso_z]) back_plate();
    // Schultern
    for(s=[-1, 1]) translate([s*shoulder_span*0.48, 0, shoulder_z])
        shoulder(s);
    // Arme
    for(s=[-1, 1]) {
        translate([s*shoulder_span*0.48, 0, shoulder_z - upperarm_length_l/2 - 20])
            upper_arm(s);
        translate([s*shoulder_span*0.48, 0, shoulder_z - upperarm_length_l - forearm_length_l/2 - 20])
            forearm(s);
        translate([s*shoulder_span*0.48, 0, shoulder_z - upperarm_length_l - forearm_length_l - forearm_length_l*0.28 - 20])
            gauntlet(s);
    }
    // Beine
    for(s=[-1, 1]) {
        translate([s*hip_width*0.30, 0, hip_z - thigh_length_l/2]) thigh(s);
        translate([s*hip_width*0.30, 0, hip_z - thigh_length_l - shin_length_l/2]) shin(s);
        translate([s*hip_width*0.30, 0, hip_z - thigh_length_l - shin_length_l - 55]) boot(s);
    }
}

// ---------- Teil-Auswahl ----------
color(c_armor)
if (part == "assembly") assembly();
else if (part == "helmet") helmet();
else if (part == "visor") visor();
else if (part == "chest") chest();
else if (part == "back") back_plate();
else if (part == "shoulder_l") shoulder(-1);
else if (part == "shoulder_r") shoulder(1);
else if (part == "upperarm_l") upper_arm(-1);
else if (part == "upperarm_r") upper_arm(1);
else if (part == "forearm_l") forearm(-1);
else if (part == "forearm_r") forearm(1);
else if (part == "gauntlet_l") gauntlet(-1);
else if (part == "gauntlet_r") gauntlet(1);
else if (part == "thigh_l") thigh(-1);
else if (part == "thigh_r") thigh(1);
else if (part == "shin_l") shin(-1);
else if (part == "shin_r") shin(1);
else if (part == "boot_l") boot(-1);
else if (part == "boot_r") boot(1);
else assert(false, "Unbekannter part-Wert");
