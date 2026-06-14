# Exoskelett (Profi-Variante V3)

> **Level:** [P] Profi  |  **Varianten:** V3  |  **Voraussetzungen:** Erfahrung mit Alu-Profil-Bau, Werkzeug (Saege, Bohrer, Gewindeschneider), Verstaendnis von Lastpfaden; Handler beim Tragen Pflicht

Das Exoskelett dient der optischen Verstaerkung der Spartan-Aesthetik. Es macht den Traeger groesser und massiver. Empfohlen wird ein passives System (Skeletonics-Stil), das die Bewegung des Traegers rein mechanisch uebertraegt.

## Prinzip: Pantograph-Linkage

Ein Pantograph ist ein Parallelogramm-basiertes Gestaenge, das Bewegungen vergroessert uebertraegt. Der Traeger bewegt den inneren Arm, der aeussere Arm folgt vergroessert.

**Verstaerkungsverhaeltnis:**
```
Ratio = Abstand Anker zu Output / Abstand Anker zu Input
Beispiel: Anker an Schulter, Input am Ellbogen (30 cm),
          Output-Arm 45 cm vom Anker = 1.5x Verstaerkung
```

Fuer Spartan-Builds: 1.3-1.5x Verstaerkung an den Armen reicht fuer imposante Wirkung.

**Referenz:** Skeletonics ARRIVE - 279 cm gross, 40 kg, rein mechanisch (keine Motoren fuer Bewegung).

## Materialien

### Hauptrahmen

| Material | Einsatz | Vorteile | Nachteile |
| --- | --- | --- | --- |
| Alu-Profil 3030 (30x30 mm T-Slot) | Wirbelsaeule, Hueftring, Oberschenkel | Stabil, leicht, modular, Nutensteine fuer einfache Montage | Teurer als 2020 |
| Alu-Profil 2020 (20x20 mm T-Slot) | Arme, Unterschenkel | Leichter, guenstiger | Weniger Tragfaehigkeit |
| PVC-Rohr | NUR Prototypen | Billig, schnell, leicht zu aendern | Nicht fuer Endprodukt! |

### Gelenke und Verbindungen

| Teil | Empfehlung | Preis ca. |
| --- | --- | --- |
| Kugellager 608ZZ (8x22x7 mm) | Skateboard-Lager, 20-30 Stueck noetig | 0.50-1 EUR/Stueck |
| M8/M20 Stahlgewindestangen | Als Hauptachsen fuer hochbelastete Gelenke | 5-15 EUR/Stueck |
| M8 Achsschrauben (Shoulder Bolts) | Drehpunkte, 20 Stueck | 2-4 EUR/Stueck |
| Zahnraeder & Seilrollen (3D-Druck) | Gedruckt aus hochfestem Filament wie **Taulman Alloy 910** | 15-30 EUR |
| T-Slot Eckverbinder | 40-60 Stueck fuer Rahmenverbindungen | 1-2 EUR/Stueck |
| 3D-gedruckte Custom-Brackets | Spezialverbinder, 1-2 kg Filament | 25-50 EUR |

### Bezugsquellen (DE/EU)

- **Motedis.com** - Alu-Profile auf Mass geschnitten, Verbinder, Zubehoer (Deutschland)
- **Dold Mechatronik** - Profile und Zubehoer
- **Amazon.de** - 608ZZ Lager, Schrauben, Hardware
- **VEVOR** - Trockenbau-Stelzen als Basis fuer Bein-Verlaengerung

## Gelenk-Mechanismen im Detail

### Schulter (Doppel-Parallelogramm)

- **Mechanismus:** Doppeltes Parallelogramm erzeugt einen virtuellen Drehpunkt der zum Schultergelenk passt
- **Freiheitsgrade:** 2 reichen fuer Cosplay (Heben/Senken + Vor/Zurueck)
- **Aufbau:** Zwei parallele Alu-Stangen (je ~25 cm) mit Lagern an allen 4 Drehpunkten
- **Lager:** 608ZZ an jedem Pivot, M8 Shoulder Bolts als Achsen
- **Bewegungsradius Ziel:** 0-150 Grad Abduktion, 0-120 Grad Flexion
- **Gewicht pro Schulter:** ~1.5-2.5 kg erreichbar

### Ellbogen (Einfaches Scharnier mit Anschlag)

- **Mechanismus:** Einzelachsen-Scharnier mit Ueberstreckungsschutz bei 0 Grad und ~150 Grad
- **DIY-Aufbau:** Zwei Alu-Flachstangen mit einem 608ZZ-Lager als Pivot, Anschlagstifte fuer Begrenzung
- **Kritische Dimension:** Pivot-Zentrum muss mit dem tatsaechlichen Ellbogen-Drehpunkt uebereinstimmen
- **Alternative:** Funktionale bionische Scharniere (Etsy, ~15-25 EUR/Paar) mit eingebauter Drehbegrenzung

### Knie (Kreuz-Viergelenkgetriebe)

- **Einfach:** Einzelachsen-Scharnier wie Ellbogen, Anschlaege bei 0 Grad (Streckung) und ~120 Grad (Beugung)
- **Besser:** Kreuz-Viergelenkgetriebe fuer polyzentrische Bewegung - ahmt das natuerliche Rollen/Gleiten des Knies nach
- **Pflicht:** Starker Anschlag bei voller Streckung (traegt das Gewicht beim Stehen, besonders mit Stelzen)

### Handgelenk

- Oft vereinfacht oder weggelassen
- Spartan-Handschuh kann starr montiert sein, Hand ragt durch die Oeffnung
- Falls gewuenscht: einfacher Pivot fuer Beugung/Streckung

## Hydraulik-Simulation & Gewichtsentlastung

Um die motorisierte Unterstuetzung der Mjolnir-Ruestung optisch zu simulieren und gleichzeitig die Gelenke mechanisch zu entlasten, wird ein kombiniertes Kolben-Feder-System empfohlen:

1. **Konstruktion der Kolben (Optik):**
   - Gehaeuse aus PEX-Rohren (1/2" und 3/8" PEX) oder PVC-Rohren bauen.
   - Um den glaenzenden Metall-Look zu erhalten, werden die Rohre mit reflektierendem Aluminium-Klebeband (Alu-Tape) umwickelt. Dies simuliert taeuschend echt hydraulische Teleskopzylinder.
2. **Gewichtsentlastung (Mechanik):**
   - Im Inneren der PEX/PVC-Kolben oder parallel dazu werden elastische Bungee-Seile oder Gasdruckfedern verbaut.
   - Dieses passive Federungssystem wirkt als Gegengewicht ("Counterbalance") und nimmt einen Grossteil der Ruestungslast von den Knien, Hueften und Schultern auf.

## Hoehe hinzufuegen (15-30 cm)

### Option A: Modifizierte Trockenbau-Stelzen (empfohlen)

- VEVOR oder Marshalltown Stelzen, auf Minimum (~15-20 cm) eingestellt
- Doppelte Federung fuer Balance
- Bein-/Fuss-/Fersen-Riemen fuer Sicherheit
- **Kosten:** 50-120 EUR/Paar
- **Modifikation:** Stelzen-Rahmen wird Teil des Exoskelett-Beins, Ruestung drueber montiert

### Option B: Plattform-Schuhe (10-15 cm, einfacher)

- Dicksohlige Plateau-Boots oder Holzbloecke auf Schuhe geschraubt
- Weniger Mobilitaet, aber viel einfacher
- Gut fuer kurze Trage-Sessions oder statische Displays

### Option C: Integrierte Bein-Verlaengerung

- Exoskelett-Unterschenkel 15-25 cm laenger als das echte Bein
- Fuss ruht auf einer internen Plattform innerhalb des "Schienbeins"
- Aeusserer "Stiefel" ist kosmetisch
- Gang aendert sich - ausfuehrlich ueben!

### Sicherheit bei Stelzen

- Stunden ueben bevor Convention (Gehen, Drehen, Aufstehen/Hinsetzen)
- **IMMER Handler dabei**
- Knie staerker beugen, hoeher als normal steigen
- **Tuerhoehe beachten:** Standard 200-210 cm. Mit 20 cm Stelzen + Helm = 220-240 cm Gesamthoehe!

## Gewichtsziele

| Komponente | Zielgewicht |
| --- | --- |
| Arm-Exo (Schulter bis Hand) pro Seite | 2-3 kg |
| Beide Arme komplett | 4-6 kg |
| Torso/Wirbelsaeulen-Rahmen | 2-3 kg |
| Bein-Exo (pro Bein) inkl. Stelze | 2-4 kg |
| Hueft-/Taillen-Rahmen | 1-2 kg |
| **Exo-Rahmen gesamt (ohne Ruestung)** | **12-18 kg** |
| Ruestungsplatten (alle Segmente) | 5-10 kg |
| **Gesamtgewicht** | **17-28 kg** |

**Gewichtsverteilung:** 80% auf der Huefte/Becken via Klettergurt.

## Bau-Phasen

1. **PVC-Prototyp** - Gesamten Rahmen aus PVC-Rohr bauen (billig, schnell iterierbar)
2. **Koerpermessungen** und Bewegungsradien pruefen am PVC-Modell
3. **Aluminium-Rahmen** schneiden und zusammenbauen
4. **Gelenke** mit Kugellagern setzen, Bewegungsfreiheit testen
5. **Stelzen** integrieren (falls gewuenscht), Gehen ueben
6. **Linkages** zur Innenstruktur (Klettergurt) verbinden
7. **Ruestung** segmentieren und auf Rahmen montieren
8. **Lack und Finish** der Ruestungsteile
9. **Ausfuehrlicher Test** - Stunden tragen, alle Bewegungen, Handler dabei

**WICHTIG:** Exo-Rahmen ZUERST bauen, dann Ruestung anpassen - nie umgekehrt!

## Ruestung auf dem Exo montieren

### Strukturelle Teile (Brust, Ruecken, Oberschenkel)

- **Direkt verschrauben** mit M5/M6 Schrauben durch Bohrloecher im Rahmen
- Gummi-Unterlegscheiben zwischen Ruestung und Rahmen (verhindert Klappern)
- T-Slot Nutensteine ermoeglichen nachtraegliche Positionsanpassung

### Kosmetische Teile (Schultern, Unterarme, Schienbeine)

- Neodym-Magnete (10x3 mm) in Ruestung und Rahmen-Montageplatten
- Heavy-Duty Snaps (E6000 Kleber, 24-72h Aushaertung)
- Industrial Velcro fuer leichte Panels
- 5-10 mm Spalt zwischen benachbarten Ruestungsteilen fuer Bewegung

## Haeufige Probleme

| Problem | Ursache | Loesung |
| --- | --- | --- |
| Gelenke klemmen | Achse Exo-Gelenk stimmt nicht mit Koerper-Gelenk ueberein | Rolling Joints, Spiel/Compliance hinzufuegen, Doppel-Scharnier |
| Gewichts-Ermuedung | Gewicht zu weit vom Koerperschwerpunkt | Schwere Teile naeher an Huefte, Gegengewichte, Arm-Exo minimieren |
| Zu gross fuer Tueren | Gesamthoehe >210 cm | Design auf max 210 cm begrenzen oder Ducken/Handler einplanen |
| Sitzen unmoeglich | Starrer Rahmen verhindert Beugen | Hueftgelenk fuer Sitzen designen oder nur-stehen akzeptieren |
| Metall-auf-Metall Geraeusche | Kontakt an Gelenken | Nylon-Buchsen, Filz-Scheiben, Lager-Fett, Gummi-Puffer an Anschlaegen |
| Ueberhitzung | Geschlossener Rahmen staut Waerme | Aktive Luefter im Torso, offene Spalte an Gelenken |

## Sicherheit (Convention)

- **Keine Motoren** fuer Bewegung (LEDs und Luefter sind OK)
- **Keine scharfen Kanten** - alle Alu-Schnitte entgraten und mit Kantenschutz versehen
- **Gummikappen** auf alle freiliegenden Profil-Enden
- Gelenk-Quetschpunkte mit kosmetischen Abdeckungen verhuellen
- **Breakaway-Montage** fuer aeussere Ruestung (loest sich bei Aufprall statt zu verletzen)
- **Not-Ausstieg unter 60 Sekunden** moeglich (Klettergurt-Schnallen)
- **Handler Pflicht** bei Builds ueber 210 cm Gesamthoehe

## Kosten (V3 Exoskelett + Ruestung)

| Kategorie | Kosten ca. |
| --- | --- |
| Alu-Profile (15-20m, 3030 + 2020) | 90-210 EUR |
| Verbinder, Lager, Schrauben | 90-230 EUR |
| 3D-gedruckte Brackets (Filament) | 25-50 EUR |
| Klettergurt | 40-80 EUR |
| Trockenbau-Stelzen (optional) | 50-120 EUR |
| Kantenschutz, Gummikappen, Sicherheit | 20-40 EUR |
| Werkzeug (Saege, Bohrer, Gewindeschneider) | 50-150 EUR |
| **Exo-Rahmen Zwischensumme** | **365-880 EUR** |
| Ruestungsmaterial (Foam / 3D-Druck) | 200-600 EUR |
| Finish (Lack, Fueller, Versiegelung) | 50-150 EUR |
| **Gesamt V3** | **615-1.630 EUR** |

## Montage auf der Ruestung

Das Exoskelett ist kein Selbstzweck - es ist das Tragesystem, an dem die Ruestung haengt und ueber das das gesamte Gewicht in den Koerper eingeleitet wird. Die Anbindung muss daher genauso sorgfaeltig geplant werden wie der Rahmen selbst. Grundprinzip: Der Klettergurt an der Huefte ist die zentrale Lastschnittstelle zwischen Mensch und Maschine. Details zum Unteranzug und zu den Befestigungsarten siehe `Documentation/Guides/Unteranzug-Befestigung.md`.

### Anbindung an Klettergurt/Harness

- **Klettergurt als Basis:** Ein gepolsterter Industrie-Klettergurt (Sitzgurt mit breitem Hueftpolster, kein duenner Sportklettergurt) wird direkt am Koerper getragen. Er nimmt den Wirbelsaeulen-Rahmen des Exos auf.
- **Anbindungspunkt Wirbelsaeule:** Der vertikale Alu-Rahmen (3030) endet unten in einer 3D-gedruckten oder gefraesten Adapterplatte, die ueber 2-4 verschraubte D-Ringe oder Stahl-Schaekel am Gurt-Rueckenteil sitzt. Keine Klebeverbindung an dieser Stelle - nur Schraub-/Schaekelverbindung.
- **Taktisches Tragesystem (Rigging):** Die Lastuebertragung wird durch ein militaerisches H-Harness (z.B. BlackHawk H-Harness) und einen robusten Polizei-Koppelguertel stabilisiert, der die Last von den Schultern auf die Hueften umleitet. Elastische Gurtbaender mit Parachute-Clips (Steckverschluesse) verbinden die beweglichen Ruestungsteile fuer maximale Beweglichkeit.
- **Hueftring:** Ein umlaufender oder halber Alu-Hueftring (3030) wird mit dem Wirbelsaeulen-Rahmen verschraubt und liegt auf dem Beckenkamm auf. Er traegt die Bein-Exos und gibt die Last in den Klettergurt ab.
- **Schulter-Stabilisierung:** Schultergurte des Harness nehmen NUR Stabilisierungslast (Kippen verhindern), nicht das Hauptgewicht. So bleibt der Lastpfad ueber Becken/Huefte.

### Lastpfad (von oben nach unten)

```
Arm-Exo + Schulterruestung
        |
   Schulter-Linkage (virtueller Drehpunkt)
        |
Wirbelsaeulen-Rahmen (3030) ----> Schultergurte (nur Stabilisierung)
        |
   Hueftring / Adapterplatte
        |
   Klettergurt (Hueftpolster) ----> Becken/Beckenkamm des Traegers
        |
   Bein-Exo (pro Seite)
        |
   Stelze / Fussplatte ----> Boden
```

Merksatz: Jedes Gramm soll moeglichst direkt von seinem Ursprungspunkt in die Huefte und von dort in die Beine/den Boden geleitet werden. Lasten, die ueber die Schultern oder die Wirbelsaeule des Traegers laufen, sind nach 30-60 Minuten schmerzhaft.

### Befestigungspunkte Ruestung am Rahmen

Es gilt dieselbe Logik wie im Abschnitt "Ruestung auf dem Exo montieren" oben, aber priorisiert nach Gewicht:

| Ruestungsteil | Anbindung | Lasttraeger |
| --- | --- | --- |
| Brust + Ruecken | M5/M6 verschraubt auf Wirbelsaeulen-Rahmen, Gummi-Unterleger | Wirbelsaeule -> Huefte |
| Oberschenkel-Platten | Verschraubt auf Bein-Exo Oberschenkelstrebe | Bein-Exo |
| Codpiece / Huefte | Verschraubt / Snaps am Hueftring | Hueftring |
| Schulterglocken | Magnete + Snaps auf Schulter-Linkage-Platte | Arm-Exo |
| Unterarme / Schienbeine | Magnete / Industrial Velcro (kosmetisch) | jeweiliges Glied |

Zwischen benachbarten Segmenten 5-10 mm Spalt fuer Bewegung lassen (siehe Abschnitt "Kosmetische Teile").

### Reihenfolge Anziehen (mit Handler)

Das Anlegen eines V3-Builds ist Zweipersonen-Arbeit. Plane 15-25 Minuten ein.

1. **Unteranzug + Kuehlweste** anziehen (siehe `Documentation/Guides/Unteranzug-Befestigung.md`).
2. **Klettergurt** anlegen und Hueftpolster mittig auf dem Beckenkamm ausrichten, alle Schnallen schliessen.
3. **Bein-Exos einsteigen** - Traeger setzt sich, Handler fuehrt Fuss in die Stelze/Fussplatte, Fersen- und Spannriemen schliessen.
4. **Aufstehen mit Handler-Stuetze** und Stand auf den Stelzen pruefen (kurz, festhalten).
5. **Wirbelsaeulen-Rahmen** auf den Klettergurt aufschrauben/einschaekeln (Handler von hinten), Schultergurte schliessen.
6. **Arm-Exos** ankoppeln, Bewegungsfreiheit der Schulter-Linkage pruefen.
7. **Ruestungsteile** in Reihenfolge schwer -> leicht montieren: Brust/Ruecken, Oberschenkel, Huefte, dann Schultern, Unterarme, Schienbeine.
8. **Helm zuletzt** (siehe `Documentation/Guides/Sicherheit.md` zu Hitze/Sicht).
9. **Abschluss-Check durch Handler:** Sitzt der Gurt, sind alle Schnallen zu, ist der Notausstieg frei erreichbar, klemmt nichts.

Ausziehen erfolgt in umgekehrter Reihenfolge. Der Notausstieg (siehe unten) ist eine separate, schnellere Sequenz.

## Gewicht und Balance

Ein V3-Build wiegt mit Ruestung realistisch **17-28 kg** (siehe Tabelle "Gewichtsziele"). Diese Last ist nur tragbar, wenn sie korrekt verteilt ist und der Schwerpunkt stimmt. Falsche Balance macht selbst 18 kg unertraeglich, gute Balance macht 25 kg ueber Stunden machbar.

### Gewichtsbudget realistisch planen

| Komponente | Realistisch | Ambitioniert (optimiert) |
| --- | --- | --- |
| Exo-Rahmen gesamt (ohne Ruestung) | 12-18 kg | 9-12 kg |
| Ruestungsplatten gesamt | 5-10 kg | 4-6 kg (duenne EVA / TPU) |
| Elektronik, Akku, Luefter | 1-2 kg | < 1 kg |
| **Gesamt am Koerper** | **18-30 kg** | **14-19 kg** |

Setze fuer jede Baugruppe ein Gewichtslimit BEVOR du baust, und wiege Teile beim Bau gegen das Budget. Ueberschreitungen summieren sich schnell.

### Schwerpunkt (Center of Gravity)

- **Ziel:** Der Gesamtschwerpunkt des angezogenen Builds soll moeglichst tief und nah an der natuerlichen Koerperachse liegen - idealerweise auf Hueft-/Beckenhoehe, mittig ueber den Fuessen.
- **Arme sind der Feind:** Gewicht an ausgestreckten Arm-Exos wirkt mit langem Hebel und kippt nach vorn/zur Seite. Arm-Exos so leicht wie moeglich, schwere Teile (Akku, Verkabelung) im Torso nahe der Wirbelsaeule platzieren.
- **Gegengewicht:** Liegt der Schwerpunkt zu weit vorne (grosse Brustplatte, Helm), kann ein kleines Gegengewicht (z.B. Akku) im Ruecken-Rahmen ausgleichen. Lieber Masse umverteilen als hinzufuegen.
- **Stelzen erhoehen das Risiko:** Je hoeher der Build, desto laenger der Hebel zum Boden. Schwerpunkt umso wichtiger.

### Warum Carbon/Alu statt Stahl

| Material | Dichte ca. | Bewertung fuer Exo |
| --- | --- | --- |
| Stahl | 7.85 g/cm3 | Sehr stabil, aber viel zu schwer - verbietet sich fuer tragbare Builds |
| Aluminium (Profil) | 2.70 g/cm3 | Standard fuer DIY-Exo: gutes Verhaeltnis Steifigkeit/Gewicht, modular, bezahlbar |
| Carbon (CFK-Rohr/Platte) | 1.55 g/cm3 | Leichteste tragende Option, sehr steif - fuer Arme/Schienbeine, wo jedes Gramm am Hebel zaehlt; teuer und schwerer zu bearbeiten |

Faustregel: Tragstruktur (Wirbelsaeule, Hueftring) aus Alu 3030; bewegte/weit aussen liegende Glieder (Arme) wo moeglich aus Alu 2020 oder Carbon, um Hebellast zu reduzieren. Stahl hoechstens fuer kleine, hochbelastete Achsen/Schaekel, nie fuer Rahmenlaengen.

### Gewichtstest-Vorgehen

1. **Wiegen:** Jede Baugruppe einzeln auf einer Personenwaage wiegen und gegen das Budget protokollieren. Dann den komplett angezogenen Build wiegen (Traeger mit/ohne Build, Differenz = Last).
2. **Schwerpunkt pruefen:** Statisch im Stand testen - kann der Traeger ohne Festhalten ruhig stehen? Kippt es in eine Richtung? Bei Bedarf Masse umverteilen, nicht zustopfen.
3. **Gehtest:** Auf ebener Flaeche, dann Bordstein/Schwelle, mit Handler. Achten auf Pendeln der Arme und Vorkippen.
4. **Sitztest:** Hinsetzen und Aufstehen mit Handler - geht es kontrolliert, oder reisst das Gewicht beim Aufstehen nach hinten/vorn?
5. **Ausdauertest:** Mindestens 30-60 Minuten am Stueck tragen (gestaffelt aufbauen), Druckstellen und Ermuedung dokumentieren. Vergleiche mit dem Test-Template unter `Tests/TestReports/`.
6. **Iterieren:** Druckstellen polstern, Schwergewichte naeher an die Huefte, Arm-Exo abspecken. Erst danach Convention.

## Sicherheit & Con-Tauglichkeit

Diese Sektion ergaenzt den Abschnitt "Sicherheit (Convention)" oben und die allgemeinen Regeln in `Documentation/Guides/Sicherheit.md` sowie `Documentation/Guides/Convention-Regeln.md`. Pruefe die Hausordnung jeder Convention VOR der Anmeldung - Exoskelett-Builds koennen zustimmungspflichtig oder eingeschraenkt sein.

### Strikt passiv (keine Motoren auf Cons)

- **Keine angetriebene Bewegung.** Das Exo ist rein mechanisch (Pantograph, Federn, Gasdruckfedern). Motoren oder Aktuatoren zur Gelenkbewegung sind auf Conventions nicht zulaessig und ein Verletzungsrisiko.
- **Erlaubt sind:** LEDs, Luefter, HUD/Audio - also passive Verbraucher ohne mechanische Kraftwirkung (siehe `Documentation/Guides/Sicherheit.md`, Abschnitt Elektronik).
- **Federunterstuetzung** (z.B. Gasdruckfedern zur Gewichtsentlastung) ist passiv und erlaubt, muss aber sicher gekapselt sein.

### Keine Quetschstellen

- **Alle bewegten Gelenke** mit kosmetischen Abdeckungen oder Faltenbaelgen verkleiden, sodass keine Finger (auch nicht von Fans/Kindern) in den Mechanismus geraten koennen.
- **Scherkanten** an Parallelogramm-Linkages entweder mechanisch begrenzen oder vollstaendig abdecken.
- **Anschlaege gummieren** (Gummi-Puffer), damit Gelenke nicht hart und schnell zuschnappen.
- **Profil-Enden und Schnittkanten** entgraten, Gummikappen aufsetzen (siehe Abschnitt "Sicherheit (Convention)").

### Notausstieg

- **Ziel: vollstaendige Befreiung in unter 60 Sekunden**, auch wenn der Traeger gestuerzt oder benommen ist.
- **Handler muss die Sequenz blind koennen** - vorher mehrfach ueben.
- **Breakaway-Logik:** Aeussere Ruestung loest sich bei Aufprall, statt zu verletzen; tragende Schnallen sind Quick-Release.
- **Notausstieg-Sequenz (durch Handler):**
  1. Schultergurte oeffnen (Quick-Release).
  2. Arm-Exos abkoppeln bzw. Traeger Arme freistellen.
  3. Wirbelsaeulen-Rahmen vom Klettergurt loesen (Schaekel/Schnellverschluss).
  4. Bein-Riemen/Stelzen oeffnen, Traeger aus den Fussplatten heben.
  5. Helm abnehmen, Belueftung/Wasser sicherstellen.
- **Keine Werkzeuge** fuer den Notausstieg noetig - alles per Hand loesbar. Schrauben, die nur mit Werkzeug aufgehen, duerfen nicht im Notausstieg-Pfad liegen.
- **Handler Pflicht** bei jedem Exo-Build, unabhaengig von der Hoehe (siehe `Documentation/Guides/Sicherheit.md`, Abschnitt Handler).
