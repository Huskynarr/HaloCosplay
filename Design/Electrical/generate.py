#!/usr/bin/env python3
"""Erzeugt editierbare Stromlaufplaene und Netzliste, ohne EDA-Abhaengigkeit."""
import argparse
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCES = {
    "ldd": "https://www.meanwell.com/Upload/PDF/LDD-L/LDD-L-SPEC.PDF",
    "buffer": "https://www.ti.com/lit/ds/symlink/sn74ahct1g125.pdf",
    "mosfet": "https://www.aosmd.com/res/data_sheets/AO3400A.pdf",
    "relay": "https://omronfs.omron.com/en_US/ecb/products/pdf/en-g5le.pdf",
    "diode": "https://www.vishay.com/docs/88503/1n4001.pdf",
    "regulator": "https://www.pololu.com/product/2831",
    "pd": "https://www.sparkfun.com/sparkfun-power-delivery-board-usb-c-qwiic.html",
    "fan": "https://www.noctua.at/pub/media/wysiwyg/Noctua_PWM_specifications_white_paper.pdf",
    "led": "https://www.ledsupply.com/leds/cree-xpe2-rgb-high-power-led",
}
CHANNELS = ("H_R", "H_G", "H_B", "N_R", "N_G", "N_B")


def design():
    d = {"schema_version": 1, "revision": "electrical-r1", "status": "design_only",
         "hardware_approved": False, "sources": SOURCES, "components": [],
         "channels": [], "unresolved": {
             "fuse_ratings_a": None, "wire_gauge_mm2": None,
             "thermal_contact_part_and_trip_temperature": None,
             "controller_gpio_assignment": None, "measured_dim_input_current_a": None,
             "power_sequencing_and_relay_release_with_diode_ms": None,
             "pd_nvm_configuration_and_source_validation": None,
         }}

    def add(ref, kind, value, pins, sheet, source=None, **more):
        d["components"].append(dict(ref=ref, kind=kind, value=value,
            pins={str(k): v for k, v in pins.items()}, sheet=sheet, source=source, **more))

    add("J10", "connector", "5 V Komfort-Eingang; kodiert", {1: "C5_RAW", 2: "C_GND"}, "01")
    add("F10", "fuse", "TBD nach Last/Leitung", {1: "C5_RAW", 2: "C5_FUSED"}, "01", rating_a=None)
    add("S10", "switch_no", "Komfort EIN/AUS; DC-Rating TBD", {1: "C5_FUSED", 2: "C5_FAN"}, "01")
    for i, zone in enumerate(("Helm links", "Helm rechts", "Torso links", "Torso rechts"), 11):
        add(f"J{i}", "connector", zone + "; 5-V-Noctua-PWM", {1: "C_GND", 2: "C5_FAN", 3: None, 4: None}, "01", "fan")
    add("J20", "module_boundary", "SparkFun DEV-15801 / STUSB4500", {"VOUT": "E15_RAW", "GND": "E_GND"}, "02", "pd", input_interface="USB-C PD", configured_output_v=15, configuration_verified=False)
    add("F20", "fuse", "TBD nach Last/Leitung", {1: "E15_RAW", 2: "E15_FUSED"}, "02", rating_a=None)
    add("S20", "switch_no", "Lichtversorgung AUS; DC-Rating TBD", {1: "E15_FUSED", 2: "E15_SW"}, "02")
    add("U20", "regulator_module", "Pololu D24V10F5 #2831", {"VIN": "E15_SW", "GND": "E_GND", "VOUT": "E5_RAW", "SHDN": None, "PG": None}, "02", "regulator")
    add("F21", "fuse", "5-V-Abgang; TBD", {1: "E5_RAW", 2: "E5_CTRL"}, "02", rating_a=None)
    add("C20", "capacitor_polarized", "33 uF / 50 V; Eingangspuffer", {"+": "E15_SW", "-": "E_GND"}, "02", "regulator")
    add("K20", "relay_no", "Omron G5LE-1A DC5", {1: "E15_SW", 3: "E15_LED", 2: "E5_CTRL", 5: "COIL_LOW"}, "02", "relay")
    add("D20", "diode", "1N4007; Freilauf", {"A": "COIL_LOW", "K": "E5_CTRL"}, "02", "diode")
    add("Q20", "nmos", "AO3400A; SOT-23", {1: "RELAY_GATE", 2: "E_GND", 3: "COIL_LOW"}, "02", "mosfet", pin_names={"1": "G", "2": "S", "3": "D"})
    add("R20", "resistor", "100 ohm", {1: "READY_AFTER_TH", 2: "RELAY_GATE"}, "02")
    add("R21", "resistor", "10 kohm", {1: "RELAY_GATE", 2: "E_GND"}, "02")
    add("J21", "connector", "Temperaturkontaktkette; potentialfreie Oeffner", {1: "MCU_READY", 2: "READY_AFTER_TH"}, "02", implementation="external_unselected_no_jumper_default")
    add("J22", "connector", "MCU lokale Versorgung; 5 V IN -> eigene 3V3-Regelung", {1: "E5_CTRL", 2: "E_GND"}, "02")
    signal_pins = {1: "E_GND", 2: "MCU_READY"}
    signal_pins.update({i + 3: f"PWM_{name}" for i, name in enumerate(CHANNELS)})
    add("J30", "connector", "3,3-V-MCU-Signale; nur Effektdomaene", signal_pins, "05")
    for i, name in enumerate(CHANNELS):
        base = 30 + i
        sheet = "03" if name.startswith("H") else "04"
        color = name[-1]
        left, right = ("HL", "HR") if sheet == "03" else ("NL", "NR")
        add(f"U{base}", "ldd", "MEAN WELL LDD-350L", {1: "E15_LED", 3: f"DIM_{name}", 4: "E_GND", 5: f"LED_{name}_RET", 6: f"LED_{name}_OUT"}, sheet, "ldd")
        add(f"B{base}", "buffer", "SN74AHCT1G125DBVR", {1: "E_GND", 2: f"PWM_{name}", 3: "E_GND", 4: f"DIM_{name}", 5: "E5_CTRL"}, "05", "buffer")
        add(f"R{base}", "resistor", "10 kohm", {1: f"PWM_{name}", 2: "E_GND"}, "05")
        add(f"C{base}", "capacitor", "100 nF / >=10 V; am IC", {1: "E5_CTRL", 2: "E_GND"}, "05", "buffer")
        add(f"LED_{left}_{color}", "led", f"{left} / {color}", {"A": f"LED_{name}_OUT", "K": f"LED_{name}_MID"}, sheet, "led", star=left)
        add(f"LED_{right}_{color}", "led", f"{right} / {color}", {"A": f"LED_{name}_MID", "K": f"LED_{name}_RET"}, sheet, "led", star=right)
        d["channels"].append({"id": name, "driver": f"U{base}", "buffer": f"B{base}", "pulldown": f"R{base}", "decoupling": f"C{base}", "leds": [f"LED_{left}_{color}", f"LED_{right}_{color}"], "current_a": 0.35, "pwm_hz_range": [100, 1000]})
    for star in ("HL", "HR", "NL", "NR"):
        pins = {}
        for i, color in enumerate("RGB"):
            name = star[0] + "_" + color
            pins[i*2 + 1] = f"LED_{name}_OUT" if star.endswith("L") else f"LED_{name}_MID"
            pins[i*2 + 2] = f"LED_{name}_MID" if star.endswith("L") else f"LED_{name}_RET"
        add("J" + star, "connector", "RGB-Star; 6 getrennte Pads", pins, "03" if star.startswith("H") else "04")
    return d


def index(d):
    return {c["ref"]: c for c in d["components"]}


def validate(d):
    """Topologiepruefung, kein Ersatz fuer ERC oder elektrische Messungen."""
    c = index(d)
    if len(c) != len(d["components"]):
        raise ValueError("Doppelte Bauteilreferenz")
    def require(ok, message):
        if not ok:
            raise ValueError(message)
    def pins(ref, expected):
        require(c[ref]["pins"] == {str(k): v for k, v in expected.items()}, "Pin-/Netzfehler: " + ref)
    for part in d["components"]:
        nets = {n for n in part["pins"].values() if n}
        require(not (any(n.startswith("C5_") or n == "C_GND" for n in nets) and any(n.startswith("E") or n.startswith("DIM_") for n in nets)), "Komfort-/Effektdomaenen verbunden")
        if part["kind"] in {"fuse", "switch_no", "resistor", "capacitor", "capacitor_polarized", "diode", "led"}:
            require(len(nets) == 2, "Kurzschluss oder offenes Zweipolbauteil: " + part["ref"])
    pins("J10", {1: "C5_RAW", 2: "C_GND"})
    pins("F10", {1: "C5_RAW", 2: "C5_FUSED"})
    pins("S10", {1: "C5_FUSED", 2: "C5_FAN"})
    for n in range(11, 15):
        pins(f"J{n}", {1: "C_GND", 2: "C5_FAN", 3: None, 4: None})
    pins("J20", {"VOUT": "E15_RAW", "GND": "E_GND"})
    pins("F20", {1: "E15_RAW", 2: "E15_FUSED"})
    pins("S20", {1: "E15_FUSED", 2: "E15_SW"})
    pins("U20", {"VIN": "E15_SW", "GND": "E_GND", "VOUT": "E5_RAW", "SHDN": None, "PG": None})
    pins("F21", {1: "E5_RAW", 2: "E5_CTRL"})
    pins("K20", {1: "E15_SW", 3: "E15_LED", 2: "E5_CTRL", 5: "COIL_LOW"})
    pins("D20", {"A": "COIL_LOW", "K": "E5_CTRL"})
    pins("Q20", {1: "RELAY_GATE", 2: "E_GND", 3: "COIL_LOW"})
    pins("R20", {1: "READY_AFTER_TH", 2: "RELAY_GATE"})
    pins("R21", {1: "RELAY_GATE", 2: "E_GND"})
    pins("J21", {1: "MCU_READY", 2: "READY_AFTER_TH"})
    pins("J22", {1: "E5_CTRL", 2: "E_GND"})
    pins("J30", {1: "E_GND", 2: "MCU_READY", **{i+3: "PWM_"+n for i,n in enumerate(CHANNELS)}})
    pins("C20", {"+": "E15_SW", "-": "E_GND"})
    require(tuple(ch["id"] for ch in d["channels"]) == CHANNELS, "Sechs eindeutige Kanaele erforderlich")
    for ch in d["channels"]:
        n = ch["id"]
        pins(ch["driver"], {1: "E15_LED", 3: "DIM_" + n, 4: "E_GND", 5: f"LED_{n}_RET", 6: f"LED_{n}_OUT"})
        pins(ch["buffer"], {1: "E_GND", 2: "PWM_" + n, 3: "E_GND", 4: "DIM_" + n, 5: "E5_CTRL"})
        pins(ch["pulldown"], {1: "PWM_" + n, 2: "E_GND"})
        pins(ch["decoupling"], {1: "E5_CTRL", 2: "E_GND"})
        pins(ch["leds"][0], {"A": f"LED_{n}_OUT", "K": f"LED_{n}_MID"})
        pins(ch["leds"][1], {"A": f"LED_{n}_MID", "K": f"LED_{n}_RET"})
    for star in ("HL", "HR", "NL", "NR"):
        expected = {}
        for j, col in enumerate("RGB"):
            led = c[f"LED_{star}_{col}"]["pins"]
            expected[2*j+1], expected[2*j+2] = led["A"], led["K"]
        pins("J" + star, expected)
    require(d["hardware_approved"] is False, "Software darf keine Hardware freigeben")
    if "nets" in d:
        expected = {}
        for part in d["components"]:
            for pin, net in part["pins"].items():
                if net:
                    expected.setdefault(net, []).append({"ref": part["ref"], "pin": pin})
        require(d["nets"] == dict(sorted(expected.items())), "Netzindex stimmt nicht mit Pins ueberein")
    return True


def steady_state(*, manual_on, effects_5v_valid, controller_connected, ready,
                 thermal_contact_closed, pwm, comfort_on=True):
    """Ideales stationaeres Logikmodell; keine Einschalt-/Fehlersimulation."""
    relay = bool(manual_on and effects_5v_valid and controller_connected and ready and thermal_contact_closed)
    return {"relay_energized": relay, "led_on": bool(relay and pwm),
            "comfort_fans_on": bool(comfort_on)}


class Sheet:
    def __init__(self, d, title, number, subtitle):
        self.c = index(d)
        self.parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1100" viewBox="0 0 1500 1100">',
            '<style>text{font-family:DejaVu Sans,sans-serif;fill:#193442} .wire{fill:none;stroke:#226862;stroke-width:2.3} .sym{fill:white;stroke:#193442;stroke-width:2.2} .small{font-size:16px} .net{font-size:14px;fill:#226862} .body{font-size:19px} .title{font-size:30px;font-weight:bold}</style>',
            '<rect width="1500" height="1100" fill="#fff"/>',
            '<rect x="24" y="24" width="1452" height="1052" fill="none" stroke="#a6b3ba"/>']
        self.text(48, 73, title, "title")
        self.text(48, 108, subtitle)
        self.line(48, 130, 1452, 130, "#a6b3ba")
        self.line(48, 1015, 1452, 1015, "#a6b3ba")
        self.text(48, 1048, "HaloCosplay | electrical-r1 | Entwurf, keine Bauabnahme | 2026-09-09", "small")
        self.text(1360, 1048, number + " / 05", "small")

    def text(self, x, y, value, cls="body", anchor="start"):
        self.parts.append(f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{html.escape(str(value))}</text>')

    def line(self, x1, y1, x2, y2, color="#193442"):
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2.2"/>')

    def wire(self, points, net):
        self.parts.append('<polyline class="wire" points="' + " ".join(f"{x},{y}" for x, y in points) + f'" data-net="{net}"/>')

    def dot(self, x, y):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#226862"/>')

    def pin(self, ref, pin, x, y):
        net = self.c[ref]["pins"][str(pin)]
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="3" fill="white" stroke="#226862" data-ref="{ref}" data-pin="{pin}" data-net="{net or "NC"}"/>')
        return net

    def port(self, ref, pin, x, y, side="left", label=True):
        net = self.pin(ref, pin, x, y)
        dx = -55 if side == "left" else 55
        if net:
            self.wire([(x, y), (x + dx, y)], net)
            if label:
                self.text(x + dx, y-10, net, "net", "end" if side == "left" else "start")
        else:
            self.line(x-5, y-5, x+5, y+5)
            self.line(x-5, y+5, x+5, y-5)
            if label:
                self.text(x + dx, y-10, "NC", "net", "end" if side == "left" else "start")

    def rect(self, x, y, w, h, dashed=False):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="sym"' + (' stroke-dasharray="6 5"' if dashed else '') + '/>')

    def resistor(self, ref, x, y, vertical=False):
        p = list(self.c[ref]["pins"])
        self.text(x + 3, y-27, ref + " / " + self.c[ref]["value"], "small")
        if vertical:
            self.rect(x-9, y+18, 18, 42)
            self.line(x, y, x, y+18); self.line(x, y+60, x, y+80)
            self.pin(ref, p[0], x, y); self.pin(ref, p[1], x, y+80)
        else:
            self.rect(x+18, y-9, 44, 18)
            self.line(x, y, x+18, y); self.line(x+62, y, x+80, y)
            if self.c[ref]["kind"] == "fuse":
                self.line(x+18, y, x+62, y)
            self.pin(ref, p[0], x, y); self.pin(ref, p[1], x+80, y)

    def switch(self, ref, x, y):
        self.text(x, y-45, ref, "small")
        self.line(x, y, x+20, y); self.line(x+20, y, x+62, y-25)
        self.line(x+70, y, x+90, y)
        self.pin(ref, 1, x, y); self.pin(ref, 2, x+90, y)
        self.dot(x+20, y); self.dot(x+70, y)

    def capacitor(self, ref, x, y, polarized=False):
        p = list(self.c[ref]["pins"])
        self.text(x+20, y+25, ref + " / " + self.c[ref]["value"], "small")
        self.line(x, y, x, y+25); self.line(x-15, y+25, x+15, y+25)
        self.line(x-15, y+38, x+15, y+38); self.line(x, y+38, x, y+65)
        if polarized:
            self.text(x-28, y+16, "+", "small")
        self.pin(ref, p[0], x, y); self.pin(ref, p[1], x, y+65)

    def led(self, ref, x, y):
        self.line(x, y, x+25, y)
        self.parts.append(f'<polygon points="{x+25},{y-16} {x+25},{y+16} {x+55},{y}" class="sym"/>')
        self.line(x+55, y-17, x+55, y+17); self.line(x+55, y, x+90, y)
        for k in (0, 14):
            self.line(x+35+k, y-25, x+49+k, y-39)
            self.line(x+49+k, y-39, x+42+k, y-37)
            self.line(x+49+k, y-39, x+47+k, y-32)
        self.text(x+45, y+44, ref, "small", "middle")
        self.text(x+10, y-20, "A", "small"); self.text(x+73, y-20, "K", "small")
        self.pin(ref, "A", x, y); self.pin(ref, "K", x+90, y)

    def ic(self, ref, x, y, w, left, right, title=None):
        h = max(len(left), len(right))*42+65
        self.rect(x, y, w, h)
        self.text(x+w/2, y+27, title or ref, "small", "middle")
        for side, items in (("left", left), ("right", right)):
            for i, (pin, label) in enumerate(items):
                py = y+65+i*42
                px = x if side == "left" else x+w
                self.port(ref, pin, px, py, side)
                self.text(px+(10 if side == "left" else -10), py-7, str(pin)+" "+label, "small", "start" if side == "left" else "end")

    def save(self):
        return "\n".join(self.parts + ["</svg>\n"])


def comfort(d):
    s = Sheet(d, "01  Komfortlueftung / unabhaengige 5 V", "01", "Vier native 5-V-Luefter; keine Drehzahlsteuerung und keine Verbindung zur Effektdomaene.")
    s.ic("J10", 135, 195, 190, [], [(1, "+5 V"), (2, "GND")], "J10 / Quelle 5 V")
    s.resistor("F10", 440, 260)
    s.text(445, 287, "Sicherung", "small")
    s.wire([(325, 260), (440, 260)], "C5_RAW")
    s.switch("S10", 675, 260)
    s.wire([(520, 260), (675, 260)], "C5_FUSED")
    s.wire([(765, 260), (1310, 260)], "C5_FAN")
    s.text(945, 241, "C5_FAN", "net")
    s.text(675, 308, "Nur Komfort AUS", "small")
    for i in range(4):
        x = 135 + i*350
        ref = f"J{11+i}"
        s.ic(ref, x, 450, 190, [(1, "GND"), (2, "+5 V"), (3, "TACH offen"), (4, "PWM offen")], [], ref + " / " + ("Helm" if i<2 else "Torso"))
        s.text(x+95, 782, "Fertiger Luefter", "small", "middle")
        s.text(x+95, 815, "5 V / voller Lauf", "small", "middle")
    s.text(65, 932, "Pin 1 = GND, Pin 2 = Versorgung, 3/4 einzeln offen. Steckeransicht nach Hersteller pruefen.")
    s.text(65, 969, "F10 und Leitung erst nach Strommessung auslegen. Ein Stromausfall stoppt auch diese Luefter.")
    return s.save()


def power(d):
    s = Sheet(d, "02  Effektversorgung / manuelle Trennung", "02", "15-V-PD-Ausgang, lokale 5 V, Relais-Freigabe. Schaltkontakt ist ohne Spulenstrom offen.")
    s.ic("J20", 130, 170, 290, [], [("VOUT", "VOUT"), ("GND", "GND")], "J20 / DEV-15801")
    s.text(145, 347, "USB-C PD -> NVM 15 V", "small")
    s.text(145, 374, "Konfiguration / Messung offen", "small")
    s.resistor("F20", 595, 235); s.switch("S20", 865, 235)
    s.wire([(475, 235), (595, 235)], "E15_RAW")
    s.wire([(675, 235), (865, 235)], "E15_FUSED")
    s.wire([(955, 235), (1090, 235)], "E15_SW")
    s.text(1050, 210, "E15_SW", "net")
    s.text(665, 317, "S20 ist erreichbar; trennt auch die lokale Effektsteuerung.", "small")
    s.ic("U20", 190, 430, 285, [("VIN", "VIN"), ("GND", "GND")], [("VOUT", "5 V"), ("SHDN", "offen"), ("PG", "offen")], "U20 / D24V10F5")
    s.resistor("F21", 680, 495)
    s.wire([(530, 495), (680, 495)], "E5_RAW")
    s.wire([(760, 495), (900, 495)], "E5_CTRL")
    s.text(810, 523, "E5_CTRL", "net")
    s.capacitor("C20", 1150, 420, True)
    s.port("C20", "+", 1150, 420)
    s.port("C20", "-", 1150, 485)
    s.text(875, 565, "C20 nah an VIN; LC-Spitzen pruefen.", "small")
    s.text(65, 663, "K20 / G5LE-1A DC5: Kontakt auf Blatt 02, Spule und Treiber auf Blatt 05.")
    s.wire([(260, 765), (480, 765)], "E15_SW")
    s.text(260, 743, "E15_SW", "net")
    s.pin("K20", 1, 480, 765); s.line(480,765,540,765); s.dot(540,765)
    s.line(540,765,600,725); s.dot(625,765); s.line(625,765,690,765); s.pin("K20",3,690,765)
    s.wire([(690,765),(1020,765)], "E15_LED")
    s.text(765,743,"E15_LED -> U30...U35", "net")
    s.text(475,811,"1 COM", "small"); s.text(640,811,"3 NO", "small")
    s.text(65,905,"K20 schaltet Freigabe, niemals PWM. Kontaktlast und Einschaltstrom am LED-Verbund messen.")
    s.text(65,946,"F20/F21 bleiben TBD. 5-V-MCU, Puffer und Spule nutzen E_GND; C_GND bleibt getrennt.")
    s.text(65,982,"Relais klebt / MOSFET defekt: kein garantierter Fehler-AUS-Zustand. S20 bleibt direkte Trennung.", "small")
    return s.save()


def leds(d, prefix):
    sheet = "03" if prefix == "H" else "04"
    s = Sheet(d, sheet + "  RGB-Konstantstrom / " + ("Helmpaar" if prefix == "H" else "Duesenpaar"), sheet,
              "Drei getrennte 350-mA-Strange; links und rechts je Farbe in Reihe. Vier Stars insgesamt.")
    channels = [ch for ch in d["channels"] if ch["id"].startswith(prefix)]
    for row, ch in enumerate(channels):
        y = 170+row*238
        s.ic(ch["driver"], 245, y, 230, [(1,"+Vin"),(3,"DIM"),(4,"-Vin")], [(6,"+Vout"),(5,"-Vout")], ch["driver"] + " / LDD-350L")
        x1,x2 = 735,1090
        s.led(ch["leds"][0],x1,y+65); s.led(ch["leds"][1],x2,y+65)
        out,mid,ret = (f"LED_{ch['id']}_{suffix}" for suffix in ("OUT","MID","RET"))
        s.wire([(530,y+65),(x1,y+65)],out)
        s.wire([(x1+90,y+65),(x2,y+65)],mid)
        s.text(910,y+47,mid,"net","middle")
        s.wire([(x2+90,y+65),(1260,y+65),(1260,y+156),(585,y+156),(585,y+107),(530,y+107)],ret)
        s.text(810,y+181,ret + " nur zu Pin 5", "net")
    s.text(65,916,"J"+prefix+"L / J"+prefix+"R: 1 R+, 2 R-, 3 G+, 4 G-, 5 B+, 6 B-. Netzzuordnung: Connectors.md.")
    s.text(65,951,"Gleichnamige Netze sind verbunden. LED_*_MID verbindet nur die zwei gleichfarbigen Chips.")
    s.text(65,985,"Keine gemeinsame Anode/Kathode, kein LED-Rueckleiter an E_GND. Nur spannungslos stecken.","small")
    return s.save()


def control(d):
    s = Sheet(d,"05  3,3-V-PWM und Freigabe", "05", "Ein Pufferkanal im Detail; identische Schaltung sechsmal. Relaisfreigabe ist separat und statisch.")
    s.ic("B30",660,180,270,[(2,"A / 3,3 V"),(1,"/OE = 0"),(3,"GND")],[(5,"VCC"),(4,"Y / DIM")],"B30 / AHCT1G125")
    s.resistor("R30",365,245,True)
    s.wire([(365,245),(605,245)],"PWM_H_R"); s.dot(365,245)
    s.port("R30",1,365,245); s.port("R30",2,365,325)
    s.capacitor("C30",1150,325)
    s.port("C30",1,1150,325); s.port("C30",2,1150,390)
    s.text(60,428,"B30...B35: Eingang bei Reset hochohmig -> R30...R35 ziehen A LOW; /OE dauerhaft an E_GND.","small")
    s.text(60,454,"DIM nicht mit 10-kohm-Pulldown allein absichern: offener LDD-DIM-Eingang bedeutet EIN.","small")
    s.text(60,480,"Direkter 5-V-Pufferausgang; DIM-Strom/LOW-Pegel real messen. Kein Ioff-Nachweis fuer den Puffer.","small")
    s.text(65,539,"Relais-Freigabe / Gate LOW bei getrenntem MCU oder offener Temperaturkontaktkette", "body")
    s.ic("J21",225,590,285,[(1,"READY")],[(2,"TH_OUT")],"J21 / externe Oeffner")
    s.text(225,718,"Temperaturkontakte unbestimmt", "small")
    s.text(225,745,"Stecker offen = keine Freigabe", "small")
    s.resistor("R20",650,655)
    s.wire([(565,655),(650,655)],"READY_AFTER_TH")
    s.wire([(730,655),(865,655)],"RELAY_GATE")
    s.resistor("R21",790,720,True)
    s.wire([(790,655),(790,720)],"RELAY_GATE"); s.dot(790,655)
    s.port("R21",2,790,800)
    # N-MOSFET with gate and channel; body diode lies inside the selected part.
    s.line(865,655,900,655); s.line(900,625,900,690)
    s.line(915,615,915,645); s.line(915,650,915,665); s.line(915,670,915,700)
    s.line(915,615,960,615); s.line(960,615,960,580)
    s.line(915,700,960,700); s.line(960,700,960,755)
    s.pin("Q20",1,865,655); s.pin("Q20",3,960,580); s.pin("Q20",2,960,755)
    s.text(975,668,"Q20 / AO3400A", "small")
    s.text(878,605,"3 D", "small"); s.text(975,735,"2 S", "small"); s.text(860,642,"1 G", "small")
    s.port("Q20",2,960,755,"right")
    s.wire([(960,580),(960,560),(1190,560),(1190,610)],"COIL_LOW")
    # Relay coil pins 2 and 5, vertically oriented, complete symbol.
    s.rect(1180,645,26,95); s.line(1193,610,1193,645); s.line(1193,740,1193,790)
    s.pin("K20",5,1193,610); s.pin("K20",2,1193,790)
    s.wire([(1190,610),(1193,610)],"COIL_LOW")
    s.port("K20",2,1193,790,"right")
    s.text(1060,685,"K20", "small"); s.text(1040,710,"Spule 2/5", "small")
    # Flyback diode A at top, K at bottom; blocks while coil energized.
    s.wire([(1193,610),(1340,610),(1340,655)],"COIL_LOW"); s.dot(1193,610)
    s.line(1340,655,1340,670)
    s.parts.append('<polygon points="1326,670 1354,670 1340,695" class="sym"/>')
    s.line(1326,695,1354,695); s.line(1340,695,1340,715)
    s.pin("D20","A",1340,655); s.pin("D20","K",1340,715)
    s.wire([(1340,715),(1340,790),(1193,790)],"E5_CTRL"); s.dot(1193,790)
    s.text(1360,678,"D20", "small"); s.text(1360,706,"1N4007", "small")
    s.text(60,874,"J30: 1 E_GND, 2 READY, 3 H_R, 4 H_G, 5 H_B, 6 N_R, 7 N_G, 8 N_B. Nur 3,3-V-Signale.")
    s.text(60,914,"J22: 1 E5_CTRL, 2 E_GND. Controller braucht dokumentierten 5-V-Eingang und eigene 3,3-V-Regelung.","small")
    s.text(60,953,"Reset-AUS gilt stationaer bei hochohmigen GPIOs; Brownout, Kontaktprellen und Abschaltimpulse messen.","small")
    s.text(60,986,"Temperatursperre/Watchdog/MCU-Pinwahl noch nicht implementiert. Kein Sicherheitsrelais, kein Not-Halt.","small")
    return s.save()


def connector_table(d):
    lines = ["# Steckerbelegung electrical-r1", "", "Netze sind logische Kabelbaumbezeichnungen. Physische Gehaeuse/Kontakte,",
        "Steckseite und Kodierung bleiben auszulegen; diese Nummern sind keine",
        "universelle JST-, USB- oder RGB-Steckerbelegung. Gegenstecker passend",
        "verdrahten und Durchgang vor dem Einschalten messen.", "",
        "| Referenz | Anschluss | Netz | Bedeutung |", "| --- | --- | --- | --- |"]
    for c in d["components"]:
        if c["kind"] not in {"connector", "module_boundary"}:
            continue
        for pin, net in c["pins"].items():
            lines.append(f"| {c['ref']} | {pin} | {net or 'NC, einzeln offen'} | {c['value']} |")
    lines.extend(["", "Bei J11...J14 gilt die native Noctua-PWM-Belegung, bei den restlichen",
        "J-Steckern die hier definierte Projektbelegung. Kein Powerbank-Ausgang",
        "wird parallel mit einem anderen Ausgang verbunden.", ""])
    return "\n".join(lines)


def bom_table(d):
    rows = ["# Elektrische Bauteile electrical-r1", "", "Bauteilwerte sind Entwurfswerte. Unbekannte Sicherungen, Leitungen und",
        "Temperaturkontakte bleiben offen; es gibt keine fertige Bestellfreigabe.", "",
        "| Referenz | Wert / Teil | Status / Quelle |", "| --- | --- | --- |"]
    for c in d["components"]:
        if c["kind"] in {"connector", "led"}:
            continue
        link = f"[Hersteller]({SOURCES[c['source']]})" if c["source"] else "Projektentwurf"
        rows.append(f"| {c['ref']} | {c['value']} | {link} |")
    rows.extend(["", "Zusaetzlich: vier RGB-Stars mit sechs elektrisch getrennten Pads, vier",
        "echte Metallkuehlkoerper, passende Optik, kodierte Stecker/Zugentlastung,",
        "separate Komfortquelle und 5-V-Luefter. Die bestehende", "[Licht-Einkaufsliste](https://github.com/Huskynarr/HaloCosplay/blob/feat/huskynarr-entry-system/Materials/Mjolnir-Licht-Einkauf.md) bleibt die",
        "Mengen-/Budgetbasis; vorhandene Teile nicht nochmals addieren.", ""])
    return "\n".join(rows)


def outputs():
    d = design()
    validate(d)
    nets = {}
    for c in d["components"]:
        for pin, net in c["pins"].items():
            if net:
                nets.setdefault(net, []).append({"ref": c["ref"], "pin": pin})
    d["nets"] = dict(sorted(nets.items()))
    return {"Netlist.json": json.dumps(d, indent=2, ensure_ascii=True)+"\n",
        "01-Comfort.svg": comfort(d), "02-Effects-Power.svg": power(d),
        "03-Helmet-RGB.svg": leds(d,"H"), "04-Nozzle-RGB.svg": leds(d,"N"),
        "05-Control.svg": control(d), "Connectors.md": connector_table(d), "BOM.md": bom_table(d)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--check", action="store_true", help="Nur Topologie und Aktualitaet der Textdateien pruefen")
    p.add_argument("--out", type=Path, default=HERE, help="Ausgabeordner")
    args = p.parse_args()
    generated = outputs()
    if args.check:
        stale = [name for name, content in generated.items() if not (args.out/name).exists() or (args.out/name).read_text(encoding="utf-8") != content]
        if stale:
            p.exit(1, "Veraltet/fehlt: " + ", ".join(stale) + "\n")
        print("Topologie und 8 erzeugte Textdateien konsistent; keine Hardwareabnahme.")
    else:
        args.out.mkdir(parents=True, exist_ok=True)
        for name, content in generated.items():
            (args.out/name).write_text(content, encoding="utf-8")
        print("8 Textdateien erzeugt in " + str(args.out))


if __name__ == "__main__":
    main()
