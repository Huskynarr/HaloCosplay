# Firmware-Tests auf dem Host

`python3 Tests/Firmware/run.py` uebersetzt die echten Sketches
`Code/HelmetControl/HelmetMultiEffects.ino` und `Code/ArmorControl/MultiEffects.ino`
mit `g++` gegen nachgebildete Arduino-Header (`mock/`) und prueft ihr Verhalten:
I2C-Protokoll, Luefter-Failsafe, Taster, Handler-Alarm und Shield-Hit-Zaehlung.
Die Sketches bleiben dafuer unveraendert; die Zeit ist virtuell (`delay()` zaehlt
nur einen Zaehler hoch), deshalb laufen auch lange Effekte sofort durch.

Zusaetzlich prueft `exo_test.cpp` die hardwarefreie Logik des Eigenbau-Beinantriebs
(`Code/ExoControl/LegAssist/exo_core.h`): CAN-Rahmen, Momentengrenzen, Stoerungen
und das Verhalten bei einem nachgebildeten Gang. Der zugehoerige ESP32-Sketch
wird nur in der CI kompiliert, nicht auf dem Host ausgefuehrt.

## Was die Tests nicht belegen

- Keine Hardware: Pegel, Timing des NeoPixel-Protokolls, PWM-Frequenz, echte
  Tasterkontakte und Sensoren bleiben ungeprueft. Ein bestandener Lauf ist
  keine Hardwareabnahme.
- Der Host rechnet mit 32-Bit-`int` und 64-Bit-`unsigned long`, der AVR mit
  16 und 32 Bit. Ueberlaeufe (zum Beispiel `millis()` nach 49 Tagen oder
  16-Bit-Produkte) zeigt nur der AVR selbst.
- Interrupt-Verhalten (I2C-Empfang mitten in `loop()`) wird nicht nachgebildet;
  ein Kommando trifft im Test immer zwischen zwei Durchlaeufen ein.

## Neue Tests

Eine Suite besteht aus Sketch und Testdatei, eingetragen in `SUITES` in `run.py`.
Tests fuer hardwarefreie Header mit eigenem `main()` stehen in `HEADER_SUITES`.
Die Testdatei sieht alle globalen Variablen und Funktionen des Sketches.
`mock_input[pin]` setzt Eingaenge, `Wire.mock_receive({...})` liefert eine
I2C-Uebertragung, `mock_on_delay` aendert Eingaenge waehrend eines blockierenden
Effekts.
