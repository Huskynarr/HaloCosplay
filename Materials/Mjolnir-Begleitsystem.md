# Begleitsystem: Beschaffung nach Plattformwahl

Aktuelle Produktzuordnung: [zentraler Produktkatalog](../web/products/) und
[Einkaufslinks mit Auswahlkriterien](Einkaufsliste-Links.md). Budgetwerte in dieser
Datei sind Planungswerte, keine aktuellen Shop-Angebote.

Stand: 2026-09-09. Ergaenzung zum
[Begleitkonzept](../Documentation/Guides/Begleitroboter-Integration.md).
Diese Positionen sind optional und werden nicht automatisch in das generische
Anzugbudget eingerechnet. Vorhandene Drohnen/Roboter zuerst pruefen; Leihe oder
Vorortvorfuehrung kann den ersten Folgetest ermoeglichen.

## 1. Originalsystem

| Position | Menge | Auswahl und Kostenstatus |
| --- | --- | --- |
| Roboter mit nativem Sender-Folgen | 1 | Go2 Pro ist ein Kandidat: Hersteller nennt 2800 USD ohne Steuern/Versand. Kein deutscher Endpreis. Alternative CyberDog nach Versionspruefung; kein verifiziertes aktuelles Angebot. |
| Passender Originalsender | 1 | Exakte Artikelnummer, Firmware und Lieferumfang schriftlich bestaetigen. Separater Preis unbekannt; nicht automatisch als enthalten annehmen. |
| Originalsteuerung fuer Bedienperson | 1 Satz | Mit Modell und gleichzeitigem Sender-Folgebetrieb kompatibel; Stopptastenfunktion vor Kauf demonstrieren lassen. |
| Originalakku, Ladegeraet, Transport | nach Einsatz | Lieferumfang pruefen; benoetigte Ersatzakkus erst nach gemessener Laufzeit festlegen. |
| SDK-faehige Edition | alternativ | Go2 EDU/X nur nach API-Pruefung; Entwicklerzugang und Preisangebot einholen. Kein 1600-USD-EDU-Preis aus dem Einstiegsmodell ableiten. |
| EngineAI T800 | spaeter, separat | Demo/Leihe und Herstellerbetreuung zuerst pruefen. Preis, Lieferbarkeit und Sender-Follow-Funktion hier nicht bestaetigt. |
| DJI Mavic Air 2 samt Originalfernbedienung | optional fuer Aussendrehs | Vorhandenes System bevorzugt. ActiveTrack benoetigt keinen zusaetzlichen Anzug-UWB-Sender. Eigener SDK-Adapter ist nicht enthalten. |

Preis-/Ausstattungsquelle: [Unitree Go2](https://www.unitree.com/go2/).
Fuer Xiaomi und EngineAI gelten die Quellen und Einschraenkungen im Begleitguide.
Es wurden keine Anfragen versendet und keine Geraete bestellt.

## 2. Einbauzubehoer fuer einen nativen Sender

Die folgenden EUR-Werte sind **eigene Material-Planwerte**, keine recherchierten
Kaufangebote. Sie gelten fuer einen ersten Senderhalter und schliessen Roboter,
Sender, Arbeitszeit und zertifizierte Stoppsysteme aus.

| Position | Menge | Planwert |
| --- | --- | --- |
| Nichtmetallische Funkkassette, PETG/ASA oder geeignetes Fertiggehaeuse | 1 | 15-35 EUR |
| Gurtaufnahme, Polster, Schrauben, werkzeugloser Verschluss | 1 Satz | 15-30 EUR |
| Geeignetes Ladekabel, Zugentlastung und Beschriftung | 1 Satz | 10-25 EUR |
| Summe erster mechanischer Einbau | | 40-90 EUR |

Keine zusaetzliche Powerbank erforderlich, solange der Originalsender seinen
eigenen Akku nutzt. Ein Touchscreen hinter einer geschlossenen Panzerplatte
ist nicht bedienbar; Tasten und Freigaben muessen am fertigen Halter erreichbar
bleiben. Befestigungslasten und Luft-/Funkraum am konkreten Teil pruefen.

## 3. Eigenentwicklung nur bei nachgewiesenem Bedarf

| Baustein | Zweck | Vor Beschaffung offen |
| --- | --- | --- |
| 2 x Qorvo DWM3001CDK | Distanzversuch mit Tag und Gegenstelle | Aktuelles Angebot, benoetigte SDK/Firmware; noch keine Peilung und kein Roboteradapter |
| AoA-System oder geeignete Mehrpunktortung | Relative Richtung zusaetzlich zur Distanz | Messgeometrie, Kalibrierung, mechanische Basis und API; kein generischer Fertigsatz festgelegt |
| Rechner am Roboter | Lokalisierungsfusion und eigene Navigation | Erst benoetigte SDK-Plattform und vorhandene Rechenleistung pruefen |
| Zusaetzliche Umgebungssensorik | Nicht erfasste Hindernisse/Abgruende | Bestehende Sensoren, SDK-Zugriff und reale Luecken messen |
| Getrennte Telemetrieverbindung | Status ins Helm-HUD | Hersteller-API, Sitzung/Authentisierung und Datenalter; lokaler UDP-Democode reicht fuer Livebetrieb nicht aus |
| Herstellerkompatibles Stoppsystem | Unabhaengiger Abbruch | Modellbezogenes Stoppverhalten; kein beliebiges ESP32-Relais als Ersatz |

[Qorvo DWM3001CDK](https://www.qorvo.com/products/ek/DWM3001CDK) ist eine
Entwicklungsplattform. Eine vorhandene UWB-Frequenz oder FiRa-Unterstuetzung
bestaetigt keine Kompatibilitaet mit einem proprietaeren Robotersender.

## 4. Datenblatt fuer Angebot oder Vorfuehrung

Vor einer Beschaffungsentscheidung werden folgende Angaben gesammelt:

- Modell/Edition, Firmware, App und Originalsender-Artikelnummer.
- Nativer Folgemodus, einstellbare Abstaende/Tempi und Verhalten bei Zielverlust.
- Verhalten bei Hindernis, niedrigem Akku, ausgeschaltetem Sender und Wiederverbindung.
- Bedienperson kann Folgebewegung mit Originalsteuerung jederzeit beenden.
- SDK-Zugang fuer Akku, Betriebszustand, Distanz und Peilung jeweils einzeln;
  kein allgemeines "SDK vorhanden" als Ersatz fuer diese Zusagen.
- Kauf-/Leihpreis mit Lieferumfang, Abgaben, Versand, Ersatzteilen und Support.
- Bei Ausstellung: erlaubter Betriebsbereich und benoetigte Betreuung.

Die Ergebnisse kommen in das jeweilige Projekt unter `build/`; fehlende Werte
bleiben unbekannt. Die konkrete Veranstaltung wird separat abgestimmt.
