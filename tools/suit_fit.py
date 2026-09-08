#!/usr/bin/env python3
"""Reproducible fit envelopes, not fabrication approval. Standard library only."""
import argparse
import html
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE = ROOT / "Design/Parametric/Profiles/Huskynarr.json"

# Synthetic design mannequin; NONE of these values are user measurements.
DEMO = {
    "height": 1660, "shoulder_width": 490, "chest_width": 410,
    "chest_depth": 290, "abdomen_width": 420, "abdomen_depth": 320,
    "torso_length": 420, "hip_width": 410, "hip_depth": 310,
    "head_width": 165, "head_depth": 205, "head_height": 245,
}
for side in ("l", "r"):
    DEMO.update({f"{key}_{side}": value for key, value in {
        "upperarm_length": 285, "upperarm_circumference": 360,
        "forearm_length": 245, "forearm_circumference": 310,
        "thigh_length": 365, "thigh_circumference": 590,
        "shin_length": 345, "calf_circumference": 405,
        "boot_width": 115, "boot_length": 275,
    }.items()})

ALLOWANCES = {
    "padding_radial": (0, 30), "clearance_radial": (1, 50),
    "shell_wall": (1, 8), "edge_clearance": (5, 60),
    "entry_clearance_each_side": (10, 100),
    "shoulder_visual_extension_each_side": (0, 80),
}


def number(value, name, low, high):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name}: endliche Zahl in mm erforderlich")
    if not math.isfinite(value) or not low <= value <= high:
        raise ValueError(f"{name}: ausserhalb {low}..{high} mm; Einheit pruefen")
    return float(value)


def bounds(key):
    if key == "height":
        return 1200, 2200
    if "circumference" in key:
        return 150, 1000
    if key.startswith("boot_width"):
        return 60, 200
    if key.startswith("head_"):
        return 100, 350
    return 100, 700


def derive(profile, concept=False):
    if profile.get("schema_version") != 1:
        raise ValueError("Unbekannte schema_version")
    raw = profile.get("measurements_mm")
    if not isinstance(raw, dict):
        raise ValueError("measurements_mm muss ein Objekt sein")
    if set(raw) != set(DEMO):
        raise ValueError("Messfelder fehlen oder sind unbekannt: " +
                         ", ".join(sorted(set(raw) ^ set(DEMO))))
    missing = sorted(key for key, value in raw.items() if value is None)
    if raw["height"] is None:
        raise ValueError("Koerpergroesse muss vorliegen; keine stille Schaetzung")
    if missing and not concept:
        raise ValueError("Fehlende Masse: " + ", ".join(missing) +
                         ". Fuer eine gekennzeichnete Konzeptansicht: --concept")
    m = {k: number(DEMO[k] if v is None else v, k, *bounds(k)) for k, v in raw.items()}
    # Do not scale synthetic widths from stature: broad shoulders are independent.
    for key in m:
        if key != "height" and m[key] >= m["height"]:
            raise ValueError(f"{key}: unplausibel gegenueber Koerpergroesse")
    if m["chest_width"] > m["shoulder_width"] + 120:
        raise ValueError("Brust-/Schulterbreite: Messdefinition pruefen")
    a = profile.get("allowances_mm", {})
    if set(a) != set(ALLOWANCES):
        raise ValueError("allowances_mm: vollstaendiger Parametersatz erforderlich")
    a = {k: number(v, k, *ALLOWANCES[k]) for k, v in a.items()}
    radial = a["padding_radial"] + a["clearance_radial"]
    wall, edge = a["shell_wall"], a["edge_clearance"]
    p = {
        "body_height": m["height"], "wall": wall, "radial_allowance": radial,
        "torso_width": max(m["chest_width"], m["abdomen_width"]) + 2 * (radial + wall),
        "torso_depth": max(m["chest_depth"], m["abdomen_depth"]) + 2 * (radial + wall),
        "torso_height": m["torso_length"] - 2 * edge,
        "shoulder_span": m["shoulder_width"] + 2 * (radial + wall + a["shoulder_visual_extension_each_side"]),
        "entry_width_required": max(m["shoulder_width"], m["hip_width"], m["chest_width"], m["abdomen_width"]) + 2 * a["entry_clearance_each_side"],
        "hip_width": m["hip_width"] + 2 * (radial + wall),
        "hip_depth": m["hip_depth"] + 2 * (radial + wall),
        "helmet_width": m["head_width"] + 2 * (radial + wall),
        "helmet_depth": m["head_depth"] + 2 * (radial + wall),
        "helmet_height": m["head_height"] + radial + wall,
        "concept_only": bool(missing) or profile.get("status") == "synthetic",
    }
    # Slide the side wings outward before pivoting doors. This is a packaging
    # requirement, not a validated telescopic joint or human passage proof.
    p["entry_slide_each_side"] = max(0, (p["entry_width_required"] -
                                            (p["torso_width"] - 2*wall)) / 2)
    for side in ("l", "r"):
        for part, circ in (("upperarm", "upperarm"), ("forearm", "forearm"),
                           ("thigh", "thigh"), ("shin", "calf")):
            p[f"{part}_length_{side}"] = m[f"{part}_length_{side}"] - 2 * edge
            # Circumference-equivalent circular gauge only, not anatomical width.
            p[f"{part}_diameter_{side}"] = m[f"{circ}_circumference_{side}"] / math.pi + 2 * (radial + wall)
        for axis in ("width", "length"):
            p[f"boot_{axis}_{side}"] = m[f"boot_{axis}_{side}"] + 2 * (a["clearance_radial"] + wall)
    if any(v <= 0 for k, v in p.items() if not isinstance(v, bool) and k != "entry_slide_each_side"):
        raise ValueError("Zuschlaege ergeben nichtpositive Geometrie")
    return {
        "schema_version": 1,
        "profile": str(profile.get("profile", "unnamed")),
        "status": "CONCEPT_NOT_MEASURED" if p["concept_only"] else "MEASURED_ENVELOPE_NOT_VALIDATED",
        "fabrication_approved": False,
        "missing_measurements": missing,
        "measurement_sources": {k: "synthetic_concept" if k in missing or profile.get("status") == "synthetic" else "profile_input" for k in m},
        "measurements_mm": m, "allowances_mm": a,
        "parameters_mm": {k: round(v, 3) if not isinstance(v, bool) else v for k, v in p.items()},
        "limits": [
            "Keine Freigabe fuer Fertigung, Festigkeit, Passform oder Kollisionsfreiheit.",
            "Kreisquerschnitte aus Umfaengen sind nur Testlehren; Breite/Tiefe am Koerper pruefen.",
            "Darstellungspositionen der Baugruppen sind keine gemessenen Gelenkachsen.",
            "Koerpergewicht und Hersteller-Passmasse fuer aktive Exoskelett-Auswahl fehlen separat.",
        ],
    }


def opening_envelope(width, depth, angle_deg, slide_each_side=0):
    """Conservative 2D AABB of paired rigid L-shaped front doors (zero wall).

    Each half runs from (W/2,0) around (W/2,-D/2) to (0,-D/2).
    Positive angle opens the right door outwards toward negative y (front).
    """
    w = number(width, "width", 1, 3000)
    d = number(depth, "depth", 1, 3000)
    slide = number(slide_each_side, "slide_each_side", 0, 300)
    angle = math.radians(number(angle_deg, "angle", 0, 110))
    c, s = math.cos(angle), math.sin(angle)
    points = []
    for sign in (-1, 1):
        for x, y in ((0, 0), (0, -d / 2), (-w / 2, -d / 2)):
            points.append((sign * (w / 2 + slide + c * x - s * y), s * x + c * y))
    return {"outer_width_mm": max(x for x, _ in points) - min(x for x, _ in points),
            "forward_reach_mm": max(0, -min(y for _, y in points)),
            "note": "Tuerhuelle; kein Durchgangs- oder Kollisionsnachweis"}


def report_md(report):
    p = report["parameters_mm"]
    lines = ["# Passformbericht", "", f"Status: **{report['status']}**", "",
             "Keine Fertigungsfreigabe. Zahlen mit Quelle synthetic_concept sind Beispielwerte.", "",
             "| Eingabe | mm | Herkunft |", "| --- | ---: | --- |"]
    for key, value in report["measurements_mm"].items():
        lines.append(f"| {key} | {value:g} | {report['measurement_sources'][key]} |")
    lines += ["", "## Abgeleitete Huelle", "", "| Parameter | mm |", "| --- | ---: |"]
    lines += [f"| {k} | {v} |" for k, v in p.items() if not isinstance(v, bool)]
    lines += ["", "## Oeffnung: idealisierte Tueren", "",
              "| Winkel | Aussenbreite mm | Reichweite nach vorn mm |", "| ---: | ---: | ---: |"]
    for angle in (0, 30, 60, 90, 105):
        e = opening_envelope(p["torso_width"], p["torso_depth"], angle,
                             0 if angle == 0 else p["entry_slide_each_side"])
        lines.append(f"| {angle} | {e['outer_width_mm']:.1f} | {e['forward_reach_mm']:.1f} |")
    lines += ["", "Die Eintrittsbreite wird separat im 1:1-Mockup geprueft; die Tabelle ist kein Passnachweis.", ""]
    return "\n".join(lines)


def layout_svg(report):
    p = report["parameters_mm"]
    esc = html.escape
    w, d = p["torso_width"], p["torso_depth"]
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="800" viewBox="0 0 1400 800">',
             '<rect width="1400" height="800" fill="#0c151b"/>',
             '<g font-family="sans-serif" fill="#edf4e4">',
             '<text x="55" y="60" font-size="28">MJOLNIR / FRONT ENTRY</text>',
             '<text x="55" y="95" font-size="16">Draufsicht - schematische Tueren und Eintrittsbreite</text>',
             f'<text x="55" y="130" font-size="16" fill="#ffca74">{esc(report["status"])}</text>',
             '<text x="55" y="740" font-size="15">Nur Oeffnungshuelle. Keine Kollisions-, Passform- oder Festigkeitsfreigabe.</text>',
             '<text x="55" y="767" font-size="15">Gruen: Schalen / Cyan: eigener Rueckentraeger / Orange: Scharnierachsen</text>', '</g>']
    for cx, angle in ((360, 0), (1030, 105)):
        scale, cy = 0.7, 470
        slide = 0 if angle == 0 else p["entry_slide_each_side"]
        def point(x, y):
            return f"{cx + x * scale:.2f},{cy + y * scale:.2f}"
        parts.append(f'<g fill="none" stroke-width="8"><path stroke="#68bcca" d="M {point(-w/2-slide,0)} L {point(-w/2-slide,d/2)} {point(w/2+slide,d/2)} {point(w/2+slide,0)}"/>')
        for sign in (-1, 1):
            pts = []
            a = math.radians(angle)
            for x, y in ((0, 0), (0, -d/2), (-w/2, -d/2)):
                pts.append(point(sign*(w/2+slide+math.cos(a)*x-math.sin(a)*y), math.sin(a)*x+math.cos(a)*y))
            parts.append(f'<polyline stroke="#8ba46b" points="{" ".join(pts)}"/>')
            parts.append(f'<circle fill="#ffca74" stroke="none" cx="{cx+sign*(w/2+slide)*scale}" cy="{cy}" r="7"/>')
        parts.append('</g>')
        parts.append(f'<text x="{cx}" y="645" text-anchor="middle" font-family="sans-serif" font-size="20" fill="#edf4e4">{angle} Grad / {"geschlossen" if angle == 0 else "offen"}</text>')
    parts.append('</svg>')
    return "\n".join(parts)


def export(report, out):
    out.mkdir(parents=True, exist_ok=True)
    (out / "fit-report.json").write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n")
    (out / "FitReport.md").write_text(report_md(report))
    scad = ["// GENERATED by tools/suit_fit.py. Do not hand-edit.",
            "// " + report["status"], "// Envelope only; no fabrication approval."]
    for key, value in report["parameters_mm"].items():
        scad.append(f"{key} = {json.dumps(value)};")
    (out / "parameters.scad").write_text("\n".join(scad) + "\n")
    (out / "OpeningEnvelope.svg").write_text(layout_svg(report))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    parser.add_argument("--out", type=Path, default=ROOT / "build/SuitFit")
    parser.add_argument("--concept", action="store_true", help="Use explicitly labelled synthetic dimensions where missing")
    args = parser.parse_args(argv)
    try:
        profile = json.loads(args.profile.read_text())
        report = derive(profile, args.concept)
        export(report, args.out)
    except (ValueError, OSError, TypeError) as exc:
        print(f"Fit-Fehler: {exc}", file=sys.stderr)
        return 2
    print(f"{report['status']}: {args.out}; {len(report['missing_measurements'])} offene Masse")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
