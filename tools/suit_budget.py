#!/usr/bin/env python3
"""Sum explicit planning allowances; never imply measured mass or live prices."""
import argparse
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BOM = ROOT / "Materials/Mjolnir-BOM.json"


def numeric(v):
    return not isinstance(v, bool) and isinstance(v, (int, float)) and math.isfinite(v) and v >= 0


def calculate(data):
    if (not isinstance(data, dict) or isinstance(data.get("schema_version"), bool)
            or data.get("schema_version") != 1 or data.get("currency") != "EUR"):
        raise ValueError("Unsupported BOM schema/currency")
    reserve = data.get("contingency_fraction")
    if not numeric(reserve) or reserve > 1:
        raise ValueError("Invalid contingency")
    if not numeric(data.get("wearable_target_g")):
        raise ValueError("Invalid mass target")
    low = high = mass = 0
    ids = set()
    missing = []
    if not isinstance(data.get("items"), list) or not all(isinstance(item, dict) for item in data["items"]):
        raise ValueError("items must be a list of BOM objects")
    for item in data["items"]:
        if item["id"] in ids:
            raise ValueError("Duplicate BOM ID")
        ids.add(item["id"])
        q = item["qty"]
        prices = item["unit_budget_eur"]
        if isinstance(q, bool) or not isinstance(q, int) or q < 1:
            raise ValueError("Invalid quantity")
        if len(prices) != 2 or not all(numeric(v) for v in prices) or prices[0] > prices[1]:
            raise ValueError("Invalid price range")
        if not isinstance(item["worn"], bool):
            raise ValueError("worn must be boolean")
        low += q * prices[0]
        high += q * prices[1]
        m = item["unit_mass_target_g"]
        if m is not None and not numeric(m):
            raise ValueError("Invalid mass")
        if item["worn"]:
            if m is None:
                missing.append(item["id"])
            else:
                mass += q * m
    return {"base_eur": [low, high],
            "with_reserve_eur": [round(low*(1+reserve), 2), round(high*(1+reserve), 2)],
            "planned_worn_g": mass, "unknown_worn_mass_ids": missing,
            "mass_target_met_in_plan": not missing and mass <= data["wearable_target_g"]}


def render(data, include_reference_notes=True):
    total = calculate(data)
    lines = ["# MJOLNIR: Stueckliste und Planbudget", "",
             "GENERATED: tools/suit_budget.py. Eigene Budgetansaetze, keine aktuellen",
             "Haendlerangebote. Massen sind Entwicklungsziele, keine Messwerte.", "",
             "| ID | Baugruppe | Anzahl | EUR je Einheit | Zielmasse je Einheit g |",
             "| --- | --- | ---: | ---: | ---: |"]
    for item in data["items"]:
        low, high = item["unit_budget_eur"]
        mass = item["unit_mass_target_g"]
        lines.append(f"| {item['id']} | {item['name']} | {item['qty']} | {low}-{high} | {mass if mass is not None else 'nicht getragen / offen'} |")
    lines += ["", f"Basisbudget: **{total['base_eur'][0]:.2f}-{total['base_eur'][1]:.2f} EUR**.",
              f"Mit {data['contingency_fraction']*100:g}% Material-/Iterationsreserve: **{total['with_reserve_eur'][0]:.2f}-{total['with_reserve_eur'][1]:.2f} EUR**.",
              f"Geplante getragene Zusatzmasse: **{total['planned_worn_g']/1000:.2f} kg**" + (
                  ", ohne normales Schuhwerk." if include_reference_notes else ", gemaess den worn-Positionen dieser Liste."),
              "", "Die Reserve erhoeht das Kostenbudget, nicht das tragbare Gewichtsbudget.",
              ("Serien-Exoskelett, dessen Akku und alle optionalen Zusatzsysteme kommen zur Masse hinzu."
               if include_reference_notes else "Fehlende getragene Baugruppen muessen in der Liste ergaenzt werden."),
              "Fehlen reale Wiegungen, ist damit keine Tragbarkeit oder Lastfreigabe bewiesen.", "",
              "Nicht enthalten:", ""] + [f"- {x}" for x in data["excluded"]]
    if not include_reference_notes:
        lines += ["", "Diese Liste ist projektspezifisch. Mengen, getragene Baugruppen und Ausschluesse",
                  "muessen zur gewaehlten Konfiguration passen. Keine Auswahl von Kaufteilen oder",
                  "Tragbarkeitsfreigabe allein aus dem Budget ableiten.", ""]
        return "\n".join(lines)
    lines += ["", "## Beschaffungsreihenfolge", "",
              "P01 zuerst. Nach Passprobe T01 und eine Tuerlagerung T03-T06 auf dem Tisch.",
              "Schalenmaterial, Helm und Gliedmassen erst nach bestaetigtem Platzbedarf.",
              "Keine komplette Aktorik oder Serien-Exoskelett-Bestellung aus dieser Liste ableiten.", "",
              "Schalenbudgets enthalten jeweiliges Material und Finish. Schrauben/Trennstellen",
              "sind in T06 enthalten; keine zweite pauschale Hardwaremasse addiert.",
              "Die Schnittstellenliste im [Einstiegsentwurf](../Documentation/Guides/Mjolnir-Einstieg.md)",
              "definiert die Auswahlkriterien. Kaufteile benoetigen Datenblaetter und eine",
              "Bemessung der gesamten Montage, bevor sie am getragenen Aufbau eingesetzt werden.", ""]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bom", type=Path, default=DEFAULT_BOM,
                        help="Custom BOM JSON; output defaults to a sibling .md file")
    parser.add_argument("--out", type=Path, help="Output Markdown path")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    target = args.out if args.out is not None else args.bom.with_suffix(".md")
    try:
        if target.resolve() == args.bom.resolve():
            raise ValueError("Output must not overwrite the source BOM")
        data = json.loads(args.bom.read_text(encoding="utf-8"))
        result = render(data, include_reference_notes=args.bom.resolve() == DEFAULT_BOM.resolve())
        if args.check:
            if not target.exists() or target.read_text(encoding="utf-8") != result:
                raise ValueError("BOM out of date: regenerate with the same --bom/--out arguments")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(result, encoding="utf-8")
        print(json.dumps(calculate(data), sort_keys=True))
    except (ValueError, OSError, TypeError, KeyError) as exc:
        print(f"BOM error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
