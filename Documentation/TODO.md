# MJOLNIR-Projektaufgaben

Diese Liste wird je Aufbau verwendet. Ein Profilname, ein Softwaretest oder eine
fertige Anleitung ist kein bestandener Hardwaretest. Nachweise gehoeren zu
Projekt, Profil und Bauteilrevision. Details im
[Konfigurations-Workflow](Guides/Mjolnir-Konfiguration.md).

## Bereits digital umgesetzt

- [x] Entwicklungsziel vom 2026-11-17 dokumentiert: [Lastpfad zum Boden](Guides/Exoskelett.md#3a-neues-entwicklungsziel-ruestungslast-zum-boden) und [optischer Spiegel-HUD-Versuch](Guides/Elektronik-AR-Display.md#11-neue-referenz-diy-brille-und-spiegel-hud); noch keine entsprechende Hardware
- [x] [Baupaket-Generator](Guides/Mjolnir-Baupaket.md) mit getrennten Projekten und Revisionen
- [x] Referenzkatalog mit 23 Bauteilen je Variante und kontrolliertem Modellimport
- [x] [Detailgestaltung](Guides/Mjolnir-Detailgestaltung.md) fuer Silhouette, weiche Uebergaenge, Visier und Finish
- [x] Sechs editierbare [CAD-Komponentenproben](../Design/Components/README.md), inklusive gefangenem Magnetpaar mit Fuehrung und Zuglasche
- [x] [Technikrechner](Guides/Mjolnir-Technik-Auslegung.md) fuer Schienen, Akkus, Scharniere und Staender
- [x] Erzeugbare Bauteil-, Bewegungs- und Finishprotokolle sowie Montage-/Transportablauf
- [x] [Einbauplan](Guides/Mjolnir-Einbauplan.md) mit separater Komfort-/Effektversorgung und konfigurierbaren Verbrauchern
- [x] Acht bewegliche Clamshell-Bauraumhuellen und [Selbstanzieh-Prueffolge](Guides/Mjolnir-Selbstanziehen.md)
- [x] Thermalrechner fuer einzelne LED-Kuehlkoerper und gemessene Luftkanaele
- [x] Sechs parametrische [Einbaumodelle und elektrische Referenzschaltplaene](Guides/Mjolnir-CAD-Schaltplaene.md) mit eigenem Quellen-/STL-Export

Die folgenden Aufgaben betreffen den realen Aufbau. Sie bleiben offen, auch
wenn digitale Vorlagen oder passende Rechenwerkzeuge bereits vorhanden sind.

## 1. Projekt und Referenz

- [ ] Eigenes leeres Profil anlegen und eindeutig benennen
- [ ] Ruestungsreferenz waehlen; Spiel, Variante und gewollte Abweichungen dokumentieren
- [ ] Referenzansichten und nutzbares Detailmodell beschaffen
- [ ] Materialweg, Betriebsumfang und optionale Ausstattung festlegen
- [ ] Verfuegbare Werkzeuge und Fertigungsmoeglichkeiten erfassen
- [ ] Eigene BOM mit Mengen, Bestandsmaterial, Preisen und Reserve anlegen

## 2. Masse und Passform

- [ ] Alle 32 Generatorfelder sowie zusaetzliche Fertigungsmasse aufnehmen
- [ ] Datum, Kleidung und Messendpunkte dokumentieren; beide Seiten separat messen
- [ ] Schuh-Aussenlaenge, -breite und zusaetzliche Spann-/Knoechelhoehe aufnehmen
- [ ] Profil ohne synthetische Ergaenzungen berechnen
- [ ] 1:1-Torso-Mockup fuer Eintritt, Sitzen und Schulterfreiheit bauen
- [ ] Leichten Helm mit Sicht-/Visiermuster pruefen
- [ ] Unterarm-/Beinpasslehren und dynamische Gelenkfreiraeume pruefen

## 3. Mechanik und Traeger

- [ ] Fuer Bodenrahmen B01-B05: Teilmassen/Schwerpunkte und zusaetzliche Gelenk-/Bein-/Fussmasse aufnehmen
- [ ] Bodenrahmen-Kinematik fuer Huefte, Knieausgleich, Knoechel und Abrollen entwickeln; Gelenke und Aufnahmen fachlich bemessen
- [ ] Ungetragenen Lastpfad im beidbeinigen und einbeinigen Stand mit Ersatzmassen pruefen
- [ ] Leichten Kinematik-Prototyp und eigenen Einstieg mit tragenden Fussaufnahmen pruefen
- [ ] Entlastung im Stehen und Gehen getrennt messen; Rahmenmasse und Restlast am Koerper bilanzieren
- [ ] Eigenen Traeger und reale Lastpfade auslegen
- [ ] Tuerlagerung, Seitenfuehrung, Verschluesse und Gegenplatten bemessen
- [ ] Eine komplette Tuereinheit ungetragen pruefen
- [ ] Handzugang, Parkpositionen, Anschlaege und werkzeuglose Trennung nachweisen
- [ ] Helm-Torso-Schulter-Prototyp testen
- [ ] Je eine Arm-/Beinkassette bauen, Gegenseite individuell anpassen
- [ ] Magnethalter am realen Untergrund montieren; Halte-/Abhebekraft, 50 Tischzyklen und beide Gegenhaende mit Handschuhen pruefen
- [ ] Drei Anzieh- und stromlose Ausstiegsproben dokumentieren
- [ ] Letzte Armschale, beide Gegenhaende, Schuhcover und alle Innengurte ohne Durchschluepfen pruefen
- [ ] Powerbankwechsel, OEM-Neblerbedienung und Helmkabel mit Handschuhen selbst erreichen

## 4. Detailmodelle und Fertigung

- [ ] Individuelle Innenkonturen und referenzgemaesse Aussenformen zusammenfuehren
- [ ] Schraub-/Gurtaufnahmen, Polster, Visier- und Luefterhalter konstruieren
- [ ] Material und Fertigungsparameter je Baugruppe dokumentieren
- [ ] Modell-/Slicerdateien mit Teil-ID und Revision ablegen und Register mit `suit_assets.py` pruefen
- [ ] Rohbau montieren, wiegen und real testen
- [ ] Finishmuster erstellen; erst nach Passprobe gesamte Ruestung lackieren
- [ ] Waschbaren Unteranzug, Handschuhe und flexible Uebergaenge fertigstellen

## 5. Ausstattung nach Auswahl

- [ ] Komfortstrom und Effektsteuerung getrennt planen; realen Strombedarf messen
- [ ] Bei Elektronik: Board, Sensoren, Schaltplan, Kabelbaum und Versorgung festlegen
- [ ] Bei Licht: Positionen, Helligkeit und Spitzenstrom pruefen
- [ ] Bei Highpower-RGB: Konstantstrom, Reset-Aus, Waermeweg und Foto-Banding pruefen
- [ ] Komfortluft, Elektronikabluft und trockene Duesenluft am Gesamtaufbau getrennt testen
- [ ] Bei Audio: Sprachverstaendlichkeit und Rueckkopplung mit Helm pruefen
- [ ] Bei HUD: Sicht ohne Anzeige sowie Befestigung und Laufzeit pruefen
- [ ] Spiegel-HUD: Display/Abbildungsoptik/Combiner als Tischmuster auf Fokus, Eyebox, Durchsicht und Helligkeit pruefen
- [ ] Spiegel-HUD: wegklappbare Helmkassette nach optischer Passprobe konstruieren; Doppelbilder mit Goldvisier pruefen
- [ ] Bei Exoskelett: Hersteller-Passmasse, Anprobe und getrennte Integration nachweisen
- [ ] Sechs-Module-Zielbild umsetzen: Verschluss kaufen und Lochbild eintragen, Armmodul drucken und pruefen, danach Bein, Helm, Torso (Bauraummodelle aller sechs Module vorhanden; Laschen unbemessen, Torso ohne Traeger) ([Guide](Guides/Mjolnir-Selbstanziehen.md#0-zielbild-sechs-module-zum-zuklemmen))
- [ ] Eigenbau-Beinantrieb X01: Mechanik konstruieren und Nachweisfolge P1-P7 durchlaufen ([Guide](Guides/Exoskelett-Eigenbau.md)); bisher nur Steuerlogik und Host-Tests
- [ ] Bei Show-Aktorik: eigenes ungetragenes Testmodul und Ausfallverhalten entwickeln
- [ ] Optional: Sprachsteuerung + Kamera-Erkennung auf Pi 5 (siehe [Elektronik-Sprachsteuerung.md](Guides/Elektronik-Sprachsteuerung.md))
- [ ] Optional: Shield-Hit, Handler-Alert, Trink-Erinnerung (siehe [Elektronik-Show-Praxis-Module.md](Guides/Elektronik-Show-Praxis-Module.md))
- [ ] Optional: Indoor-Navigation fuer Gamescom/IFA (siehe [Elektronik-Indoor-Navigation.md](Guides/Elektronik-Indoor-Navigation.md))
- [ ] Optional: Schubduesen-Effekt und Nebler aufbauen (siehe [Elektronik-Schubduesen.md](Guides/Elektronik-Schubduesen.md))

## 6. Betrieb und Ausstellung

- [ ] Vollstaendigen Aufbau auf Bewegung, Sicht, Waerme und Laufzeit pruefen
- [ ] Notausstieg mit Handschuhen, stromlos und bei blockierter Tuer pruefen
- [ ] Wartungszugang und Ersatzteile festlegen
- [ ] Bei Ausstellung: Staender, Aufnahmen und Kippsicherung pruefen
- [ ] Bei Ausstellung: Projektanzeige und Datenquelle konfigurieren
- [ ] Transportaufnahmen, Kisten und Packliste erstellen
- [ ] Konkrete Veranstaltungsausgabe und Stand-/Besuchsmodus festlegen
- [ ] Passende Veranstalterunterlagen beschaffen und Vorfuehrung abstimmen
- [ ] Betreuungsrollen und geprobten Tagesablauf festhalten

## 7. Optionales Begleitsystem

- [x] [Plattformvergleich und Senderkassette](Guides/Begleitroboter-Integration.md) mit Herstellerquellen dokumentiert
- [ ] Konkrete Edition, Firmware und kompatiblen Originalsender bestaetigen
- [ ] Nativen Follow-/HOLD-Ablauf mit Originalsteuerung ohne Ruestung erproben
- [ ] Senderhalter vermessen und Funkabschattung mit vollstaendiger Ruestung testen
- [ ] Lokale Stopplogik, Zielverlust, Wiederverbindung und Bremsweg nachweisen
- [ ] Fuer eigene SDK-Integration: Datenfelder und Bewegungs-APIs am Modell pruefen
- [x] HUD-Mehrschreiber geloest: alle Bruecken schreiben ueber `hud_state.merge()` (Dateisperre + atomarer Ersatz)
- [ ] Datenalter beim Prozessausfall vor Live-Anbindung loesen
- [ ] Drohnenablauf mit Pilot und ausgeschaltetem Anzugnebel getrennt pruefen
- [ ] Vorfuehrflaeche, Betreuung und konkrete Veranstalterbedingungen dokumentieren

## Nachweise

[Prototypenfolge](../BuildGuides/Armor/Mjolnir-Prototypen.md),
[Abnahmebogen](../Tests/TestReports/Mjolnir-Abnahme.md) und
[Nachweisbericht](../Progress/Mjolnir-Readiness.md).
Die versionierten Beispiele sind kein Abschlussnachweis fuer neue Projekte.
