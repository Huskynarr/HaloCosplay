#!/usr/bin/env python3
"""Steady-state heat and measured airflow planning; no hardware approval."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys

NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9 ._-]{0,63}\Z")


def name(value, path):
    if not isinstance(value, str) or not NAME.fullmatch(value) or value != value.strip():
        raise ValueError(f"{path}: ASCII name, 1-64 characters required")
    return value


def record(value, fields, path):
    if not isinstance(value, dict) or set(value) != set(fields):
        raise ValueError(f"{path}: expected fields {', '.join(fields)}")
    return value


def number(value, path, missing, *, positive=False, temperature=False):
    if value is None:
        missing.append(path)
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{path}: finite number required")
    try:
        finite = math.isfinite(value)
    except OverflowError:
        finite = False
    if (not finite or (temperature and value <= -273.15)
            or (not temperature and value < 0) or (positive and value <= 0)):
        raise ValueError(f"{path}: invalid number or unit range")
    return value


def collection(value, path):
    if not isinstance(value, list):
        raise ValueError(f"{path}: list required")
    ids = set()
    for item in value:
        if not isinstance(item, dict):
            raise ValueError(f"{path}: object required")
        ident = name(item.get("id"), path + ".id")
        if ident in ids:
            raise ValueError(f"{path}: duplicate id {ident}")
        ids.add(ident)
    return value


def new_project(project="My Suit"):
    return {
        "schema_version": 1, "project": name(project, "project"),
        "status": "inputs_pending", "notes": "",
        "modules": [{"id": "Sink-1", "heat_load_w": None, "ambient_c": None,
                     "sink_ambient_k_per_w": None, "surface_limit_c": None,
                     "junction_paths": [{"id": "Die-1", "heat_w": None,
                                         "junction_to_sink_k_per_w": None,
                                         "junction_limit_c": None}]}],
        "vents": [{"id": "Duct-1", "heat_w": None, "measured_flow_m3_h": None,
                   "ambient_c": None, "rho_kg_m3": None, "cp_j_kg_k": None}],
    }


def finite_results(value):
    if isinstance(value, dict):
        for child in value.values():
            finite_results(child)
    elif isinstance(value, list):
        for child in value:
            finite_results(child)
    elif isinstance(value, (int, float)):
        try:
            finite = math.isfinite(value)
        except OverflowError:
            finite = False
        if not finite:
            raise ValueError("Calculation overflow: reduce input magnitudes")


def difference(limit, value):
    return None if limit is None or value is None else limit - value


def finding(headroom):
    return "missing_inputs" if headroom is None else (
        "nonpositive_model_headroom" if headroom <= 0 else "positive_model_headroom")


def calculate(data):
    record(data, new_project().keys(), "input")
    if isinstance(data["schema_version"], bool) or data["schema_version"] != 1:
        raise ValueError("Unsupported thermal schema")
    project = name(data["project"], "project")
    if data["status"] not in ("inputs_pending", "synthetic", "entered"):
        raise ValueError("status must be inputs_pending, synthetic or entered")
    if not isinstance(data["notes"], str) or len(data["notes"]) > 4000:
        raise ValueError("notes: text of at most 4000 characters required")
    missing, modules, vents = [], [], []
    for module in collection(data["modules"], "modules"):
        record(module, new_project()["modules"][0].keys(), "module")
        prefix = "modules." + module["id"]
        heat = number(module["heat_load_w"], prefix + ".heat_load_w", missing)
        ambient = number(module["ambient_c"], prefix + ".ambient_c", missing, temperature=True)
        resistance = number(module["sink_ambient_k_per_w"], prefix + ".sink_ambient_k_per_w", missing, positive=True)
        limit = number(module["surface_limit_c"], prefix + ".surface_limit_c", missing, temperature=True)
        sink = None if None in (heat, ambient, resistance) else ambient + heat * resistance
        headroom = difference(limit, sink)
        max_resistance, bound_note = None, "missing_inputs"
        if None not in (heat, ambient, limit):
            if heat == 0:
                bound_note = "zero_heat_no_resistance_bound"
            elif limit <= ambient:
                bound_note = "ambient_at_or_above_limit_no_positive_resistance_possible"
            else:
                max_resistance = (limit - ambient) / heat
                bound_note = "surface_constraint_only"
        paths, path_heats = [], []
        for junction in collection(module["junction_paths"], prefix + ".junction_paths"):
            record(junction, new_project()["modules"][0]["junction_paths"][0].keys(), "junction")
            jp = prefix + ".junction_paths." + junction["id"]
            die_heat = number(junction["heat_w"], jp + ".heat_w", missing)
            die_resistance = number(junction["junction_to_sink_k_per_w"], jp + ".junction_to_sink_k_per_w", missing, positive=True)
            die_limit = number(junction["junction_limit_c"], jp + ".junction_limit_c", missing, temperature=True)
            junction_c = None if None in (sink, die_heat, die_resistance) else sink + die_heat * die_resistance
            junction_headroom = difference(die_limit, junction_c)
            path_heats.append(die_heat)
            paths.append({"id": junction["id"], "heat_w": die_heat,
                          "junction_to_sink_k_per_w": die_resistance,
                          "junction_temperature_c": junction_c,
                          "junction_limit_c": die_limit, "junction_headroom_k": junction_headroom,
                          "finding": finding(junction_headroom)})
        known_heat = sum(h for h in path_heats if h is not None)
        if heat is not None and known_heat > heat and not math.isclose(known_heat, heat, rel_tol=1e-9, abs_tol=1e-12):
            raise ValueError(prefix + ": known junction heat exceeds total shared-sink heat_load_w")
        unassigned = None if heat is None or None in path_heats else max(0, heat - known_heat)
        modules.append({"id": module["id"], "heat_load_w": heat, "ambient_c": ambient,
                        "sink_ambient_k_per_w": resistance, "sink_temperature_c": sink,
                        "surface_limit_c": limit, "surface_headroom_k": headroom,
                        "surface_max_sink_ambient_k_per_w": max_resistance,
                        "surface_resistance_bound_note": bound_note,
                        "finding": finding(headroom), "junction_paths": paths,
                        "heat_not_assigned_to_junctions_w": unassigned})
    for vent in collection(data["vents"], "vents"):
        record(vent, new_project()["vents"][0].keys(), "vent")
        prefix = "vents." + vent["id"]
        heat = number(vent["heat_w"], prefix + ".heat_w", missing)
        flow = number(vent["measured_flow_m3_h"], prefix + ".measured_flow_m3_h", missing)
        ambient = number(vent["ambient_c"], prefix + ".ambient_c", missing, temperature=True)
        density = number(vent["rho_kg_m3"], prefix + ".rho_kg_m3", missing, positive=True)
        capacity = number(vent["cp_j_kg_k"], prefix + ".cp_j_kg_k", missing, positive=True)
        rise, note = None, "missing_inputs"
        if flow == 0:
            note = "zero_flow_unbounded_in_this_model" if heat is not None and heat > 0 else "zero_flow_no_advective_solution"
        elif None not in (heat, flow, density, capacity):
            denominator = density * capacity * (flow / 3600)
            if denominator == 0 or not math.isfinite(denominator):
                raise ValueError(prefix + ": calculation overflow or underflow; revise input magnitudes")
            rise, note = heat / denominator, "steady_sensible_electronics_heat_only"
        outlet = None if None in (rise, ambient) else ambient + rise
        vents.append({"id": vent["id"], "heat_w": heat, "measured_flow_m3_h": flow,
                      "ambient_c": ambient, "air_temperature_rise_k": rise,
                      "model_outlet_temperature_c": outlet, "finding": note})
    report = {"schema_version": 1, "project": project, "input_status": data["status"],
              "hardware_approved": False, "fabrication_approved": False,
              "model": "steady_shared_sink_and_sensible_electronics_airflow_only",
              "missing_inputs": missing, "modules": modules, "vents": vents,
              "omitted_sections": (["modules"] if not modules else []) + (["vents"] if not vents else []),
              "limitations": [
                  "Planrechnung ohne Hardware-, Fertigungs- oder Beruehrungsschutzfreigabe.",
                  "heat_load_w umfasst alle Waermequellen am gemeinsamen Kuehlkoerper; einzelne Dies sind darin enthalten und werden nicht erneut addiert.",
                  "Volle elektrische Leistung als lokale Waerme ist eine konservative Annahme; Treiber an einem anderen Ort werden separat bilanziert.",
                  "Ein gleichmaessig temperierter Kuehlkoerper wird angenommen; lokale Hotspots und thermische Kopplung der Dies sind nicht aufgeloest.",
                  "Junction-to-sink muss Gehaeuse, Leiterplatte, Kontakt und Isolierlage abdecken; ein Junction-to-case-Wert allein reicht nicht.",
                  "Widerstaende muessen zu Einbaulage, Abdeckung und realem Luftstrom passen; Temperaturgrenzen werden nicht vorgegeben.",
                  "Stationaeres Modell ohne Aufheizzeit, Pulsbetrieb, direkte Sonne oder Rueckstrom heisser Abluft.",
                  "Volumenstrom ist am fertig eingebauten Kanal zu messen; der Freiluftwert des Luefters ersetzt diese Messung nicht.",
                  "Luftrechnung betrifft nur sensible Elektronikwaerme; keine Aussage ueber Koerperkuehlung, Verdunstung oder ausreichende Frischluft.",
                  "Null-Volumenstrom ergibt keine endliche Loesung fuer den Lufttransport; andere Waermewege bleiben unmodelliert.",
              ]}
    finite_results(report)
    return report


def display(value):
    return "offen" if value is None else f"{value:.5g}"


def render(report):
    lines = ["# MJOLNIR: thermische Planrechnung", "", f"Projekt: **{report['project']}**.",
             f"Eingabestatus: `{report['input_status']}`. Keine Hardwarefreigabe.", "",
             "Tsink = Ta + Pgesamt * Rsa. Tjunction = Tsink + Pdie * Rjunction-sink.", "",
             "Pgesamt enthaelt die einzelnen Die-Leistungen bereits. Die gesamte RGB-Waerme",
             "erwaermt den gemeinsamen Kuehlkoerper; der jeweilige Die hat einen eigenen Pfad.", "",
             "## Gemeinsame Kuehlkoerper", "",
             "| Modul | Waerme W | Umgebung C | Rsa K/W | Tsink C | Grenze C | Abstand K | Max. Rsa K/W | Befund |",
             "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |"]
    for module in report["modules"]:
        keys = ("heat_load_w", "ambient_c", "sink_ambient_k_per_w", "sink_temperature_c", "surface_limit_c", "surface_headroom_k", "surface_max_sink_ambient_k_per_w")
        lines.append("| " + module["id"] + " | " + " | ".join(display(module[k]) for k in keys) + " | `" + module["finding"] + "` |")
    lines += ["", "Max. Rsa gilt nur fuer die eingetragene Oberflaechengrenze. Chipgrenzen",
              "muessen zusaetzlich anhand ihrer eigenen Temperaturabstaende beurteilt werden.", "",
              "## Einzelne Chip-Pfade", "", "| Modul / Die | Waerme W | Rjunction-sink K/W | Tjunction C | Grenze C | Abstand K | Befund |",
              "| --- | ---: | ---: | ---: | ---: | ---: | --- |"]
    for module in report["modules"]:
        for junction in module["junction_paths"]:
            keys = ("heat_w", "junction_to_sink_k_per_w", "junction_temperature_c", "junction_limit_c", "junction_headroom_k")
            lines.append("| " + module["id"] + " / " + junction["id"] + " | " + " | ".join(display(junction[k]) for k in keys) + " | `" + junction["finding"] + "` |")
    for module in report["modules"]:
        lines += ["", f"`{module['id']}`: Rsa-Bedingung `{module['surface_resistance_bound_note']}`;",
                  "nicht einzelnen Chip-Pfaden zugeordnete Waerme: " + display(module["heat_not_assigned_to_junctions_w"]) + " W.", ""]
    lines += ["## Gemessene Elektronik-Luftkanaele", "", "Delta T = P / (rho * cp * Q / 3600), mit Q in m3/h.", "",
              "| Kanal | Waerme W | Gemessene m3/h | Umgebung C | Temperaturanstieg K | Modell-Abluft C | Befund |",
              "| --- | ---: | ---: | ---: | ---: | ---: | --- |"]
    for vent in report["vents"]:
        keys = ("heat_w", "measured_flow_m3_h", "ambient_c", "air_temperature_rise_k", "model_outlet_temperature_c")
        lines.append("| " + vent["id"] + " | " + " | ".join(display(vent[k]) for k in keys) + " | `" + vent["finding"] + "` |")
    lines += ["", "## Fehlende Eingaben", ""]
    lines += ["- `" + item + "`" for item in report["missing_inputs"]] or ["Keine leeren Felder. Die Eingabedaten sind dadurch nicht praktisch bestaetigt."]
    lines += ["", "Explizit ausgelassene Bereiche: " + (", ".join(report["omitted_sections"]) or "keine") + ".", "", "## Modellgrenzen", ""]
    lines += ["- " + item for item in report["limitations"]]
    if "input_sha256" in report:
        lines += ["", f"SHA-256 der Eingabedatei: `{report['input_sha256']}`."]
    return "\n".join(lines) + "\n"


def export(input_path, out=None, check=False):
    source = Path(input_path)
    raw = source.read_bytes()
    report = calculate(json.loads(raw))
    report["input_sha256"] = hashlib.sha256(raw).hexdigest()
    destination = Path(out) if out is not None else source.parent / (source.stem + "-thermal")
    outputs = {destination / "ThermalReport.json": json.dumps(report, indent=2, ensure_ascii=True, allow_nan=False) + "\n",
               destination / "ThermalReport.md": render(report)}
    if any(path.resolve() == source.resolve() or (path.exists() and path.samefile(source)) for path in outputs):
        raise ValueError("Output must not overwrite the source input")
    if len({path.resolve() for path in outputs}) != len(outputs):
        raise ValueError("Output paths must be distinct")
    paths = list(outputs)
    if all(path.exists() for path in paths) and paths[0].samefile(paths[1]):
        raise ValueError("Output files must not be hardlinked together")
    for path, content in outputs.items():
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                raise ValueError("Thermal report out of date: " + str(path))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--init", type=Path)
    parser.add_argument("--name", default="My Suit")
    parser.add_argument("--input", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.init is not None:
            if args.input is not None or args.out is not None or args.check:
                raise ValueError("--init cannot be combined with --input, --out or --check")
            data = new_project(args.name)
            args.init.parent.mkdir(parents=True, exist_ok=True)
            with args.init.open("x", encoding="utf-8") as stream:
                stream.write(json.dumps(data, indent=2, ensure_ascii=True) + "\n")
            print(str(args.init))
            return 0
        if args.input is None:
            raise ValueError("--input or --init is required")
        report = export(args.input, args.out, args.check)
        print(json.dumps({"project": report["project"], "input_status": report["input_status"],
                          "missing_count": len(report["missing_inputs"]), "hardware_approved": False}))
        return 0
    except (OSError, ValueError, TypeError, OverflowError) as exc:
        print("Thermal error: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
