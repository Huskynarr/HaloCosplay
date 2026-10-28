# Mjolnir: Helm-Innenausbau, Kamera und Kommunikation

Der Helm wird als wartbares Modul mit eigener optischer Durchsicht ausgelegt.
Die Grundausstattung umfasst Luftkanaele, nach aussen gerichtete Lichtmodule,
ein Mundmikrofon und vorbereitete Kamera-/HUD-Aufnahmen. Leistungsakku und
Sprachlautsprecher sitzen am Rumpf. Die Auswahl bleibt pro Projekt anpassbar;
Koerpergroesse oder Kopfumfang alleine bestimmen den Innenraum nicht.

## 1. Verbindliche Aufteilung des Bauraums

| Zone | Vorgesehene Teile | Freizuhaltender Bereich |
| --- | --- | --- |
| Stirn / aeusserer Sensorblock | Kamerakassette mit eigenem optischem Fenster | Kamera-Sichtkegel und Visierbewegung |
| Seitliche aeussere Helmleuchten | RGB-Modul mit thermischem Pfad nach aussen | Keine direkte Abstrahlung auf Auge, Kamera oder Visierrueckseite |
| Seitlich oberhalb einer Blickachse | Optionales wegklappbares monokulares HUD | Zentraler Blick, Blick zum Boden, Brille und Wimpern |
| Wange am Mundwinkel | Mikrofon mit weichem Halter und Windschutz | Direkter Atemstrahl, Frischluftduese und Helmverschluss |
| Kinn-/Wangenoeffnungen | Getrennte Frischluftwege fuer Visier und Kopf | Mikrofonkapsel, optische Fenster und Lautsprecher bleiben ohne Anblasung |
| Obere hintere Helmzone | Warmluftaustritt; gegebenenfalls leichte Elektronikkassette | Abstroemquerschnitt und Druckpolster am Kopf |
| Seitlicher unterer Helmrand | Loesbare elektrische Schnittstelle mit Zugentlastung | Keine Schlaufe um den Hals, kein verdeckter Handgriff |
| Vorderer Brust-/Kragengrill | Sprachlautsprecher in herausnehmbarer Kassette | Schallweg, Brustverschluss und Zugriff auf Bedienelemente |

Diese Zonen sind Einbauziele. Die genaue Lage folgt dem gewaehlten
[Referenzhelm](Authentizitaet-Referenz.md) und einer realen Passprobe. Ein
sichtbarer neuer Kuehlkoerper muss in vorhandene Leuchten-/Sensorformen passen,
wenn die genaue Halo-Referenz erhalten bleiben soll.

Die [Helmbelueftung](Elektronik-Luefter.md) fuehrt Aussenluft ueber getrennte
Kanaele an die Visierinnenseite und in den Kopfbereich; warme Luft tritt oben
hinten aus. Nebel, dessen Schlaeuche und Duesenluefter bilden ein vollstaendig
separates System. Kamerafenster und HUD werden nicht als Luftauslass verwendet.

## 2. Helmkamera: unauffaelliger Einbau mit freier Optik

Die bevorzugte Kamerastelle ist ein bestehender Stirn- oder Sensorblock. Die
Kamera sitzt unmittelbar hinter einem eigenen klaren, austauschbaren Fenster.
Ein schwarzer matter Innenkragen schirmt die Linse gegen die benachbarten RGB-
Leuchten ab. Die Aussenform kann das Fenster als Sensordetail einbinden; die
Linse wird dabei nicht durch Gitter, Lochblech oder Goldfolie verdeckt.

Ein gold getoentes Visier vor der Kamera vermindert Licht und kann Farbstiche,
Spiegelbilder und Autofokusprobleme verursachen. Der Einbau dahinter ist daher
kein Standardpfad. Ein zusaetzliches Kamerafenster wird mit Testaufnahmen gegen
Aufnahmen ohne Fenster verglichen. Glas-/Kunststoffform, Dicke, Oberflaeche und
Dichtung duerfen die Bildqualitaet nicht unbemerkt verschlechtern.

### Auswahl und reale Schnittstellen

**Raspberry Pi Camera Module 3 Wide** ist ein verifizierter kleiner Kandidat:
25 x 24 x 12.4 mm, Autofokus und CSI-2. Die 120 Grad beziehen sich auf das
**diagonale** Sichtfeld; im gewaehlten Videoformat kann der verwendete Ausschnitt
abweichen. Die Standardversion ohne Wide ist weniger weitwinklig. Fuer die
Farbaufnahme wird eine Variante mit IR-Sperrfilter vorgesehen.
[Herstellerdaten](https://www.raspberrypi.com/products/camera-module-3/)

Die Kamera hat einen 15-poligen Anschluss. Raspberry Pi Zero und Pi 5 verwenden
am Rechner den kleineren 22-poligen Anschluss; erforderlich ist ein passendes
Standard-Mini-Kamerakabel. Die FPC-Leitung wird fest und ohne scharfe Knicke
verlegt. [Kabel- und Montageanleitung](https://www.raspberrypi.com/documentation/accessories/camera.html)

| Recorder-Variante | Vorteil | Verbleibende Pruefung |
| --- | --- | --- |
| Kameramodul und kleiner lokaler Recorder in einem loesbaren Sensorpod | Kurze interne CSI-Leitung; nur Versorgung ueber die Helmtrennung | Waerme, Masse, Aufnahmemodus, Speicherzugriff und Kopfkomfort |
| Kleine USB-UVC-Kamera, Recorder am Rumpf | Rechenwaerme und groessere Platine bleiben ausserhalb des Helms | Konkrete Kamera noch auszuwaehlen; FOV, echter UVC-Modus, Kabel, Zugentlastung und Videoqualitaet |
| Eigenstaendige kleine Aufnahmekamera | Weniger eigene Videoelektronik | Bauform, Eigenakku, Aufnahmedauer, Bedienbarkeit und Waerme |

Ein vorhandener Pi Zero 2 W ist fuer einen lokalen Recorder ein
Entwicklungskandidat, keine Zusage fuer jeden Kameramodus oder gleichzeitige
HUD-/Audiolast. Fuer die Standardplanung verlaeuft keine ungeschuetzte lange
CSI-Flachbandleitung ueber das Halsgelenk bis zum Brustkorb. Ein beliebiger
passiver Verlaengerungsadapter ist kein Nachweis fuer diese Strecke.

### Fenster und Halter dimensionieren

Die Kameraplatine bekommt eine definierte Auflage, einen wiederholbaren
Anschlag und eine loesbare Sicherung. Keine Heisskleberfixierung auf der Linse,
kein Druck auf Autofokusmechanik oder Flachbandstecker. Fenster und
Kameraplatine muessen getrennt wechselbar bleiben.

Als geometrische Vorpruefung kann fuer den freien Fensterhalbwinkel gelten:
`freie halbe Breite >= Abstand zur Eintrittspupille * tan(horizontaler FOV/2)`.
Dazu kommen realer Strahlenbuendelquerschnitt, Ausrichtungs- und
Montagereserve. Die 120-Grad-Diagonale darf dabei nicht als horizontaler Winkel
eingesetzt werden. Der Nachweis erfolgt durch Bilder aller Ecken bei den
geplanten Foto-/Videomodi und unterschiedlichen Fokusstellungen. Eine tiefe
kleine Bohrung kann trotz kleiner Linse das Bild stark abschatten.

Die Kamera ist fuer Aufnahmen und den Ausstellungsmonitor vorgesehen.
Record-Taster, erkennbare Aufnahmezustandsanzeige und Speicherzugriff werden
in die Kassette eingeplant. Die optische Integration bedeutet keine verdeckte
Aufnahmefunktion. Ein erfolgreicher Kamera-Stream macht den Helm nicht zu einem
geprueften Video-Sichtersatz.

## 3. Mikrofon, Lautsprecher und Stoertrennung

Das Mikrofon sitzt seitlich am Mundwinkel, auf einem eigenen weichen Halter.
Die Zuluft fuer das Visier wird an der Kapsel vorbeigefuehrt. Luefter und
Mikrofon teilen sich weder eine starre kleine Halterplatte noch einen
unmittelbaren Luftkanal. Bei laufenden Lueftern wird die Position zuerst
akustisch geprueft; Filtersoftware kommt danach.

Der Sprachlautsprecher sitzt vorn hinter einem Brust- oder Kragengitter mit
kurzem offenem Schallweg und eigener kleiner Schallwand. Er zeigt von Helm und
Mikrofon weg. Elektronik und Batterie des Verstaerkers bleiben erreichbar.
Eine Brustschale, die fuer den Einstieg aufklappt, bekommt einen gesicherten
Kabelbogen an der Scharnierseite oder einen vor dem Oeffnen erreichbaren
Stecker. Die Leitung darf die Klappe nicht festhalten.

[Audio und Stimmeffekte](Elektronik-Audio.md) beschreibt fertige Sprachsets,
optionale Signalverarbeitung, getrennte Soundeffekte und Umgebungshoeren. Ein
lauter Lautsprecher im Helm ist kein Ersatz fuer einen freien Schallweg nach
aussen.

## 4. Helmtrennung und alleine bedienbare Schnittstellen

Eine seitlich am unteren Helmrand erreichbare Schnittstelle fuehrt die
notwendigen Versorgungs- und Signalleitungen. Die Steckverbinder werden nach
realer Spannung, Spitzenstrom und Signalart gewaehlt; kein Universalstecker
wird hier ohne Beleg festgelegt. Getrennte Spannungen erhalten unterscheidbare,
verpolungssichere Anschluesse. Kontakte bleiben beruehrungsgeschuetzt.

- Anschluss und Entriegelung funktionieren vor dem Schliessen des Helms mit
  den vorgesehenen Handschuhen.
- Die Leitung hat ausreichende Reserve fuer Kopfdrehung, aber keine freie
  Schlaufe um Hals oder vor dem Gesicht.
- Beidseitige Zugentlastung verhindert Zug auf Platinenbuchsen. Eine
  mechanisch leicht erreichbare Trennung wird im Ausstieg getestet.
- USB fuer eine Kamera, analoges Mikrofon und geschaltete hohe LED-Stroeme
  erhalten passende getrennte Kabelfuehrungen. Ein gemeinsames ungeschirmtes
  Buendel kann Stoerungen erzeugen.
- Beim Oeffnen des Helms muss die Beleuchtung abschaltbar sein, damit die
  Aussenleuchte in neuer Position nicht direkt ins Gesicht strahlt.

Die Versorgung stammt aus dem [Rumpf-Elektroniksystem](Mjolnir-Elektronik.md).
Ein zusaetzlicher Akku im Helm ist keine Voraussetzung. Erhoeht eine optionale
Kamera das Kopfgewicht oder die Waerme spuerbar, wird der Recorder zuerst am
Rumpf erprobt.

## 5. Zusaetzliche Masse und Einbauproben

Diese Werte ergaenzen das Koerperprofil und bleiben bis zur Messung offen.
Es gibt keine Ableitung allein aus Koerpergroesse, Fotos oder Kopfumfang.

| Kennung | Messung / Eigenschaft | Zweck |
| --- | --- | --- |
| H01 | Augenlage zum getragenen Helm: Hoehe, seitliche Lage, Tiefe | Sichtfenster und HUD-Grundposition |
| H02 | Pupillenabstand und benoetigte Brillenkontur | Optikjustage und kollisionsfreier Augenraum |
| H03 | Kleinster Augen-/Wimpern-/Brillenabstand bei Kopfbewegung | Mechanische Freiraeume |
| H04 | Vorder-/Seitensicht und Blick zum Boden im realen Visier | Freizuhaltende Sichtflaeche |
| H05 | Nutzbarer Stirn-Sensorraum einschliesslich Stecker und Kabelbogen | Kamerakassette |
| H06 | Gewaehltes Optikmodul: Eyebox, Fokus und Parkvolumen | HUD-Halter und Schwenkbereich |
| H07 | Mundwinkel, Wangenpolster und Frischluftkanal | Mikrofonposition |
| H08 | Erreichbare Helmtrennung mit Handschuhen bei geschlossenem Torso | Selbststaendiges Absetzen |
| H09 | Helmmasse und Schwerpunkt mit jeder Ausstattung | Tragekomfort und Aufhaengung |
| H10 | Kameramodus, echter Bildausschnitt und Fensterabstand | Freies Kamerafenster |

Die erste Probe nutzt Karton-/Schaumstoff-Platzhalter in realer Kaufteilgroesse,
mit geschlossenem Visier und vorhandener Brille. Dann folgen Kamera mit
Testfenster, Mikrofon bei laufender Lueftung und erst zuletzt die HUD-Optik.

## 6. Nachweise fuer die konkrete Helmrevision

1. Sichtprobe vor jedem weiteren Einbau; neue Einschraenkungen dokumentieren.
2. Kamerabild mit RGB aus/an und verschiedenen Helligkeiten vergleichen;
   Reflexe, PWM-Streifen, Fokus und Vignettierung festhalten.
3. HUD mit und ohne Visier pruefen; Scharfstellung, Reflexe und mechanisches
   Wegklappen aufnehmen. Kein bestandener Softwaretest ersetzt dies.
4. Sprache bei jeder Luefterstufe aufnehmen und mit geschlossenem Torso
   wiedergeben. Rueckkopplungs- und Kabelzugprobe ergaenzen.
5. Gleichzeitig eingeschaltete Maximal-Konfiguration auf Waerme, Verbrauch
   und Beschlag pruefen; Ergebnisse im technischen Projektbericht erfassen.
6. Helm alleine oeffnen, Versorgung trennen und absetzen, ohne an einem
   Kabel zu ziehen. Eine erste beaufsichtigte Probe belegt die Bedienbarkeit;
   die Absicht allein gilt nicht als bestandener Selbstanzieh-Test.

Dieser Guide liefert Einbauentscheidungen und Schnittstellen. Ein angepasstes
Kameragehaeuse, eine optisch gepruefte HUD-Kassette und ein physisch erprobter
Helm werden damit nicht als bereits gefertigt ausgegeben.
