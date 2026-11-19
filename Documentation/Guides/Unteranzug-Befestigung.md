# Unteranzug und Befestigungssysteme

> **Level:** [A] Anfaenger | [F] Fortgeschritten | [P] Profi  |  **Varianten:** alle  |  **Voraussetzungen:** keine (Referenz/Optionen); fuer Custom-Suit Naehkenntnisse

Wie die Ruestung am Koerper befestigt wird und was man drunter traegt.

## Unteranzug-Optionen & Thermomanagement

Da eine geschlossene Ruestung (Foam oder 3D-Druck) stark isoliert und Waerme staut, ist ein durchdachter Unteranzug ueberlebenswichtig.

### Basis-Layer (Techsuit)

- **Feuchtigkeitsableitende Funktionskleidung:** Under Armour HeatGear oder Lycra/Spandex-Morphsuits sind Pflicht (niemals Baumwoll-T-Shirts tragen, da sie Schweiss aufsaugen und klamm werden).
- **Zweck:** Haelt die Haut trocken, verhindert Wundreiben an Ruestungskanten und erleichtert das An- und Ausziehen des schweren Anzugs.

### Kuehlung & Kondensationsschutz (PCM)

- **Phase Change Material (PCM) Kuehlwesten:** Fuer lange Convention-Tage wird eine PCM-Kuehlweste (z. B. von ThermApparel) empfohlen.
- **Vorteil:** PCM-Kuehlpacks kristallisieren bei einer konstanten Temperatur von ca. **14 Grad C (58 Grad F)**. Im Gegensatz zu Eispacks sind sie kuehl genug, erzeugen aber **kein Kondenswasser**. Dies ist extrem wichtig, um die im Suit verbaute Elektronik (Raspberry Pi, Arduino, LiPos) vor Feuchtigkeitsschaeden und Kurzschluessen zu schuetzen.

### Tragesystem & Ruestungsbefestigung

- **Dive Skin (Lycra, 1-2 mm):** Haltbarer als duenne Morphsuits, bietet leichte Polsterung.
- **Custom Rigging:** Ein Zwei-Schicht-System aus innerem Funktions-Layer und einer aeusseren Tragweste/Harness (z. B. H-Harness) zur verdeckten Montage der Ruestungspunkte.

## Befestigungssysteme

### Neodym-Magnete

Neodym-Magnete werden als passive Anlegehilfe eingeplant: Bauteil ansetzen,
ueber eine kurze Fuehrung ausrichten lassen und bei tragenden Baugruppen den
mechanischen Verschluss schliessen. Zum Abnehmen dient eine erreichbare
Zuglasche. Das ist ein Konstruktionsvorschlag; Halter und Magnetanzahl sind
noch nicht am realen Anzug erprobt.

Die digitale Umsetzung liegt als
[Magnetpaar mit vier CAD-Druckteilen](../../Design/Components/README.md#magnetpaar-zum-leichteren-anlegen)
vor: zwei Traeger mit wechselbaren, verschraubten Lochdeckeln, zwei
Fuehrungsstiften und einer Aufnahme fuer die Textil-Zugschlaufe. 10 x 3 mm
ist voreingestellt; eine Vergleichskonfiguration fuer 12 x 3 mm ist enthalten.
Diese Variante verwendet Magnetpaare mit formschluessiger Rueckhaltung ohne
Kleber. Sie hat konstruktionsbedingt einen Abstand zwischen den Magnetflaechen,
der bei der realen Halteprobe beruecksichtigt werden muss.

#### Zuordnung am Anzug

| Bauteil | Vorgesehener Magneteinsatz | Zusaetzliche Halterung |
| --- | --- | --- |
| Handrueckenplatte, kleine Blende | Abnehmbare leichte Kosmetikplatte ansetzen | Kurze Positionierlaschen; bei Verlustgefahr loesbares textiles Fangband |
| Serviceklappe | Deckel anziehen und geschlossen halten | Gefangenes Scharnier oder Fangband; erreichbare Griffkante |
| Schulterhaube, Oberarmplatte | Ausrichten an der bereits verbundenen Textilaufnahme | Gurt-/Scharnieraufhaengung traegt das Teil; vordere Sicherung bleibt bedienbar |
| Unterarm-/Schienbeinkassette | Geoeffnete Schalen beim Zuklappen zueinander fuehren | Scharnier und manuell loesbarer Rast-/Spannverschluss |
| Brust, Ruecken, Oberschenkel | Kosmetikplatten ausrichten, Fugen zusammenfuehren | Eigener Traeger, Gurte und mechanische Verschluesse tragen die Last |

#### Magnetgroesse und Gegenstueck

Fuer erste Vergleichsmuster **axial magnetisierte Scheiben mit 10 x 3 mm**
verwenden; **12 x 3 mm** ist eine zweite Versuchsgroesse, wenn Bauraum und
gewollte Loesekraft passen. Als Herstellerbeispiele dienen S-10-03-N (N42)
und S-12-03-N (N45). Das sind reale Abmessungen und Gueten, keine bereits
passende Lastbemessung. Nicht pauschal die staerkste Magnetisierung auswaehlen.
Siehe [10-x-3-mm-Datenblatt](https://www.supermagnete.de/data_sheet_S-10-03-N.pdf)
und [12-x-3-mm-Herstellerdaten](https://www.supermagnete.de/scheibenmagnete-neodym/scheibenmagnet-12mm-3mm_S-12-03-N).

Je Kontaktpunkt entweder zwei Magnete mit anziehender Polung oder einen Magneten
mit ferromagnetischem Stahlgegenstueck verwenden. Stahl muss tatsaechlich
magnetisch sein; Material und Dicke am Muster pruefen. Bei Magnetpaaren beide
zusammengehoerenden Kontaktflaechen vor dem Einbau markieren und trocken
zusammenstecken. Die benoetigte Stueckzahl verdoppelt sich gegenueber der Anzahl
der Kontaktpunkte; Magnet/Stahl braucht nur einen Magneten je Kontaktpunkt.

Die Shop-Haftkraft gilt fuer Zug senkrecht zur Kontaktflaeche unter den jeweiligen
Messbedingungen. Seitliches Verschieben, Abheben an einer Kante sowie Stoff,
Lack und Druckteilwaende zwischen den Kontaktflaechen muessen separat geprueft
werden. Aus einer Angabe wie "haelt 1,8 kg" folgt keine zulaessige Ruestungsmasse.
Grundlagen: [Haftkraft und Scherkraft](https://www.supermagnete.ch/faq/Wie-unterscheiden-sich-Haftkraft-und-Verschiebekraft-Scherkraft)
sowie [Einfluss von Abstand, Werkstoff und Oberflaeche](https://live-katalog.ganternorm.com/pdf/ganter/DE/magnete_intro.pdf?dispositiontype=attachment).

#### Halter, Fuehrung und Loeselasche

1. Magnet in eine separate Aufnahme mit mechanischer Rueckhaltung einsetzen,
   etwa eine Tasche mit verschraubtem Deckel. Die Aufnahme breit an Schale
   oder Gurtband befestigen; nicht den nackten Magneten auf dehnbares Lycra kleben.
2. Kurze, abgerundete Fuehrungslaschen mit Freigang gegen seitliches Verrutschen
   vorsehen. Sie muessen sich beim Oeffnen direkt freigeben und duerfen keinen
   geschlossenen Ring um Arm oder Bein bilden. Magnete ziehen die Kontaktflaechen
   zusammen; die Fuehrung richtet das Bauteil aus.
3. Kontaktabstand klein und reproduzierbar halten. Jede Schutzlage zwischen den
   Kontaktflaechen gehoert in die Halteprobe. Koerperseitig bleiben Magnet und
   Gegenstueck abgedeckt; keine freiliegenden Metallkanten auf der Haut.
4. Klebstoff passend zu Magnetbeschichtung und Halterwerkstoff waehlen und nach
   Herstellerangabe aushaerten lassen. Geeigneten Polymer- oder 2K-Epoxidkleber
   am Materialrest testen. Sekundenkleber ist keine pauschale Empfehlung;
   Heisskleber nicht fuer Neodym verwenden. Grundlage:
   [Herstellerhinweise zum Kleben](https://www.supermagnete.de/faq/Wie-kann-ich-Magnete-kleben).
5. Eine mit Handschuhen greifbare Textillasche an der kosmetischen Platte
   vorsehen. Sie hebt eine Kante kontrolliert ab, waehrend Scharnier oder
   Aufhaengung das Teil haelt. Bei Kassetten zuerst die mechanische Sicherung
   loesen; die Magnetlasche ersetzt deren Entriegelung nicht.

Fuer Gurtverbindungen kann alternativ ein fertiger magnetisch gefuehrter,
mechanisch verriegelnder Verschluss verglichen werden, etwa aus dem
[FIDLOCK-Komponentensystem](https://www.fidlock.com/components/en).
Die konkrete Ausfuehrung muss zu Gurtbreite, Last und erreichbarer
Entriegelungsrichtung passen; eine reine Magnetpaarung ist kein Rastverschluss.

#### Erste Anlegeprobe

Zuerst eine leichte Blende und eine Unterarmkassette mit echten Haltern bauen.
Als eigenes Versuchssetup zwei raeumlich getrennte Magnetkontakte gegen
Verdrehen vergleichen; Anzahl und Abstand danach anhand der Probe festlegen.
Die [kleine Materialauswahl](../../Materials/Mjolnir-Einkauf-Prototyp.md#magnetmuster-fuer-das-leichtere-anlegen)
ist fuer diesen Versuch gedacht.

- Reale Teilemasse, Kontaktabstand, Magnettyp, Polung und Halterrevision notieren.
- Am ungetragenen Aufbau senkrechtes Loesen, seitliches Verschieben und Abheben
  an der Lasche pruefen; Kraefte und Versuchsaufbau dokumentieren.
- 50-mal am Tisch ansetzen und loesen; danach auf gelockerte Magnete,
  Beschaedigungen, verrutschte Aufnahmen und veraenderte Loesekraft pruefen.
- Mit vorgesehenem Unteranzug, Polster und Handschuhen beide Seiten einzeln
  anlegen. Gerade die zweite Armschale mit bereits geruesteter Gegenhand pruefen.
- Erst nach unauffaelliger Tischprobe den vollstaendigen
  [An-/Ausziehversuch](Mjolnir-Selbstanziehen.md) durchfuehren; normale Bewegung
  darf keine Platte unbeabsichtigt loesen. Ausziehen bleibt stromlos moeglich.

50 Wiederholungen sind eine erste Funktionsprobe, kein Lebensdauer- oder
Lastnachweis. Bis zur dokumentierten realen Probe bleiben die Ergebnisse offen.

### Klettverschluss (Hook and Loop)

- **Industrial-Strength Velcro** oder **3M Dual Lock** (staerkste Option)
- Loop-Seite auf Ruestungs-Innenseite kleben, Hook-Seite auf Unteranzug naehen
- Zuverlaessig fuer leichtere Teile (Unterarme, Schienbeine, Schultern)

### Schnallen und Gurte

- **Quick-Release Schnallen** (ITW Nexus / Duraflex Stil, 25 mm Gurtband) fuer Brust, Ruecken, Oberschenkel
- **25 mm Nylon-Gurtband** durch Schlaufen in der Ruestung, verbunden mit **Klettergurt** oder **MOLLE-Guertel** an der Huefte
- **Huefte traegt die Last** - Schultergurte nur zur Stabilisierung

### Kombinations-Ansatz (Empfohlen)

| Funktion | Befestigung | Beispiel-Teile |
| --- | --- | --- |
| Last tragen | Gurte + mechanische Schnallen am Harness; Magnete als Anlegehilfe | Brust, Ruecken, Oberschenkel |
| Bewegliche Schale fuehren und schliessen | Textil-/Scharnieraufnahme + mechanischer Verschluss; Magnete zur Ausrichtung | Schultern, Oberarme, Unterarm-/Schienbeinkassetten |
| Leichte Kosmetik abnehmen | Gefangene Magnethalter + Positionierlaschen, gegebenenfalls Fangband | Handplatten, Blenden, Serviceabdeckungen |

## Polsterung

### Helm

- **Taktische/Airsoft-Helm-Padding-Kits** (Amazon, unter 15 EUR) - vorgeschnittene Memory-Foam Pads mit Klett-Rueckseite
- Dicke: 6 mm allgemein, bis 10 mm fuer Passform-Anpassung
- Mit **Klettstreifen** befestigen (abnehmbar fuer Reinigung und Repositionierung)
- **Kinnriemen** (Motorrad- oder Fahrrad-Stil) fuer Sicherheit

### Ruestung

- Innenseite mit **6 mm EVA-Foam** oder **Cosplay-Polster-Foam** auskleiden
- Mit **Kontaktkleber** oder **Spruehkleber** befestigen
- Fokus auf **Druckstellen**: Kanten an der Haut, Gewichtstragende Flaechen, Bewegungsbereiche

### Belueftung

- Helm: zwei 40 mm Luefter (Pflicht fuer Convention-Komfort)
- Koerper: **Lueftungsspalte** zwischen Ruestungsteilen lassen, besonders Achseln und Kniekehlen
