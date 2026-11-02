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

## Display-Auswahl: vom Retro-OLED bis AR-Brille

Die Auswahl des HUD-Displays entscheidet, wie viel "Cortana" am Ende moeglich
ist. Vier Stufen, aufsteigend nach Preis und Moeglichkeiten:

| Stufe | Display | Preis ca. | Farbe/Aufloesung | Wofuer |
| --- | --- | --- | --- | --- |
| A | Transparentes OLED 1,51" (SSD1309, 128x64, SPI) | 20-30 EUR | einfarbig blau/weiss | Kompass, Pfeile, Munition, Radar-Punkte, Textzeilen |
| A+ | Transparentes OLED 0,71" (128x40) | 10-15 EUR | einfarbig | Minimal-HUD, wenn Platz knapp ist |
| B | Micro-OLED-Modul (0,39"/0,6", 1080p) + Halbspiegel vor dem Auge | 100-200 EUR | Farbe, volle Aufloesung | Echte schwebende Einblendungen, viel Bastelaufwand |
| C | AR-Display-Brille (Birdbath, Micro-OLED) im Helm | 270-600 EUR | Farbe, 1080p, 50-57 Grad FOV | Vollwertiges HUD inkl. Cortana-Einblendungen |

### Stufe A: Transparentes OLED (Repo-Baseline)

Das 1,51"-Modul (Waveshare, SSD1309) ist die Basis von `hud_display.py` - keine
Software-Arbeit noetig. AliExpress-Klone kosten ca. 6-10 EUR. Wichtig:

- Einfarbig reicht fuer das Halo-Gefuehl: Das Spiel-HUD ist selbst minimal
  (Kompass, Schild/Munition, Pfeile). Blau = Halo/Cortana-Look, Gruen = Military-
  Retro (Fallout-Stil), Amber = warm und gut lesbar. Alles drei lieferbar.
- **Kein Cortana-Portraet, keine Grafik** - 128x64 Pixel sind ein Text-/Icon-HUD.
- Schaerfe: Display wenige Zentimeter vor dem Auge braucht eine Lupe (+8 bis
  +10 dpt) oder den Spiegel-Trick (`HUD_MIRROR`, schraege Plexiglasscheibe).
- Der getoente Gold-Visor hilft hier sogar: dunkler Hintergrund = mehr Kontrast.

### Stufe C: AR-Display-Brillen im Helm (2026-Stand)

Display-Brillen (Birdbath-Optik, Sony Micro-OLED) sind heute die praktischste
"richtige HUD"-Loesung und passen - leicht demontiert - gut in Helme:

| Modell | Preis ca. | Panel | Bemerkung |
| --- | --- | --- | --- |
| RayNeo Air 3s | 270-300 EUR | 1080p, 650 Nits | Budget-Einstieg |
| XREAL One | 400-500 EUR | 1080p, 600 Nits | X1-Chip, elektrochromische Abdunklung |
| Rokid Max 2 | 400-450 EUR | 1200p, 600 Nits | schaerfstes Panel in der Klasse |
| XREAL One Pro / VITURE Beast | 550-650 EUR | 1200p, 700-1250 Nits | hellste Panels, 57-58 Grad FOV |

Vorteile: Vollfarbe (Cortana-Einblendungen, echte Grafik), scharf, Helligkeit
reicht gegen das Umgebungslicht, Modelle mit elektrochromischer Abdunklung
(XREAL 1S/One/One Pro) koennen die Sicht abdunkeln - ideal hinter Visor.

Haken und Loesungen:

- **Eingang ist USB-C DisplayPort, nicht HDMI.** Der Pi 5 hat keinen DP-Alt-Mode
  am USB-C-Port - Loesung: micro-HDMI auf USB-C-DP-Wandler (aktiv, ca. 25-40 EUR)
  oder der Pi rendert das HUD als Video-Signal. Latenz ist mit gutem Wandler
  unkritisch (<1 Frame).
- **Strom:** Die Brille zieht Strom vom Quellgeraet - Wandlung + Brille mit ca.
  2-4 W einplanen (Strombudget oben erweitern).
- **Hitze/Gewicht:** 75-90 g, passiv gekuehlt - im Helm gut machbar, aber
  Helmluefter nicht sparen.
- **Einbau:** Buegel demontieren, Brillenkorpus vor dem dominanten Auge fixieren.
  Passt nicht in jeden Helm - vor dem Kauf Schablone aus Karton testen.

### Empfehlung nach Budget

- **Bis 30 EUR / Retro-Look:** 1,51" transparentes OLED in Blau. Passt zum
  Repo-Code, null Zusatzsoftware, authentisch minimalistisch.
- **"Was Gutes":** XREAL One oder Rokid Max 2 im Helm + HDMI-DP-Wandler. Erst
  damit werden Navigation in echt, Cortana-Einblendungen und Farb-Grafik moeglich.
  Die Stufe-A-OLED bleibt als Fallback eingebaut, falls die Brille auf der Con
  zickt (beide an den Pi, Umschalter im Code).

Die tiefe Herstellerrecherche zu Near-Eye-Optik, Birdbath-Modulen und
AR-Kandidaten (Viture Pro XR, Even Realities G1, ENMESI R3) steht in
[Elektronik-AR-Display.md](Elektronik-AR-Display.md).
