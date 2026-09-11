#!/usr/bin/env python3
"""Export editable component fit coupons; no fabrication or load approval."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

try:
    from . import suit_fit
except ImportError:
    import suit_fit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Design/Components"
DEFAULTS = json.loads((SOURCE / "ExampleConfig.json").read_text(encoding="utf-8"))
BOUNDS = {
    "visor_radius_mm": (40, 250), "visor_angle_deg": (10, 60),
    "visor_sheet_mm": (0.4, 3), "visor_lip_mm": (1, 4),
    "visor_base_mm": (1, 4), "visor_depth_mm": (3, 15),
    "fan_size_mm": (25, 80), "fan_hole_pitch_mm": (15, 75),
    "fan_hole_mm": (2, 5), "fan_opening_mm": (15, 75),
    "bracket_edge_mm": (3, 10), "bracket_thickness_mm": (2, 6),
    "bracket_mount_hole_mm": (2, 5), "seam_tile_mm": (25, 60),
    "seam_thickness_mm": (2.5, 8), "seam_tongue_width_mm": (4, 20),
    "seam_tongue_height_mm": (0.8, 4), "seam_tongue_length_mm": (2, 8),
    "joint_length_mm": (40, 120), "joint_width_mm": (25, 80),
    "joint_base_mm": (0.6, 3), "joint_rib_width_mm": (1, 4),
    "joint_pitch_mm": (3, 12), "joint_rib_height_mm": (0.5, 5),
    "hinge_pin_mm": (2, 5), "hinge_barrel_mm": (8, 14),
    "hinge_barrel_height_mm": (5, 20), "hinge_plate_mm": (3, 8),
    "fastener_shaft_mm": (2, 6), "fastener_head_mm": (5, 12),
    "fastener_counterbore_mm": (1, 4),
}
COMPONENTS = {
    "visor_retainer": {
        "title": "Segmentierte Visierleisten-Probe",
        "material": "PETG als Tischprobe; keine Temperatur- oder Hautkontaktfreigabe",
        "quantity": "3 separate Bogensegmente",
        "purchased": "1 Reststueck des vorgesehenen Visiermaterials; gemessene Dicke eintragen",
        "purpose": "Nutbreite, Halt und schonende Einfuehrung des Visiermaterials vergleichen.",
        "test": "Spiele in aufsteigender Y-Reihenfolge zuordnen, Masse messen, Folie einfuehren und wieder loesen. Kein Klemmen, sichtbarer Abrieb oder Riss. Haltewirkung und elastische Rueckstellung protokollieren. Keine optische Visierform oder Helmbefestigung nachgewiesen.",
        "parameters": ["visor_radius_mm", "visor_angle_deg", "visor_sheet_mm", "visor_lip_mm", "visor_base_mm", "visor_depth_mm", "clearances_mm"],
    },
    "fan_bracket": {
        "title": "Abnehmbarer Luefter-Montagerahmen",
        "material": "PETG als Passprobe; Temperatur und Schwingungen separat pruefen",
        "quantity": "1 Rahmen mit 4 Luefterbohrungen und 2 Befestigungslaschen",
        "purchased": "1 realer Luefter; 4 passende Luefterbefestiger; 2 loesbare Befestiger fuer die Laschen; Abmessungen und Laengen am Aufbau bestimmen",
        "purpose": "Kaufteil-Lochbild und Montagezugang mit einem austauschbaren Rahmen pruefen.",
        "test": "Lochabstand und Luefterausschnitt mit dem Kaufteil abgleichen. Luefter manuell frei drehen, Befestiger duerfen Rotor und Leitungen nicht beruehren. Ausbau ohne Zerlegen der Schale demonstrieren. Beruehrschutz, Luftdurchsatz und Betriebswaerme sind separate Tests.",
        "parameters": ["fan_size_mm", "fan_hole_pitch_mm", "fan_hole_mm", "fan_opening_mm", "bracket_edge_mm", "bracket_thickness_mm", "bracket_mount_hole_mm"],
    },
    "seam_coupon": {
        "title": "Schalenfugen- und Ausrichtungsprobe",
        "material": "Gleiches Schalenmaterial, Druckorientierung und Finish wie spaeterer Aufbau",
        "quantity": "3 Paare: je 1 Federplatte und 1 Nutplatte",
        "purchased": "Schleif- und Lackiermuster des geplanten Schalenaufbaus",
        "purpose": "Passung einer Ausrichtungsfeder vor und nach Lackierung vergleichen.",
        "test": "Paare in aufsteigender Y-Reihenfolge markieren. Passung und Spalt vor/nach Finish messen; mehrmals von Hand verbinden und trennen. Keine Klemmung oder Abplatzung. Die Feder richtet aus und ersetzt keinen Verschluss.",
        "parameters": ["seam_tile_mm", "seam_thickness_mm", "seam_tongue_width_mm", "seam_tongue_height_mm", "seam_tongue_length_mm", "clearances_mm"],
    },
    "joint_cover": {
        "title": "Gerippte flexible Gelenkabdeckungsprobe",
        "material": "TPU-Probe in dokumentierter Shore-Haerte; alternativ als Formreferenz fuer Textil",
        "quantity": "1 flache gerippte Materialprobe",
        "purchased": "Reststueck des vorgesehenen Unteranzugstoffs zur Kontakt- und Nahtprobe",
        "purpose": "Rippenoptik, Rueckstellung und Biegekomfort einer nicht tragenden Abdeckung pruefen.",
        "test": "Zunaechst nur am Tisch biegen. Biegeradius, Rueckstellung, Rippenkontakt und Rissbildung dokumentieren. Danach an einem Stoffmuster befestigen und Scheuerkanten pruefen. Keine Fixierung eines Gelenks; kein Ersatz fuer Bewegungs- und Trageprobe.",
        "parameters": ["joint_length_mm", "joint_width_mm", "joint_base_mm", "joint_rib_width_mm", "joint_pitch_mm", "joint_rib_height_mm"],
    },
    "hinge_coupon": {
        "title": "Scharnierstift- und Befestiger-Lehre",
        "material": "Vorgesehenes Gehaeusematerial; gedruckter Stift nur zum Vergleich",
        "quantity": "1 Pruefplatte mit 3 Huelsen und 3 Schraubenbohrungen; 1 loser Vergleichsstift",
        "purchased": "1 realer gemessener Stift; 1 realer gemessener Befestiger mit passendem Kopf",
        "purpose": "Bohrungsspiel und Kopffreiraum pruefen, ohne ein tragendes Scharnier vorzugeben.",
        "test": "Spiele von links nach rechts zuordnen. Reale Stifte und Schrauben einfuehren; Spiel, Drehbarkeit und Restmaterial messen. Gedruckter Vergleichsstift ersetzt kein Kaufteil. Keine Scharnierlast, Lebensdauer oder Koerperlast daraus ableiten.",
        "parameters": ["hinge_pin_mm", "hinge_barrel_mm", "hinge_barrel_height_mm", "hinge_plate_mm", "fastener_shaft_mm", "fastener_head_mm", "fastener_counterbore_mm", "clearances_mm"],
    },
}


def parameters(report, overrides=None):
    """Geometric sanity checks only; the limits are design bounds, not ratings."""
    if overrides is None:
        overrides = {}
    if not isinstance(overrides, dict) or set(overrides) - set(DEFAULTS):
        raise ValueError("Komponenten-Konfiguration: unbekannte Felder oder kein Objekt")
    result = dict(DEFAULTS)
    # This seeds a curved coupon, never the optical contour of a real visor.
    result["visor_radius_mm"] = report["parameters_mm"]["helmet_width"] / 2
    result.update(overrides)
    for key, (low, high) in BOUNDS.items():
        result[key] = suit_fit.number(result[key], key, low, high)
    gaps = result["clearances_mm"]
    if not isinstance(gaps, list) or len(gaps) != 3:
        raise ValueError("clearances_mm: genau drei aufsteigende Gesamtspiele erforderlich")
    gaps = [suit_fit.number(value, "clearances_mm", 0.1, 1.2) for value in gaps]
    if gaps != sorted(set(gaps)):
        raise ValueError("clearances_mm: genau drei verschiedene aufsteigende Spiele")
    result["clearances_mm"] = gaps
    c = max(gaps)
    checks = [
        (result["fan_opening_mm"] + 2*result["fan_hole_mm"] + 2 <= math.sqrt(2)*result["fan_hole_pitch_mm"], "Luefteroeffnung schneidet Eckbohrungen"),
        (result["fan_opening_mm"] + 4 <= result["fan_size_mm"], "Luefteroeffnung laesst zu wenig Rahmen"),
        (result["fan_hole_pitch_mm"] + result["fan_hole_mm"] + 4 <= result["fan_size_mm"] + 2*result["bracket_edge_mm"], "Luefterbohrungen haben zu wenig Rand"),
        (result["seam_tongue_height_mm"] + c + 1 <= result["seam_thickness_mm"], "Fugennut laesst zu wenig Deck-/Bodenmaterial"),
        (result["seam_tongue_width_mm"] + c + 4 < result["seam_tile_mm"], "Fugennut zu breit"),
        (result["joint_rib_width_mm"] < result["joint_pitch_mm"], "Rippen ueberlappen"),
        (result["hinge_pin_mm"] + c + 3 < result["hinge_barrel_mm"], "Stifthuelse hat zu wenig Wand"),
        (result["fastener_head_mm"] >= result["fastener_shaft_mm"] + 1, "Schraubenkopf muss groesser als Schaft sein"),
        (result["fastener_counterbore_mm"] + 1 <= result["hinge_plate_mm"], "Kopfsenkung laesst zu wenig Boden"),
    ]
    for valid, reason in checks:
        if not valid:
            raise ValueError(reason)
    return result


def bom(report, values):
    return {
        "schema_version": 1, "profile": report["profile"],
        "status": "COMPONENT_PROTOTYPES_NOT_VALIDATED", "fabrication_approved": False,
        "fit_status": report["status"],
        "note": "Material- und Kaufteilbedarf ohne Preis-, Massen- oder Festigkeitsnachweis.",
        "components": [{"id": key, "title": spec["title"], "quantity": spec["quantity"],
                        "material": spec["material"], "purchased_items": spec["purchased"],
                        "parameters": {name: values[name] for name in spec["parameters"]},
                        "measured_mass_g": None, "physical_test_passed": False}
                       for key, spec in COMPONENTS.items()],
    }


def component_readme(key, spec, values):
    lines = ["# " + spec["title"], "", "Status: **UNGEPRUEFTE KOMPONENTENPROBE**", "",
             spec["purpose"], "", "## Material und Bedarf", "",
             "- Menge: " + spec["quantity"], "- Material: " + spec["material"],
             "- Zusaetzlich: " + spec["purchased"], "", "## Abmessungen", "",
             "Alle Laengen in mm; visor_angle_deg in Grad. clearances_mm ist das gesamte",
             "diametrale beziehungsweise Nut-Spiel, nicht der Zuschlag je Seite.", "",
             "| Parameter | Wert |", "| --- | ---: |"]
    lines += [f"| {name} | {json.dumps(values[name])} |" for name in spec["parameters"]]
    lines += ["", "## Export", "", "Im erzeugten Ordner:", "", "```bash",
              f"openscad --hardwarnings -D 'component=\"{key}\"' -o {key}.stl ComponentKit.scad",
              "```", "", "## Passprobe", "", spec["test"], "",
              "Parameter, Drucker, Materialcharge, Orientierung, Finish, Istmasse und Ergebnis",
              "im projektbezogenen Pruefprotokoll festhalten. Erst nach der Tischprobe ueber",
              "die Integration entscheiden. Diese Datei erteilt keine Fertigungsfreigabe.", ""]
    return "\n".join(lines)


def export(profile_path, out, concept=False, config_path=None):
    profile_path, out = Path(profile_path), Path(out)
    profile_bytes = profile_path.read_bytes()
    raw = json.loads(profile_bytes)
    report = suit_fit.derive(raw, concept=concept)
    if raw["status"] == "synthetic" and not concept:
        raise ValueError("Synthetisches Profil erfordert --concept")
    config_bytes = Path(config_path).read_bytes() if config_path else None
    overrides = json.loads(config_bytes) if config_bytes is not None else {}
    values = parameters(report, overrides)
    protected = {profile_path.resolve(), Path(__file__).resolve()}
    if config_path:
        protected.add(Path(config_path).resolve())
    names = ["ComponentKit.scad", "Parameters.scad", "Config.json", "BOM.json", "Manifest.json", "README.md"]
    names += [key + ".md" for key in COMPONENTS]
    if out.resolve().is_relative_to(SOURCE.resolve()):
        raise ValueError("Ausgabe darf nicht im Komponenten-Quellordner liegen")
    if any((out / name).resolve() in protected for name in names):
        raise ValueError("Ausgabe darf Profil oder Konfiguration nicht ueberschreiben")
    if out.exists() or out.is_symlink():
        raise ValueError("Ausgabe existiert bereits; --out mit neuem Revisionsordner waehlen")
    source_bytes = (SOURCE / "ComponentKit.scad").read_bytes()
    manifest = {"schema_version": 1, "profile": report["profile"],
                "status": "COMPONENT_PROTOTYPES_NOT_VALIDATED", "fit_status": report["status"],
                "fabrication_approved": False, "profile_sha256": hashlib.sha256(profile_bytes).hexdigest(),
                "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
                "config_sha256": hashlib.sha256(config_bytes).hexdigest() if config_bytes is not None else None,
                "parameter_origin": {key: "explicit_config" if key in overrides else (
                    "half_helmet_envelope_width_only" if key == "visor_radius_mm" else "generic_coupon_default") for key in values},
                "components": list(COMPONENTS), "parameters": values}
    texts = {"ComponentKit.scad": source_bytes.decode("utf-8"),
             "Parameters.scad": "// GENERATED: unvalidated component coupons; units mm except angle.\n" +
                 "\n".join(f"{key} = {json.dumps(value)};" for key, value in values.items()) + "\n",
             "Config.json": json.dumps(values, indent=2) + "\n",
             "BOM.json": json.dumps(bom(report, values), indent=2, ensure_ascii=True) + "\n",
             "Manifest.json": json.dumps(manifest, indent=2, ensure_ascii=True) + "\n",
             "README.md": "# Komponentenproben\n\nProfil: **" + report["profile"] + "**\n\n" +
                 "Status: **COMPONENT_PROTOTYPES_NOT_VALIDATED** / " + report["status"] + "\n\n" +
                 "Keine fertigen Halo-Aussenschalen; keine Fertigungs-, Last- oder Tragefreigabe.\n" +
                 "Visierradius ohne explizite Konfiguration: halbe Helmhuellenbreite als Formprobe,\n" +
                 "keine optische Visierkontur. Alle anderen Masse sind editierbare Probenvorgaben.\n\n" +
                 "ComponentKit.scad oeffnen; component auf gewuenschte Probe stellen. layout ist\n" +
                 "nur eine Uebersicht, kein Druckplattenlayout. Einzelteile separat exportieren.\n" +
                 "Parameters.scad ist direkt editierbar. Fuer nachvollziehbare neue Revisionen\n" +
                 "Config.json anpassen und CLI mit --config und neuem --out erneut ausfuehren.\n\n" +
                 "\n".join(f"- [{spec['title']}]({key}.md)" for key, spec in COMPONENTS.items()) + "\n\n" +
                 "BOM.json enthaelt Material-/Kaufteilbedarf ohne Preise und ohne Gewichtsannahmen.\n" +
                 "Manifest.json bindet Eingabeprofil, Konfiguration und CAD-Quelle per SHA-256.\n"}
    texts.update({key + ".md": component_readme(key, spec, values) for key, spec in COMPONENTS.items()})
    out.mkdir(parents=True, exist_ok=False)
    for name, content in texts.items():
        (out / name).write_text(content, encoding="utf-8")
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--profile", type=Path)
    mode.add_argument("--demo", action="store_true", help="Explicit synthetic demo; requires --concept")
    parser.add_argument("--concept", action="store_true")
    parser.add_argument("--config", type=Path, help="Partial or complete overrides; see ExampleConfig.json")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.demo and not args.concept:
            raise ValueError("--demo erfordert --concept")
        profile_path = suit_fit.DEMO_PROFILE if args.demo else args.profile
        raw = json.loads(profile_path.read_text(encoding="utf-8"))
        name = suit_fit.profile_name(raw.get("profile"))
        out = args.out if args.out else ROOT / "build" / name / "Components"
        manifest = export(profile_path, out, args.concept, args.config)
    except (ValueError, OSError, TypeError, AttributeError) as exc:
        print(f"Komponenten-Fehler: {exc}", file=sys.stderr)
        return 2
    print(f"{manifest['status']}: {out}; {len(COMPONENTS)} Komponentenproben")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
