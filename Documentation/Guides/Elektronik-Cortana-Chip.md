# Elektronik: Cortana-Chip als kontaktloses Daten-Dock

> **Level:** [P] Profi | **Varianten:** V2/V3 | **Status:** KONZEPT, kein
> funktionierender Aufbau. Alle Bauteile sind Einzelnachweise; keine
> Passfreigabe, keine Beschaffung, keine gepruefte Integration.

Das Modul macht aus dem ikonischen Cortana-Chip ein echtes Bauteil: Ein
3D-gedruckter Chip am Kostuem koppelt kontaktlos an ein externes Display
(Holo-Box oder Smartphone) und zeigt dort Charakter-Status, Telemetrie und
gespeicherte Daten. Zwei Chips mit unterschiedlichen IDs koennen unterschiedliche
Charaktere anzeigen (z. B. Cortana und Husky).

## 1. Drei Bausteine

| Baustein | Kandidat | Funktion | Status |
| --- | --- | --- | --- |
| 3D-Druck | [MakerWorld 1482318](https://makerworld.com/models/1482318) | Cortana-Chip-Gehaeuse | Modell existiert, Druckdaten offen |
| Kontaktlose Kopplung | [ST60A3H1](https://www.st.com/en/wireless-connectivity/st60a3h1.html) (STMicroelectronics) | 60-GHz-mmWave-Transceiver, tunnelt eUSB2/UART/GPIO/I2C durch einen Luftspalt | Serienprodukt, ca. 10-15 EUR/Stk. |
| Anzeige | Holo-Box (Razer Project AVA, chinesische Hersteller) oder Smartphone | Zeigt Charakter-Daten aus dem Chip | Kein Serienprodukt fuer Hobby; Smartphone als Fallback |

## 2. Funktionsprinzip

```
  [Cortana-Chip am Kostuem]                [Holo-Box / Smartphone]
  ST60-Tx  <-- 60 GHz, 1-2 cm Spalt -->  ST60-Rx  -->  Anzeige-App
     |                                        |
  ESP32-S3 / Pi Pico                   Empfaenger-Geraet
  haelt Charakter-Daten                rendert Cortana / Husky
```

Der Chip ist ein **passives bis halbaktives Datendock**: Er haelt seine
Charakter-ID und einen kleinen Datensatz (Name, Status, Telemetrie-Snippets,
ggf. Bitmaps) in einem ESP32-S3 oder Pi Pico. Das Anzeigegeraet liest diese
Daten kontaktlos ueber den ST60 und rendert sie. Umgekehrt kann das Anzeigegeraet
auch Daten in den Chip schreiben (z. B. neue Statuswerte nach einer Show).

**Charakter-Varianten:** Jede physische Chip-Variante traegt eine eigene ID
(z. B. `cortana_v1`, `husky_v1`). Die Anzeige-App laedt passend zur ID das
richtige Design und die passenden Daten. Der Wechsel ist also ein physischer
Tausch des Chips, nicht ein Software-Eingriff.

## 3. Warum der ST60 und nicht BLE oder NFC

| Verbindung | Reichweite | Datenrate | Passt hier? |
| --- | --- | --- | --- |
| BLE | 10-50 m | ~1 Mbit/s | Ja, aber sichtbar "online" und pairing-Lastig |
| NFC | < 4 cm | ~400 kbit/s | Zu kurz; Chip muesste direkt aufs Display |
| **ST60 (60 GHz)** | **1-2 cm Spalt** | **bis 6,25 Gbit/s** | **Kontakt ohne Kabel, kein Pairing, physikalisch begrenzt** |

Der ST60 loest genau das Problem, das BLE hier haette: Er verhaelt sich wie
ein Kabel (deterministisch, kein Pairing, keine sichtbare Funkverbindung), ist
aber physisch abnehmbar. Die kurze Reichweite ist ein Feature, kein Bug - der
Chip ist nur lesbar, wenn er wirklich nahe am Empfaenger haengt.

**Ehrliche Einschaetzung:** Der ST60 ist ein Industrie-Produkt fuer
Kamera-Flip-Module und Docking-Anwendungen. Fuer ein Cosplay-Modul ist er
teuer, braucht eine eigene Platine und eine 5-V-Versorgung. Es gibt keine
Fertigmodule mit Steckern fuer Bastler; man muss selbst eine kleine PCB
entwerfen oder ein Evaluationsboard verdrahten. Das ist Profi-Level.

## 4. Daten, die der Chip haelt

Realistisch (ESP32-S3 mit 8 MB Flash, 2-8 MB PSRAM):

| Datentyp | Groesse | Beispiel |
| --- | --- | --- |
| Charakter-ID und Name | < 1 kB | "CORTANA-V1" |
| Status-Objekt | < 2 kB | Schild, Energie, Modus |
| Telemetrie-Snippets | < 5 kB | Letzte Messwerte vom Anzug |
| 1-2 kleine Bitmaps | < 20 kB | Logo, Icon |
| **Gesamt** | **< 30 kB** | Passt locker in den Flash |

"Aktiv lagern" im Sinne von grossen Datensaetzen (Bilder, Videos, Musik) ist
mit einem ESP32-S3 nicht sinnvoll. Wenn das Ziel mehr ist als Status-Daten,
wird der Chip zum WLAN-Client, der Daten vom Pi 5 nachlaedt - dann ist er
aber kein Offline-Dock mehr und braucht eine Verbindung.

## 5. Strombudget

| Komponente | Typisch | Peak | Hinweis |
| --- | --- | --- | --- |
| ESP32-S3 (idle, WiFi aus) | 0.02 A | 0.35 A | Deep Sleep noch niedriger |
| ST60A3H1 (Tx oder Rx) | ca. 0.15 A | 0.25 A | Herstellerangabe, zu verifizieren |
| **Summe Chip-Modul** | **ca. 0.17 A** | **0.6 A** | Nur aktiv, wenn an Dock |

Der Chip kann im Deep Sleep liegen und per Annaeherung (oder Taster) aufwachen.
Ohne Dock verbraucht er dann fast nichts. Das Modul gehoert auf eine eigene
Schiene oder an den FX-Rail-Peak, nicht auf die Pi-Rail.

## 6. Druck und Gehaeuse

Das [MakerWorld-Modell 1482318](https://makerworld.com/models/1482318) liefert
die Cortana-Optik. Fuer den Einbau muessen drei Anpassungen geplant werden:

1. **Innenausschnitt** fuer ESP32-S3-WROOM und ST60-Modul (ca. 25 x 18 x 5 mm
   plus Antennenfreiraum).
2. **Antennenfenster**: Der ST60 strahlt durch Kunststoff, nicht durch Metall
   oder dickes Filament. Ein Fenster aus 1-2 mm PETG oder ein
   Akkugraphit-freier Bereich ist noetig. Position laut ST-Layoutempfehlung.
3. **Lade-/Wartungsoeffnung** fuer USB-C oder LiPo-Anschluss, ohne den Chip
   vom Kostuem zu nehmen.

Druckmaterial: PETG oder ABS/ASA (Hitzestabilitaet im Kostuem), nicht PLA
fuer bauchnahe Bereiche. Fill 20-30 %, 3 Wandungen; Antennenfenster mit
mindestens 2 mm Abstand zu allen Metallteilen.

## 7. Software-Architektur

**Auf dem Chip (ESP32-S3):**

- Charakter-Daten als statisches JSON im Flash (LittleFS oder eingebettetes
  Blob).
- ST60-Treiber als eUSB2- oder UART-Tunnel; der Chip verhaelt sich wie ein
  USB-Geraet oder UART-Endpunkt.
- Optional: Status-Updates vom Anzug per I2C empfangen (an den Helm-Nano
  gekoppelt wie die anderen Module).

**Auf dem Anzeigegeraet (Smartphone / Holo-Box):**

- App oder Web-App, die per USB/UART (durch den ST60-Tunnel) die Charakter-ID
  liest und das passende Design rendert.
- Fuer den Prototyp reicht ein Smartphone mit USB-C-OTG: ST60-Rx-Board an den
  USB-C-Port, App liest seriell. Keine Holo-Box noetig.

## 8. Offene Punkte (Blocker fuer den Bau)

| Punkt | Warum offen |
| --- | --- |
| ST60-Evaluationsboard verfuegbar? | ST verkauft EVALST60A3H1; Bastler-Verfuegbarkeit und Preis pruefen |
| Antennenlayout | ST-Layoutguide nötig; Falschlayout = keine Verbindung |
| Holo-Box-Verfuegbarkeit | Razer Project AVA ist ein Konzept; chinesische Produkte sind nicht verifiziert |
| MakerWorld-Modell anpassbar? | Lizenz und Remix-Erlaubnis pruefen |
| Stromversorgung im Chip | LiPo + Lader oder Kabel vom Anzug; Gewicht und Sicherheit klaeren |

## 9. Pragmatischer Einstieg ohne ST60

Wer das Modul bauen will, ohne sofort eine eigene PCB zu entwerfen:

1. MakerWorld-Cortana drucken, ESP32-S3 + OLED klein einbauen, Charakter-ID
   und Status anzeigen.
2. Anzeige-App erst mal ueber BLE (ESP32-S3 hat WiFi/BLE an Bord) statt
   ST60 anbinden. Der Effekt (Chip am Kostuem, App zeigt Charakter) ist
   derselbe, nur nicht kontaktlos.
3. ST60 nachruesten, wenn das BLE-Prototyp-Setup funktioniert und das
   Layout-Problem geloest ist.

Damit ist der Cortana-Chip erst mal ein funktionierendes Show-Modul und wird
dann zur kontaktlosen Variante ausgebaut. Der Weg ist einfacher und die
erste Stufe kostet kein ST60-Evaluationsboard.
