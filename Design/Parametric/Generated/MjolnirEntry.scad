// MJOLNIR front-entry concept. Millimetres. OpenSCAD 2021.01+.
// Original envelope geometry, NOT a finished Halo surface or load-rated frame.
include <parameters.scad>

view = "assembly"; // assembly, torso, frame, forearm_ring, hardware
open_fraction = 0; // 0 closed, 1 open; animate with -D 'open_fraction=$t'
show_device_envelope = false; // Generic reserved volume, NOT a product CAD model
show_stand = false;
side = "l"; // forearm_ring: l/r
$fn = 48;
assert(open_fraction >= 0 && open_fraction <= 1);
assert(view == "assembly" || view == "torso" || view == "frame" ||
       view == "forearm_ring" || view == "hardware", "Unknown view");
assert(side == "l" || side == "r", "Unknown side");

olive = [0.30, 0.38, 0.23];
dark = [0.08, 0.12, 0.14];
cyan = [0.18, 0.63, 0.67];
orange = [1, 0.58, 0.16];
gold = [0.80, 0.51, 0.15];
slide = entry_slide_each_side * min(1,open_fraction*4);
angle = 105 * max(0,(open_fraction-0.25)/0.75);
// Placement is a display datum, not a derived skeleton or joint alignment.
hip_z = body_height * 0.49;
torso_z = hip_z + 70;
shoulder_z = torso_z + torso_height;

module plate(size) { cube(size, center=true); }

// Open-ended faceted shell, constant offset in XY, planar base and top.
module shell(w, d, h, t=wall) {
    assert(w > 2*t && d > 2*t && h > 0);
    linear_extrude(height=h) difference() {
        polygon([[-w/2+18,-d/2], [w/2-18,-d/2], [w/2,-d/2+18],
                 [w/2,d/2-18], [w/2-18,d/2], [-w/2+18,d/2],
                 [-w/2,d/2-18], [-w/2,-d/2+18]]);
        offset(delta=-t) polygon([[-w/2+18,-d/2], [w/2-18,-d/2], [w/2,-d/2+18],
                 [w/2,d/2-18], [w/2-18,d/2], [-w/2+18,d/2],
                 [-w/2,d/2-18], [-w/2,-d/2+18]]);
    }
}

module quadrant(w, d, h, right=true, front=true) {
    intersection() {
        shell(w,d,h);
        translate([right ? 1 : -w, front ? -d : 1, -1])
            cube([w-1, d-1, h+2]); // 2 mm assembly seams at x/y centre
    }
}

module torso_door(sign=1) {
    // x right, y back, z up. Front is negative y.
    translate([sign*(torso_width/2+slide),0,0]) rotate([0,0,sign*angle])
        translate([-sign*torso_width/2,0,0]) union() {
            color(olive) quadrant(torso_width,torso_depth,torso_height,sign>0,true);
            // Floating-looking chest applique, actually attached to its own door.
            color(olive) translate([sign*torso_width*0.24,-torso_depth/2-5,torso_height*0.69])
                rotate([6,0,sign*6]) plate([torso_width*0.40,12,torso_height*0.35]);
            color(dark) translate([sign*torso_width*0.24,-torso_depth/2-13,torso_height*0.70])
                plate([torso_width*0.23,4,12]);
        }
}

module torso() {
    for(sign=[-1,1]) {
        color(olive) translate([sign*slide,0,0])
            quadrant(torso_width,torso_depth,torso_height,sign>0,false);
        torso_door(sign);
        color(orange) translate([sign*(torso_width/2+slide),0,30]) cylinder(d=8,h=torso_height-60);
    }
    // Sliding rear wings overlap this fixed cosmetic spine cover.
    color(olive) translate([0,torso_depth/2+5,torso_height/2])
        plate([2*entry_slide_each_side+60,wall,torso_height]);
    // Sternum cover travels with right door; never bridges both sides rigidly.
    translate([torso_width/2+slide,0,0]) rotate([0,0,angle]) translate([-torso_width/2,0,0])
        color(olive) translate([0,-torso_depth/2-18,torso_height*0.30])
            plate([35,8,torso_height*0.45]);
}

module frame() {
    // Cyan blocks are interfaces/reserved frame volumes, not metal cut drawings.
    color(cyan) for(sign=[-1,1])
        translate([sign*torso_width*0.32,torso_depth/2+22,hip_z+torso_height/2])
            plate([20,12,torso_height+100]);
    color(cyan) translate([0,torso_depth/2+22,hip_z+15])
        plate([hip_width*0.8,12,50]);
    color(dark) translate([0,torso_depth/2+2,hip_z+15])
        plate([hip_width*0.8,25,100]);
}

module clamshell(dia, len, sign=1) {
    color(olive) intersection() {
        shell(dia,dia*0.88,len);
        translate([-dia,1,-1]) cube([2*dia,dia,len+2]);
    }
    translate([sign*dia/2,0,0]) rotate([0,0,sign*angle]) translate([-sign*dia/2,0,0])
        color(olive) intersection() {
            shell(dia,dia*0.88,len);
            translate([-dia,-dia,-1]) cube([2*dia,dia-1,len+2]);
        }
    color(orange) translate([sign*dia/2,0,10]) cylinder(d=6,h=len-20);
}

module shoulder(sign=1) {
    // Outward pivot clears the entrance; textile floating mount during wear.
    translate([sign*shoulder_span/2,0,shoulder_z-40]) rotate([0,sign*55*open_fraction,0])
        color(olive) difference() {
            cube([125,torso_depth*0.65,125],center=true);
            translate([0,0,-wall]) cube([125-2*wall,torso_depth*0.65-2*wall,125],center=true);
        }
}

module helmet() {
    translate([0,0,shoulder_z+45]) {
        color(olive) difference() {
            union() {
                shell(helmet_width,helmet_depth,helmet_height);
                translate([0,0,helmet_height-wall]) linear_extrude(wall)
                    offset(r=0) square([helmet_width-36,helmet_depth-36],center=true);
            }
            translate([-helmet_width/2,-helmet_depth,helmet_height*0.48])
                cube([helmet_width,helmet_depth,helmet_height*0.30]);
        }
        color(gold) translate([0,-helmet_depth/2,helmet_height*0.63])
            plate([helmet_width*0.85,3,helmet_height*0.28]);
    }
}

module device_envelope() {
    // Deliberately generic concept, no implied Hypershell/DNSYS compatibility.
    color([0.9,0.35,0.25,0.35]) for(sign=[-1,1])
        translate([sign*(hip_width/2+55),0,hip_z]) {
            rotate([0,90,0]) cylinder(d=120,h=80,center=true);
            translate([0,0,-150]) plate([45,80,240]);
        }
}

module stand() {
    // Storage fixture only; not a human support. Dimensions are illustrative.
    color([0.35,0.40,0.43]) {
        translate([0,torso_depth/2+180,25]) plate([900,800,30]);
        translate([0,torso_depth/2+190,shoulder_z/2]) plate([40,40,shoulder_z]);
        translate([0,torso_depth/2+100,shoulder_z-100]) plate([torso_width+100,220,25]);
    }
}

module assembly() {
    frame();
    translate([0,0,torso_z]) torso();
    for(sign=[-1,1]) {
        left = sign < 0;
        thigh_len = left ? thigh_length_l : thigh_length_r;
        shin_len = left ? shin_length_l : shin_length_r;
        upper_len = left ? upperarm_length_l : upperarm_length_r;
        fore_len = left ? forearm_length_l : forearm_length_r;
        shoulder(sign);
        translate([sign*shoulder_span/2,0,shoulder_z-125-upper_len])
            clamshell(left ? upperarm_diameter_l : upperarm_diameter_r,upper_len,sign);
        translate([sign*shoulder_span/2,-20,shoulder_z-170-upper_len-fore_len])
            clamshell(left ? forearm_diameter_l : forearm_diameter_r,fore_len,sign);
        translate([sign*hip_width*0.29,0,hip_z-50-thigh_len])
            clamshell(left ? thigh_diameter_l : thigh_diameter_r,thigh_len,sign);
        translate([sign*hip_width*0.29,0,110])
            clamshell(left ? shin_diameter_l : shin_diameter_r,shin_len,sign);
        color(olive) translate([sign*hip_width*0.29,-35,45])
            plate([left ? boot_width_l : boot_width_r,left ? boot_length_l : boot_length_r,75]);
    }
    helmet();
    if(show_device_envelope) device_envelope();
    if(show_stand) stand();
}

if(view=="assembly") assembly();
if(view=="torso") torso();
if(view=="frame") frame();
if(view=="forearm_ring") {
    // This ring is deliberately circular; confirm actual section in a mockup.
    diameter = side=="l" ? forearm_diameter_l : forearm_diameter_r;
    difference() { cylinder(d=diameter,h=12); translate([0,0,-1]) cylinder(d=diameter-2*wall,h=14); }
}
if(view=="hardware") {
    // Non-load-bearing bolt-hole spacing coupon, 50 mm centre distance.
    difference() {
        cube([80,30,4]);
        for(x=[15,65]) translate([x,15,-1]) cylinder(d=5.5,h=6);
    }
}
