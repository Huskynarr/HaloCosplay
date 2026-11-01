
// Energy Sword Prop - offensichtlich Sci-Fi, con-sicher.
// Konstruktionsmodell ohne Freigabe; Klinge ist stumpf und ohne Spitze.
// Einheit mm. OpenSCAD 2021.01+.

// Gesamtlaenge und Klinge
total_length = 950;      // 90-100 cm Klinge laut Guide
blade_length = 620;
blade_width = 110;
blade_thickness = 22;
handle_length = 220;
handle_width = 42;
handle_depth = 30;
guard_width = 200;
guard_depth = 40;
guard_thickness = 18;

// Wandstaerken
wall = 3.0;
split_gap = 1.0;         // Fuge fuer zweiteilige Klinge

// Detail
$fn = 48;

c_blade = [0.35, 0.85, 0.95];
c_handle = [0.12, 0.15, 0.17];
c_guard = [0.25, 0.28, 0.30];

// Klinge: flaches, nach oben zulaufendes Blatt mit abgerundeter Spitze
module blade() {
    color(c_blade)
    linear_extrude(height=blade_thickness, center=true)
        hull() {
            translate([0, -blade_length/2 + 20]) circle(r=blade_width*0.42);
            translate([0, blade_length/2 - blade_width*0.35]) circle(r=blade_width*0.16);
        }
}

// Griff: zylindrischer Kern mit Fingerrillen
module handle() {
    color(c_handle) difference() {
        union() {
            cylinder(h=handle_length, d=handle_width, center=true);
            // Griffsensoren
            for(i=[-2,-1,0,1,2])
                translate([0, 0, i*handle_length*0.16])
                    cylinder(h=handle_length*0.06, d=handle_width+6, center=true);
        }
        // Kabelkanal
        cylinder(h=handle_length+2, d=12, center=true);
    }
}

// Parierstange: die ikonischen seitlichen Zinken
module guard() {
    color(c_guard) difference() {
        union() {
            // Basis
            rounded_base();
            // Zinken
            for(s=[-1,1])
                translate([s*guard_width*0.36, 0, 0])
                    rotate([0,0,s*20])
                        cylinder(h=guard_depth, d=guard_width*0.16, center=true);
        }
        // Ausschnitt fuer Klinge
        cube([blade_width*0.7, blade_thickness*1.2, guard_depth*1.2], center=true);
    }
}

module rounded_base() {
    linear_extrude(height=guard_thickness, center=true)
        hull() for(x=[-guard_width*0.30, guard_width*0.30], y=[-guard_depth/2+4, guard_depth/2-4])
            translate([x, y]) circle(r=6);
}

// Montage
module assembly() {
    translate([0, blade_length/2 + handle_length/2, 0]) blade();
    handle();
    translate([0, -handle_length/2 - guard_depth/2 + 4, 0]) guard();
}

assembly();
