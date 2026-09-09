#!/usr/bin/env python3
"""Reproducible fit envelopes, not fabrication approval. Standard library only."""
import argparse
import html
import json
import math
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "Design/Parametric/ProfileSchema.json"
DEFAULT_PROFILE = ROOT / "Design/Parametric/Profiles/Template.json"
DEMO_PROFILE = ROOT / "Design/Parametric/Profiles/Demo.json"
MODEL_PATH = ROOT / "Design/Parametric/MjolnirEntry.scad"
SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
# Synthetic example only; never silently applied outside --concept.
DEMO = json.loads(DEMO_PROFILE.read_text(encoding="utf-8"))["measurements_mm"]
ALLOWANCES = {k: (v["min"], v["max"]) for k, v in SCHEMA["allowances"].items()}
PROFILE_STATUSES = {"measurements_pending", "synthetic", "measured"}


def profile_name(value):
    if not isinstance(value, str) or value != value.strip() or not re.fullmatch(
            r"[A-Za-z0-9][A-Za-z0-9 ._-]{0,63}", value):
        raise ValueError("profile: 1-64 ASCII-Buchstaben/Ziffern, Leerzeichen, ._-; "
                         "Beginn mit Buchstabe/Ziffer, keine aeusseren Leerzeichen")
    return value


def build_config(value=None):
    if value is None:
        value = {}
    if not isinstance(value, dict) or set(value) - (set(SCHEMA["build_fields"]) | {"features"}):
        raise ValueError("build: unbekannte Felder oder kein Objekt")
    result = {}
    for key, field in SCHEMA["build_fields"].items():
        selected = value.get(key, field["default"])
        if not isinstance(selected, str) or selected not in field["options"]:
            raise ValueError(f"build.{key}: ungueltige Auswahl")
        result[key] = selected
    features = value.get("features", {})
    if not isinstance(features, dict) or set(features) - set(SCHEMA["feature_fields"]):
        raise ValueError("build.features: unbekannte Felder oder kein Objekt")
    result["features"] = {}
    for key, field in SCHEMA["feature_fields"].items():
        selected = features.get(key, field["default"])
        if not isinstance(selected, bool):
            raise ValueError(f"build.features.{key}: bool erforderlich")
        result["features"][key] = selected
    return result


def new_profile(name="New-profile"):
    return {"schema_version": 1, "profile": profile_name(name),
            "status": "measurements_pending",
            "measurements_mm": {key: None for key in SCHEMA["measurements"]},
            "allowances_mm": {key: value["default"] for key, value in SCHEMA["allowances"].items()},
            "build": build_config()}


def number(value, name, low, high):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name}: endliche Zahl in mm erforderlich")
    if not math.isfinite(value) or not low <= value <= high:
        raise ValueError(f"{name}: ausserhalb {low}..{high} mm; Einheit pruefen")
    return float(value)


def bounds(key):
    field = SCHEMA["measurements"][key]
    return field["min"], field["max"]


def derive(profile, concept=False):
    if (not isinstance(profile, dict) or isinstance(profile.get("schema_version"), bool)
            or profile.get("schema_version") != 1):
        raise ValueError("Unbekannte schema_version")
    name = profile_name(profile.get("profile"))
    status = profile.get("status")
    if not isinstance(status, str) or status not in PROFILE_STATUSES:
        raise ValueError("status: measurements_pending, synthetic oder measured erforderlich")
    if "build" in profile and not isinstance(profile["build"], dict):
        raise ValueError("build muss ein Objekt sein")
    build = build_config(profile.get("build"))
    raw = profile.get("measurements_mm")
    if not isinstance(raw, dict):
        raise ValueError("measurements_mm muss ein Objekt sein")
    if set(raw) != set(SCHEMA["measurements"]):
        raise ValueError("Messfelder fehlen oder sind unbekannt: " +
                         ", ".join(sorted(set(raw) ^ set(SCHEMA["measurements"]))))
    missing = sorted(key for key, value in raw.items() if value is None)
    if status == "measured" and missing:
        raise ValueError("status measured widerspricht fehlenden Massen")
    if missing and not concept:
        raise ValueError("Fehlende Masse: " + ", ".join(missing) +
                         ". Fuer eine gekennzeichnete Konzeptansicht: --concept")
    m = {k: number(DEMO[k] if v is None else v, k, *bounds(k)) for k, v in ((k, raw[k]) for k in SCHEMA["measurements"])}
    # Do not scale synthetic widths from stature: broad shoulders are independent.
    for key in m:
        if key != "height" and m[key] >= m["height"]:
            raise ValueError(f"{key}: unplausibel gegenueber Koerpergroesse")
    if m["chest_width"] > m["shoulder_width"] + 120:
        raise ValueError("Brust-/Schulterbreite: Messdefinition pruefen")
    a = profile.get("allowances_mm", {})
    if not isinstance(a, dict) or set(a) != set(ALLOWANCES):
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
        "profile": name,
        "input_status": status,
        "build": build,
        "status": "CONCEPT_NOT_MEASURED" if p["concept_only"] else (
            "MEASURED_ENVELOPE_NOT_VALIDATED" if status == "measured" else "INPUT_ENVELOPE_NOT_VALIDATED"),
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
    build = report["build"]
    lines = ["# Passformbericht", "", f"Profil: **{report['profile']}**", "",
             f"Status: **{report['status']}**", "",
             f"Referenz: {build['armor_reference']} / Material: {build['material']} / Betrieb: {build['operating_mode']}",
             f"Nebeleffekt (Planung): {build['fog_system']}",
             "Optionen: " + ", ".join(f"{key}={str(value).lower()}" for key, value in build["features"].items()), "",
             "Die Auswahl dokumentiert den Baupfad; sie erzeugt keine fertigen Referenzschalen oder Kaufteilintegration.", "",
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
    opened = opening_envelope(w, d, 105, p["entry_slide_each_side"])
    max_width = max(w + 2 * p["entry_slide_each_side"], opened["outer_width_mm"])
    forward = max(d / 2, opened["forward_reach_mm"])
    # One common scale keeps both poses comparable and inside their panels,
    # including broad/deep profiles at the accepted input limits.
    scale = min(600 / max_width, 420 / (forward + d / 2))
    cy = 190 + forward * scale
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="800" viewBox="0 0 1400 800">',
             '<rect width="1400" height="800" fill="#0c151b"/>',
             '<g font-family="sans-serif" fill="#edf4e4">',
             '<text x="55" y="60" font-size="28">MJOLNIR / FRONT ENTRY</text>',
             f'<text x="55" y="95" font-size="16">Profil: {esc(report["profile"])} / Draufsicht - schematische Tueren</text>',
             f'<text x="55" y="130" font-size="16" fill="#ffca74">{esc(report["status"])}</text>',
             '<text x="55" y="740" font-size="15">Nur Oeffnungshuelle. Keine Kollisions-, Passform- oder Festigkeitsfreigabe.</text>',
             '<text x="55" y="767" font-size="15">Gruen: Schalen / Cyan: eigener Rueckentraeger / Orange: Scharnierachsen</text>', '</g>']
    for cx, angle in ((360, 0), (1030, 105)):
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
    out = Path(out)
    if (out / "MjolnirEntry.scad").resolve() == MODEL_PATH.resolve():
        raise ValueError("Ausgabe darf die CAD-Quelldatei nicht ueberschreiben")
    source = MODEL_PATH.read_text(encoding="utf-8")
    include = "include <Generated/parameters.scad>"
    if source.count(include) != 1:
        raise ValueError("CAD-Quelle: erwarteter Parameter-Include fehlt oder ist mehrfach vorhanden")
    portable = source.replace(include, "include <parameters.scad>")
    out.mkdir(parents=True, exist_ok=True)
    (out / "fit-report.json").write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n")
    (out / "FitReport.md").write_text(report_md(report))
    scad = ["// GENERATED by tools/suit_fit.py. Do not hand-edit.",
            "// " + report["status"], "// Envelope only; no fabrication approval."]
    for key, value in report["parameters_mm"].items():
        scad.append(f"{key} = {json.dumps(value)};")
    (out / "parameters.scad").write_text("\n".join(scad) + "\n")
    (out / "OpeningEnvelope.svg").write_text(layout_svg(report), encoding="utf-8")
    (out / "MjolnirEntry.scad").write_text(portable, encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    mode.add_argument("--init", type=Path, help="Create a blank profile without overwriting files")
    parser.add_argument("--name", help="Name for --init; default New-profile")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--concept", action="store_true", help="Use explicitly labelled synthetic dimensions where missing")
    args = parser.parse_args(argv)
    try:
        if args.init is not None:
            if args.concept or args.out is not None:
                raise ValueError("--init ist nicht mit --concept oder --out kombinierbar")
            profile = new_profile(args.name if args.name is not None else "New-profile")
            args.init.parent.mkdir(parents=True, exist_ok=True)
            with args.init.open("x", encoding="utf-8") as handle:
                handle.write(json.dumps(profile, indent=2, ensure_ascii=True) + "\n")
            print(f"Leeres Profil erstellt: {args.init}; 32 Masse offen")
            return 0
        if args.name is not None:
            raise ValueError("--name ist nur zusammen mit --init erlaubt")
        profile = json.loads(args.profile.read_text(encoding="utf-8"))
        report = derive(profile, args.concept)
        out = args.out if args.out is not None else ROOT / "build" / report["profile"]
        if args.profile.resolve() in {
                (out / name).resolve() for name in
                ("fit-report.json", "FitReport.md", "parameters.scad", "OpeningEnvelope.svg", "MjolnirEntry.scad")}:
            raise ValueError("Ausgabe darf das Eingabeprofil nicht ueberschreiben")
        export(report, out)
    except (ValueError, OSError, TypeError) as exc:
        print(f"Fit-Fehler: {exc}", file=sys.stderr)
        return 2
    print(f"{report['status']}: {out}; {len(report['missing_measurements'])} offene Masse")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
