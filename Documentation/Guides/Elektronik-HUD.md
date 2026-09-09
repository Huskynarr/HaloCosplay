# Elektronik: HUD-Inbetriebnahme

Der vorhandene Python-Code ist eine Anzeige-Demonstration fuer SSD1309 mit
128 x 64 Bildpunkten. Eine funktionierende Displayansteuerung und eine im Helm
lesbare optische Anzeige sind getrennte Arbeitsschritte. Grundlage sind
[Displaywahl und Optik](Elektronik-AR-Display.md) sowie
[Einbauorte im Helm](Mjolnir-Helmintegration.md).

## Hardwarepfad

1. Ein gewaehltes SSD1309-Modul auf der Werkbank mit der Herstellerdemo pruefen.
2. Schnittstellenmodus, Reset, Pegel, Anschlussbelegung und sichtbare
   Bildkoordinaten protokollieren.
3. Den Repository-HUD-Code mit dem tatsaechlich geprueften Modul verbinden.
4. Erst danach eine optische Passprobe und den mechanischen Einbau durchfuehren.

Fuer das Waveshare 1.51inch Transparent OLED ist Vierdraht-SPI der
Auslieferungszustand. I2C erfordert eine Hardware-Umschaltung. Die
[Herstelleranleitung](https://www.waveshare.net/wiki/1.51inch_Transparent_OLED)
ist fuer den exakten Platinenstand massgeblich. Die fruehere pauschale
Vier-Leitungs-Anweisung ohne Modus-/Resetpruefung ist kein gueltiger
Verdrahtungsplan.

## Vorhandene Software und Grenzen

| Datei | Bereits vorhanden | Zusaetzlich zu pruefen |
| --- | --- | --- |
| [hud_display.py](../../Code/HelmetControl/hud_display.py) | Bildaufbau, Animationen, I2C-Backend ueber luma.oled | Reales Modul, Busadresse, Reset, Bildausrichtung und sichtbare Pixel |
| [config.example.json](../../Code/HelmetControl/config.example.json) | Konfigurationsvorlage | Tatsaechliche I2C-Adresse und Projektpfade |
| [hud_state.example.json](../../Code/HelmetControl/hud_state.example.json) | Beispielwerte fuer die Anzeige | Reale Datenquelle; ohne Quelle bleibt es Demo |
| [battery.example.json](../../Code/HelmetControl/battery.example.json) | Beispiel fuer Batteriewerte | Gepruefte Messung oder Herstellertelemetrie |
| [requirements.txt](../../Code/HelmetControl/requirements.txt) | Softwareabhaengigkeiten | Installation auf der gewaehlten OS-Version |

Der Code besitzt gegenwaertig kein auswaehlbares SPI-Backend und keine im Code
konfigurierte modulspezifische Resetleitung. Ein SPI-Modul ist deshalb kein
unveraendert einsteckbarer Ersatz. Die Auswahl eines Boards im Einkauf oder im
Konfigurator fuegt fehlende Treiber nicht hinzu.

Ein hardwarefreier Bildtest aus dem Repository-Stamm:

```bash
python3 Code/HelmetControl/hud_display.py --selftest build/HudTest.png
```

Der Ausgabeordner muss vorher existieren. Das Ergebnis belegt den Bildaufbau;
Busfunktion, Stromaufnahme und Optik sind dabei nicht beteiligt.

## Versorgung und Montage

Fuer die Grundausstattung ist kein Akku im Helm vorgesehen. Die Versorgung
kommt ueber einen geschuetzten, loesbaren Helm-Kabelstrang aus dem getragenen
Elektroniksystem. Akku- und Wandlerwahl richten sich nach dem gemessenen
[Strombudget](Elektronik-Strombudget.md). Akkus oder Powerbank-Ausgaenge werden
nicht direkt parallel verbunden. Eine gewuenschte Umschaltung zwischen
Versorgungen braucht dafuer ausgelegte Hardware.

Display und moeglicher lokaler Kamerarechner teilen sich nicht automatisch eine
Stromfreigabe mit starken Aussen-LEDs. Lueftung bleibt beim Ausschalten der
Showeffekte verfuegbar; die konkrete Verteilung beschreibt
[Mjolnir-Elektronik](Mjolnir-Elektronik.md).

Die Platine sitzt in einer loesbaren trockenen Kassette. Die Halterung des
Anzeigemoduls wird nach der optischen Passprobe festgelegt. Die generische
[Visierhalter-Probe](../../Design/Components/README.md) liefert keine
Near-Eye-Optik und keinen Nachweis fuer das Anbringen von Displayglas am Auge.

## Nachweise vor geschlossenem Helm

- Reales Testbild mit allen Randpixeln und eindeutiger Links-/Rechtsmarkierung.
- Start, Neustart, Spannungsabfall und vollstaendige Abschaltung auf der Werkbank.
- Lesbarkeit, freie zentrale Sicht und Reflexe im hellen sowie dunklen Umfeld.
- Mechanisches Wegklappen mit Handschuhen und Brille, ohne Kontakt zum Gesicht.
- Stromaufnahme und Temperatur mit dem gleichzeitig laufenden Kameramodul.

Alle Resultate gehoeren mit Kaufteilrevision, Konfiguration und Foto in das
eigene Bauprojekt. Ein Testwert aus einer anderen Helmform ist keine
Passbestaetigung fuer diese Konstruktion.
