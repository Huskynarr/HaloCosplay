// Parametrische Hardware-Prototypen. Einheit mm; keine Geraete-Passfreigabe.
include <Parameters.scad>;
component = "preview";
part = "base";
$fn = 48;
eps = 0.02;

assert(wall >= 2.4 && wall <= 8, "wall ausserhalb 2.4..8 mm");
assert(clearance >= 0.2 && clearance <= 2, "clearance ausserhalb 0.2..2 mm");
assert(m3_clearance >= 3.1 && m3_clearance <= 3.8, "M3-Durchgang pruefen");
assert(m4_clearance >= 4.1 && m4_clearance <= 4.8, "M4-Durchgang pruefen");
assert(strap_width >= 15 && strap_width <= 40 && strap_slot >= 3 && strap_slot <= 5,
       "Gurt und Schlitz pruefen");
assert(powerbank_width > 2*wall + 20 && powerbank_length > 2*strap_width + 30,
       "Powerbank-Grundflaeche zu klein");
assert(powerbank_depth > wall && powerbank_rail_height >= wall &&
       powerbank_rail_height < powerbank_depth, "Powerbank-Fuehrung verdeckt das Geraet");
assert(transmitter_width > strap_width + 18 && transmitter_length > 2*strap_width + 20,
       "Sender-Grundflaeche zu klein");
assert(transmitter_depth > wall && transmitter_rail_height >= wall &&
       transmitter_rail_height < transmitter_depth, "Sender-Fuehrung pruefen");
assert(camera_inner_width >= 36 && camera_inner_depth >= 28 && camera_inner_height >= 34,
       "Kameragehaeuse fuer Schraubdome zu klein");
assert(camera_lens_d >= 4 && camera_lens_d < min(camera_inner_width-16, camera_inner_height-16),
       "Linsenausschnitt zu gross");
assert(camera_board_pitch_x >= 10 && camera_board_pitch_x <= camera_inner_width-18 &&
       camera_board_pitch_z >= 10 && camera_board_pitch_z <= camera_inner_height-16,
       "Kamera-Lochbild kollidiert mit Gehaeuse/Domen");
assert(camera_cable_d >= 4 && camera_cable_d <= 10, "Kabeloeffnung pruefen");
assert(hud_base_width >= 50 && hud_base_depth >= 30 && hud_arm_length >= 50,
       "HUD-Halter zu klein");
assert(hud_mount_width >= 34 && hud_mount_width <= 60 && hud_mount_depth >= 24,
       "HUD-Montageplatte pruefen");
assert(hud_pin_d >= 3.1 && hud_pin_d <= 3.8, "HUD-Achse ist M3");
assert(nozzle_wall >= 6 && nozzle_outer_d >= 120 &&
       nozzle_free_bore >= 40 && nozzle_outer_d-nozzle_free_bore >= 60,
       "Ringbreite fuer Lichttraeger/Schrauben zu klein");
assert(nozzle_example_outlet_d > 0 && nozzle_example_outlet_d < nozzle_free_bore,
       "OEM-Auslass beruehrt Schutzring");
assert(nozzle_height >= 16 && nozzle_height <= 60 &&
       nozzle_height > wall + 8 && nozzle_wall <= 10, "Duesenblende pruefen");
assert(fan_size >= 40 && fan_size <= 80 && fan_pitch > fan_bore &&
       fan_pitch <= fan_size - m3_clearance - 3 && fan_bore > 20,
       "Luefter-Lochbild/Stegbreite pruefen");
assert(controller_inner_width >= 90 && controller_inner_depth >= 65 &&
       controller_inner_height >= 20, "Servicewanne zu klein");
assert(controller_board_pitch_x >= 20 && controller_board_pitch_y >= 20 &&
       controller_board_pitch_x <= controller_inner_width-24 &&
       controller_board_pitch_y <= controller_inner_depth-20,
       "Platinendome kollidieren mit Seitenwand oder Deckeldomen");

module rounded_plate(w, d, h, r=3) {
    assert(w > 2*r && d > 2*r && h > 0, "Ungueltige Plattenabmessungen");
    linear_extrude(h) hull()
        for(x=[-w/2+r,w/2-r],y=[-d/2+r,d/2-r])
            translate([x,y]) circle(r=r);
}

module slot(length, width, height) {
    assert(length >= width && width > 0 && height > 0, "Ungueltiger Langschlitz");
    hull() for(x=[-(length-width)/2,(length-width)/2])
        translate([x,0,0]) cylinder(d=width,h=height);
}

module hole(d,h) { translate([0,0,-eps]) cylinder(d=d,h=h+2*eps); }

// Offene Schale mit separaten Gurtdurchfuehrungen neben dem Geraet.
module powerbank_base() {
    iw=powerbank_width+2*clearance;
    il=powerbank_length+2*clearance;
    ow=iw+2*wall;
    ol=il+2*wall;
    flange=12;
    difference() {
        union() {
            rounded_plate(ow+2*flange,ol+1,wall);
            for(x=[-iw/2-wall/2,iw/2+wall/2])
                translate([x,0,wall]) rounded_plate(wall,il, powerbank_rail_height,wall/3);
            // Zwei geteilte Endanschlaege lassen die Mitte fuer Anschluesse frei.
            for(y=[-il/2-wall/2,il/2+wall/2],x=[-iw*0.37,iw*0.37])
                translate([x,y,wall]) rounded_plate(iw*0.23,wall,powerbank_rail_height,wall/3);
        }
        for(x=[-ow/2-flange/2,ow/2+flange/2],y=[-il*0.28,il*0.28])
            translate([x,y,-eps]) rotate([0,0,90]) slot(strap_width+2,strap_slot,wall+2*eps);
        // Bodenrippen statt geschlossener Tasche; Kabel bleiben ausserhalb.
        for(y=[-il*0.22,0,il*0.22])
            translate([0,y,-eps]) slot(iw*0.64,5,wall+2*eps);
    }
}

module transmitter_base() {
    iw=transmitter_width+2*clearance;
    il=transmitter_length+2*clearance;
    ow=iw+2*wall;
    ol=il+2*wall;
    difference() {
        union() {
            rounded_plate(ow+1,ol+1,wall);
            // +Y bleibt bis zum Rand offen: beispielhafte Antennenseite.
            for(x=[-iw/2-wall/2,iw/2+wall/2])
                translate([x,-il*0.08,wall]) rounded_plate(wall,il*0.80,transmitter_rail_height,wall/3);
            translate([0,-il/2-wall/2,wall]) rounded_plate(ow,wall,transmitter_rail_height,wall/3);
        }
        // Gurt wird vor dem Sender durch die Rueckplatte eingefaedelt.
        for(y=[-il*0.32,il*0.32])
            translate([0,y,-eps]) slot(strap_width+2,strap_slot,wall+2*eps);
        // Zwei Schlitze fuer eine unabhaengige, schmale Geraetesicherung.
        for(x=[-iw/2+5,iw/2-5])
            translate([x,-il*0.18,-eps]) rotate([0,0,90]) slot(15,strap_slot,wall+2*eps);
        translate([0,-il/2-wall-eps,wall+transmitter_rail_height/2])
            rotate([-90,0,0]) cylinder(d=8,h=wall+2*eps);
    }
}

module corner_bosses(iw,id,h) {
    for(x=[-iw/2+4,iw/2-4],y=[-id/2+4,id/2-4])
        translate([x,y,0]) cylinder(d=11,h=h);
}

module corner_holes(iw,id,h,nut=false) {
    for(x=[-iw/2+4,iw/2-4],y=[-id/2+4,id/2-4]) {
        translate([x,y,0]) hole(m3_clearance,h);
        if(nut) translate([x,y,-eps]) cylinder(d=6.6,h=2.5+eps,$fn=6);
    }
}

module camera_base() {
    iw=camera_inner_width;
    id=camera_inner_depth;
    ih=camera_inner_height;
    h=ih+wall;
    difference() {
        union() {
            difference() {
                rounded_plate(iw+2*wall,id+2*wall,h);
                translate([0,0,wall]) rounded_plate(iw,id,ih+eps,2);
            }
            corner_bosses(iw,id,h);
            // Vier Montagepunkte fuer eine senkrechte Sensorplatine, optische Achse -Y.
            for(x=[-camera_board_pitch_x/2,camera_board_pitch_x/2],
                z=[wall+ih/2-camera_board_pitch_z/2,wall+ih/2+camera_board_pitch_z/2])
                translate([x,id/2-6,z]) rotate([-90,0,0]) cylinder(d=7,h=6+eps);
        }
        corner_holes(iw,id,h,true);
        translate([0,-id/2-wall-eps,wall+ih/2]) rotate([-90,0,0])
            cylinder(d=camera_lens_d,h=wall+2*eps);
        for(x=[-camera_board_pitch_x/2,camera_board_pitch_x/2],
            z=[wall+ih/2-camera_board_pitch_z/2,wall+ih/2+camera_board_pitch_z/2])
            translate([x,0,z]) rotate([-90,0,0]) cylinder(d=m3_clearance,h=id/2+wall+eps);
        translate([0,id/2-eps,wall+camera_cable_d/2+2]) rotate([-90,0,0])
            cylinder(d=camera_cable_d,h=wall+2*eps);
    }
}

module camera_lid() {
    difference() {
        rounded_plate(camera_inner_width+2*wall,camera_inner_depth+2*wall,wall);
        corner_holes(camera_inner_width,camera_inner_depth,wall);
    }
}

module hud_base() {
    hinge_y=hud_base_depth/2;
    difference() {
        union() {
            rounded_plate(hud_base_width,hud_base_depth,4);
            // Zwei feststehende Scharnieraugen, mittleres Auge ist Teil des Arms.
            for(x=[-21,21]) {
                translate([x,hinge_y-3,4]) cube([10,6,5],center=true);
                translate([x-5,hinge_y,9]) rotate([0,90,0]) cylinder(d=10,h=10);
            }
        }
        for(y=[-7,7]) translate([0,y,-eps]) slot(hud_base_width-24,m3_clearance,4+2*eps);
        translate([-hud_base_width/2-1,hinge_y,9]) rotate([0,90,0])
            cylinder(d=hud_pin_d,h=hud_base_width+2);
    }
}

module hud_arm() {
    difference() {
        union() {
            translate([-10,0,5]) rotate([0,90,0]) cylinder(d=10,h=20);
            translate([0,-hud_arm_length/2,3]) rounded_plate(18,hud_arm_length,4);
            translate([0,-hud_arm_length+hud_mount_depth/2,3])
                rounded_plate(hud_mount_width,hud_mount_depth,4);
        }
        translate([-11,0,5]) rotate([0,90,0]) cylinder(d=hud_pin_d,h=22);
        for(x=[-hud_mount_width/2+7,hud_mount_width/2-7])
            translate([x,-hud_arm_length+hud_mount_depth/2,3-eps]) rotate([0,0,90])
                slot(hud_mount_depth-10,m3_clearance,4+2*eps);
        translate([0,-18,3-eps]) hole(4,4);
    }
}

module nozzle_shroud() {
    ro=nozzle_outer_d/2;
    ri=ro-nozzle_wall;
    difference() {
        union() {
            difference() {
                cylinder(d=nozzle_outer_d,h=nozzle_height);
                translate([0,0,wall]) cylinder(r=ri,h=nozzle_height);
            }
            // Drei Laschen montieren den Dekoring an einer separaten kalten Struktur.
            for(a=[30,150,270]) rotate([0,0,a]) translate([ro+3,0,0])
                rounded_plate(18,16,wall,4);
        }
        hole(nozzle_free_bore,nozzle_height);
        for(a=[30,150,270]) rotate([0,0,a]) translate([ro+6,0,0]) hole(m4_clearance,wall);
        // Befestigungslochbild fuer einen separat ausgelegten Metall-Lichttraeger.
        for(a=[45,135,225,315]) rotate([0,0,a]) translate([(nozzle_free_bore/2+ri)/2,0,0])
            hole(m3_clearance,wall);
        // Deckring mit M3-Durchgang; lange Bolzen und Muttern, keine Heissklebestellen.
        for(a=[0,90,180,270]) rotate([0,0,a]) translate([ro-nozzle_wall/2,0,0])
            hole(m3_clearance,nozzle_height);
    }
}

module nozzle_diffuser() {
    difference() {
        cylinder(d=nozzle_outer_d,h=2);
        hole(nozzle_free_bore,2);
        for(a=[0,90,180,270]) rotate([0,0,a])
            translate([nozzle_outer_d/2-nozzle_wall/2,0,0]) hole(m3_clearance,2);
    }
}

module nozzle_fan_bracket() {
    difference() {
        union() {
            rounded_plate(fan_size+8,fan_size+8,wall);
            translate([0,fan_size/2+7,0]) rounded_plate(fan_size+8,20,wall);
        }
        hole(fan_bore,wall);
        for(x=[-fan_pitch/2,fan_pitch/2],y=[-fan_pitch/2,fan_pitch/2])
            translate([x,y,0]) hole(m3_clearance,wall);
        for(x=[-fan_size/3,fan_size/3]) translate([x,fan_size/2+11,0]) hole(m4_clearance,wall);
    }
}

module controller_base() {
    iw=controller_inner_width;
    id=controller_inner_depth;
    ih=controller_inner_height;
    h=ih+wall;
    difference() {
        union() {
            difference() {
                rounded_plate(iw+2*wall,id+2*wall,h);
                translate([0,0,wall]) rounded_plate(iw,id,ih+eps,2);
                // Wand-Luftschlitze; die Unterkante behaelt einen zusammenhaengenden Steg.
                for(x=[-iw*0.30,0,iw*0.30],y=[-id/2-wall/2,id/2+wall/2])
                    translate([x,y,wall+ih*0.65]) cube([iw*0.19,wall+2*eps,5],center=true);
            }
            corner_bosses(iw,id,h);
            for(x=[-controller_board_pitch_x/2,controller_board_pitch_x/2],
                y=[-controller_board_pitch_y/2,controller_board_pitch_y/2])
                translate([x,y,wall]) cylinder(d=8,h=6);
        }
        corner_holes(iw,id,h,true);
        for(x=[-controller_board_pitch_x/2,controller_board_pitch_x/2],
            y=[-controller_board_pitch_y/2,controller_board_pitch_y/2])
            translate([x,y,0]) hole(m3_clearance,wall+6);
        translate([0,id/2+wall/2,wall+5]) cube([16,wall+2*eps,8],center=true);
        // Bodenoeffnungen nur im zentralen Bereich zwischen den Platinendomen.
        for(y=[-8,0,8]) translate([0,y,-eps]) slot(controller_board_pitch_x-14,4,wall+2*eps);
    }
}

module controller_lid() {
    difference() {
        rounded_plate(controller_inner_width+2*wall,controller_inner_depth+2*wall,wall);
        corner_holes(controller_inner_width,controller_inner_depth,wall);
        for(y=[-controller_inner_depth*0.28:7:controller_inner_depth*0.28])
            translate([0,y,-eps]) slot(controller_inner_width*0.58,4,wall+2*eps);
    }
}

module dispatch(c,p) {
    if(c=="powerbank") { assert(p=="base", "Powerbank: part=base"); powerbank_base(); }
    else if(c=="transmitter") { assert(p=="base", "Sender: part=base"); transmitter_base(); }
    else if(c=="camera") {
        assert(p=="base" || p=="lid", "Kamera: base|lid");
        if(p=="base") camera_base(); else camera_lid();
    } else if(c=="hud") {
        assert(p=="base" || p=="arm", "HUD: base|arm");
        if(p=="base") hud_base(); else hud_arm();
    } else if(c=="nozzle") {
        assert(p=="shroud" || p=="diffuser" || p=="fan_bracket", "Duese: shroud|diffuser|fan_bracket");
        if(p=="shroud") nozzle_shroud(); else if(p=="diffuser") nozzle_diffuser(); else nozzle_fan_bracket();
    } else if(c=="controller") {
        assert(p=="base" || p=="lid", "Servicewanne: base|lid");
        if(p=="base") controller_base(); else controller_lid();
    } else assert(false, "Unbekanntes Bauteil");
}

if(component=="preview") {
    color("SlateGray") translate([-170,100,0]) powerbank_base();
    color("OliveDrab") translate([-30,100,0]) transmitter_base();
    color("LightSteelBlue") translate([90,120,0]) camera_base();
    color("LightSteelBlue") translate([90,55,0]) camera_lid();
    color("Goldenrod") translate([-170,-70,0]) hud_base();
    color("Goldenrod") translate([-100,-35,0]) hud_arm();
    color("DarkSeaGreen") translate([15,-65,0]) nozzle_shroud();
    color("PaleTurquoise") translate([175,-65,0]) nozzle_diffuser();
    color("DarkSeaGreen") translate([140,35,0]) nozzle_fan_bracket();
    color("SteelBlue") translate([-155,-200,0]) controller_base();
    color("SteelBlue") translate([-20,-200,0]) controller_lid();
} else dispatch(component,part);
