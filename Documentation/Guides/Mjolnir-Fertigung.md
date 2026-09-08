# Von der Referenz zum tragbaren Bauteil

## Aufbau und Verantwortungsgrenzen

Referenz, Materialweg und Umfang kommen aus dem
[Projektprofil](Mjolnir-Konfiguration.md). Foam, Druck und Hybrid benoetigen
jeweils eigene Verstaerkungs-, Klebe- und Verbindungsversuche. Die gleiche
Bauraumgeometrie bedeutet keine gleiche Festigkeit. Nur ausgewaehlte
Elektronik-/Exoskelettmodule in die Fertigungsplanung aufnehmen.

Jede Baugruppe besteht aus Aussenhaut, lokalem Verstaerkungsrahmen,
austauschbarer Verbindung und Polster-/Textilabschluss. Der eigene Ruestungstraeger
haelt die Schalen. Das optionale Serien-Exoskelett bleibt ein separat anzupassendes
Herstellergeraet mit eigener Versorgung. Eine Gewichtsableitung zum Boden ist
nicht nachgewiesen und nicht Teil der Basiskonstruktion.

Der aktuelle OpenSCAD-Entwurf bleibt eine Bauraumstudie. Keine leere STL und kein
Konzeptkoerper wird als fertiges Halo-Druckteil bezeichnet.

## Baugruppen und Fertigungsentscheidungen

| ID | Baugruppe | Konstruktionsvorgabe | Erster realer Nachweis |
| --- | --- | --- | --- |
| K01 | Helm | Teilbare Schale, separat wechselbares Visier, Kopfpolsterung, freie Ohren; HUD nach Sichtprobe | Leichter Passhelm mit Visiermuster |
| T01 | Torso | Eigener Traeger; Seitenfluegel und Frontschalen als vormontierte Einheit | 1:1-Mockup mit echtem Unteranzug |
| S01/02 | Schultern | Beweglich am Traeger, Freiraum zum Helm, keine Last am Hals | Armheben und Kopfdrehung |
| A01/02 | Ober-/Unterarme | Schalen aufklappbar, Verschluss ausserhalb Ellbeuge; Kabelfuehrung separat | Eine komplette Armkassette |
| H01 | Huefte | Flexible Uebergaenge, Sitz- und Toilettenzugang, kein starrer Ring ueber Leiste | Sitzen und freier Schritt |
| L01/02 | Beine | Getrennte Oberschenkel-/Schienbeinmodule, Kniekehle frei | Gehen, Stufe, Richtungswechsel |
| F01/02 | Schuhe | Abnehmbare Cover am normalen Schuh, Sohle frei | Abrollen ohne Schleifen |
| U01 | Unteranzug | Waschbare Textilbasis, strukturierte flexible Auflagen, zugaengliche Verschluesse | Bewegung unter kompletter Rohruestung |
| D02 | Ausstellungsstaender | Eigene Struktur, kein Mensch als Dauersupport, Sicherung gegen Kippen | Ungetragene Last-/Kipppruefung |

ID D02 bezeichnet den separat zu entwickelnden Messe-Staender. Die Basis-BOM
enthaelt unter D01 nur die Anziehstation; deren Eignung als Exponattraeger ist
nicht nachgewiesen. L/R kennzeichnet die individuell angepassten Seiten.

## Schnittstellen, die vor Kaufteilen feststehen muessen

| Schnittstelle | Eingaben | Zeichnung und Pruefung |
| --- | --- | --- |
| Traeger / Torso | Reale Masse, Schwerpunkt, Gurtlage, dynamische Lastannahmen | Lastpfad, Verstaerkung, Ausreiss-/Schlupfversuch |
| Seitenfuehrung / Fronttuer | Schwenkhuelle, Hub, Tuergewicht, Verkanten | Zwei Endlagen, Anschlaege, Halter, Quetschstellen |
| Handschliesser | Zugrichtung, Zugang innen/aussen, Handschuhbedienung | Sekundaere Sicherung gegen unbeabsichtigtes Oeffnen, manuelle Entriegelung |
| Kabel / Schale | Biegeradius, Strom, Bewegung, Serviceweg | Zugentlastung, Verpolschutz, werkzeuglose Trennstelle |
| Modul / Staender | Aufnahmehoehe, Masse, Schwerpunkt, Entnahmeweg | Sicherung, Fussabdruck, Ballast-/Bodenlastnachweis |

Keine pauschale Schraubengroesse oder Wandstaerke gilt als Lastfreigabe.
Magnete dienen zur Ausrichtung; tragende Befestigung separat nachweisen.
Druckschichten, Waerme und lokale Spannungsspitzen bei allen Haltern beruecksichtigen.

## Fertigungspaket je Teil

- Teil-ID, Revision, Seite und Referenzbild-IDs; natives editierbares CAD.
- Masszeichnung in mm, Bezugsachsen, Gegenstueck und tolerierte Funktionsmasse.
- Geschlossene, gepruefte Exportgeometrie; korrektes STL-/3MF-Einheitenhandling.
- Material, Orientierung, Wandaufbau, Stuetzzonen und Slicerprojekt.
- Verbindungsmittel, Einlegeteile, Montagefolge und Werkzeugzugang.
- Ziel-/Ist-Masse, Schwerpunkt bei bewegten Teilen, Seriennummer des Prototyps.
- Passprobe und Testbericht mit Fotos; nach Aenderungen betroffene Tests wiederholen.

## Reihenfolge mit Entscheidungspunkten

1. Referenzansichten vervollstaendigen und reales Messblatt aufnehmen.
2. Helm-, Brust- und Schultervolumen aus leichten Mustern pruefen. Erst dann
   Detailoberflaechen modellieren oder ein rechtmaessig nutzbares Set anpassen.
3. Eine Seitenfuehrung und Tuer am Tisch bauen; Hub, Anschlag, Verkanten und
   Handentriegelung testen. Danach mit ungetragenem Torso kombinieren.
4. Tragbaren Helm-Torso-Schulter-Prototyp pruefen; alle Rueckbauwege frei halten.
5. Je eine Arm-/Beinkassette fertigstellen, Passform korrigieren, Gegenseite
   individuell anpassen. Kein automatisches Spiegeln anatomischer Innenmasse.
6. Vollstaendigen Rohbau wiegen und testen. Erst nach bestandenen Passproben
   Oberflaechenfinish und verdeckte Elektronik finalisieren.
7. Ausstellungsstaender und Demonstration separat testen. Motorische Panels
   bleiben ein eigener ungetragener Pruefstand bis zur belastbaren Auslegung.

Die [Prototypenfolge](../../BuildGuides/Armor/Mjolnir-Prototypen.md) und der
[Abnahmebogen](../../Tests/TestReports/Mjolnir-Abnahme.md) dokumentieren die Nachweise.
