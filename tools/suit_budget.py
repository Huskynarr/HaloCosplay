#!/usr/bin/env python3
"""Sum explicit planning allowances; never imply measured mass or live prices."""
import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def numeric(v):
    return not isinstance(v, bool) and isinstance(v, (int, float)) and math.isfinite(v) and v >= 0


def calculate(data):
    if data.get("schema_version") != 1 or data.get("currency") != "EUR":
        raise ValueError("Unsupported BOM schema/currency")
    reserve = data.get("contingency_fraction")
    if not numeric(reserve) or reserve > 1:
        raise ValueError("Invalid contingency")
    if not numeric(data.get("wearable_target_g")):
        raise ValueError("Invalid mass target")
    low = high = mass = 0
    ids = set()
    missing = []
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


def render(data):
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
              f"Geplante getragene Zusatzmasse: **{total['planned_worn_g']/1000:.2f} kg**, ohne normales Schuhwerk.",
              "", "Die Reserve erhoeht das Kostenbudget, nicht das tragbare Gewichtsbudget.",
              "Serien-Exoskelett, dessen Akku und alle optionalen Zusatzsysteme kommen zur Masse hinzu.",
              "Fehlen reale Wiegungen, ist damit keine Tragbarkeit oder Lastfreigabe bewiesen.", "",
              "Nicht enthalten:", ""] + [f"- {x}" for x in data["excluded"]]
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = json.loads((ROOT / "Materials/Mjolnir-BOM.json").read_text())
    target = ROOT / "Materials/Mjolnir-BOM.md"
    result = render(data)
    if args.check:
        if not target.exists() or target.read_text() != result:
            raise SystemExit("BOM out of date: run python3 tools/suit_budget.py")
    else:
        target.write_text(result)
    print(json.dumps(calculate(data), sort_keys=True))
