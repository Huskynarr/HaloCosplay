#!/usr/bin/env python3
"""Compile the real sketches against mock Arduino headers and run their host tests.

Usage: python3 Tests/Firmware/run.py   (needs g++ with C++17)
The sketches are included unchanged; only function prototypes are generated,
as the Arduino build does.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SUITES = [
    ("Code/HelmetControl/HelmetMultiEffects.ino", "helmet_test.cpp"),
    ("Code/ArmorControl/MultiEffects.ino", "armor_test.cpp"),
]
PROTOTYPE = re.compile(r"^((?:void|bool|int|long|float|uint8_t|uint16_t|uint32_t|unsigned long)\s+\w+\s*\([^)]*\))\s*\{", re.M)


def main():
    failed = False
    with tempfile.TemporaryDirectory() as tmp:
        for sketch, test in SUITES:
            source = (ROOT / sketch).read_text(encoding="ascii")
            prototypes = "\n".join(match + ";" for match in PROTOTYPE.findall(source))
            unit = Path(tmp) / (Path(test).stem + "_unit.cpp")
            unit.write_text('#include "Arduino.h"\n%s\n#line 1 "%s"\n%s\n#include "%s"\n'
                            % (prototypes, sketch, source, (HERE / test).as_posix()), encoding="ascii")
            binary = Path(tmp) / Path(test).stem
            print("== %s" % sketch, flush=True)
            build = subprocess.run(["g++", "-std=c++17", "-Wall", "-Wextra", "-Wno-unused-function", "-O1",
                                    "-I", str(HERE / "mock"), "-I", str(HERE), str(unit), "-o", str(binary)])
            if build.returncode or subprocess.run([str(binary)]).returncode:
                failed = True
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
