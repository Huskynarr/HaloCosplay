#!/usr/bin/env python3
"""Export portable opening limb envelopes; not anatomy, hinges or build approval."""
import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import sys

try:
    from . import suit_fit
except ImportError:
    import suit_fit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Design/Clamshell"
PARTS = ("upperarm", "forearm", "thigh", "shin")
LABELS = ("Oberarm", "Unterarm", "Oberschenkel", "Schienbein")
SIDES = ("l", "r")
MODULE_SOURCES = ("ModuleCommon.scad", "ArmModule.scad", "LegModule.scad", "TorsoModule.scad", "HelmetModule.scad",
                  "SuitAssembly.scad")
MODULE_CHECKS = {
    "common": (
        ("MOD01", "Modul bleibt nach dem Ablegen vollstaendig verbunden; kein loses Teil, kein Werkzeug"),
        ("MOD05", "Alle Verschluesse des Moduls selbst schliessen und oeffnen, auch geruestet, mit Handschuh und stromlos"),
        ("MOD06", "Zeit und Zahl der Handgriffe fuer An- und Ablegen des Moduls festhalten"),
    ),
    "arm": (
        ("MOD02", "Beide Schalen parken zur selben Seite offen; Arm in einem Zug radial einlegen"),
        ("MOD03", "Einhaengepunkt an der Schulter traegt das gewogene Modul und loest einzeln"),
        ("MOD04", "Ellbogen bis zur benoetigten Beugung bewegen; kein Schalenkontakt, kein Zug am Textil"),
    ),
    "leg": (
        ("MOD02", "Beide Schalen parken zur selben Seite offen; Bein im Sitzen in einem Zug einlegen, der Fuss durchquert kein geschlossenes Teil"),
        ("MOD03", "Einhaengepunkt am Hueftgurt traegt das gewogene Modul und loest einzeln"),
        ("MOD04", "Knie fuer Sitzen, Treppe und Hocke beugen; kein Schalenkontakt in der Kniekehle, kein Zug am Textil"),
        ("MOD07", "Gehen, Abrollen und Knien: Schuhcover bleibt am Schuh, Sohle und Fersengurt bleiben frei"),
    ),
    "torso": (
        ("MOD02", "Fluegel und Tueren parken offen; Einstieg und Ausstieg ohne Hilfe, auch bei blockierter Tuer"),
        ("MOD03", "Jede der vier Aufnahmen traegt ihr gewogenes Arm- oder Beinmodul und loest einzeln"),
        ("MOD04", "Tief atmen, vorbeugen, sitzen und Arme heben; kein Druck auf Rippen, Hals oder Huefte"),
    ),
    "helmet": (
        ("MOD02", "Hintere Schale parkt offen; Kopf ohne Zwang einsetzen, auch mit Brille oder Hoerschutz"),
        ("MOD03", "Helm sitzt ohne Halten; hintere Schale kann nicht unbeabsichtigt aufgehen"),
        ("MOD04", "Kopf drehen und nicken; Sichtfeld, Atmung und Hoeren am geschlossenen Helm pruefen"),
    ),
}
CHECKS = (
    ("OPEN01", "Alle Schalen und innenliegenden Gurte vollstaendig oeffnen; kein geschlossener Ring bleibt"),
    ("OPEN02", "Arm oder Bein radial einlegen und entnehmen; Hand/Fuss muss keine Schale durchqueren"),
    ("OPEN03", "Offenhalter bleibt ohne Festhalten eingerastet und laesst sich mit Gegenhand loesen"),
    ("OPEN04", "Verschluss bei tragbarer Pose mit Gegenhand erreichen, inklusive letzter Arm und Handschuh"),
    ("OPEN05", "Polster, Stoff und Kabel bleiben aus Scharnier, Verschluss und Schalenfuge"),
    ("OPEN06", "Schale schliessen und wieder oeffnen; vorher/nachher freie Bewegung des menschlichen Gelenks"),
    ("OPEN07", "Stromlos sitzend mit Kostuemhandschuhen oeffnen; jede Kassette hat eigenen mechanischen Ausstieg"),
    ("OPEN08", "Offene Schalen und Station kollidieren nicht mit Koerper, Nachbarschale oder freiem Fluchtweg"),
    ("OPEN09", "Frontzugriff auf Akku-Trenner, Hauptschalter und beidseitige Entriegelungen bei geschlossenem Torso"),
    ("OPEN10", "Drei vollstaendige An-/Ausziehfolgen ohne Hilfe dokumentieren; Beobachter fuer Entwicklungsprobe vorhanden"),
)


def front_point(x, y, radius, hinge_offset, angle_deg, side):
    """Mirror opening around the lateral Z-axis; XY model front is negative Y."""
    if side not in SIDES:
        raise ValueError("side: l oder r erforderlich")
    sign = -1 if side == "l" else 1
    hinge_x = sign * (radius + hinge_offset)
    angle = math.radians(sign * angle_deg)
    dx = x - hinge_x
    return (hinge_x + math.cos(angle) * dx - math.sin(angle) * y,
            math.sin(angle) * dx + math.cos(angle) * y)


def free_flex_deg(diameter, gap, relief):
    """Flexion at which the cut-back edges of two straight round envelopes meet.

    diameter is the envelope whose edge closes the joint: the forearm at the elbow,
    the larger of thigh and shin at the knee. Soft tissue, padding, the real joint
    axis and real armor contours are not considered.
    """
    return round(math.degrees(2 * math.atan((gap / 2 + relief) / (diameter / 2))), 1)


elbow_free_flex_deg = free_flex_deg


# Assumptions of the print plan; both are command line options.
DEFAULT_BUILD_VOLUME_MM = (325.0, 320.0, 325.0)
DEFAULT_DENSITY_G_CM3 = 1.24
LUG_HEIGHT_MM = 16.0
LUG_SLOT_CENTRE_MM = 8.0
LEG_LUG_AZIMUTH_DEG = 50.0


def link_length_mm(radius_upper, radius_lower, half_span, flex_deg, azimuth_deg=0.0, opens=True):
    """Straight distance between the two strap slots of a joint link at a given flexion.

    The slots sit on the rear halves, azimuth_deg away from straight back, half_span above
    and below the joint centre. opens=True is the elbow (the rear side opens when bending),
    False the knee. The real strap runs around the joint, so this is a lower bound.
    """
    azimuth = math.radians(azimuth_deg)
    theta = math.radians(-flex_deg if opens else flex_deg)
    upper = (radius_upper * math.sin(azimuth), radius_upper * math.cos(azimuth), half_span)
    y, z = radius_lower * math.cos(azimuth), -half_span
    lower = (radius_lower * math.sin(azimuth), y * math.cos(theta) - z * math.sin(theta),
             y * math.sin(theta) + z * math.cos(theta))
    return round(math.dist(upper, lower), 1)


def link_lengths(radius_upper, radius_lower, half_span, free_flex, azimuth_deg, opens):
    angles = {"straight": 0.0, "at_45_deg": 45.0, "at_90_deg": 90.0, "at_free_flex_estimate": free_flex}
    lengths = {key: link_length_mm(radius_upper, radius_lower, half_span, angle, azimuth_deg, opens)
               for key, angle in angles.items()}
    lengths["required_min"] = max(lengths.values())
    return lengths


def _half_tube_cm3(diameter, wall, length):
    radius = diameter / 2
    return math.pi / 2 * (radius ** 2 - (radius - wall) ** 2) * length / 1000


def _cut_ellipsoid_mm3(a, b, c, centre_z):
    """Volume of an ellipsoid above the plane z = 0 when its centre sits at centre_z."""
    u = -centre_z / c
    return math.pi * a * b * c * ((1 - u) - (1 - u ** 3) / 3)


def pieces(values):
    """Printable pieces with bounding box and shell volume; small tabs and pads are left out."""
    wall = values["wall_mm"]
    result = []

    def add(piece_id, module, bbox, volume_cm3):
        result.append({"id": piece_id, "module": module, "bbox_mm": [round(v, 1) for v in bbox],
                       "shell_volume_cm3": round(volume_cm3, 1)})

    for column, side in enumerate(SIDES):
        upper, fore = values["limbs_mm"][column], values["limbs_mm"][2 + column]
        thigh, shin = values["limbs_mm"][4 + column], values["limbs_mm"][6 + column]
        boot = values["boots_mm"][column]
        arm, leg = f"arm_module_{side}", f"leg_module_{side}"
        # (piece, dims, cut-back at the joint, strap tabs) per half: rear first, then front.
        for module, name, dims, cuts, lugs in (
                (arm, "upperarm", upper, (0, values["elbow_relief_mm"]), (2, 0)),
                (arm, "forearm", fore, (0, values["elbow_relief_mm"]), (1, 0)),
                (leg, "thigh", thigh, (values["knee_relief_mm"], 0), (2, 0)),
                (leg, "shin", shin, (values["knee_relief_mm"], 0), (2, 0))):
            for half, cut, lug in zip(("rear", "front"), cuts, lugs):
                length = dims[1] - cut
                add(f"{name}_{side}_{half}", module, (dims[0], dims[0] / 2, length + lug * LUG_HEIGHT_MM),
                    _half_tube_cm3(dims[0], wall, length))
        pad_r = max(thigh[0], shin[0]) / 2 + 6 + wall
        pad_h = values["knee_gap_mm"] + 80
        add(f"kneepad_{side}", leg, (2 * pad_r * math.sin(math.radians(45)),
                                     pad_r - (pad_r - wall) * math.cos(math.radians(45)), pad_h),
            math.pi / 4 * (pad_r ** 2 - (pad_r - wall) ** 2) * pad_h / 1000)
        height = values["boot_height_mm"]
        # Rough: top face plus the two side walls and the toe, all one wall thick.
        add(f"shoe_cover_{side}", leg, (boot[0], boot[1], height),
            0.88 * (boot[0] * boot[1] + height * (2 * boot[1] + boot[0])) * wall / 1000)
    for name, (width, depth), height, lug in (("torso", values["torso_mm"][:2], values["torso_mm"][2], 1),
                                              ("belt", values["hip_mm"], values["belt_height_mm"], 1)):
        quarter = (2 * (width - 36) + 2 * (depth - 36) + 4 * 18 * math.sqrt(2)) / 4
        for side in SIDES:
            for half in ("rear", "door"):
                piece = f"{half}_wing_{side}" if (name, half) == ("torso", "rear") else (
                    f"door_{side}" if name == "torso" else f"belt_{half}_{side}")
                add(piece, "torso_module", (width / 2, depth / 2, height + (lug * LUG_HEIGHT_MM if half == "rear" else 0)),
                    quarter * wall * height / 1000)
    width, depth, height = values["helmet_mm"]
    shell = (_cut_ellipsoid_mm3(width / 2, depth / 2, 0.55 * height, 0.45 * height) -
             _cut_ellipsoid_mm3(width / 2 - wall, depth / 2 - wall, 0.55 * height - wall, 0.45 * height)) / 1000
    v = 2 * values["helmet_split_fraction"]
    # A thin shell splits by area, which for a plane cut grows linearly with the cut position.
    front_share = (1 + v) / 2
    visor = 1.1 * 0.8 * width * 0.27 * height * wall / 1000
    add("helmet_front", "helmet_module", (width, depth * (0.5 + values["helmet_split_fraction"]), height),
        shell * front_share - visor)
    add("helmet_rear", "helmet_module", (width, depth * (0.5 - values["helmet_split_fraction"]), height), shell * (1 - front_share))
    return result


def print_plan(values, build_volume=DEFAULT_BUILD_VOLUME_MM, density=DEFAULT_DENSITY_G_CM3):
    """Fit every piece into the build volume along the machine axes and estimate solid-wall mass."""
    volume = sorted(float(v) for v in build_volume)
    if len(volume) != 3 or min(volume) <= 0 or not 0.5 <= density <= 3:
        raise ValueError("Bauraum braucht drei positive Masse, Dichte 0.5 bis 3 g/cm3")
    rows = []
    for piece in pieces(values):
        box = sorted(piece["bbox_mm"])
        fits = all(b <= v for b, v in zip(box, volume))
        # Cutting across the longest edge only; the two shorter edges must fit as they are.
        parts = 1 if fits else (math.ceil(box[2] / volume[2]) if box[0] <= volume[0] and box[1] <= volume[1] else None)
        # One lap joint, placed 25 mm above the middle so it clears the latch land there.
        split = None
        if parts == 2 and piece["id"].split("_")[0] in ("thigh", "shin", "upperarm", "forearm", "rear", "door"):
            cut = round(piece["bbox_mm"][2] / 2 + 25, 1)
            if max(cut + values["split_lap_mm"], piece["bbox_mm"][2] - cut) <= volume[2]:
                split = cut
        rows.append({**piece, "fits_build_volume": fits, "parts_if_cut_across_longest_edge": parts,
                     "suggested_split_z_mm": split,
                     "mass_estimate_g": round(piece["shell_volume_cm3"] * density)})
    return rows


def interface_checks(report, values, module_plan):
    """Plain geometric comparisons between modules and body measurements; no collision model."""
    m, p = report["measurements_mm"], report["parameters_mm"]
    checks = []

    def add(check_id, text, value, limit, ok):
        checks.append({"id": check_id, "check": text, "value_mm_or_deg": value, "limit": limit,
                       "result": "ok" if ok else "review"})

    if all(m.get(f"thigh_circumference_{side}") is not None for side in SIDES) and m.get("hip_width") is not None:
        thighs = round(values["limbs_mm"][4][0] + values["limbs_mm"][5][0], 1)
        add("IF01", "Beide Oberschenkelschalen nebeneinander gegen die Hueftbreite der Huelle", thighs, p["hip_width"],
            thighs <= p["hip_width"])
    for module in module_plan:
        if module["kind"] in ("arm", "leg"):
            joint = "elbow" if module["kind"] == "arm" else "knee"
            flex = module[f"{joint}_free_flex_estimate_deg"]
            add("IF02", f"{module['id']}: geschaetzte freie Beugung fuer Sitzen und Greifen", flex, 90.0, flex >= 90)
        if module["kind"] == "torso":
            add("IF03", "Freie Einstiegsbreite bei ausgefahrenen Fluegeln gegen den Bedarf des Profils",
                module["clear_entry_width_mm"], p["entry_width_required"],
                module["clear_entry_width_mm"] >= p["entry_width_required"])
        if module["kind"] == "helmet" and m.get("head_width") is not None and m.get("head_depth") is not None:
            # A review here is expected: it is the reason for the opening rear shell.
            add("IF04", "Halsoeffnung gegen Kopfbreite; kleiner bedeutet Einstieg nur ueber die hintere Schale",
                module["neck_opening_mm"][0], m["head_width"], module["neck_opening_mm"][0] >= m["head_width"])
    return checks


def module_checks(kind):
    return sorted(MODULE_CHECKS["common"] + MODULE_CHECKS[kind])


def modules(values):
    open_fields = {"hardware_model": None, "measured_mass_g": None, "measured_donning_time_s": None,
                   "physical_test_passed": False}
    arms, legs = [], []
    for column, side in enumerate(SIDES):
        upper_l = values["limbs_mm"][column][1]
        fore_d, fore_l = values["limbs_mm"][2 + column]
        thigh_d, thigh_l = values["limbs_mm"][4 + column]
        shin_d, shin_l = values["limbs_mm"][6 + column]
        arms.append({
            "id": f"arm_module_{side}", "module": "M4" if side == "l" else "M5", "kind": "arm",
            "label": "Armmodul", "side": side, "source": "ArmModule.scad",
            "segments": [f"upperarm_{side}", f"forearm_{side}"],
            "overall_length_mm": round(upper_l + values["elbow_gap_mm"] + fore_l, 3),
            "elbow_gap_mm": values["elbow_gap_mm"], "elbow_relief_mm": values["elbow_relief_mm"],
            "elbow_free_flex_estimate_deg": free_flex_deg(fore_d, values["elbow_gap_mm"], values["elbow_relief_mm"]),
            "opening_side": "Beide Schalen oeffnen zur Innenseite; Scharniere aussen",
            "hinge_pins_mm": [round(upper_l - values["elbow_relief_mm"] + 6, 1),
                              round(fore_l - values["elbow_relief_mm"] + 6, 1)],
            "hang_point": "Gurtlasche oben an der hinteren Oberarmschale; Gegenstueck am Rueckenfluegel des Torsomoduls",
            "elbow_link": "Gurtband zwischen zwei Laschen an den hinteren Schalen; kein starres Gelenk",
            "elbow_link_length_mm": link_lengths(
                values["limbs_mm"][column][0] / 2, fore_d / 2, values["elbow_gap_mm"] / 2 - LUG_SLOT_CENTRE_MM,
                free_flex_deg(fore_d, values["elbow_gap_mm"], values["elbow_relief_mm"]), 0.0, True),
            "latch_lands": 2, "target_hand_latches": 2, "measured_elbow_flex_deg": None, **open_fields,
        })
        legs.append({
            "id": f"leg_module_{side}", "module": "M1" if side == "l" else "M2", "kind": "leg",
            "label": "Beinmodul", "side": side, "source": "LegModule.scad",
            "segments": [f"thigh_{side}", f"shin_{side}", f"kneepad_{side}", f"shoe_cover_{side}"],
            "overall_length_mm": round(thigh_l + values["knee_gap_mm"] + shin_l + values["ankle_gap_mm"] +
                                       values["boot_height_mm"], 3),
            "knee_gap_mm": values["knee_gap_mm"], "knee_relief_mm": values["knee_relief_mm"],
            "knee_free_flex_estimate_deg": free_flex_deg(max(thigh_d, shin_d), values["knee_gap_mm"],
                                                         values["knee_relief_mm"]),
            "shoe_cover_mm": values["boots_mm"][column] + [values["boot_height_mm"]],
            "opening_side": "Beide Schalen oeffnen zur Innenseite; Schuhcover wird von vorn aufgesetzt",
            "hinge_pins_mm": [round(thigh_l - values["knee_relief_mm"] + 6, 1),
                              round(shin_l - values["knee_relief_mm"] + 6, 1)],
            "hang_point": "Gurtlasche oben aussen an der hinteren Oberschenkelschale; Gegenstueck am Guertel des Torsomoduls",
            "knee_link": "Gurtband aussen-hinten zwischen zwei Laschen; Kniepad haengt textil davor, kein starres Gelenk",
            "ankle_link": "Gurtband von der unteren Schienbeinlasche zum Schuhcover; Fersengurt durch zwei Schlitze",
            "knee_link_length_mm": link_lengths(
                thigh_d / 2, shin_d / 2, values["knee_gap_mm"] / 2 + values["knee_relief_mm"] - LUG_SLOT_CENTRE_MM,
                free_flex_deg(max(thigh_d, shin_d), values["knee_gap_mm"], values["knee_relief_mm"]),
                LEG_LUG_AZIMUTH_DEG, False),
            "latch_lands": 2, "target_hand_latches": 3, "measured_knee_flex_deg": None, **open_fields,
        })
    width, depth, height = values["torso_mm"]
    torso = {
        "id": "torso_module", "module": "M3", "kind": "torso", "label": "Torsomodul", "side": None,
        "source": "TorsoModule.scad",
        "segments": ["rear_wing_l", "rear_wing_r", "door_l", "door_r",
                     "belt_rear_l", "belt_rear_r", "belt_door_l", "belt_door_r"],
        "overall_height_mm": round(height + values["belt_gap_mm"] + values["belt_height_mm"], 3),
        "clear_entry_width_mm": round(width - 2 * values["wall_mm"] + 2 * values["entry_slide_mm"], 3),
        "opening_side": "Rueckenfluegel fahren seitlich aus, danach schwenken die Fronttueren nach aussen",
        "hang_points": "Zwei Laschen oben an den Rueckenfluegeln (Armmodule), zwei unten am Guertel (Beinmodule)",
        "belt_link": "Guertel haengt textil unter dem Brustteil; keine starre Verbindung ueber die Taille",
        "not_modelled": "Traeger, Fuehrung der Fluegel, Schulterhauben, Kragen und Servicepod",
        "latch_lands": 3, "target_hand_latches": 3, **open_fields,
    }
    h_width, h_depth, h_height = values["helmet_mm"]
    # Section of the inner ellipsoid at the flat neck cut, see HelmetModule.scad.
    neck = math.sqrt(1 - ((0.45 * h_height) / (0.55 * h_height - values["wall_mm"])) ** 2)
    helmet = {
        "id": "helmet_module", "module": "M6", "kind": "helmet", "label": "Helmmodul", "side": None,
        "source": "HelmetModule.scad", "segments": ["helmet_front", "helmet_rear"],
        "neck_opening_mm": [round((h_width - 2 * values["wall_mm"]) * neck, 1),
                            round((h_depth - 2 * values["wall_mm"]) * neck, 1)],
        "opening_side": "Hintere Schale schwenkt um eine seitliche virtuelle Achse; Verschluss auf der Gegenseite unten",
        "not_modelled": "Visier, Polster, Halsabdeckung, Lueftung, Elektronik und jede Schutzwirkung",
        "latch_lands": 1, "target_hand_latches": 1, **open_fields,
    }
    return legs + [torso] + arms + [helmet]


def parameters(report):
    p = report["parameters_mm"]
    # Each shell ends one edge clearance short of the joint centre, so the gap between
    # two shells is twice that clearance. A wider gap would make the module longer than the limb.
    joint_gap = 2.0 * report["allowances_mm"]["edge_clearance"]
    return {
        "wall_mm": p["wall"], "seam_gap_mm": 2.0,
        "hinge_offset_mm": 8.0, "opening_deg": 110.0,
        "hinge_pin_d_mm": 3.0, "hinge_knuckle_mm": 20.0, "hinge_clearance_mm": 0.4, "split_lap_mm": 15.0,
        "elbow_gap_mm": joint_gap, "elbow_relief_mm": 50.0,
        "knee_gap_mm": joint_gap, "knee_relief_mm": 95.0, "ankle_gap_mm": 25.0, "boot_height_mm": 110.0,
        "belt_height_mm": 110.0, "belt_gap_mm": 20.0,
        "helmet_opening_deg": 100.0, "helmet_split_fraction": 0.12,
        "strap_width_mm": 25.0, "latch_pad_mm": [30.0, 18.0, 4.0],
        "latch_hole_d_mm": 0.0, "latch_holes_mm": [], "keeper_holes_mm": [],
        "limbs_mm": [[p[f"{part}_diameter_{side}"], p[f"{part}_length_{side}"]]
                     for part in PARTS for side in SIDES],
        "boots_mm": [[p[f"boot_width_{side}"], p[f"boot_length_{side}"]] for side in SIDES],
        "torso_mm": [p["torso_width"], p["torso_depth"], p["torso_height"]],
        "hip_mm": [p["hip_width"], p["hip_depth"]],
        "shoulder_span_mm": p["shoulder_span"], "entry_slide_mm": p["entry_slide_each_side"],
        "helmet_mm": [p["helmet_width"], p["helmet_depth"], p["helmet_height"]],
    }


def plan(report, values, build_volume=DEFAULT_BUILD_VOLUME_MM, density=DEFAULT_DENSITY_G_CM3):
    parts = []
    for index, part in enumerate(PARTS):
        for side in SIDES:
            diameter, length = values["limbs_mm"][index * 2 + SIDES.index(side)]
            parts.append({
                "id": f"{part}_{side}", "label": LABELS[index], "side": side,
                "diameter_mm": diameter, "length_mm": length,
                "inner_gauge_diameter_mm": round(diameter - 2 * values["wall_mm"], 3),
                "cross_section": "CIRCUMFERENCE_EQUIVALENT_CIRCLE_NOT_ANATOMY",
                "hinge": "Aussen/laengs; nur virtuelle Drehachse im Modell",
                "closure": "Vorne/innen, mit Gegenhand erreichbar; manueller Rastverschluss mit Sicherung",
                "park": "Formschluessige offene Position; am Tisch auslegen und betaetigen",
                "release": "Eigene von vorn erreichbare mechanische Entriegelung, stromunabhaengig",
                "strap": "Vollstaendig oeffnender Gurt mit gefangenem Ende; kein verbleibender Ring",
                "wiring": "Keine Leitung ueber freie Eintrittsfuge; Zugentlastung an beiden Seiten des Scharniers",
                "hardware_model": None, "measured_opening_force_n": None,
                "measured_release_force_n": None, "measured_mass_g": None,
                "physical_test_passed": False,
            })
    rows = print_plan(values, build_volume, density)
    module_plan = modules(values)
    for module in module_plan:
        module["shell_mass_estimate_g"] = sum(row["mass_estimate_g"] for row in rows if row["module"] == module["id"])
    return {"schema_version": 1, "project": report["profile"],
            "status": "CLAMSHELL_ENVELOPES_NOT_VALIDATED",
            "fit_status": report["status"], "fabrication_approved": False,
            "solo_donning_verified": False, "parts": parts,
            "modules": module_plan, "interface_checks": interface_checks(report, values, module_plan),
            "print_assumptions": {
                "build_volume_mm": list(build_volume), "density_g_cm3": density,
                "note": "Bauraum und Dichte sind Eingaben. Masse = Schalenvolumen mal Dichte bei massiver Wand; "
                        "ohne Laschen, Verschluesse, Polster, Gurte, Lack und Elektronik.",
            },
            "print_plan": rows,
            "limits": [
                "Module: Laschen und Verschlussflaechen sind unbemessene Platzhalter; Gelenkspalte, Freischnitte und Beugewinkel sind Annahmen.",
                "Verschluss-Lochbild entsteht nur aus eingetragenen Datenblattwerten; ohne Eintrag bleiben die Flaechen ungebohrt.",
                "Torso und Helm sind Huellen aus Breite, Tiefe und Hoehe; Traeger, Fuehrungen, Visier und Polster fehlen.",
                "Runde, gerade Huellen aus Umfaengen; reale Breite, Tiefe und anatomische Verjuengung fehlen.",
                "Arm- und Beinmodule haben gedruckte Scharnieraugen fuer einen Kaufstift; Spiel, Stift und Haltbarkeit sind unerprobt.",
                "Torso und Helm drehen weiter um virtuelle Achsen; Kaufverschluesse sind nirgends integriert.",
                "Keine 3D-Kollisionspruefung, Lastbemessung, Passform- oder Alleinanziehfreigabe.",
                "Handschale, Schulterhauben und Halsabdeckung benoetigen separate offene Schnittstellen.",
            ]}


def readme(report):
    return "\n".join([
        "# Aufklappbare Arm- und Beinhuellen", "",
        "Profil: **" + report["profile"] + "** / " + report["status"], "",
        "Status: **CLAMSHELL_ENVELOPES_NOT_VALIDATED**. Keine fertige Halo-Ruestung.",
        "Vier Typen mit getrennten linken/rechten Massen. Die Vorderhaelfte dreht um",
        "eine aussen liegende, gespiegelte Z-Achse; die hintere Auflage bleibt stehen.",
        "Die virtuelle Achse zeigt Bewegung und ist kein druckfertiges Scharnier.", "",
        "## Portable CAD-Dateien", "",
        "LimbClamshell.scad bindet ausschliesslich die benachbarte Parameters.scad ein.",
        "Alle Masse in mm; opening_deg in Grad. Parameters.scad ist editierbar.",
        "Reihenfolge von limbs_mm: upperarm_l, upperarm_r, forearm_l, forearm_r,",
        "thigh_l, thigh_r, shin_l, shin_r; je [Aussendurchmesser, Laenge].",
        "Diese geraden Kreishuellen ersetzen keine am Koerper gemessenen Querschnitte.", "",
        "```bash",
        "openscad --hardwarnings -D 'part=\"forearm\"' -D 'side=\"l\"' -D 'open_fraction=1' -o forearm_l_open.stl LimbClamshell.scad",
        "openscad --hardwarnings -D 'part=\"shin\"' -D 'side=\"r\"' -D 'piece=\"front\"' -o shin_r_front.stl LimbClamshell.scad",
        "```", "",
        "Selektoren: part=upperarm/forearm/thigh/shin; side=l/r; open_fraction=0..1;",
        "piece=assembly/rear/front. assembly ist eine Bewegungsansicht, kein Drucklayout.",
        "Die Vorschau markiert die virtuelle Achse; sie ist nicht Teil der STL-Ausgabe.",
        "Nach Parameterbearbeitung gelten die Manifest-Hashes des Originalexports nicht",
        "fuer die geaenderte Geometrie. Fuer eine neue Profilrevision neu exportieren.", "",
        "## Sechs Module", "",
        "Vier weitere Dateien setzen die Huellen zu den sechs Modulen des Zielbilds",
        "zusammen; ModuleCommon.scad enthaelt die gemeinsamen Bausteine der Arm- und",
        "Beinmodule. ArmModule.scad: Oberarm und Unterarm. LegModule.scad:",
        "Oberschenkel, Kniepad, Schienbein und Schuhcover. TorsoModule.scad: zwei",
        "Rueckenfluegel, zwei Fronttueren, Guertel und die vier Aufnahmen fuer Arm- und",
        "Beinmodule. HelmetModule.scad: vordere Schale und seitlich schwenkende hintere",
        "Schale. Gelenke bleiben frei; die Schalen verbindet Gurtband an Laschen.", "",
        "```bash",
        "openscad --hardwarnings -D 'side=\"l\"' -D 'open_fraction=1' -o arm_l_open.stl ArmModule.scad",
        "openscad --hardwarnings -D 'side=\"r\"' -D 'segment=\"shin\"' -D 'piece=\"rear\"' -o shin_r_rear.stl LegModule.scad",
        "openscad --hardwarnings -D 'piece=\"door\"' -D 'side=\"l\"' -o door_l.stl TorsoModule.scad",
        "openscad --hardwarnings -D 'piece=\"rear\"' -o helmet_rear.stl HelmetModule.scad",
        "```", "",
        "Arm: side, open_fraction, elbow_flex_deg=0..150, piece=assembly/rear/front,",
        "segment=both/upperarm/forearm. Bein: side, open_fraction, knee_flex_deg=0..150,",
        "piece=assembly/rear/front, segment=all/thigh/shin/kneepad/shoe. Torso: side,",
        "open_fraction, piece=assembly/rear/door/belt_rear/belt_door. Helm:",
        "hinge_side=l/r, open_fraction, piece=assembly/front/rear. Zum Drucken ein",
        "einzelnes Teil waehlen; assembly ist eine Bewegungsansicht.", "",
        "Verschlussflaechen bleiben ungebohrt, solange latch_holes_mm und",
        "keeper_holes_mm leer sind. Jeder Eintrag ist [quer, laengs]: Abstand von der",
        "Fugenmitte und Versatz entlang der Fuge ab Flaechenmitte, aus dem Datenblatt",
        "des gekauften Verschlusses. latch_hole_d_mm ist der Bohrdurchmesser,",
        "latch_pad_mm muss Grundflaeche und Lochbild aufnehmen. Laschen sind nicht",
        "bemessen. Die im Plan genannten freien Beugewinkel sind Schaetzungen fuer",
        "gerade Rundhuellen, keine gemessenen Werte.", "",
        "Arm- und Beinschalen tragen aussen abwechselnde Scharnieraugen fuer einen",
        "durchgehenden Stift (hinge_pin_d_mm, Laengen je Schale im Plan). Zu lange",
        "Teile lassen sich mit split_z_mm und split_keep=lower/upper an einer",
        "Ueberlappungsfuge teilen; PrintPlan.csv schlaegt die Hoehe vor. Beides ist",
        "ungedruckt: Spiel, Klebung der Fuge und Haltbarkeit zeigt erst der Prototyp.", "",
        "SuitAssembly.scad zeigt alle sechs Module als einfache Koerper in einer Figur",
        "und faerbt Ueberschneidungen rot. Die seitliche Lage von Beinen und Armen ist",
        "dort eine Anzeigeannahme (leg_spread_mm, arm_gap_mm), kein Koerpermass.", "",
        "## Druckplan und Massen", "",
        "PrintPlan.csv nennt je Druckteil Huellmasse, ob es achsparallel in den",
        "angegebenen Bauraum passt, die Zahl der Stuecke bei Teilung quer zur laengsten",
        "Kante, Schalenvolumen und geschaetzte Masse. Bauraum und Dichte sind Eingaben",
        "(--build-volume, --density) und stehen in ClamshellPlan.json. Die Masse gilt",
        "fuer massive Wand ohne Laschen, Verschluesse, Polster, Gurte, Lack und",
        "Elektronik; Teilungsfugen, Stuetzstruktur und Druckrichtung sind nicht",
        "bewertet. ClamshellPlan.json enthaelt ausserdem die Bandlaengen der",
        "Gelenkverbindungen und einfache Schnittstellenvergleiche (interface_checks).", "",
        "## Reale Mechanik", "",
        "ClamshellPlan.json beschreibt alle acht Kassetten und laesst Kaufteile, Kraefte",
        "und Testergebnisse unbekannt. Ein ungemessener Standardwinkel von 110 Grad",
        "und 8 mm Achsabstand zeigen die Bewegung; beide sind keine Bauvorgabe.",
        "Gurte oeffnen auf der Verschlussseite vollstaendig. Keine Rohrmanschette,",
        "Fussschlaufe oder Kabelbruecke darf die Eintrittsfuge wieder schliessen.",
        "Manuelle Scharniere, eindeutig rastende Verschluesse und eigene Offenhalter",
        "werden am leichten Prototyp erprobt. Keine koerpergelenkfuehrenden Scharniere.", "",
        "## Nachweise", "",
        "Checklists.csv startet fuer jede Kassette und den Gesamtanzug offen.",
        "Entwicklungsproben mit Beobachter und leichter Attrappe; der spaetere normale",
        "Ablauf allein ist erst nach drei dokumentierten Gesamtfolgen nachgewiesen.",
        "Offene Querschnitte, reale Reichweite beider Haende und der letzte Handschuh",
        "sind separat zu pruefen. Eine Software-/STL-Pruefung setzt keinen Haken.", "",
        "Profile.json ist ein exakter lokaler Profilsnapshot und kann Koerpermasse enthalten.",
        "Manifest.json bindet Profil, CAD-Quelle und Parameterdatei mit SHA-256.", "",
    ])


def print_csv(rows):
    handle = io.StringIO(newline="")
    writer = csv.writer(handle)
    writer.writerow(["piece", "module", "bbox_x_mm", "bbox_y_mm", "bbox_z_mm", "fits_build_volume",
                     "parts_if_cut_across_longest_edge", "suggested_split_z_mm", "shell_volume_cm3", "mass_estimate_g"])
    for row in rows:
        parts = row["parts_if_cut_across_longest_edge"]
        writer.writerow([row["id"], row["module"], *row["bbox_mm"], "yes" if row["fits_build_volume"] else "no",
                         "" if parts is None else parts,
                         "" if row["suggested_split_z_mm"] is None else row["suggested_split_z_mm"],
                         row["shell_volume_cm3"], row["mass_estimate_g"]])
    return handle.getvalue()


def export(profile_path, out, concept=False, build_volume=DEFAULT_BUILD_VOLUME_MM, density=DEFAULT_DENSITY_G_CM3):
    profile_path, out = Path(profile_path), Path(out)
    profile_bytes = profile_path.read_bytes()
    profile = json.loads(profile_bytes)
    report = suit_fit.derive(profile, concept=concept)
    if profile["status"] == "synthetic" and not concept:
        raise ValueError("Synthetisches Profil erfordert --concept")
    values = parameters(report)
    if out.resolve().is_relative_to(SOURCE.resolve()):
        raise ValueError("Ausgabe darf nicht im Clamshell-Quellordner liegen")
    if out.exists() or out.is_symlink():
        raise ValueError("Ausgabe existiert bereits; neuen Revisionsordner waehlen")
    source = (SOURCE / "LimbClamshell.scad").read_bytes()
    module_sources = {name: (SOURCE / name).read_bytes() for name in MODULE_SOURCES}
    module_plan = modules(values)
    parameter_bytes = ("// GENERATED: opening envelopes only; mm except opening_deg.\n" +
                       "\n".join(f"{key} = {json.dumps(value)};" for key, value in values.items()) +
                       "\n").encode("utf-8")
    manifest = {"schema_version": 1, "profile": report["profile"],
                "status": "CLAMSHELL_ENVELOPES_NOT_VALIDATED", "fit_status": report["status"],
                "fabrication_approved": False, "solo_donning_verified": False,
                "profile_sha256": hashlib.sha256(profile_bytes).hexdigest(),
                "source_sha256": hashlib.sha256(source).hexdigest(),
                "module_sources_sha256": {name: hashlib.sha256(data).hexdigest()
                                          for name, data in module_sources.items()},
                "parameters_sha256": hashlib.sha256(parameter_bytes).hexdigest(),
                "parts": [f"{part}_{side}" for part in PARTS for side in SIDES],
                "modules": [module["id"] for module in module_plan],
                "parameters": values,
                "parameter_origin": {"wall_mm": "profile_allowance", "limbs_mm": "profile_circular_envelope",
                                     "seam_gap_mm": "concept_assumption", "hinge_offset_mm": "concept_assumption",
                                     "opening_deg": "concept_assumption", "elbow_gap_mm": "profile_allowance",
                                     "hinge_pin_d_mm": "concept_assumption", "hinge_knuckle_mm": "concept_assumption",
                                     "hinge_clearance_mm": "concept_assumption", "split_lap_mm": "concept_assumption",
                                     "elbow_relief_mm": "concept_assumption", "strap_width_mm": "concept_assumption",
                                     "latch_pad_mm": "concept_assumption",
                                     "knee_gap_mm": "profile_allowance", "knee_relief_mm": "concept_assumption",
                                     "ankle_gap_mm": "concept_assumption", "boot_height_mm": "concept_assumption",
                                     "belt_height_mm": "concept_assumption", "belt_gap_mm": "concept_assumption",
                                     "helmet_opening_deg": "concept_assumption",
                                     "helmet_split_fraction": "concept_assumption",
                                     "latch_hole_d_mm": "unset_until_latch_datasheet",
                                     "latch_holes_mm": "unset_until_latch_datasheet",
                                     "keeper_holes_mm": "unset_until_latch_datasheet",
                                     "boots_mm": "profile_shoe_envelope", "torso_mm": "profile_box_envelope",
                                     "hip_mm": "profile_box_envelope", "shoulder_span_mm": "profile_box_envelope",
                                     "entry_slide_mm": "profile_allowance", "helmet_mm": "profile_box_envelope"}}
    rows = io.StringIO(newline="")
    writer = csv.writer(rows)
    writer.writerow(["test_id", "part_id", "task", "revision", "observer", "status", "evidence", "notes"])
    for part in manifest["parts"] + ["complete_suit"]:
        for key, task in CHECKS:
            if (part == "complete_suit") == (key in ("OPEN09", "OPEN10")):
                writer.writerow([key, part, task, "", "", "open", "", ""])
    for module in module_plan:
        for key, task in module_checks(module["kind"]):
            writer.writerow([key, module["id"], task, "", "", "open", "", ""])
    full_plan = plan(report, values, build_volume, density)
    texts = {"Manifest.json": json.dumps(manifest, indent=2, ensure_ascii=True) + "\n",
             "ClamshellPlan.json": json.dumps(full_plan, indent=2, ensure_ascii=True) + "\n",
             "PrintPlan.csv": print_csv(full_plan["print_plan"]),
             "Checklists.csv": rows.getvalue(), "README.md": readme(report)}
    out.mkdir(parents=True, exist_ok=False)
    (out / "Profile.json").write_bytes(profile_bytes)
    (out / "LimbClamshell.scad").write_bytes(source)
    for name, data in module_sources.items():
        (out / name).write_bytes(data)
    (out / "Parameters.scad").write_bytes(parameter_bytes)
    for name, content in texts.items():
        (out / name).write_text(content, encoding="utf-8")
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--concept", action="store_true")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--build-volume", type=float, nargs=3, metavar=("X", "Y", "Z"),
                        default=DEFAULT_BUILD_VOLUME_MM, help="Bauraum des Druckers in mm")
    parser.add_argument("--density", type=float, default=DEFAULT_DENSITY_G_CM3,
                        help="Materialdichte in g/cm3 (PLA etwa 1.24, PETG 1.27, ABS/ASA 1.05)")
    args = parser.parse_args(argv)
    try:
        result = export(args.profile, args.out, concept=args.concept,
                        build_volume=tuple(args.build_volume), density=args.density)
        print(json.dumps({"out": str(args.out), "status": result["status"], "parts": result["parts"],
                          "modules": result["modules"]}))
        return 0
    except (ValueError, OSError, TypeError, KeyError) as exc:
        print("Clamshell-Fehler: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
