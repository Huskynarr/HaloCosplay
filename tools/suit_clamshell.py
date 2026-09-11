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


def parameters(report):
    p = report["parameters_mm"]
    return {
        "wall_mm": p["wall"], "seam_gap_mm": 2.0,
        "hinge_offset_mm": 8.0, "opening_deg": 110.0,
        "limbs_mm": [[p[f"{part}_diameter_{side}"], p[f"{part}_length_{side}"]]
                     for part in PARTS for side in SIDES],
    }


def plan(report, values):
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
    return {"schema_version": 1, "project": report["profile"],
            "status": "CLAMSHELL_ENVELOPES_NOT_VALIDATED",
            "fit_status": report["status"], "fabrication_approved": False,
            "solo_donning_verified": False, "parts": parts,
            "limits": [
                "Runde, gerade Huellen aus Umfaengen; reale Breite, Tiefe und anatomische Verjuengung fehlen.",
                "Bewegliche Schalenhaelften, keine konstruierten Scharniere oder integrierten Kaufverschluesse.",
                "Keine 3D-Kollisionspruefung, Lastbemessung, Passform- oder Alleinanziehfreigabe.",
                "Schuhcover, Handschale, Torso, Schulter und Helm benoetigen separate offene Schnittstellen.",
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


def export(profile_path, out, concept=False):
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
    parameter_bytes = ("// GENERATED: opening envelopes only; mm except opening_deg.\n" +
                       "\n".join(f"{key} = {json.dumps(value)};" for key, value in values.items()) +
                       "\n").encode("utf-8")
    manifest = {"schema_version": 1, "profile": report["profile"],
                "status": "CLAMSHELL_ENVELOPES_NOT_VALIDATED", "fit_status": report["status"],
                "fabrication_approved": False, "solo_donning_verified": False,
                "profile_sha256": hashlib.sha256(profile_bytes).hexdigest(),
                "source_sha256": hashlib.sha256(source).hexdigest(),
                "parameters_sha256": hashlib.sha256(parameter_bytes).hexdigest(),
                "parts": [f"{part}_{side}" for part in PARTS for side in SIDES],
                "parameters": values,
                "parameter_origin": {"wall_mm": "profile_allowance", "limbs_mm": "profile_circular_envelope",
                                     "seam_gap_mm": "concept_assumption", "hinge_offset_mm": "concept_assumption",
                                     "opening_deg": "concept_assumption"}}
    rows = io.StringIO(newline="")
    writer = csv.writer(rows)
    writer.writerow(["test_id", "part_id", "task", "revision", "observer", "status", "evidence", "notes"])
    for part in manifest["parts"] + ["complete_suit"]:
        for key, task in CHECKS:
            if (part == "complete_suit") == (key in ("OPEN09", "OPEN10")):
                writer.writerow([key, part, task, "", "", "open", "", ""])
    texts = {"Manifest.json": json.dumps(manifest, indent=2, ensure_ascii=True) + "\n",
             "ClamshellPlan.json": json.dumps(plan(report, values), indent=2, ensure_ascii=True) + "\n",
             "Checklists.csv": rows.getvalue(), "README.md": readme(report)}
    out.mkdir(parents=True, exist_ok=False)
    (out / "Profile.json").write_bytes(profile_bytes)
    (out / "LimbClamshell.scad").write_bytes(source)
    (out / "Parameters.scad").write_bytes(parameter_bytes)
    for name, content in texts.items():
        (out / name).write_text(content, encoding="utf-8")
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--concept", action="store_true")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        result = export(args.profile, args.out, concept=args.concept)
        print(json.dumps({"out": str(args.out), "status": result["status"], "parts": result["parts"]}))
        return 0
    except (ValueError, OSError, TypeError, KeyError) as exc:
        print("Clamshell-Fehler: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
