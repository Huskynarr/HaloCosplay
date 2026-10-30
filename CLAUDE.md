# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A comprehensive DIY project repository for building a Halo Master Chief MJOLNIR cosplay suit. This is primarily a **documentation and planning repo** with supporting embedded code - not a traditional software project. Content is written in German.

Three build variants exist: V1 Einsteiger (foam), V2 Fortgeschritten (3D-print/hybrid with HUD), V3 Profi (exoskeleton + premium).

## Repository Structure

- `Documentation/TODO.md` - master TODO list for the entire project
- `Documentation/Guides/` - core knowledge base (build techniques, electronics, safety, costs, schedules)
- `Documentation/Guides/3D-Druck.md` - Bambu Lab H2C print settings, splitting, orientation, times
- `Documentation/Guides/Lackierung-Finishing.md` - surface prep, painting, weathering, visor creation
- `Documentation/Guides/Unteranzug-Befestigung.md` - undersuit options, magnets, velcro, harness
- `Documentation/Guides/Elektronik-*.md` - HUD, battery, wiring, fans, audio, autostart guides
- `Documentation/Guides/Elektronik-Show-Praxis-Module.md` - shield-hit touch effect, handler alert, hydration reminder
- `Documentation/Guides/Convention-Regeln.md` - German con rules (Gamescom, DoKomi, MCC, etc.) + Waffengesetz
- `Documentation/Guides/Transport.md` - packing and transporting armor to conventions
- `BuildGuides/` - step-by-step build phases for Armor, Helmet, and Electronics
- `Code/` - Arduino (.ino) and Python control code for helmet HUD and armor LEDs
- `Materials/ShoppingList.md` - detailed BOM with prices (filament, electronics, paint, attachment)
- `Design/` - sketches, 3D model references, ideas
- `Resources/STL-Quellen.md` - curated STL sources (Galactic Armory, MakerWorld, 405th, etc.)
- `Tests/TestReports/` - physical fit/function test report templates

## Code / Electronics

### HUD Display (Python, runs on Raspberry Pi Zero 2 W)
- `Code/HelmetControl/hud_display.py` - main HUD loop driving a transparent OLED (SSD1309) over I2C
- Dependencies: `pip install -r Code/HelmetControl/requirements.txt` (luma.oled, Pillow, smbus2)
- Config: copy `config.example.json` to `config.json`; battery status via `battery.example.json` to `battery.json`
- No test suite exists; testing is manual on hardware (hardware-free `--selftest` modes run in CI)
- All writers of `hud_state.json` must use `hud_state.merge()` (file lock + atomic replace) so modules don't clobber each other's keys

### Voice control + vision (Python, Raspberry Pi 5, optional)
- `Code/HelmetControl/voice_control.py` - push-to-talk voice commands (Vosk), I2C to helmet Arduino, optocoupler "button presses" to thruster/armor Arduinos, helmet radio voice (Audio Option C)
- `Code/HelmetControl/vision_bridge.py` - AI Camera (IMX500) detections -> `vision_contacts` in `hud_state.json` -> motion tracker
- Guide: `Documentation/Guides/Elektronik-Sprachsteuerung.md`

### Arduino Controllers
- `Code/HelmetControl/MainControlCode.ino` - I2C slave receiving brightness commands (basic)
- `Code/HelmetControl/HelmetMultiEffects.ino` - **advanced**: 5 visor effects + I2C commands + fan PWM + button switching
- `Code/ArmorControl/MultiEffects.ino` - **advanced**: 5 LED effects + button switching + boot sequence + shield-hit touch sensors + handler alert
- `Code/HelmetControl/LightingEffectsCode.ino` - simple LED running effect
- `Code/ArmorControl/MainControlCode.ino` - simple LED breathing effect
- `Code/ArmorControl/LightingEffectsCode.ino` - simple LED chase effect
- Compiled via Arduino IDE or `arduino-cli compile`; pin assignments must be adapted per build
- LED effect patterns documented in `Documentation/Guides/LED-Effekte.md`

## Conventions

- All documentation is in **German** (ASCII-safe: ae/oe/ue instead of umlauts)
- Markdown files use `#` heading hierarchy; no frontmatter
- File and folder names use PascalCase (e.g., `BuildGuides`, `ShoppingList.md`)
- Contributions follow fork-and-PR workflow (see CONTRIBUTING.md)
