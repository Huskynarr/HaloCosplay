// MJOLNIR Ruestungsmodell - Master-Chief-Proportionen, skaliert auf Profilmasse.
// Einheit mm. Beispielmasse aus Design/Parametric/Generated/parameters.scad.
// Keine Passfreigabe; Schalen sind Konstruktion, keine Vermessung einer Person.

include <../Parametric/Generated/parameters.scad>;

// Master-Chief-Kanon: Ruestung verbreitert und vergroebert den Koerper.
// Faktoren relativ zu den Profil-Huellmassen (Konzept, nicht Vermessung).
chest_scale_w = 1.15;   // Brust breiter als Torso-Huellmasse
chest_scale_d = 1.10;
shoulder_scale = 1.35;  // Mark-VI-Schulterpanzer sind uebergross
helmet_scale_w = 1.10;
helmet_scale_h = 1.05;

// Wandstaerken und Druckeinstellungen
shell_wall = 3.0;          // Druckwand der Schalen
plate_wall = 4.0;          // Deko-Panzerplatten
split_gap = 1.0;           // Fuge zwischen Schalenhaelften
strap_slot_w = 25.0;       // Gurtschlitz
strap_slot_h = 4.0;
m3_clear = 3.4;            // M3-Durchgang

// Visier (separat drucken, transparentes Filament oder Abguss)
visor_wall = 2.5;
visor_frame = 8.0;

// Detailgrad fuer Vorschau; STL-Export nutzt $fn=64
$fn = 48;
