# Ausstellungs- und Vorfuehrbetrieb

Ziel ist ein originalgetreues Fanprojekt mit nachvollziehbarer Technik. Ein
Standplatz, eine Partnerschaft oder eine Veranstalterfreigabe ist nicht zugesagt.
Die gewaehlte Veranstaltung und Ausgabe muessen vor der Einsatzplanung feststehen.

## Betriebsarten nach Projektkonfiguration

Das Profil unterscheidet `wearable`, `exhibition` und `both`. Die folgenden
Betriebsarten gelten nur fuer den tatsaechlich geplanten Umfang; Wartung ist
bei jedem Aufbau erforderlich. Eine Ausstellungsauswahl bestaetigt weder
Tragbarkeit noch die Eignung eines vorhandenen Staenders.

| Modus | Ausstattung | Bedienung und Grenze |
| --- | --- | --- |
| Getragen | Manueller Einstieg, Sicht, Lueftung, Stimme, dezente LEDs | Begleitperson, kurze geplante Auftritte, stromloser Ausstieg |
| Ungetragen ausgestellt | Eigener Staender, geoeffnete Mechanik, Monitor | Betreute Vorfuehrung; Bewegungsraum getrennt vom Publikum |
| Wartung | Abgeschaltete Antriebe, getrennte Energiequellen, abgestuetzte Panels | Zugang nur fuer eingewiesene Personen; nach Eingriff erneute Funktionsprobe |

Die Web-Anzeige steuert keine Bewegung, bestaetigt keine sichere Verriegelung
und ersetzt keine hardwareseitige Abschaltung. Serien-Exoskelette nicht aus
Showsoftware ansteuern. Ein Antriebsstopp darf notwendige Lueftung und den
mechanischen Ausstieg nicht blockieren. Neustart darf keine Bewegung ausloesen.

## Gestaltung fuer gamescom und IFA

Gamescom-Schwerpunkt: geschlossene Halo-Silhouette, Fotoauftritt und kurze
Ankleidedemonstration. IFA-Schwerpunkt: geoeffneter Aufbau, nachvollziehbarer
Lastpfad, modulare Fertigung, reale Telemetrie und dokumentierte Grenzen.
Beides sind Ausstellungskonzepte, keine bestaetigte Programmeignung.

Exponatbeschriftung: "MJOLNIR Fanprojekt - mechanisch oeffnende Cosplay-Ruestung.
Entwicklungsstand und Messdaten siehe Anzeige. Keine Schutzruestung."
Fiktive Schild-/Reaktorwerte nur als erkennbarer Spieleffekt. Keine behauptete
Kraftverstaerkung, Traglast oder Einsatzdauer ohne passenden Messnachweis.

## Vorfuehrablauf, Planwert drei Minuten

1. 0:00-0:30: Geschlossenen Anzug zeigen; Originalvorlage und Eigenentwicklung benennen.
2. 0:30-1:30: Ungetragenes Modul am gesicherten Staender manuell oeffnen;
   Zuschauer ausserhalb der Schwenkhuelle. Mechanik und Trennung zum Traeger erklaeren.
3. 1:30-2:30: Temperatur-/Akkumessung oder deutlich markierten Beispieldatensatz
   auf dem Monitor zeigen. Datenquelle und Alter bleiben sichtbar.
4. 2:30-3:00: Modul schliessen und mechanisch pruefen; Fragen. Bei Stoerung auf
   unbewegtes Exponat und vorbereitete Bilder wechseln.

Zeitangaben sind Ablaufziele. Im getragenen Modus erfolgt keine automatische
Oeffnungssequenz. Kein ungeprueftes Dauercycling oder unbeaufsichtigte Aktorik.

## Infrastruktur und Tagesbetrieb

- Standflaeche aus geoeffneter Schwenkhuelle, Betreuerplatz und Zugang ableiten.
  Keine pauschale Quadratmeterzahl als ausreichend deklarieren.
- Strombedarf aus gemessenen Verbrauchern und Spitzenstroemen auflisten;
  Netzanschluss, zugelassene Netzteile und Ladestelle mit Standplanung abstimmen.
- Offline-Laptop/Monitor, lokale Kopie der Inhalte und Ersatzversorgung vorsehen.
- Zwei benannte Rollen: Vorfuehrung und Betreuung/Unterstuetzung. Bei fehlender
  Betreuung nur statische, gesicherte Ausstellung.
- Tagesbeginn: Befestigungen, Leitungen, Visier, Luefter, Ausstieg und Standfestigkeit.
  Vor jeder Demo Sichtpruefung; nach Transport oder Stoerung erneute Funktionsprobe.
- Wartungssatz: identifizierte Ersatzverschluesse, Gurte, Luefter, Stecker,
  geeignetes Werkzeug und dokumentierte Austauschfolge.
- Transport: Module mit gepolsterten Aufnahmen, verriegelte bewegliche Teile,
  Kistenliste, Lade-/Akkutransport nach den tatsaechlichen Komponenten/Transportwegen.
- Tragezeiten stufenweise erproben; Pausen nach realer Belastung festlegen.
  Bei Sichtverlust, Hitzeproblemen, Druckschmerz oder unklarer Mechanik abbrechen.

## Veranstalterpaket vor Einreichung

Fotos geschlossen/offen, Abmessungen beider Zustaende, Gesamtmasse und Standlast,
Strom-/Akkuliste, Bewegungsbeschreibung, Schutzeinrichtungen, Betriebsablauf,
Transport-/Aufbauplan, Ansprechpartner und Testnachweise zusammenstellen.
Branding, gezeigte Assets und Audio fuer die konkrete Nutzung klaeren.
Keine E-Mails oder Anmeldungen werden durch dieses Dokument versendet.

[IFA-Serviceportal](https://www.ifa-berlin.com/portal): technische Standrichtlinien,
Health & Safety und Einreichungsinformationen, abgerufen 2026-09-08. Fuer gamescom
sind die konkreten Kostuem-/Ausstellerregeln noch zu beschaffen. Es gibt noch
keine Freigabe fuer eine der beiden Veranstaltungen.

## Lokale Messeanzeige

[Anleitung zur Anzeige](../../Code/Exhibition/README.md). Die Anzeige startet ohne
Messwerte. Beispieldaten und importierte Mess-Snapshots sind unterscheidbar;
veraltete Daten werden ausgeblendet. Keine Internetverbindung, Cloud oder
Antriebsverbindung erforderlich.

[Zusaetzliches Messebudget](../../Materials/Mjolnir-Messebudget.md): Stand, Logistik,
Praesentation und Fachpruefung sind in der bisherigen Basis-BOM nicht voll enthalten.
