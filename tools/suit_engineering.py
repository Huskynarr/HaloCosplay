#!/usr/bin/env python3
"""Explicit electrical and static planning calculations; no hardware approval."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
GRAVITY_M_S2 = 9.80665
NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9 ._-]{0,63}\Z")


def record(value, fields, path):
    if not isinstance(value, dict) or set(value) != set(fields):
        raise ValueError(f"{path}: expected fields {', '.join(fields)}")
    return value


def name(value, path):
    if not isinstance(value, str) or not NAME.fullmatch(value) or value != value.strip():
        raise ValueError(f"{path}: ASCII name, 1-64 characters required")
    return value


def number(value, path, missing, *, positive=False, signed=False, fraction=False, integer=False):
    if value is None:
        missing.append(path)
        return None
    if (isinstance(value, bool) or not isinstance(value, (int, float))
            or not math.isfinite(value) or (not signed and value < 0)
            or (positive and value <= 0) or (fraction and value > 1)
            or (integer and not isinstance(value, int))):
        raise ValueError(f"{path}: invalid number or unit range")
    return value


def collection(value, path, *, allow_empty=False):
    if not isinstance(value, list) or (not value and not allow_empty):
        raise ValueError(f"{path}: nonempty list required; use null inputs for an unmeasured component")
    ids = set()
    for item in value:
        if not isinstance(item, dict):
            raise ValueError(f"{path}: object required")
        ident = name(item.get("id"), path + ".id")
        if ident in ids:
            raise ValueError(f"{path}: duplicate id {ident}")
        ids.add(ident)
    return value


def total(values):
    return None if any(v is None for v in values) else sum(values)


def product(*values):
    return None if any(v is None for v in values) else math.prod(values)


def finite_results(value):
    if isinstance(value, dict):
        for item in value.values():
            finite_results(item)
    elif isinstance(value, list):
        for item in value:
            finite_results(item)
    elif isinstance(value, (float, int)) and not math.isfinite(value):
        raise ValueError("Calculation overflow: reduce input magnitudes")


def new_project(project="My Suit"):
    return {
        "schema_version": 1, "project": name(project, "project"), "status": "inputs_pending",
        "notes": "", "target_duration_h": None,
        "batteries": [{"id": "B1", "usable_energy_wh": None}],
        "rails": [{"id": "R1", "battery_id": "B1", "voltage_v": None,
                   "efficiency_fraction": None, "idle_input_w": None,
                   "consumers": [{"id": "C1", "quantity": None, "power_w": None,
                                  "duty_fraction": None, "peak_power_w": None}]}],
        "hinges": [{"id": "H1", "panel_mass_kg": None, "com_distance_m": None,
                    "gravity_axis_factor": None}],
        "stand": {"total_mass_kg": None, "base_width_x_m": None, "base_width_y_m": None,
                  "com_x_m": None, "com_y_m": None, "force_x_n": None,
                  "force_y_n": None, "force_height_m": None},
    }


def calculate(data):
    record(data, new_project().keys(), "input")
    if isinstance(data["schema_version"], bool) or data["schema_version"] != 1:
        raise ValueError("Unsupported engineering schema")
    project = name(data["project"], "project")
    if data["status"] not in ("inputs_pending", "synthetic", "entered"):
        raise ValueError("status must be inputs_pending, synthetic or entered")
    if not isinstance(data["notes"], str) or len(data["notes"]) > 4000:
        raise ValueError("notes: text of at most 4000 characters required")
    missing = []
    duration = number(data["target_duration_h"], "target_duration_h", missing, positive=True)
    batteries = {}
    for battery in collection(data["batteries"], "batteries", allow_empty=True):
        record(battery, ("id", "usable_energy_wh"), "battery")
        bid = battery["id"]
        energy = number(battery["usable_energy_wh"], f"batteries.{bid}.usable_energy_wh", missing)
        batteries[bid] = {"id": bid, "usable_energy_wh": energy, "rails": []}
    rails = []
    for rail in collection(data["rails"], "rails", allow_empty=True):
        record(rail, ("id", "battery_id", "voltage_v", "efficiency_fraction", "idle_input_w", "consumers"), "rail")
        rid = rail["id"]
        prefix = f"rails.{rid}"
        bid = rail["battery_id"]
        if bid is None:
            missing.append(prefix + ".battery_id")
        elif not isinstance(bid, str) or bid not in batteries:
            raise ValueError(prefix + ": unknown battery_id")
        voltage = number(rail["voltage_v"], prefix + ".voltage_v", missing, positive=True)
        efficiency = number(rail["efficiency_fraction"], prefix + ".efficiency_fraction", missing, positive=True, fraction=True)
        idle = number(rail["idle_input_w"], prefix + ".idle_input_w", missing)
        consumers = []
        for consumer in collection(rail["consumers"], prefix + ".consumers"):
            record(consumer, ("id", "quantity", "power_w", "duty_fraction", "peak_power_w"), "consumer")
            cp = prefix + ".consumers." + consumer["id"]
            qty = number(consumer["quantity"], cp + ".quantity", missing, positive=True, integer=True)
            power = number(consumer["power_w"], cp + ".power_w", missing)
            duty = number(consumer["duty_fraction"], cp + ".duty_fraction", missing, fraction=True)
            peak = number(consumer["peak_power_w"], cp + ".peak_power_w", missing)
            if power is not None and peak is not None and peak < power:
                raise ValueError(cp + ": peak_power_w must include at least power_w")
            consumers.append({"id": consumer["id"], "average_w": product(qty, power, duty),
                              "simultaneous_full_load_w": product(qty, power),
                              "specified_peak_w": product(qty, peak)})
        average = total([item["average_w"] for item in consumers])
        full = total([item["simultaneous_full_load_w"] for item in consumers])
        peak = total([item["specified_peak_w"] for item in consumers])
        input_average = None if None in (average, efficiency, idle) else average / efficiency + idle
        result = {"id": rid, "battery_id": bid, "consumers": consumers,
                  "average_output_w": average, "simultaneous_full_load_w": full,
                  "specified_peak_w": peak,
                  "full_load_current_a": None if None in (full, voltage) else full / voltage,
                  "specified_peak_current_a": None if None in (peak, voltage) else peak / voltage,
                  "average_battery_input_w": input_average}
        rails.append(result)
        if bid is not None:
            batteries[bid]["rails"].append(result)
    battery_results = []
    for battery in batteries.values():
        assigned = battery.pop("rails")
        average = total([item["average_battery_input_w"] for item in assigned]) if assigned else None
        energy = battery["usable_energy_wh"]
        runtime = None if average is None or average == 0 or energy is None else energy / average
        required = product(average, duration)
        battery_results.append({**battery, "rail_ids": [item["id"] for item in assigned],
                                "average_input_w": average, "estimated_runtime_h": runtime,
                                "target_energy_wh": required,
                                "energy_difference_wh": None if None in (energy, required) else energy - required,
                                "runtime_note": "not_calculable_or_no_load" if runtime is None else "constant_load_model_only"})
    active = [battery for battery in battery_results if battery["rail_ids"]]
    runtime = None
    if active and all(r["battery_id"] is not None for r in rails) and all(b["estimated_runtime_h"] is not None for b in active):
        runtime = min(b["estimated_runtime_h"] for b in active)
    hinges = []
    for hinge in collection(data["hinges"], "hinges", allow_empty=True):
        record(hinge, ("id", "panel_mass_kg", "com_distance_m", "gravity_axis_factor"), "hinge")
        hp = "hinges." + hinge["id"]
        mass = number(hinge["panel_mass_kg"], hp + ".panel_mass_kg", missing)
        radius = number(hinge["com_distance_m"], hp + ".com_distance_m", missing)
        axis_factor = number(hinge["gravity_axis_factor"], hp + ".gravity_axis_factor", missing, fraction=True)
        hinges.append({"id": hinge["id"], "static_gravity_moment_nm": product(mass, GRAVITY_M_S2, radius, axis_factor)})
    stand = record(data["stand"], new_project()["stand"].keys(), "stand") if data["stand"] is not None else {}
    values = {key: number(value, "stand." + key, missing, signed=key in ("com_x_m", "com_y_m"),
                         positive=key in ("total_mass_kg", "base_width_x_m", "base_width_y_m"))
              for key, value in stand.items()}
    edges = []
    for axis in (("x", "y") if stand else ()):
        width, offset = values[f"base_width_{axis}_m"], values[f"com_{axis}_m"]
        overturning = product(values[f"force_{axis}_n"], values["force_height_m"])
        for sign, direction in ((1, "+"), (-1, "-")):
            lever = None if None in (width, offset) else width / 2 - sign * offset
            restoring = product(values["total_mass_kg"], GRAVITY_M_S2, lever)
            margin = None if None in (restoring, overturning) else restoring - overturning
            edges.append({"edge": direction + axis, "gravity_lever_m": lever,
                          "restoring_moment_nm": restoring, "overturning_moment_nm": overturning,
                          "moment_difference_nm": margin,
                          "finding": "missing_inputs" if margin is None else
                          "positive_static_moment_difference" if margin > 0 else "nonpositive_static_moment_difference"})
    result = {"schema_version": 1, "project": project, "input_status": data["status"],
              "hardware_approved": False, "model": "electrical_average_and_quasistatic_only",
              "gravity_m_s2": GRAVITY_M_S2, "missing_inputs": missing,
              "omitted_sections": (["electrical_rails"] if not rails else []) +
              (["hinges"] if not hinges else []) + (["stand"] if not stand else []),
              "rails": rails, "batteries": battery_results, "estimated_system_runtime_h": runtime,
              "hinges": hinges, "stand_edges": edges,
              "stand_load_model": "four_directional_adverse_cases_not_one_force_vector",
              "limitations": ["Keine Freigabe fuer Strom, Sicherung, Leitung, Stecker oder Akku.",
                              "Spitzensummen stammen aus Eingaben; transiente Lasten sind nicht gemessen.",
                              "Statische Momente enthalten keinen Stoss, Reibung, Befestigungsnachweis oder Ermuedung.",
                              "Sockelmodell: ebener starrer Boden und rechteckiges tatsaechliches Aufstandspolygon.",
                              "Kraftbetraege wirken in vier getrennten unguenstigen Richtungsfaellen; kein einzelner gleichzeitiger Kraftvektor.",
                              "Keine Nachweise gegen Rutschen, Verformung oder dynamische Besucher- und Bewegungslasten."]}
    finite_results(result)
    return result


def display(value):
    return "offen" if value is None else f"{value:.4g}"


def render(report):
    lines = ["# MJOLNIR: technische Planrechnung", "", f"Projekt: **{report['project']}**.",
             f"Eingabestatus: `{report['input_status']}`. Keine Hardwarefreigabe.", "",
             "Alle Werte entstehen ausschliesslich aus der Eingabedatei. Ein positives",
             "Rechenergebnis bestaetigt weder Tragfaehigkeit noch eine sichere Betriebsdauer.", "",
             "Explizit nicht enthalten: " + (", ".join(report["omitted_sections"]) or "keine Bereiche") + ".", "",
             "## Elektrische Schienen", "",
             "| Schiene | Mittelwert W | Gleichzeitige Volllast W | Angegebene Spitze W | Volllast A | Spitze A | Akku-Mittelwert W |",
             "| --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for rail in report["rails"]:
        keys = ("average_output_w", "simultaneous_full_load_w", "specified_peak_w", "full_load_current_a", "specified_peak_current_a", "average_battery_input_w")
        lines.append("| " + rail["id"] + " | " + " | ".join(display(rail[k]) for k in keys) + " |")
    lines += ["", "## Batterien", "",
              "| Akku | Schienen | Nutzbare Wh | Mittlere Eingangsleistung W | Modelllaufzeit h | Bedarf fuer Zielzeit Wh | Energiedifferenz Wh |",
              "| --- | --- | ---: | ---: | ---: | ---: | ---: |"]
    for battery in report["batteries"]:
        keys = ("usable_energy_wh", "average_input_w", "estimated_runtime_h", "target_energy_wh", "energy_difference_wh")
        lines.append("| " + battery["id"] + " | " + ", ".join(battery["rail_ids"]) + " | " + " | ".join(display(battery[k]) for k in keys) + " |")
    lines += ["", f"Modelllaufzeit bis zum ersten benoetigten leeren Akku: **{display(report['estimated_system_runtime_h'])} h**.",
              "Fehlende Lastdaten und Null-Last erzeugen keine unendliche oder bestaetigte Laufzeit.", "",
              "## Scharniere", "", "| Baugruppe | Statisches Gewichtsmoment Nm |", "| --- | ---: |"]
    lines += [f"| {h['id']} | {display(h['static_gravity_moment_nm'])} |" for h in report["hinges"]]
    lines += ["", "## Sockel: vier Kippkanten", "",
              "Vier getrennte unguenstige Richtungsfaelle: Jeder Kraftbetrag wird gegen beide",
              "Kanten seiner Achse angesetzt. Kein einzelner gleichzeitiger Kraftvektor.", "",
              "| Kante | Gewichtskraft-Hebel m | Rueckstellmoment Nm | Kippmoment Nm | Differenz Nm | Befund |",
              "| --- | ---: | ---: | ---: | ---: | --- |"]
    for edge in report["stand_edges"]:
        keys = ("gravity_lever_m", "restoring_moment_nm", "overturning_moment_nm", "moment_difference_nm")
        lines.append("| " + edge["edge"] + " | " + " | ".join(display(edge[k]) for k in keys) + " | `" + edge["finding"] + "` |")
    lines += ["", "## Fehlende Eingaben", ""]
    lines += [f"- `{field}`" for field in report["missing_inputs"]] or ["Keine leeren Eingabefelder. Die Daten sind dadurch nicht praktisch bestaetigt."]
    lines += ["", "## Grenzen", ""] + ["- " + text for text in report["limitations"]]
    if "input_sha256" in report:
        lines += ["", f"SHA-256 der Eingabedatei: `{report['input_sha256']}`."]
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--init", type=Path, help="Create a new empty project JSON without overwriting")
    parser.add_argument("--name", default="My Suit")
    parser.add_argument("--input", type=Path, help="Engineering JSON; there is no automatic demo input")
    parser.add_argument("--out", type=Path, help="Report directory; default beside input in <stem>-engineering")
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
        raw = args.input.read_bytes()
        report = calculate(json.loads(raw))
        report["input_sha256"] = hashlib.sha256(raw).hexdigest()
        out = args.out if args.out is not None else args.input.parent / (args.input.stem + "-engineering")
        outputs = {out / "EngineeringReport.json": json.dumps(report, indent=2, allow_nan=False) + "\n",
                   out / "EngineeringReport.md": render(report)}
        if any(path.resolve() == args.input.resolve() or
               (path.exists() and path.samefile(args.input)) for path in outputs):
            raise ValueError("Output must not overwrite the source input")
        for path, content in outputs.items():
            if args.check:
                if not path.exists() or path.read_text(encoding="utf-8") != content:
                    raise ValueError("Engineering report out of date: " + str(path))
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
        print(json.dumps({"project": report["project"], "input_status": report["input_status"],
                          "missing_count": len(report["missing_inputs"]), "hardware_approved": False}))
        return 0
    except (OSError, ValueError, TypeError, OverflowError) as exc:
        print("Engineering error: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
