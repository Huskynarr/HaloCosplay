#!/usr/bin/env python3
"""Sprachsteuerung + Helmfunk fuer den Spartan-Helm (Raspberry Pi 5).

Push-to-Talk-Taster halten, Befehl sprechen, loslassen. Erkannt wird offline
mit Vosk (deutsches Modell). Die Befehle gehen an die VORHANDENEN Module, ohne
eine neue Abhaengigkeit zu schaffen (Grundprinzip aus V3-Systemarchitektur.md):

  Helm-Arduino (HelmetMultiEffects.ino)  I2C 0x08: Effekt, Helligkeit, Farbe, Luefter
  Schubduesen-Arduino                    Optokoppler parallel zum Boost-Taster
  Ruestungs-Arduino (MultiEffects.ino)   Optokoppler parallel zum Effekt-Taster
  vision_bridge.py                       liest hud_state.json (Scanner-Ansagen)

Faellt dieses Programm (oder der ganze Pi) aus, laufen alle Module weiter und
ihre eigenen Taster funktionieren wie bisher.

Optional (Elektronik-Audio.md, Option C): Solange PTT NICHT gedrueckt ist, geht
die Stimme mit Funk-Effekt an einen I2S-Verstaerker mit Lautsprecher an der
Brust. Nicht zusammen mit ar_passthrough.py auf demselben Pi betreiben.

Rueckmeldungen (Pieptoene, Sprachausgabe) kommen ueber die USB-Soundkarte auf
die inneren Lautsprecher. Diese spielen nie das Mikrofonsignal ab - deshalb
entsteht trotz Mikrofon im Helm keine Rueckkopplung.

Hardwarefreier Test:    python3 voice_control.py --selftest
Tippen statt sprechen:  python3 voice_control.py --keyboard
Anleitung:              Documentation/Guides/Elektronik-Sprachsteuerung.md
"""

import argparse
import json
import math
import os
import queue
import subprocess
import sys
import tempfile
import threading
import time
import wave

try:
    import numpy as np
except ImportError:          # nur fuer Audio noetig, nicht fuer --selftest
    np = None

import hud_state

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULTS = {
    "i2c_bus": 1,
    "helmet_addr": "0x08",
    "ptt_gpio": 17,               # Taster gegen GND
    "boost_gpio": 27,             # -> Optokoppler -> Boost-Taster Schubduesen
    "armor_gpio": 22,             # -> Optokoppler -> Effekt-Taster Ruestung
    "pulse_ms": 200,              # "Tastendruck"-Dauer
    "mic_device": "USB",          # Teil des Geraetenamens (python3 -m sounddevice)
    "outer_device": "MAX98357",   # I2S-Verstaerker Brust; "" = kein Helmfunk
    "inner_alsa": "plughw:CARD=Device,DEV=0",   # USB-Soundkarte, siehe aplay -L
    "voice_gate": 0.010,          # Rauschsperre: darunter bleibt der Lautsprecher stumm
    "voice_drive": 6.0,           # Funk-Saettigung
    "voice_volume": 0.8,
    "vosk_model": "models/vosk-model-small-de-0.15",
    "piper_voice": "voices/de_DE-kerstin-low.onnx",   # optional, sonst espeak-ng
    "state_path": "hud_state.json",
    "announce": {"person": "Person", "dog": "Hund", "cat": "Katze"},
    "announce_pause_s": 12,
    "hydration_interval_min": 45,
}

# Helm-Arduino-Protokoll (siehe HelmetMultiEffects.ino / helmet_control.py)
CMD_BRIGHTNESS = 0x01
CMD_FAN = 0x02
CMD_EFFECT = 0x03
CMD_COLOR = 0x04

# Reihenfolge MUSS zu HelmetMultiEffects.ino passen
EFFECTS = {"statisch": 0, "atmen": 1, "herzschlag": 2, "lauflicht": 3, "flackern": 4}
DEFAULT_EFFECT = EFFECTS["atmen"]
COLORS = {
    "gold": (255, 180, 20), "rot": (255, 0, 0), "gruen": (0, 255, 0),
    "blau": (0, 60, 255), "gelb": (255, 220, 0), "orange": (255, 90, 0),
    "weiss": (255, 255, 255), "lila": (150, 0, 255), "tuerkis": (0, 255, 170),
}
WORDS = ["visier", "ruestung", "licht", "weiter", "nebel", "boost", "schub", "show",
         "alarm", "stopp", "ruhe", "heller", "dunkler", "aus", "an", "luefter", "voll",
         "leise", "normal", "staerker", "schwaecher", "scanner", "stimme", "status",
         "wasser", "trinken", "spaeter"]

# Vosk liefert echte Umlaute; der Code arbeitet ASCII (Repo-Konvention).
UMLAUTS = {0xe4: "ae", 0xf6: "oe", 0xfc: "ue", 0xdf: "ss", 0xc4: "Ae", 0xd6: "Oe", 0xdc: "Ue"}
SPOKEN = {"ruestung": "r\u00fcstung", "luefter": "l\u00fcfter", "staerker": "st\u00e4rker",
          "schwaecher": "schw\u00e4cher", "gruen": "gr\u00fcn", "weiss": "wei\u00df",
          "tuerkis": "t\u00fcrkis", "spaeter": "sp\u00e4ter"}
VOCAB = sorted({SPOKEN.get(w, w) for w in WORDS + list(EFFECTS) + list(COLORS)})


def asciify(text):
    return text.translate(UMLAUTS)


def log(*args):
    print(time.strftime("%H:%M:%S"), *args, flush=True)


def load_config(path):
    config = json.loads(json.dumps(DEFAULTS))
    if path and os.path.exists(path):
        with open(path, "r", encoding="utf-8") as handle:
            config.update(json.load(handle))
    for key in ("vosk_model", "piper_voice", "state_path"):
        if config[key] and not os.path.isabs(config[key]):
            config[key] = os.path.join(BASE_DIR, config[key])
    if isinstance(config["helmet_addr"], str):
        config["helmet_addr"] = int(config["helmet_addr"], 0)
    return config


def cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r", encoding="utf-8") as handle:
            return int(handle.read()) / 1000.0
    except (OSError, ValueError):
        return 0.0


# ============================== Befehlslogik ==============================

class Commander:
    """Erkannter Text -> Aktionen. Rein logisch, ohne Hardware (testbar).

    `out` stellt bereit: helmet(cmd, value), pulse(name), say(text), beep(kind),
    show(), set_scanner(on), set_voice(on), status().
    """

    def __init__(self, out):
        self.out = out
        self.brightness = 160
        self.fan = 180
        self.color = COLORS["gold"]
        self.effect = DEFAULT_EFFECT

    def set_color(self, rgb):
        self.color = rgb
        self.out.helmet(CMD_COLOR, list(rgb))

    def set_effect(self, effect):
        self.effect = effect
        self.out.helmet(CMD_EFFECT, effect)

    def handle(self, text):
        words = asciify(text.lower()).split()
        w = set(words)
        out = self.out
        log("Befehl:", repr(" ".join(words)))
        if not words:
            out.beep("err")
            return False

        if w & {"nebel", "boost", "schub"}:
            out.pulse("boost")
            out.beep("ok")
        elif "show" in w:
            out.show()
        elif "alarm" in w:
            self.set_color(COLORS["rot"])
            self.set_effect(EFFECTS["herzschlag"])
            out.say("Alarm.")
        elif w & {"stopp", "ruhe"}:
            self.set_color(COLORS["gold"])
            self.set_effect(DEFAULT_EFFECT)
            out.say("Normalbetrieb.")
        elif "luefter" in w:
            self._fan(w)
        elif "scanner" in w:
            out.set_scanner("aus" not in w)
        elif "stimme" in w:
            out.set_voice("aus" not in w)
        elif "status" in w:
            out.status()
        elif w & {"wasser", "trinken", "spaeter"}:
            if "aus" in w:
                out.hydration("off")
            elif "an" in w:
                out.hydration("on")
            elif "spaeter" in w:
                out.hydration("snooze")
            else:
                out.hydration("done")
            out.beep("ok")
        elif w & {"ruestung", "licht"}:
            out.pulse("armor")          # naechster Effekt am Ruestungs-Arduino
            out.beep("ok")
        else:
            return self._visor(words, w)
        return True

    def _fan(self, w):
        if "voll" in w:
            self.fan = 255
        elif "leise" in w:
            self.fan = 110
        elif "staerker" in w:
            self.fan = min(255, self.fan + 50)
        elif "schwaecher" in w:
            self.fan = max(80, self.fan - 50)
        elif "aus" in w:
            self.fan = 0
        else:
            self.fan = 180
        self.out.helmet(CMD_FAN, self.fan)
        if self.fan == 0:
            self.out.say("Luefter aus. Achtung, Hitzestau.")
        else:
            self.out.say(f"Luefter {round(self.fan * 100 / 255)} Prozent.")

    def _visor(self, words, w):
        color = next((COLORS[x] for x in words if x in COLORS), None)
        effect = next((EFFECTS[x] for x in words if x in EFFECTS), None)
        handled = False
        if color:
            self.set_color(color)
            handled = True
        if effect is not None:
            self.set_effect(effect)
            handled = True
        if w & {"heller", "dunkler"}:
            step = 60 if "heller" in w else -60
            self.brightness = max(20, min(255, self.brightness + step))
            self.out.helmet(CMD_BRIGHTNESS, self.brightness)
            handled = True
        elif "aus" in w:
            self.out.helmet(CMD_BRIGHTNESS, 0)
            handled = True
        elif "an" in w:
            self.out.helmet(CMD_BRIGHTNESS, self.brightness)
            handled = True
        self.out.beep("ok" if handled else "err")
        return handled


# ============================== Hydration ==============================

class HydrationTimer:
    """Erinnert alle N Minuten ans Trinken: Ansage innen + HUD-Banner.

    Das HUD-Flag (hydration_due) geht ueber hud_state.merge() in die
    hud_state.json - hud_display.py zeigt solange ein blinkendes Banner.
    Faellt der Pi aus, faellt nur die Erinnerung aus - kein Sicherheitsmodul.
    """

    def __init__(self, cfg, out, interval_min=None):
        # interval_min nur fuer den Selftest; Produktion floort auf 60 s
        if interval_min is None:
            self.interval = max(60.0, float(cfg.get("hydration_interval_min", 45)) * 60.0)
        else:
            self.interval = max(0.0, float(interval_min)) * 60.0
        self.snooze_s = 0.0
        self.state_path = cfg["state_path"]
        self.out = out
        self.enabled = True
        self.wake = threading.Event()
        self.stop = threading.Event()
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        while not self.stop.is_set():
            wait = self.snooze_s or self.interval
            self.snooze_s = 0.0
            self.wake.clear()
            if self.stop.wait(wait):
                return
            if self.wake.is_set() or not self.enabled:
                continue        # neu gestartet (getrunken/snooze) oder deaktiviert
            hud_state.merge(self.state_path, {"hydration_due": True})
            self.out.say("Hydration erforderlich.")
            self.out.beep("ok")

    def done(self):
        """Getrunken: Flag weg, Timer voll neu starten."""
        hud_state.merge(self.state_path, remove=("hydration_due",))
        self.wake.set()

    def snooze(self, minutes=10):
        """Flag weg, naechste Erinnerung erst in `minutes` Minuten."""
        self.snooze_s = minutes * 60.0
        hud_state.merge(self.state_path, remove=("hydration_due",))
        self.wake.set()

    def set_enabled(self, on):
        self.enabled = bool(on)
        hud_state.merge(self.state_path, remove=("hydration_due",))
        self.wake.set()


# ============================== Hardware ==============================

class InnerAudio:
    """Pieptoene + Sprachausgabe auf den inneren Lautsprechern (eine Warteschlange)."""

    def __init__(self, cfg):
        self.alsa = cfg["inner_alsa"]
        self.q = queue.Queue()
        self.voice = None
        if os.path.exists(cfg["piper_voice"]):
            try:
                from piper import PiperVoice
                self.voice = PiperVoice.load(cfg["piper_voice"])
            except Exception as exc:
                log("Piper nicht nutzbar, nehme espeak-ng:", exc)
        self.tones = {"on": self._tone(1400, 0.07), "off": self._tone(900, 0.07),
                      "ok": self._tone(1800, 0.05), "err": self._tone(400, 0.2)}
        threading.Thread(target=self._loop, daemon=True).start()

    @staticmethod
    def _tone(freq, dur, rate=48000):
        frames = bytearray()
        n = int(rate * dur)
        for i in range(n):
            env = min(1.0, i / 400.0, (n - i) / 400.0)
            sample = int(0.35 * 32767 * env * math.sin(2 * math.pi * freq * i / rate))
            frames += sample.to_bytes(2, "little", signed=True)
        path = os.path.join(tempfile.gettempdir(), f"voice_tone_{freq}.wav")
        with wave.open(path, "wb") as handle:
            handle.setnchannels(1)
            handle.setsampwidth(2)
            handle.setframerate(rate)
            handle.writeframes(bytes(frames))
        return path

    def beep(self, kind):
        self.q.put(("wav", self.tones[kind]))

    def say(self, text):
        self.q.put(("say", text))

    def _play(self, path):
        subprocess.run(["aplay", "-q", "-D", self.alsa, path], check=False)

    def _loop(self):
        tts_path = os.path.join(tempfile.gettempdir(), "voice_tts.wav")
        while True:
            kind, value = self.q.get()
            try:
                if kind == "wav":
                    self._play(value)
                elif self.voice:
                    with wave.open(tts_path, "wb") as handle:
                        if hasattr(self.voice, "synthesize_wav"):
                            self.voice.synthesize_wav(value, handle)
                        else:                       # aeltere Piper-Versionen
                            self.voice.synthesize(value, handle)
                    self._play(tts_path)
                else:
                    tts = subprocess.Popen(["espeak-ng", "-v", "de+f3", "-s", "165", "--stdout", value],
                                           stdout=subprocess.PIPE)
                    subprocess.run(["aplay", "-q", "-D", self.alsa], stdin=tts.stdout, check=False)
                    tts.wait()
            except Exception as exc:
                log("Audio innen:", exc)


class RadioVoice:
    """Helmfunk: Bandpass 300-3400 Hz + Saettigung + Rauschsperre mit weichen Uebergaengen."""

    def __init__(self, rate, block, cfg):
        from scipy.signal import butter, sosfilt
        self.sosfilt = sosfilt
        self.sos = butter(4, (300, 3400), btype="bandpass", fs=rate, output="sos")
        self.zi = np.zeros((self.sos.shape[0], 2))
        self.gate, self.drive, self.volume = cfg["voice_gate"], cfg["voice_drive"], cfg["voice_volume"]
        self.gain, self.hold = 0.0, 0
        self.hold_blocks = max(1, int(0.25 * rate / block))   # 250 ms Nachlauf
        self.rng = np.random.default_rng()

    def process(self, x):
        if float(np.sqrt(np.mean(x * x))) > self.gate:
            self.hold = self.hold_blocks
        elif self.hold > 0:
            self.hold -= 1
        target = 1.0 if self.hold > 0 else 0.0
        new = self.gain + (target - self.gain) * (0.6 if target > self.gain else 0.15)
        ramp = np.linspace(self.gain, new, len(x))
        self.gain = new
        y, self.zi = self.sosfilt(self.sos, x, zi=self.zi)
        y = np.tanh(y * self.drive) + self.rng.uniform(-0.004, 0.004, len(x))
        return (y * ramp * self.volume).astype(np.float32)


class AudioEngine:
    """Mikrofon -> (PTT gedrueckt) Vosk  |  (sonst) Helmfunk an der Brust."""

    def __init__(self, cfg, on_text):
        import sounddevice as sd
        self.sd = sd
        self.on_text = on_text
        self.ptt = False
        self.voice_on = True
        self.recognizer_ok = False
        self.cmd_q = queue.Queue()
        self.out_q = queue.Queue(maxsize=6)

        mic = self._find(cfg["mic_device"], "max_input_channels")
        outer, self.out_ch = None, 0
        if cfg["outer_device"]:
            try:
                outer = self._find(cfg["outer_device"], "max_output_channels")
                self.out_ch = min(2, sd.query_devices(outer)["max_output_channels"])
            except RuntimeError as exc:
                log(exc, "- Helmfunk deaktiviert")
        self.rate = self._common_rate(mic, outer)
        self.block = self.rate // 100                 # 10 ms -> geringe Latenz
        self.fx = RadioVoice(self.rate, self.block, cfg) if outer is not None else None

        self.streams = [sd.InputStream(device=mic, samplerate=self.rate, blocksize=self.block,
                                       channels=1, dtype="float32", callback=self._in_cb)]
        if outer is not None:
            self.streams.append(sd.OutputStream(device=outer, samplerate=self.rate, blocksize=self.block,
                                                channels=self.out_ch, dtype="float32", callback=self._out_cb))
        for stream in self.streams:
            stream.start()
        log(f"Audio laeuft ({self.rate} Hz, Helmfunk {'an' if self.fx else 'aus'})")
        threading.Thread(target=self._vosk_loop, args=(cfg["vosk_model"],), daemon=True).start()

    def _find(self, name, key):
        for i, dev in enumerate(self.sd.query_devices()):
            if name.lower() in dev["name"].lower() and dev[key] > 0:
                return i
        raise RuntimeError(f"Audiogeraet '{name}' nicht gefunden (python3 -m sounddevice)")

    def _common_rate(self, mic, outer):
        for rate in (48000, 44100):
            try:
                self.sd.check_input_settings(device=mic, samplerate=rate, channels=1, dtype="float32")
                if outer is not None:
                    self.sd.check_output_settings(device=outer, samplerate=rate,
                                                  channels=self.out_ch, dtype="float32")
                return rate
            except Exception:
                continue
        raise RuntimeError("Keine gemeinsame Abtastrate fuer Mikrofon und Verstaerker")

    # Echtzeit-Callbacks: nur rechnen, nie blockieren
    def _in_cb(self, indata, frames, t, status):
        x = indata[:, 0].copy()
        if self.ptt:
            self.cmd_q.put((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
        if not self.out_ch:
            return
        y = self.fx.process(x) if (self.voice_on and not self.ptt) else np.zeros_like(x)
        try:
            self.out_q.put_nowait(y)
        except queue.Full:                  # Latenz begrenzen: aeltesten Block verwerfen
            try:
                self.out_q.get_nowait()
            except queue.Empty:
                pass
            self.out_q.put_nowait(y)

    def _out_cb(self, outdata, frames, t, status):
        try:
            y = self.out_q.get_nowait()
        except queue.Empty:
            y = None
        if y is None or len(y) != frames:
            outdata.fill(0)
        else:
            outdata[:] = y[:, None]

    def ptt_down(self):
        self.ptt = True

    def ptt_up(self):
        self.ptt = False
        self.cmd_q.put(None)

    def _vosk_loop(self, model_path):
        if not os.path.isdir(model_path):
            log("Vosk-Modell fehlt:", model_path)
            return
        try:
            from vosk import KaldiRecognizer, Model, SetLogLevel
            SetLogLevel(-1)
            grammar = json.dumps([" ".join(VOCAB), "[unk]"])
            rec = KaldiRecognizer(Model(model_path), self.rate, grammar)
        except Exception as exc:
            log("Vosk-Fehler:", exc)
            return
        self.recognizer_ok = True
        log("Spracherkennung bereit")
        parts = []
        while True:
            item = self.cmd_q.get()
            if item is None:                 # Taster losgelassen -> auswerten
                parts.append(json.loads(rec.FinalResult()).get("text", ""))
                text = " ".join(parts).replace("[unk]", " ")
                parts = []
                rec.Reset()
                self.on_text(" ".join(text.split()))
            elif rec.AcceptWaveform(item):
                parts.append(json.loads(rec.Result()).get("text", ""))


class Helmet:
    """Verbindet Commander mit der echten Hardware. Jeder Teil darf fehlen."""

    def __init__(self, cfg):
        self.cfg = cfg
        self.scanner = False
        self.helmet_ok = None
        self.last_announce = {}
        self.inner = self._try("Innen-Audio", lambda: InnerAudio(cfg))
        self.bus = self._try("I2C", self._open_bus)
        self.outputs = {}
        self.audio = None
        self.commander = Commander(self)
        self.hydration = self._try("Hydration-Timer", lambda: HydrationTimer(cfg, self))
        self._setup_gpio()
        threading.Thread(target=self._scanner_loop, daemon=True).start()

    @staticmethod
    def _try(name, factory):
        try:
            return factory()
        except Exception as exc:
            log(f"{name} nicht verfuegbar:", exc)
            return None

    def _open_bus(self):
        from smbus2 import SMBus
        return SMBus(self.cfg["i2c_bus"])

    def _setup_gpio(self):
        try:
            from gpiozero import Button, DigitalOutputDevice
        except ImportError as exc:
            log("gpiozero fehlt - kein PTT/Optokoppler:", exc)
            return
        for name in ("boost", "armor"):
            pin = self.cfg.get(f"{name}_gpio")
            if pin is not None:
                self.outputs[name] = self._try(f"GPIO {name}", lambda p=pin: DigitalOutputDevice(p))
        ptt = self._try("PTT-Taster", lambda: Button(self.cfg["ptt_gpio"], pull_up=True, bounce_time=0.03))
        if ptt:
            ptt.when_pressed = self._ptt_down
            ptt.when_released = self._ptt_up
            self.ptt_button = ptt

    def start_audio(self):
        if np is None:
            log("numpy fehlt - keine Spracherkennung (pip install -r requirements-voice.txt)")
            return
        self.audio = self._try("Audio", lambda: AudioEngine(self.cfg, self.commander.handle))

    # --- Ausgaben fuer den Commander ---
    def helmet(self, cmd, value):
        if self.bus is None:
            return
        values = value if isinstance(value, list) else [value]
        for _ in range(3):
            try:
                self.bus.write_i2c_block_data(self.cfg["helmet_addr"], cmd, [v & 0xFF for v in values])
                self.helmet_ok = True
                return
            except OSError:
                time.sleep(0.05)
        self.helmet_ok = False
        log("Helm-Arduino antwortet nicht")

    def pulse(self, name):
        dev = self.outputs.get(name)
        if dev:
            dev.blink(on_time=self.cfg["pulse_ms"] / 1000.0, off_time=0.05, n=1, background=True)
        else:
            log(f"Ausgang '{name}' nicht eingerichtet")

    def say(self, text):
        log(">>", text)
        if self.inner:
            self.inner.say(text)

    def beep(self, kind):
        if self.inner:
            self.inner.beep(kind)

    def set_voice(self, on):
        if self.audio:
            self.audio.voice_on = on
        self.say("Helmfunk an." if on else "Helmfunk aus.")

    def set_scanner(self, on):
        self.scanner = on
        self.commander.set_effect(EFFECTS["lauflicht"] if on else DEFAULT_EFFECT)
        self.say("Scanner aktiv." if on else "Scanner aus.")

    def hydration(self, action):
        if self.hydration is None:
            self.say("Trink-Erinnerung nicht aktiv.")
            return
        if action == "done":
            self.hydration.done()
            self.say("Hydration protokolliert.")
        elif action == "snooze":
            self.hydration.snooze(10)
            self.say("Erinnerung in 10 Minuten.")
        elif action == "off":
            self.hydration.set_enabled(False)
            self.say("Trink-Erinnerung aus.")
        elif action == "on":
            self.hydration.set_enabled(True)
            self.say("Trink-Erinnerung an.")

    def status(self):
        state = hud_state.load(self.cfg["state_path"])
        cam = "aktiv" if time.time() - float(state.get("vision_ts") or 0) < 3 else "aus"
        helm = {True: "verbunden", False: "getrennt", None: "unbekannt"}[self.helmet_ok]
        self.say(f"Temperatur {cpu_temp():.0f} Grad. Helm {helm}. Kamera {cam}.")

    def show(self):
        def run():
            previous = self.commander.effect
            self.say("Showtime.")
            self.commander.set_effect(EFFECTS["lauflicht"])
            self.pulse("boost")
            time.sleep(6.0)
            self.commander.set_effect(previous)
        threading.Thread(target=run, daemon=True).start()

    # --- PTT ---
    def _ptt_down(self):
        if self.audio:
            self.audio.ptt_down()
        self.beep("on")

    def _ptt_up(self):
        if self.audio:
            self.audio.ptt_up()
            if not self.audio.recognizer_ok:
                self.say("Spracherkennung nicht verfuegbar.")
        self.beep("off")

    # --- Scanner: Ansagen aus vision_bridge.py ---
    def _scanner_loop(self):
        pause = float(self.cfg["announce_pause_s"])
        while True:
            time.sleep(0.5)
            if not self.scanner:
                continue
            state = hud_state.load(self.cfg["state_path"])
            if time.time() - float(state.get("vision_ts") or 0) > 2:
                continue
            now = time.time()
            for contact in state.get("vision_contacts") or []:
                label = contact.get("label") if isinstance(contact, dict) else None
                name = self.cfg["announce"].get(label)
                if not name or now - self.last_announce.get(label, 0) < pause:
                    continue
                self.last_announce[label] = now
                bearing = float(contact.get("bearing") or 0)
                side = "links" if bearing < -10 else "rechts" if bearing > 10 else "voraus"
                self.say(f"{name} {side}.")


# ============================== Selftest / Main ==============================

class Recorder:
    """Ersatz-Hardware fuer --selftest: protokolliert nur."""

    def __init__(self):
        self.calls = []

    def __getattr__(self, name):
        def record(*args):
            self.calls.append((name,) + args)
        return record


def test_hydration_timer():
    """Timer mit verkuerztem Intervall: Ansage + Flag, done() raeumt auf."""
    state = os.path.join(tempfile.gettempdir(), "hydration_selftest.json")
    if os.path.exists(state):
        os.remove(state)
    rec = Recorder()
    timer = HydrationTimer({"state_path": state}, rec, interval_min=0.01)  # 0,6 s
    time.sleep(0.9)
    ok_announce = ("say", "Hydration erforderlich.") in rec.calls
    ok_flag = hud_state.load(state).get("hydration_due") is True
    timer.done()
    ok_cleared = "hydration_due" not in hud_state.load(state)
    timer.stop.set()
    failed = sum(not x for x in (ok_announce, ok_flag, ok_cleared))
    print(f"  [{'ok' if failed == 0 else 'FEHLER'}] Hydration-Timer: "
          f"Ansage={ok_announce} Flag={ok_flag} done()={ok_cleared}")
    return failed


def run_selftest():
    rec = Recorder()
    cmd = Commander(rec)
    cases = [
        ("visier rot", ("helmet", CMD_COLOR, [255, 0, 0])),
        ("visier herzschlag", ("helmet", CMD_EFFECT, 2)),
        ("visier heller", ("helmet", CMD_BRIGHTNESS, 220)),
        ("nebel", ("pulse", "boost")),
        ("r\u00fcstung weiter", ("pulse", "armor")),
        ("l\u00fcfter voll", ("helmet", CMD_FAN, 255)),
        ("scanner an", ("set_scanner", True)),
        ("stimme aus", ("set_voice", False)),
        ("alarm", ("helmet", CMD_EFFECT, 2)),
        ("stopp", ("helmet", CMD_COLOR, list(COLORS["gold"]))),
        ("wasser", ("hydration", "done")),
        ("spaeter", ("hydration", "snooze")),
        ("trinken aus", ("hydration", "off")),
        ("trinken an", ("hydration", "on")),
        ("blablub", ("beep", "err")),
    ]
    failed = 0
    for text, expected in cases:
        rec.calls.clear()
        cmd.handle(text)
        ok = expected in rec.calls
        failed += not ok
        print(f"  [{'ok' if ok else 'FEHLER'}] {asciify(text):<18} -> {rec.calls}")
    failed += test_hydration_timer()
    missing = [w for w in WORDS if SPOKEN.get(w, w) not in VOCAB]
    if missing or failed:
        sys.exit(f"Selftest fehlgeschlagen ({failed} Faelle, fehlende Woerter: {missing})")
    print(f"\nSelftest ok - Vokabular: {len(VOCAB)} Woerter")


def main():
    parser = argparse.ArgumentParser(description="Sprachsteuerung + Helmfunk (Pi 5)")
    parser.add_argument("--config", default=os.path.join(BASE_DIR, "voice_config.json"),
                        help="Konfiguration (Standard: voice_config.json)")
    parser.add_argument("--keyboard", action="store_true", help="Befehle tippen statt sprechen")
    parser.add_argument("--selftest", action="store_true", help="Befehlslogik ohne Hardware pruefen")
    args = parser.parse_args()
    if args.selftest:
        run_selftest()
        return

    cfg = load_config(args.config)
    helmet = Helmet(cfg)
    if args.keyboard:
        print("Befehle eintippen (z.B. 'visier rot', 'nebel', 'scanner an'), Ctrl+D beendet:")
        for line in sys.stdin:
            helmet.commander.handle(line.strip())
        return
    helmet.start_audio()
    helmet.say("Sprachsteuerung bereit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log("beendet")


if __name__ == "__main__":
    main()
