# Elektronik: Batterieloesungen und Laufzeitplanung

> **Level:** [A] Anfaenger | [F] Fortgeschritten | [P] Profi  ·  **Varianten:** alle
> **Voraussetzungen:** Strombudget gerechnet (`Documentation/Guides/Elektronik-Strombudget.md`); fuer Option C (LiPo) Wissen zu BMS/Schutzschaltung (Batterie-Management-System, schuetzt vor Ueberladung/Tiefentladung).

Wie man genug Strom fuer einen ganzen Convention-Tag mitbringt.

## Laufzeitberechnung

### Gesamtstromverbrauch (V2 typisch)

| Komponente | Strom (A) |
| --- | --- |
| Pi Zero 2 W (optimiert) | 0.30 |
| Transparentes OLED | 0.04 |
| 2x 40mm Luefter | 0.20 |
| 60 WS2812B LEDs (50% gruen) | 0.60 |
| Arduino Nano | 0.03 |
| Audio-Verstaerker (intermittierend) | 0.10 |
| **Gesamt** | **~1.27 A** |

### Formel

```
Laufzeit (h) = Kapazitaet (mAh) / Strom (mA) x Effizienz (0.85)
```

### Beispielrechnungen

| Batterie-Setup | Kapazitaet | Laufzeit bei 1.27 A |
| --- | --- | --- |
| PiSugar 3 Plus allein | 5.000 mAh | ~3.3 h |
| 1x 10.000 mAh Powerbank | 10.000 mAh | ~6.7 h |
| 2x 10.000 mAh Powerbank | 20.000 mAh | ~13.4 h |
| PiSugar + 10.000 mAh Powerbank | 15.000 mAh | ~10 h |

## Batterie-Strategien fuer 8+ Stunden

### Option A: Dual-Powerbank (Empfohlen, sicherste Variante)

- **2x 10.000 mAh schlanke USB-Powerbanks** im Backpack
- Eine fuer Pi/HUD/Luefter, eine fuer LEDs/Audio
- Sicherste Loesung (eingebaute Schutzschaltungen)
- Gesamt ca. 20-40 EUR

### Option B: PiSugar + externe Powerbank

- **PiSugar 3 Plus** fuer Pi (UPS-Funktion, sauberer Neustart bei Stromausfall)
- **10.000 mAh Powerbank** fuer LEDs/Luefter/Audio
- Vorteil: Pi hat unterbrechungsfreie Versorgung

### Option C: 3S LiPo + Step-Down

- **3S LiPo 5.000 mAh (11.1V)** + **5V 5A Step-Down Regler** (z.B. Pololu D24V50F5)
- Einzelner Akku, leichter, kompakter
- Nachteil: Ladeelektronik und BMS erforderlich, mehr Fachwissen noetig
- **Nur mit Schutzschaltung/BMS!**

## Spannungsregler

- **USB-Powerbanks:** eingebaute 5V-Regelung, einfach nutzen
- **Roher LiPo:** Pololu 5V 5A Step-Down (D24V50F5) oder UBEC 5V/5A (~10-15 EUR)
- Sicherung nahe der Batterie: 2-3 A fuer Logik, 5-10 A fuer LED-Power

## Pi Zero 2 W Stromsparen

In `/boot/config.txt`:
```
# HDMI deaktivieren (spart ~25 mA)
hdmi_blanking=2

# Bluetooth deaktivieren
dtoverlay=disable-bt

# GPU-Speicher reduzieren
gpu_mem=16
```

Unnoetige Dienste deaktivieren:
```bash
sudo systemctl disable bluetooth
sudo systemctl disable avahi-daemon
sudo systemctl disable triggerhappy
```

## Sicherheitsregeln

- **Akkus NIE im Kostuem laden** — immer extern
- USB-Powerbanks sind am sichersten (eingebaute Schutzkreise)
- LiPo nur mit BMS/Schutzschaltung
- Batterien im Backpack/Torso montieren (Gewichtsverteilung)
- Not-Aus oder Schnelltrennung einplanen
- Strom vor Einbau mit Multimeter messen
- 20-30% Reserve fuer Spitzenlast einplanen

## Einkaufsliste Batterie/Strom

| Komponente | Preis ca. |
| --- | --- |
| PiSugar 3 Plus (5000 mAh) | 40-50 EUR |
| 10.000 mAh USB Powerbank (schlank) | 15-25 EUR |
| Pololu 5V 5A Step-Down (optional) | 10-15 EUR |
| UBEC 5V/5A (Alternative) | 8-12 EUR |
| Sicherungen (2-3A, 5-10A) | 3-5 EUR |
