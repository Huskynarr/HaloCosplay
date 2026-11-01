#!/usr/bin/env bash
# Exportiert alle MJOLNIR-Ruestungsteile als STL. Benoetigt OpenSCAD.
# Aufruf: ./Design/Armor/export_stl.sh [pfad-zu-openscad]
set -euo pipefail

OPENSCAD="${1:-openscad}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR="${SCRIPT_DIR}/STL"

mkdir -p "${OUT_DIR}"

parts=(helmet visor chest back shoulder_l shoulder_r
       upperarm_l upperarm_r forearm_l forearm_r gauntlet_l gauntlet_r
       thigh_l thigh_r shin_l shin_r boot_l boot_r)

for part in "${parts[@]}"; do
    echo "Exportiere ${part} ..."
    if [[ "${part}" == boot_* ]]; then
        "${OPENSCAD}" -o "${OUT_DIR}/armor-${part}.stl" -D 'part="${part}"' -D '$fn=24' \
            "${SCRIPT_DIR}/MasterChiefArmor.scad"
    else
        "${OPENSCAD}" -o "${OUT_DIR}/armor-${part}.stl" -D 'part="${part}"' \
            "${SCRIPT_DIR}/MasterChiefArmor.scad"
    fi
done

echo "Fertig: ${OUT_DIR}"
