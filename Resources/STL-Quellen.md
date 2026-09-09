# Detailmodelle: Quellen, Auswahl und Import

Stand: 2026-09-09. Der [Referenzkatalog](../Documentation/References/ArmorReferenceLibrary.json)
ordnet Modelle und Bilder den Profilwerten `chief-infinite`, `mark-vii` und
`custom` zu. Die verlinkten Modellangebote wurden anhand der jeweiligen
Anbieterseiten geprueft. Kaufdateien wurden nicht bezogen, geoeffnet oder auf
Vollstaendigkeit und Passform getestet.

## 1. Konkrete Modellkandidaten

| Referenz | Quelle | Belegter Angebotsumfang | Vor dem Einsatz offen |
| --- | --- | --- | --- |
| chief-infinite | [Galactic Armory: Infinite Master Chief Armor](https://galacticarmory.net/products/infinite-master-chief-armor-3d-print-files) | Armor Only oder Armor + Helmet; getrennte Druckteile, flexible Anschlussvarianten und Lueftungsvarianten laut Anbieter | Exakte Dateiliste, Visierherstellung, Revision, individuelle Passform, Einbaumasse |
| chief-infinite | [Nikko Industries: Halo Infinite Master Chief Armor](https://www.nikkoindustries.com/products/halo-infinite-master-chief-armor) | Nach Koerperteilen getrennte Ruestung | Helm-/Visierumfang und vollstaendige Dateiliste nicht aus der Beschreibung ableitbar |
| mark-vii | [Nikko Industries: Halo MK7 Full Armor](https://www.nikkoindustries.com/products/halo-mk7-full-armor) | Als volle Ruestung angebotene STL-Dateien, nach Koerperteilen getrennt | Konkrete Schulter-/Knievariante, Helm-/Visierumfang, Passform gegen Guide pruefen |
| custom | Projektbezogene Quelle | Erst nach Festlegung der Ruestungsvariante | Alle Bauteile, Rechte und Varianten dokumentieren |

Fuer einen Chief-Aufbau ist das Galactic-Armory-Angebot der erste
Pruefkandidat, weil dessen Beschreibung die Anschluesse an flexible Teile und
Lueftungsvarianten konkret benennt. Dies ist eine Auswahl fuer die weitere
Dateipruefung, keine bestaetigte Druck- oder Kaufempfehlung fuer eine bereits
passende Ruestung. Ein Helm-Bundle ersetzt kein transparentes Visier.

Nikko beschreibt persoenliche Nutzung und schliesst kommerziellen Druck aus.
Galactic Armory verweist fuer kommerzielle Nutzung auf eine gesonderte
Mitgliedschaft. Die konkreten Bedingungen zum bezogenen Modellstand gehoeren
in das lokale Assetregister. Daraus folgt keine pauschale Freigabe fuer Verkauf,
Weitergabe oder einen gesponserten Ausstellungsauftritt.

Kosten werden erst mit gewaehlt identischem Paket und aktuellem Angebot in die
Projekt-BOM eingetragen. Ein sichtbarer Einstiegspreis wird nicht als Preis
eines Helm-Komplettpakets uebernommen. Keine Datei wird automatisch gekauft.

## 2. Offizielle Formreferenz getrennt vom Druckmodell

- [Mark-VII-Cosplay-Guide](https://www.halowaypoint.com/news/official-cosplay-guide-mark-vii):
  offizielle Bild- und Materialreferenz. Lokale PDFs unter
  [CosplayGuides](CosplayGuides/README.md); Kapitelzuordnung in
  [Authentizitaet-Referenz](../Documentation/Guides/Authentizitaet-Referenz.md).
- [Kolby Jukes: Master Chief, Halo Infinite](https://kolbyjukes.artstation.com/projects/OyBR0w):
  Bildquelle des Originalmodellautors fuer Chief; kein freies druckbares Modell.
- [Halo Waypoint: Season-5-Varianten](https://www.halowaypoint.com/news/customization-overview-season-5):
  Kampagnen-Chief und Multiplayer-Kit unterscheiden sich unter anderem bei der 117.

Eine Halo-3-Mark-VI-Datei ist kein Infinite-Mark-VI-GEN3-Modell. Ein Mark-VII-Guide
legt keine Chief-Geometrie fest. Reine Sammelsuchen, unbestaetigte Reuploads und
angebliche kostenlose Komplettpakete werden hier nicht als gepruefte
Beschaffung gefuehrt. Der Katalog hat derzeit keinen als vollstaendig und
referenzpassend geprueften kostenlosen Komplettsatz.

## 3. Lokales Assetregister anlegen

Die Befehle werden im Repository-Verzeichnis ausgefuehrt. Fuer ein Projekt mit
anderer Referenz wird der Profilwert entsprechend ersetzt.

```bash
python3 tools/suit_assets.py --init build/Suit-A/assets.json --project Suit-A --reference chief-infinite
python3 tools/suit_assets.py --manifest build/Suit-A/assets.json
```

Ein leeres Register ist absichtlich unvollstaendig. Bei fehlenden Dateien oder
Nachweisen endet die Pruefung mit Exitcode 2. Jede der 23 Teil-IDs muss genau
einmal vorkommen. Pfade werden relativ zum Verzeichnis der Registerdatei
aufgeloest; absolute Pfade und Verweise ausserhalb dieses Verzeichnisses werden
abgewiesen.

| Feld pro Teil | Eintrag |
| --- | --- |
| id / revision | Stabile Bauteil-ID aus dem Katalog und eigener Dateistand |
| kind | `mesh`; fuer `undersuit` und `neck_seal` alternativ `pattern` |
| source_url / license_note | Konkrete HTTP(S)-Quelle und lokale Dokumentation der Nutzungsbedingungen |
| reference_views | Liste konkreter Bild-IDs oder Seiten-/Ansichtsbezeichnungen |
| native_path / native_sha256 | Editierbare CAD-/Musterquelle und SHA-256; z.B. `models/helmet-r1.blend` |
| mesh_path / mesh_sha256 | STL-Pruefexport und SHA-256; bei `pattern` nicht erforderlich |
| unit_scale_mm | Millimeter je STL-Koordinateneinheit; bei Millimeterexport `1`, nicht pauschal raten |
| notes | Paketbestand, Anpassungen, Bezugsdatum und offene Fragen |

Fuer eine aus STLs aufgebaute Arbeitsdatei das importierte Modell im nativen
Format des Editors speichern; der STL-Download allein ist keine editierbare
CAD-Quelldatei im Register. Ein Teil aus mehreren Komponenten erhaelt eine
native Baugruppe und einen gemeinsamen STL-Pruefexport. Weitere Original- und
Druckdateien bleiben mit Dateinamen in `notes` dokumentiert. Der Checker erfasst
nur die beiden eingetragenen Dateien.

Der Bericht nennt berechnete Pruefsummen, falls diese noch fehlen; sie koennen
nach Abgleich in das Register uebernommen werden. Fuer die Ablage des Berichts:

```bash
python3 tools/suit_assets.py --manifest build/Suit-A/assets.json --report build/Suit-A/asset-report.json
```

Der Checker prueft Existenz/Hash der Quelldatei und bei STL die Struktur,
endliche Koordinaten, Flaechen, Abmessungen und exakte Kantenpaarung. Er
interpretiert die native Datei nicht und prueft weder Selbstschnitte noch
Wanddicken, Originaltreue oder Festigkeit. `fabrication_approved` und
`authenticity_verified` bleiben daher immer `false`. Aktuelle Grenzen: maximal
100 MiB je Datei und 300.000 Dreiecke pro Pruefexport; hochaufgeloeste Originale
koennen ausserhalb dieses Pruefexports lokal aufbewahrt werden.

Download-Archive und unveraenderte Originaldateien bleiben lokal unter
`build/Suit-A/`. Der Ordner ist von Git ausgeschlossen. Auch lizenzierte Kaufdateien
gehoeren ohne ausdrueckliche Weitergaberechte nicht in ein oeffentliches Repo.
Der private lokale Bestand benoetigt eine eigene Sicherung, da `build/` kein
Archivierungsdienst ist. Oeffentlich bleiben Quellenkatalog, Werkzeuge und
leere Vorlagen.

## 4. Ein konkreter Importablauf

1. Paketname, Anbieter-URL, Bezugsdatum, Version und Nutzungsbedingungen erfassen.
   Downloadarchiv unveraendert aufbewahren. Eine separate Arbeitskopie anlegen.
2. Dateien den 23 Bauteil-IDs zuordnen. Fehlende Haende, Hals, Unteranzug und Visier
   ausdruecklich offen lassen; die Bezeichnung "Full Armor" ersetzt die Inventur
   nicht. Mehrere Dateien fuer ein Teil bleiben im nativen Baugruppendokument und in
   `notes` als Satz nachvollziehbar; die Teil-ID wird nicht dupliziert.
3. Einheit und Original-Abmessungen im Modellprogramm pruefen. STL enthaelt
   normalerweise keine eindeutige Laengeneinheit; keine 20%- oder 100%-Annahme
   aus dem Dateinamen ableiten.
4. Front, Ruecken und Gelenkanschluesse gemeinsam laden. Urspruengliche
   Skalierungsunterschiede messen; keine pauschale 97,78%-Korrektur anwenden.
5. Jedes Segment an die benoetigte Innengeometrie anpassen. Laenge, Breite und
   Tiefe getrennt pruefen. Gravierungen und Wanddicken nach der Anpassung
   kontrollieren. Keine globale Standardskalierung nach Koerpergroesse.
6. Offene Kanten, invertierte Flaechen, Selbstdurchdringungen, duenne Waende und
   nicht passende Anschlussstellen pruefen. Automatische Reparaturen mit der
   Originalkopie vergleichen und erst dann uebernehmen.
7. Druckraum des tatsaechlichen Druckers, Duese und gewaehltes Material eintragen.
   Druckschnitte an unauffaellige oder vorgesehene Fugen legen; Servicefugen von
   spaeter zu verklebenden Drucknaehten unterscheiden.
8. Kurze Passringe und Verbindungsmuster drucken. Erst nach deren Auswertung den
   Helm/Torso/Schulter-Musterbau beginnen. Proben im Material und in der
   Orientierung des spaeteren Bauteils herstellen.
9. Jede Aenderung mit neuem Dateistand und Pruefsumme erfassen. Hersteller-
   Varianten, eigene Reparaturen und persoenliche Anpassungen getrennt benennen.

Es gibt hier keinen vorgeschriebenen Drucker, kein universelles Infill-Limit
und keine von einem Softwaretest belegte Materialfestigkeit. Kosmetische Schalen
und tragende Beschlaege erfordern unterschiedliche Konstruktion und Erprobung.
Fuer den gestalterischen Ablauf gilt
[Mjolnir-Detailgestaltung](../Documentation/Guides/Mjolnir-Detailgestaltung.md).
