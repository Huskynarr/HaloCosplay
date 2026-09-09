# RGB-Lichtmodule fuer Helm und Schubduesen

Stand: 2026-09-09. Arbeitsentwurf fuer austauschbare Module; keine thermische
oder optische Bauabnahme. Die [Einkaufsliste](../../Materials/Mjolnir-Licht-Einkauf.md)
enthaelt eine nachvollziehbare Prototypenbasis und deren Kostenrahmen.

## Festgelegter Aufbau

Vorgesehen sind zwei nach aussen strahlende Helmlampen und zwei Lichtmodule an
den Rueckenduese-Auslaessen. Jedes Modul erhaelt einen RGB-Star auf
Metallkernplatine, einen echten Metallkuehlkoerper und einen wechselbaren
Optikhalter. Sichtbare Kuehlrippen koennen in die seitlichen Helmgehaeuse
integriert werden, sofern die ausgewaehlte Halo-Referenz diese Kontur zulaesst.
Eine abnehmbare, offene Abdeckung schuetzt Rippen und Verkabelung.

Der Startpunkt sind **350 mA je Farbkanal**. Das ist eine
Prototypenentscheidung und weder eine garantierte sichere Helligkeit noch eine
Aussage ueber die spaetere Dauerbetriebsgrenze. Erst Licht-, Temperatur- und
Kameraproben bestimmen die erlaubten Betriebsstufen. Hoehere Chip-Stromratings
sind kein Anlass, unmittelbar mit dem Maximalstrom zu beginnen.

| Aufgabe | Lichtquelle | Wirkung und Begrenzung |
| --- | --- | --- |
| Nach aussen gerichtete Helmlampen | RGB-Power-Star mit diffuser Optik und schwarzer Abschirmung zum Visier | Definierter Lichtaustritt; keine direkte Sicht auf den Chip aus dem Helminneren |
| Beleuchteter Nebel | RGB-Power-Star seitlich am offenen Auslass, zum austretenden Nebel gerichtet | Farbiges Streulicht im Nebel; Wirkung haengt von Hintergrund, Umgebungslicht und Kamera ab |
| Kleine Statuslichter oder umlaufende Animation | Separater adressierbarer Pixelring mit passender Versorgung | Einzelne Pixel und Laufmuster; kein Ersatz fuer eine gebuendelte Lichtquelle |
| Innenraum und HUD | Eigene sehr schwach eingestellte Anzeige | Keine Power-LEDs hinter dem Visier und keine gemeinsame Helligkeitsregelung mit Aussenlicht |

RGB-Power-Stars haben in diesem Aufbau sechs getrennte elektrische Anschluesse
fuer drei LED-Chips. "Individually addressable" auf einer Star-Produktseite
bezeichnet hier die einzeln zugaenglichen Chips, kein WS2812-Datenprotokoll.
Ein Pixelprogramm oder ein ueblicher RGB-Streifencontroller ersetzt daher
weder die Konstantstromtreiber noch deren thermische Absicherung.

## LED-Auswahl und Rechenbasis

Arbeitsbasis ist der **Cree XP-E2 RGB 20-mm-Star, CREEXPE2-RGB** von LEDSupply.
Die fertig bestueckte Metallkernplatine vermeidet einen eigenen Reflow-Aufbau.
Die Produktseite nennt drei konkrete Cree-Bestellnummern. Vor der Bestellung
werden gelieferte Chip-Revision, Platinenverschaltung und passende Optik in der
Projektakte festgehalten.
[Modulhersteller: CREEXPE2-RGB](https://www.ledsupply.com/leds/cree-xpe2-rgb-high-power-led).

Bei der Recherche unterscheiden sich die Angaben auf der Modulproduktseite
von der aktuellen Chip-Dokumentation. Das muss bei der Bestellung geklaert
werden; die niedrigeren Werte duerfen nicht ungeprueft fuer aelteren Lagerbestand
verwendet werden.

| Datenstand bei 350 mA je Chip | Rot typ. | Gruen typ. | Blau typ. | Berechnete elektrische Leistung RGB je Star |
| --- | --- | --- | --- | --- |
| Cree XP-E2, CLD-DS56 Rev. 25B, 25 C | 2,08 V | 2,70 V | 2,85 V | 2,6705 W |
| Aeltere Werte auf CREEXPE2-RGB-Modulseite | 2,10 V | 3,40 V | 3,20 V | 3,045 W |

Die erste Zeile stammt aus dem [aktuellen Cree-Datenblatt, Seiten 3-4](https://downloads.cree-led.com/files/ds/x/XLamp-XPE2.pdf).
Die zweite dokumentiert die abweichende Modulquelle oben. Die Leistung folgt
aus `P_LED = I_R*V_R + I_G*V_G + I_B*V_B`, bei voll eingeschalteten Kanaelen.
Vier aktuelle Stars ergeben rechnerisch 10,682 W reine LED-Leistung; aus den
aelteren typischen Angaben folgen 12,18 W. Treiber, Wandler und Controller
kommen dazu. Keiner dieser Werte ist eine gemessene Anlagenleistung.

Fuer die vorlaeufige Versorgung kann beispielsweise mit 3,64 W je Star gerechnet
werden: angenommene 0,35 A mal 2,6 + 3,9 + 3,9 V. Diese bewusst aufgerundete
Spannungshuelle ist eine Planungsannahme; Stromtoleranz, Temperatur, wirkliche
Revision und Zuleitungsverluste bleiben gesondert zu pruefen. Unbekannte
Waermewiderstaende werden nicht mit null eingesetzt.

**Alternative:** Cree XM-L Color auf 20-mm-Star bietet RGBW in einem Gehaeuse.
Das [Cree-Datenblatt CLD-DS58 Rev. 7](https://downloads.cree-led.com/files/ds/x/XLamp-XML-Color.pdf)
nennt bei 350 mA typische RGB-Spannungen von 2,25 / 3,30 / 3,10 V.
RGB ergibt damit 3,0275 W; ein Weisskanal benoetigt einen vierten Treiber.
Die [CREEXML-RGBW-Modulseite](https://www.ledsupply.com/leds/cree-xml-rgbw-star-led)
war beim Abruf ausverkauft und enthaelt abweichende Maximalstromangaben.
Generationen und Grenzwerte werden deshalb nicht vermischt. RGBW bleibt eine
Beschaffungsalternative, kein bereits freigegebener Austausch.

## Konstantstrom und Verschaltung

Der Prototyp verwendet **sechs MEAN WELL LDD-350L**: drei fuer das Helmlampenpaar
und drei fuer das Duesenpaar. Jeweils die zwei roten Chips eines Paars bilden
eine Reihenschaltung; fuer Gruen und Blau gilt dasselbe. Jeder Farbstrang
erhaelt seinen eigenen Treiber. Links und rechts zeigen innerhalb eines Paars
dieselbe Farbe und Helligkeitsstufe. Helm und Duesen sind unabhaengig regelbar.

Dieser Aufbau ist bewusst gewaehlt: Ein einzelner warmer roter Chip kann unter
die minimale Ausgangsspannung des Treibers fallen. Zwei gleiche Farbchips in
Reihe lassen mehr Regelreserve. LED-Ausgaenge werden weder parallel geschaltet
noch mit der Versorgungsmasse verbunden. Die Platine muss getrennte Chip-Pads
haben; ein Modul mit intern gemeinsamer Anode oder Kathode passt nicht
ungeprueft in diesen Plan.

Die **15-V-Effektschiene** wird als Schnittstelle vorgesehen. Sie muss unter
Last stabil vorliegen; ein mit "USB-C" beschrifteter Anschluss liefert nicht
automatisch 15 V. Passender PD-Vertrag, Leistungsbudget und Verhalten beim
Anstecken eines zweiten Verbrauchers werden an der konkreten Powerbank geprueft.

Der LDD-350L besitzt laut [Herstellerdatenblatt](https://www.meanwell.com/Upload/PDF/LDD-L/LDD-L-SPEC.PDF)
9-36 V Eingang, 2-32 V Ausgang und etwa 3 V erforderliche Spannungsdifferenz.
Zwei Chips mit je 3,9 V ergeben 7,8 V; an 15 V bleibt damit rechnerisch Reserve.
PWM-Dimmung arbeitet bei diesem Modell mit 100-1000 Hz. DIM braucht ein zur
Revision passendes Signal; die dokumentierte LDD-350L-Fassung erwartet ueber
3,5 V fuer HIGH und unter 0,5 V fuer LOW. Ein offener DIM-Eingang schaltet ein.
Eine direkte 3,3-V-Ansteuerung wird deshalb nicht vorausgesetzt.

Die daraus abgeleitete Steuerungsschnittstelle:

- Sechs getrennte 5-V-PWM-Signale mit verifiziertem Pegeltreiber, Bezug auf
  `-Vin`; keine LED-Leistung aus GPIO-Pins.
- Definierter LOW-Zustand an allen DIM-Eingaengen bei Start, Reset und
  abgezogenem Controller. Ein passender Pull-down allein ist erst nach
  Pegelmessung eine belastbare Loesung.
- Erreichbarer Hardware-Schalter trennt die 15-V-Lichtversorgung unabhaengig
  von Software. Ein Temperaturfehler muss die betroffene Lichtversorgung
  sperren; Komfortlueftung bleibt versorgt.
- Steckbare Modulverbindungen enthalten alle benoetigten getrennten Leitungen,
  sind gegen Verpolung geschuetzt und zugentlastet. LED-Strang nur spannungslos
  trennen oder verbinden; ein abgezogenes Modul unterbricht sein Paar.
- Fuer unabhaengige linke/rechte Farben ist eine neue Treiberauslegung noetig,
  die auch niedrige rote Vorwaertsspannungen abdeckt. Einfaches Auftrennen in
  einzelne LDD-350L-Strange ist kein universell passender Ausbau.

Diese Schnittstelle ist ein Verdrahtungs- und Entwicklungsplan. Die bisherigen
Pixel-Sketches implementieren die sechs Leistungskanaele, Temperatursperre und
Resetlogik noch nicht. Unbekannte Abschalttemperaturen werden nicht durch
willkuerliche Zahlen ersetzt.

## Kuehlkoerper als Helm-Aussenbauteil

Der Waermepfad fuehrt vom Chip ueber die Metallkernplatine und eine duenne,
geeignete Waermeleitlage in einen verschraubten Aluminiumkuehlkoerper.
Die freiliegenden Rippen geben die Waerme an die Aussenluft ab. Eine aufgeklebte
3D-Druck-Attrappe oder eine MCPCB allein ersetzt diesen Pfad nicht.
Die Bedeutung von Platine und Waermeuebergang erlaeutert
[Cree: PCB Thermal Performance](https://downloads.cree-led.com/files/da/x/XLamp-PCB-Thermal.pdf).

Der konstruktive Entwurf sieht vor:

1. Lampenkassette von aussen abschraubbar, mit formschluessiger Befestigung am
   Helmtraeger und eigenem Servicekabel.
2. LED und Optik vor dem Kuehlkoerper, seitliche blendfreie Lichtblende, schwarzer
   geschlossener Lichtweg gegen Reflexionen ins Visier.
3. Rippen hinter einem offenen Schutzgitter; Rippenrichtung und freie Flaeche
   im getragenen Zustand pruefen. Polster, Haare oder Lack duerfen den Luftweg
   und die thermische Kontaktflaeche nicht verdecken.
4. Thermisch schwach leitende Distanzierung zum Helminneren, ausreichender
   Abstand zu Haut und Visier. Abdeckungen duerfen nicht direkt auf heisse
   Rippen aufliegen.
5. Temperaturmesspunkt am MCPCB/Loetpunkt nach LED-Dokumentation und am
   Kuehlkoerper. Zusaetzlich die beruehrbaren Oberflaechen und benachbarte
   gedruckte Halter messen.

Ein aufgedruckter LED-Grenzwert fuer die Sperrschicht ist kein zulaessiger
Hautkontaktwert. Der Kuehlkoerper wird nach seiner Kennlinie fuer Einbaulage und
Luftbewegung ausgewaehlt. Bei gemeinsamer Kuehlflaeche zaehlt die Summe der
Verlustleistungen. Ohne bekannte optische Effizienz dient die elektrische
LED-Leistung als konservativer Waermeeintrag fuer die erste Abschaetzung.
Die Pruefung erfolgt zuerst am ungetragenen Modul und danach mit der echten
Schutzabdeckung; ein Kurzimpuls beweist keinen Dauerbetrieb.

Die Helmlueftung bekommt einen separaten Frischluftweg. Sie saugt weder die
warme Lampenabluft noch Duesennebel an. Ein leiser Luefter im Helm kuehlt die
tragende Person nur durch Luftaustausch und Verdunstung; er ersetzt keinen
Metallwaermepfad fuer Power-LEDs.

## Helligkeit fuer Fotos und Messebetrieb

Zwei getrennte Einstellungen werden eingemessen: eine schwache, blendarm
ausgerichtete Messebeleuchtung und eine freigegebene Fotostufe mit festgelegter
Impulsdauer. Der Star bleibt aus normalen Blickwinkeln verdeckt. Fuer helle
Fotos wird zuerst Optik, Ausrichtung und Hintergrund angepasst; mehr Strom
allein garantiert kein sichtbares Nebelbild bei Tageslicht.

RGB-Mischungen verlieren auf der Kamera ihre Farbe, wenn Kanaele ausbrennen.
Der Test erfolgt deshalb mit dem vorgesehenen Motivabstand, Weissabgleich,
Verschluss, Blende und ISO. Eine Fotoserie prueft beispielhaft 1/50, 1/100,
1/250 und 1/1000 s sowie die benoetigten Video-Bildraten. Das sind Testpunkte,
keine Zusage fuer flimmerfreie Bilder. Mit 100-1000-Hz-Dimmung koennen besonders
bei kurzem Verschluss und Rolling Shutter Streifen entstehen. 100 % Einschaltdauer
vermeidet die PWM-Unterbrechungen eines Kanals, ersetzt aber weder die
Waermepruefung noch eine Kameraprobe. Fuer anspruchsvolle Zeitlupe braucht es
gegebenenfalls andere, nachweisbar passende Treiber.

Die [Duesendokumentation](Elektronik-Schubduesen.md) beschreibt die manuelle
Nebelkoordination und unabhaengige trockene Effektluefter.
