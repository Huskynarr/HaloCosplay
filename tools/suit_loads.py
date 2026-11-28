#!/usr/bin/env python3
"""Rough static load estimate for the X01 concept geometry; no strength approval.

Beam and bolt formulas on nominal sections with assumed material values. No fatigue,
no notch or weld factors, no buckling, no out-of-plane load case, no test.
"""
import argparse
import json
import math
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
EXO = ROOT / "Design/Exo"
PARAMETERS = EXO / "Parameters.scad"
LOAD_CASE = EXO / "LoadCase.json"
OUT_JSON = EXO / "LoadEstimate.json"
OUT_MD = EXO / "LoadEstimate.md"
GRAVITY = 9.80665
SHEAR = 0.58  # shear yield as a fraction of tensile yield (von Mises)


def scad_parameters(text):
    values = {}
    for name, raw in re.findall(r"^(\w+) = ([^;]+);", text, re.M):
        raw = raw.strip()
        if raw.startswith("["):
            values[name] = [float(v) for v in raw.strip("[]").split(",")]
        elif re.fullmatch(r"-?[\d.]+", raw):
            values[name] = float(raw)
    return values


def stop_geometry(p):
    r_in = p["flange_d_mm"] / 2 + 2 + 2
    r_out = p["housing_bolt_circle_mm"] / 2 - 5
    return r_in, r_out


def estimate(p, case):
    """Return (checks, info). A check carries a stress and is rated per material."""
    torque = case["peak_torque_nm"] * 1000  # Nmm
    bolts = case["bolts"]["stress_area_mm2"]
    checks, info = [], []

    def add(check_id, part, text, stress, kind="normal", bolt=False):
        checks.append({"id": check_id, "part": part, "check": text, "kind": kind, "bolt": bolt,
                       "stress_mpa": round(stress, 1)})

    w, t_arm, t_bar, d = p["bar_w_mm"], p["arm_t_mm"], p["bar_t_mm"], p["joint_bolt_d_mm"]
    add("E01", "Abtriebsarm", "Biegung am Nabenrand", 6 * torque / (t_arm * w ** 2))
    add("E02", "Abtriebsarm", "Biegung im Lochquerschnitt", torque * (w / 2) / (t_arm * (w ** 3 - d ** 3) / 12))
    add("E03", "Strebe", "Biegung im Lochquerschnitt", torque * (w / 2) / (t_bar * (w ** 3 - d ** 3) / 12))

    r_in, r_out = stop_geometry(p)
    stop_force = torque * case["stop_impact_factor"] / r_in
    arc = math.radians(14) * (r_in + r_out) / 2
    add("E04", "Anschlagblock", "Scherung am Fuss, mit Stossfaktor", stop_force / (arc * (r_out - r_in)), "shear")

    flange_force = torque / (p["output_bolt_count"] * p["output_bolt_circle_mm"] / 2)
    add("E05", "Flanschschrauben M4", "Scherung je Schraube", flange_force / bolts["M4"], "shear", True)
    housing_force = torque / (p["housing_bolt_count"] * p["housing_bolt_circle_mm"] / 2)
    add("E06", "Gehaeuseschrauben M3", "Scherung je Schraube", housing_force / bolts["M3"], "shear", True)
    joint_force = torque / p["hole_pitch_mm"]
    add("E07", "Strebenschrauben M6", "Scherung je Schraube, Kraeftepaar im Lochraster", joint_force / bolts["M6"], "shear", True)
    add("E08", "Strebe", "Lochleibung an den Strebenschrauben", joint_force / (d * t_bar))

    block = p["hinge_block_mm"]
    add("E09", "Motorplatte", "Biegung im Hals unter dem Gelenkblock", 6 * torque / (p["plate_t_mm"] * block[1] ** 2))
    ear_force = torque / (block[1] + p["fork_ear_t_mm"])
    add("E10", "Gabel am Seitenarm", "Lochleibung am Gelenkbolzen", ear_force / (p["hinge_bolt_d_mm"] * p["fork_ear_t_mm"]))
    add("E11", "Gelenkbolzen M8", "Scherung je Gabelohr", ear_force / bolts["M8"], "shear", True)
    add("E12", "Seitenarm", "Biegung hochkant", 6 * torque / (t_bar * p["frame_bar_h_mm"] ** 2))

    outer, wall = p["frame_tube_mm"]
    mid = outer - wall
    add("E13", "Rueckenrohr", "Torsion, duennwandig", torque / (2 * mid ** 2 * wall), "shear")
    insert_arm = math.sqrt(2) * (outer - 2 * wall - 0.4) / 2
    add("E14", "Schrauben Rohreinsatz M6", "Scherung je Schraube", torque / insert_arm / bolts["M6"], "shear", True)

    length = p["pelvis_clear_width_mm"]
    tube_j = mid ** 3 * wall
    flat_j = p["frame_bar_h_mm"] * t_bar ** 3 / 3
    lever = p["hip_to_cuff_mm"]
    cuff_force = torque / lever
    for name, material in case["materials"].items():
        twist = lambda j: round(math.degrees(torque * length / (material["g_mpa"] * j)), 2)
        info.append({"id": "I01", "material": name, "text": "Verdrehung des Rueckenrohrs bei Spitzenmoment, Grad",
                     "value": twist(tube_j)})
        info.append({"id": "I02", "material": name,
                     "text": "Zum Vergleich: Flachstab gleicher Hoehe statt Rohr, Grad", "value": twist(flat_j)})
        info.append({"id": "I03", "material": name, "text": "Durchbiegung der Strebe an der Manschette in Bewegungsrichtung, mm",
                     "value": round(cuff_force * lever ** 3 / (3 * material["e_mpa"] * t_bar * w ** 3 / 12), 2)})
        info.append({"id": "I04", "material": name,
                     "text": "Seitliche Auslenkung der Strebe an der Manschette je %g N Querkraft, mm" % case["lateral_test_force_n"],
                     "value": round(case["lateral_test_force_n"] * lever ** 3 / (3 * material["e_mpa"] * w * t_bar ** 3 / 12), 1)})
    info.append({"id": "I05", "material": None, "text": "Kraft der Manschette am Oberschenkel bei Spitzenmoment, N",
                 "value": round(cuff_force, 1)})
    info.append({"id": "I06", "material": None, "text": "Mittlerer Druck unter der Manschette bei Spitzenmoment, kPa",
                 "value": round(cuff_force / (p["cuff_h_mm"] * p["thigh_cuff_d_mm"]) * 1000, 1)})
    info.append({"id": "I07", "material": None, "text": "Kraft am Anschlag ohne Stossfaktor, N",
                 "value": round(torque / r_in)})

    factor = case["safety_factor"]
    for check in checks:
        shear = SHEAR if check["kind"] == "shear" else 1.0
        if check["bolt"]:
            check["utilisation"] = {"Schraube 8.8": round(check["stress_mpa"] * factor / (shear * case["bolts"]["yield_mpa"]), 2)}
        else:
            check["utilisation"] = {name: round(check["stress_mpa"] * factor / (shear * material["yield_mpa"]), 2)
                                    for name, material in case["materials"].items()}
    lugs = case["hang_lugs"]
    area = lugs["net_width_mm"] * lugs["thickness_mm"]
    lug_rows = [{"module": name, "mass_kg": mass,
                 "stress_mpa": round(mass * GRAVITY * lugs["dynamic_factor"] / area, 2),
                 "utilisation": round(mass * GRAVITY * lugs["dynamic_factor"] / area * factor / lugs["print_strength_mpa"], 2)}
                for name, mass in lugs["modules"].items()]
    return checks, info, lug_rows


def report():
    case = json.loads(LOAD_CASE.read_text(encoding="utf-8"))
    checks, info, lugs = estimate(scad_parameters(PARAMETERS.read_text(encoding="ascii")), case)
    return {"schema_version": 1, "status": "ROUGH_ESTIMATE_NOT_A_STRENGTH_APPROVAL",
            "peak_torque_nm": case["peak_torque_nm"], "safety_factor": case["safety_factor"],
            "stop_impact_factor": case["stop_impact_factor"], "checks": checks, "info": info, "hang_lugs": lugs}


def render(data):
    names = list(data["checks"][0]["utilisation"])
    lines = [
        "# X01: Lastabschaetzung der Konzeptgeometrie", "",
        "**Erzeugt von `tools/suit_loads.py`; nicht von Hand aendern.** Eingaben:",
        "[Parameters.scad](Parameters.scad) und [LoadCase.json](LoadCase.json).", "",
        "Status: `ROUGH_ESTIMATE_NOT_A_STRENGTH_APPROVAL`. Balken- und Schraubenformeln am",
        "Nennquerschnitt mit angenommenen Werkstoffwerten. Nicht enthalten: Ermuedung,",
        "Kerbwirkung, Schweiss- und Klebestellen, Knicken und Beulen, Lasten quer zur",
        "Bewegungsebene, Sturz, Fertigungsfehler und jede Messung. Eine Auslastung unter 1",
        "heisst nur, dass diese eine Rechnung den Querschnitt nicht ausschliesst.", "",
        "Lastfall: %g Nm Spitzenmoment an einem Hueftantrieb, Sicherheitsfaktor %g gegen" % (
            data["peak_torque_nm"], data["safety_factor"]),
        "die Streckgrenze, Stossfaktor %g am Anschlag. Auslastung = Spannung mal" % data["stop_impact_factor"],
        "Sicherheitsfaktor durch Streckgrenze (bei Scherung 0,58 davon).", "",
        "## Querschnitte", "",
        "| ID | Teil | Nachweis | Spannung MPa | " + " | ".join(names) + " |",
        "| --- | --- | --- | --- | " + " | ".join("---" for _ in names) + " |",
    ]
    bolt_lines = ["", "## Schrauben (Festigkeitsklasse 8.8)", "",
                  "| ID | Schraube | Nachweis | Spannung MPa | Auslastung |", "| --- | --- | --- | --- | --- |"]
    for check in data["checks"]:
        util = check["utilisation"]
        if check["bolt"]:
            bolt_lines.append("| %s | %s | %s | %s | %s |" % (check["id"], check["part"], check["check"],
                                                             check["stress_mpa"], util["Schraube 8.8"]))
        else:
            cells = " | ".join(("**%s**" % util[n]) if util[n] > 1 else str(util[n]) for n in names)
            lines.append("| %s | %s | %s | %s | %s |" % (check["id"], check["part"], check["check"], check["stress_mpa"], cells))
    lines += bolt_lines
    lines += ["", "Fett: Auslastung ueber 1, der Querschnitt reicht in dieser Rechnung nicht.", "",
              "## Verformung und Kraefte", "", "| ID | Groesse | Werkstoff | Wert |", "| --- | --- | --- | --- |"]
    for row in data["info"]:
        lines.append("| %s | %s | %s | %s |" % (row["id"], row["text"], row["material"] or "-", row["value"]))
    lines += ["", "## Einhaengelaschen der Ruestungsmodule", "",
              "Zug im Restquerschnitt neben dem Gurtschlitz (2 x 6 mm breit, 6 mm dick) mit",
              "angenommener Modulmasse, dynamischem Faktor und angenommener Festigkeit des",
              "Drucks quer zur Schicht. Kriechen, Schlag und Schichtlage sind nicht erfasst.", "",
              "| Modul | Masse kg | Spannung MPa | Auslastung |", "| --- | --- | --- | --- |"]
    for row in data["hang_lugs"]:
        lines.append("| %s | %s | %s | %s |" % (row["module"], row["mass_kg"], row["stress_mpa"], row["utilisation"]))
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the committed outputs are out of date")
    args = parser.parse_args(argv)
    try:
        data = report()
    except (OSError, ValueError, KeyError) as exc:
        print("Lastabschaetzung-Fehler: " + str(exc), file=sys.stderr)
        return 2
    outputs = {OUT_JSON: json.dumps(data, indent=2, ensure_ascii=True) + "\n", OUT_MD: render(data)}
    if args.check:
        stale = [path.name for path, text in outputs.items() if not path.exists() or path.read_text(encoding="utf-8") != text]
        if stale:
            print("Veraltet: " + ", ".join(stale) + "; python3 tools/suit_loads.py ausfuehren", file=sys.stderr)
            return 1
        print("Lastabschaetzung aktuell")
        return 0
    for path, text in outputs.items():
        path.write_text(text, encoding="utf-8")
    worst = max((value, check["id"]) for check in data["checks"] for value in check["utilisation"].values())
    print("%d Nachweise, hoechste Auslastung %s (%s)" % (len(data["checks"]), worst[0], worst[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
