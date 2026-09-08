# MJOLNIR: Bauphasen und Abnahme

Diese Folge macht den Systementwurf praktisch pruefbar. Alle physischen
Ergebnisse sind derzeit **offen**; vorhandene Dokumentation bedeutet nicht,
dass eine Baugruppe schon gefertigt oder bestanden ist.

## Phasen mit nachvollziehbarem Ergebnis

| Phase | Arbeit | Ergebnis fuer naechste Phase | Aufwand als Planansatz |
| --- | --- | --- | --- |
| P0 | Masse im Tragezustand erfassen, Silhouette festlegen | Datierter Messsatz ohne offene kritische Masse | 2-4 h |
| P1 | 1:1-Torso aus Karton, Seitenfuehrungsattrappen, Schulter-/Bauchkontur | Eintritt, Sitzen, Arme bewegen, Freigabe von Hals und Gesicht | 8-16 h |
| P2 | Einzelne Fronttuer auf Tisch pruefen | Gewicht, Lagerung, Verschluss, Parkposition und Trennstelle dokumentiert | 12-24 h |
| P3 | Leichter eigener Traeger und unmotorisierte Torso-Probe | Lastverteilung, Erreichbarkeit, Ausstieg ohne Station | 16-32 h |
| P4 | Eine Arm-/Beinkassette, dann gespiegelte Gegenseite individuell | Kein Zwang ueber Gelenke, Kassetten bleiben vormontiert | 20-40 h |
| P5 | Anziehstation und kompletter unmotorisierter Rohbau | Wiederholbares Anziehen ohne Anschrauben einzelner Teile | 12-24 h |
| P6 | Serien-Exoskelett separat anprobieren, falls weiterverfolgt | Originalpassform und gemeinsame Gurt-/Bewegungsprobe bestanden | Nach Termin und Geraet |
| P7 | Endkonturen, Drucksegmentierung, Oberflaeche und Licht | Rohbau bestanden, Elektrik und Wartungszugang geprueft | 60-140 h |
| P8 | Gestaffelte Tragprobe und Generalprobe | Dokumentierte Passform und Grenzen fuer den konkreten Einsatz | Mindestens mehrere getrennte Termine |
| P9 optional | Motorisches Dekorpanel auf Tischmodell | Eigener Mechanik-/Ausfallnachweis vor koerpernahem Einsatz | Separates Projektbudget |

Die Stunden sind Schaetzungen fuer Handarbeit; Drucklaufzeiten, Lieferzeit,
Fehlversuche und professionelle Konstruktionspruefung kommen hinzu. Kein
Fertigstellungstermin wird aus ihnen automatisch abgeleitet.

## Fertigungsreihenfolge

Zuerst nur Passlehren und Rohmodelle. Endgueltige Helm- und Torsoteile werden
nicht vor dem Grund-Mockup fertig lackiert. Die bisherigen generischen
Foam-/Druckguides gelten fuer Materialverarbeitung, nicht als bereits
validierte Schnittfuehrung fuer diesen Anzug.

1. Karton und einfache Verschlussattrappen fuer Eintrittsquerschnitt.
2. Getrennte Scharnier-/Fuehrungsprobe mit groesserer, gut greifbarer Lasche.
3. Eigener Traeger mit schrittweise zugeladener, bekannter Ruestungsmasse.
4. Unlackierte kosmetische Segmente; Schalenhalter und Parkanschlaege montieren.
5. Scharniere nicht ueber Druckteil-Schweiss-/Klebenaehte allein belasten;
   geeignete Montageunterlagen nach der Lastpruefung verwenden.
6. Kabel und Serviceklappen am vollstaendigen unmotorisierten Rohbau planen.
7. Erst nach bestandenen Bewegungs-/Ausstiegsproben Oberflaechen fertigstellen.

## Abnahmeblatt je Iteration

Kopie als `Tests/TestReports/Mjolnir-YYYY-MM-DD.local.md` ablegen; private
Messdaten bleiben lokal. Bei gewuenschter Veroeffentlichung zuerst die
Koerpermasse entfernen. Eine Fehlprobe wird mit Fehler und Korrektur behalten.

| Protokollfeld | Eintrag |
| --- | --- |
| Datum / Versionsstand / Pruefende | OFFEN |
| Profildatei und Messdatum | OFFEN |
| Getestete Baugruppen | OFFEN |
| Masse real, je Baugruppe und insgesamt | OFFEN |
| Serien-Exoskelett Modell / Groesse / Originaleinstellung | OFFEN oder NICHT VERWENDET |
| Unteranzug / Polster / Schuhe | OFFEN |
| Fotos des ungetragenen Aufbaus und Messpunkte | OFFEN |
| Festigkeitspruefung: Lastfaelle, Methode, Ergebnis, Verantwortliche | OFFEN |

## Funktionspruefungen

| ID | Versuch | Bestehen bedeutet | Ergebnis |
| --- | --- | --- | --- |
| FIT-01 | Torso betreten und verlassen | Kein Verdrehen/Zusammendruecken der Schultern; kein Halskontakt | OFFEN |
| FIT-02 | Sitzen, Aufstehen, Oberkoerper leicht drehen | Bauchlamellen weichen aus, Brust wird nicht nach oben geschoben | OFFEN |
| FIT-03 | Arm heben, beugen, Hand zur Visor-/Verschlusslasche | Eigene noetige Bewegung ohne harte Kollision erreichbar | OFFEN |
| FIT-04 | Gehen, kontrolliert wenden, Sitzen | Kein Knie-/Hueftzwang, Schuhe bleiben frei auf dem Boden | OFFEN |
| MECH-01 | Tueren/Fuehrungen 50-mal ungetragen oeffnen/schliessen | Kein Klemmen, Losdrehen, Riss oder ungewolltes Schliessen | OFFEN |
| MECH-02 | Verschluss und Parkposition | Formschluessig gehalten, manuell eindeutig freigebbar | OFFEN |
| MECH-03 | Leichtes Anstossen am ungetragenen Aufbau | Keine unkontrollierte Panelbewegung; Prueflast vorher festlegen | OFFEN |
| ENTRY-01 | Dreimal komplett an-/ausziehen | Ohne Schrauben/Werkzeug; Ziel Anziehen jeweils <=5 min | OFFEN |
| EXIT-01 | Gesamte Ruestung stromlos freigeben | Sicht/Atmung zuerst, Ziel vollstaendig <=60 s | OFFEN |
| EXIT-02 | Eine Tuer blockiert, separate Trennstelle nutzen | Andere Freigaben funktionieren; Last kontrolliert gehalten | OFFEN |
| EXIT-03 | Sitzend und mit Handschuhen | Laschen erreichbar und eindeutig zu bedienen | OFFEN |
| ELEC-01 | Komfort/Effekte/Display einzeln ausfallen lassen | Mechanischer Ausstieg immer moeglich; Ausfall sichtbar | OFFEN |
| EXO-01 | Originalgeraet plus eigener Traeger | Keine Gurt-/Sensor-/Motor-/Kabelkollision | OFFEN |
| EXO-02 | Originalakku und Abschaltung bedienen | Von aussen ohne Ruestungsdemontage moeglich | OFFEN |
| USE-01 | Akkuwechsel, Schuerze/Toilette, Helm abnehmen | Vorgesehene Ablaufe ohne Vollzerlegung | OFFEN |

50 Zyklen sind ein frueher Funktionsscreen, kein Lebensdauer- oder
Festigkeitsnachweis. Eine begrenzte Tragprobe beginnt kurz und wird nur bei
unauffaelligem Ergebnis verlaengert. Druck, Taubheit, Atemeinschraenkung,
Unsicherheit, starke Erwaermung oder unerwartete Bewegung beenden die Probe.
Keine Sturzprobe mit einer Person und kein Lasttest am angezogenen System.

## Aenderungsregel

Eine Aenderung an Gurtlage, Scharnierachse, Verschluss, Polster, Masse oder
Seriengeraet setzt die dazugehoerigen Tests wieder auf OFFEN. Softwaretests
belegen nur die Berechnungslogik, nicht die Eignung des getragenen Anzugs.
