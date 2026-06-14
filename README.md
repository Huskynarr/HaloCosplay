# HaloCosplay: Master Chief MJOLNIR Projekt

Dieses Repository ist eine vollstaendige DIY-Projektmappe fuer ein moeglichst authentisches Halo Master Chief Cosplay mit Ruestung, Helm, Prop-Waffe und optionaler Elektronik (HUD, Akku-Backpack, AR/Display). Das Projekt ist in drei Varianten strukturiert: Einsteiger (Foam), Fortgeschritten (3D-Druck/Hybrid) und Profi (Exoskelett + Premium-Materialien).

## Varianten im Ueberblick

| Variante | Ziel | Materialien | Technik | Budget (Richtwert) | Dauer (Richtwert) |
| --- | --- | --- | --- | --- | --- |
| V1 Einsteiger | klassisches Cosplay | EVA-Foam, Kunststoff, Holz | einfache LEDs | 800-2.700 EUR | 2-5 Monate |
| V2 Fortgeschritten | detailstark + stabil | 3D-Druck + Foam | HUD + Pi, Akku | 2.400-6.600 EUR | 4-8 Monate |
| V3 Profi | High-End + Exoskelett | Alu/Carbon, CNC/3D | HUD, Sensorik, Exo | 6.000+ EUR | 8-14 Monate |

## Hinweis zu Kosten

Die Kosten sind stark abhaengig von Tools, Fehlversuchen, Versand und Premium-Materialien. Realistisch ist oft das 2-3x der Minimalannahmen.

## Projektziele

- **Authentische MJOLNIR-Optik:** Mark VII / Mark VI Gen 3 Look mit originalen Farbcodes von 343 Industries.
- **Tragbare, sichere Bauweise:** Modularer Aufbau fuer Conventions mit Notausstieg in <60 Sekunden.
- **Mechanisches Exoskelett (V3):** Passives Traggestell zur Lastableitung (Schultern -> Huefte) mit Taulman Alloy 910 Gelenken, H-Harness Rigging und bungeegestuetzten PEX-Hydraulikkolben.
- **AR HUD & OpenCV (V3):** Near-Eye-Display (NED/Vufine) mit Pi 4/5, OpenCV-Bildverarbeitung (Freund-Feind-Erkennung / IFF), Nachtsicht, digitalem Zoom und BT-Waffentelemetrie.
- **Munitionszaehler (MA40/MA5):** Integrierte Zaehlerelektronik (Arduino/Pico) mit SSD1306-OLED-Anzeige, Schussabnahme am Abzug und Reload-Erkennung.

## Quick Start

1. **Roter Faden / Komplett-Walkthrough (Anfaenger bis Profi):** `Documentation/Guides/Komplett-Walkthrough.md`
2. **Start-Here-Guide lesen:** `Documentation/Guides/Start-Hier.md`
3. **Projektuebersicht lesen:** `Documentation/README.md`
4. **Variante waehlen (V1 Foam, V2 3D-Druck, V3 Exoskelett):** `Documentation/Guides/Varianten.md`
5. **TODO-Liste nutzen:** `Documentation/TODO.md`
6. **Bau- und Skalierungsplanung (Shin +15%, Biceps 1.1x):** `BuildGuides/Armor/Step1.md`
7. **Exoskelett & Hydraulik-Bauplaene:** `Documentation/Guides/Exoskelett.md`
8. **Schubduesen & Nebeleffekte:** [Elektronik-Schubduesen.md](Documentation/Guides/Elektronik-Schubduesen.md)
9. **Kosten und Zeitplan:** `Documentation/Guides/Kosten.md` und `Documentation/Guides/Zeitplan.md`
10. **Elektronik-Systemplanung:** `Documentation/Guides/Elektronik-HUD.md` und `Materials/ShoppingList.md`
11. **Code-Uebersicht (OLED HUD, AR, LED-Effekte, Ammo-Counter):** `Code/README.md`

## Projektstruktur

- `Documentation/` Projektuebersicht, Sicherheits- und Technikdokumentation
- `Documentation/TODO.md` **Haupt-Todoliste** fuer das gesamte Projekt
- `BuildGuides/` Schritt-fuer-Schritt Bauphasen (Ruestung, Helm, Elektronik)
- `Materials/` Einkaufslisten, Komponenten und Quellen
- `Code/` Beispielcode fuer HUD, LEDs und Controller
- `Design/` Skizzen, Vorlagen, 3D-Modelle
- `Resources/` Tools, Links, STL-Quellen, Community, Referenzen
- `Support/` FAQ und Kontakt

## Sicherheit und Conventions

- Siehe `Documentation/Guides/Sicherheit.md`
- Siehe `Documentation/Guides/Convention-Regeln.md`

## Community

- 405th Infantry Division: https://www.405th.com/
- RPF: https://www.therpf.com/

Viel Erfolg beim Bau. Schritt fuer Schritt, und immer zuerst die sichere Tragbarkeit testen.
