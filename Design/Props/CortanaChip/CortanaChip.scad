// Cortana-Chip - körpergetragenes Daten-Dock (Konzept).
// Enthält Innenausschnitt für ESP32-S3-WROOM, ST60-Freiraum und USB-Zugang.
// Einheit mm. OpenSCAD 2021.01+. Keine Passfreigabe, keine Lastfreigabe.

// ---- Parameter ----
chip_w = 90;          // Breite des Cortana-Chips (MakerWorld-Referenz)
chip_h = 60;          // Höhe
chip_d = 12;          // Dicke
wall = 2.4;           // Wandstärke
corner_r = 6;         // Eckenradius

// Elektronik (ESP32-S3-WROOM-1-N8R8: 18x25.5x3.1 mm + Antennenfreiraum)
esp_w = 18.0;
esp_l = 25.5;
esp_h = 3.4;
esp_clearance = 1.0;  // Spiel rund um das Modul
antenna_free = 6.0;   // Freiraum über der Antennenseite (kein Filament)

// ST60-Modul (Evaluationsboard grob 20x15 mm, Platz für PCB-Design)
st60_w = 20.0;
st60_l = 15.0;
st60_h = 2.0;
st60_clearance = 2.0;

// USB-C-Öffnung
usb_w = 10.0;
usb_h = 4.0;

// Befestigung: zwei Gurtschlitze hinten
strap_slot_w = 22.0;
strap_slot_h = 4.0;

$fn = 48;

c_case = [0.18, 0.55, 0.62];
c_dark = [0.10, 0.13, 0.15];
c_glow = [0.30, 0.85, 0.90];

// ---- Hilfsbausteine ----
module rounded_plate(w, d, h, r) {
    assert(w > 2*r && d > 2*r && h > 0, "Ungültige Plattenmaße");
    linear_extrude(height=h, center=true)
        hull() for(x=[-w/2+r, w/2-r], y=[-d/2+r, d/2-r])
            translate([x, y]) circle(r=r);
}

module strap_slot() {
    hull() for(x=[-strap_slot_w/2+strap_slot_h/2, strap_slot_w/2-strap_slot_h/2])
        cylinder(h=chip_d*3, d=strap_slot_h, center=true);
}

// ---- Gehäuse: Rückplatte + Rahmen ----
module case_back() {
    color(c_dark) difference() {
        rounded_plate(chip_w, chip_h, wall, corner_r);
        // Gurtschlitze
        for(sy=[-1, 1])
            translate([0, sy*(chip_h*0.28), 0]) strap_slot();
    }
}

module case_frame() {
    // Rahmen mit Innenausschnitt für Elektronik
    color(c_case) difference() {
        difference() {
            rounded_plate(chip_w, chip_h, chip_d-wall, corner_r);
            translate([0, 0, 0])
                rounded_plate(chip_w-2*wall, chip_h-2*wall, chip_d, corner_r-1);
        }
        // ESP32-Bauraum
        translate([-chip_w*0.18, chip_h*0.10, 0])
            cube([esp_w+2*esp_clearance, esp_l+2*esp_clearance, chip_d*2], center=true);
        // Antennenfenster: freier Bereich über ESP-Antenne
        translate([-chip_w*0.18, chip_h*0.10 + esp_l/2 + antenna_free/2, 0])
            cube([esp_w+2*esp_clearance, antenna_free, chip_d*2], center=true);
        // ST60-Bauraum (nahe Oberkante, Richtung Display)
        translate([chip_w*0.20, chip_h*0.28, 0])
            cube([st60_w+2*st60_clearance, st60_l+2*st60_clearance, chip_d*2], center=true);
        // USB-C-Öffnung an der Unterseite
        translate([0, -chip_h/2+wall/2, 0])
            cube([usb_w, wall*3, usb_h], center=true);
    }
}

// Frontplatte mit "Chip-Glow"-Ausschnitt (optional, Deko)
module case_front() {
    color(c_glow, 0.6) difference() {
        rounded_plate(chip_w, chip_h, wall, corner_r);
        for(i=[0:3])
            translate([-chip_w*0.25 + i*chip_w*0.17, 0, 0])
                rounded_plate(chip_w*0.10, chip_h*0.5, wall*3, 3);
    }
}

// Montage: alles zusammen (Vorschau)
module assembly() {
    translate([0, 0, -chip_d/2+wall/2]) case_back();
    case_frame();
    translate([0, 0, chip_d/2-wall/2]) case_front();
}

part = "assembly"; // assembly|back|frame|front
if (part == "assembly") assembly();
else if (part == "back") case_back();
else if (part == "frame") case_frame();
else if (part == "front") case_front();
else assert(false, "Unbekannter part-Wert");
