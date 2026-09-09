# Ruestungsreferenz und optische Abnahme

Die Ruestungsreferenz wird im [Projektprofil](Mjolnir-Konfiguration.md) bewusst
gewaehlt. Ein Referenzpaket gehoert zu genau einem Spiel, Ruestungstyp und
Aussehen. Die mechanische Oeffnung ist eine eigene Interpretation und soll
die geschlossene Silhouette der gewaehlten Vorlage erhalten.

| Profilwert | Bezug | Benoetigte Festlegung |
| --- | --- | --- |
| chief-infinite | Master Chief, Halo Infinite Kampagne, Mark VI GEN3 | Kampagnenansichten, Markierungen und Farb-/Visiermuster |
| mark-vii | Halo Infinite Multiplayer, Mark VII GEN3 | Guide-Aufbau mit Mark-VII-Helm, UA/AGATHIUS-Schultern, UA/TYPE-SA-Knien; Abweichungen belegen |
| custom | Eigene Halo-Referenz oder bewusst eigener Entwurf | Spiel/Quelle, Modellvariante, Farbe, Embleme und Abweichungen |

Die Referenzwahl im Profil erzeugt keine Detailmodelle. Fuer `custom` ist die
zusaetzliche Referenzbeschreibung im Bauprotokoll erforderlich. Verschiedene
Profile duerfen verschiedene Vorlagen verwenden; innerhalb eines Projekts
muessen Quellen und gewollte Abweichungen konsistent bleiben.

## Quellen und Grenzen

- [Halo: Customization Overview, Season 5](https://www.halowaypoint.com/news/customization-overview-season-5)
  benennt Chiefs Kampagnenruestung als GEN3 Mark VI. Das Multiplayer-Kit laesst
  laut Artikel die 117-Gravur weg und erlaubt andere Farben/Embleme. Daher keine
  beliebige Multiplayer-Konfiguration als exakte Kampagnenvorlage verwenden.
- [Offizieller Mark-VII-Guide](https://www.halowaypoint.com/news/official-cosplay-guide-mark-vii)
  behandelt Mark VII GEN3 aus dem Multiplayer. Die vorhandenen PDFs passen zu
  dieser Ruestungsfamilie; sie sind keine Mark-VI-Mass- oder Farbvorlage.
- [Kolby Jukes: originales Infinite-Modell](https://kolbyjukes.artstation.com/projects/OyBR0w)
  liefert eine Quelle des Modellautors fuer Chief. Das
  [Cinematic-Modell von Omid Moradi](https://omiiidmoradi.artstation.com/projects/d04ogJ)
  ist eine eigene Bearbeitung und wird als ergaenzende Variante gefuehrt.
- Abrufstand: 2026-09-09. Im
  [maschinenlesbaren Katalog](../References/ArmorReferenceLibrary.json) sind
  Quellen, 23 Bauteile je Referenz, erforderliche Ansichten und verbleibende
  Nachweise hinterlegt. Katalogeintraege sind keine erworbenen Modell-Dateien.
- Bilder/Spielmodelle wurden nicht als eigene Werke uebernommen. Nutzungsrechte
  jeder spaeteren Modelldatei separat festhalten.

## Referenzpaket vor der Detailmodellierung

Je Ansicht eine eindeutige Bild-ID, URL oder eigene Aufnahme, Spielszene,
Aufnahmedatum, Perspektive und zulaessige Nutzung dokumentieren. Die zum Projekt
passenden Ansichten haben Vorrang; etwaige Varianten-Abweichungen explizit markieren. Perspektivische
Bilder dienen der Form, nicht als Millimeterzeichnung.

| ID | Erforderliche Ansicht | Zu pruefende Merkmale |
| --- | --- | --- |
| REF-01 | Ganzkoerper frontal, neutral | Helm-/Brustbreite, Schulterlage, Segmentlaengen |
| REF-02 | Ganzkoerper hinten | Rueckenmodule, Huefte, Fugen und Kabelfreiheit |
| REF-03/04 | Beide Seiten | Brusttiefe, Helmprofil, Schulterversatz, Knie |
| REF-05 | Helm vorne/seitlich/hinten | Visierkontur, Kinn, Seitenmodule, Halsabschluss |
| REF-06 | Brust und Ruecken nah | Plattengrenzen, referenzgemaesse Markierungen, Vertiefungen, Oberflaechen |
| REF-07 | Arme/Haende und Beine/Schuhe | Ueberlappungen und sichtbarer Unteranzug |
| REF-08 | Farbe in mehreren Lichtsituationen | Gewaehlte Farben, Glanzgrad, Visier, Gebrauchsspuren |

Fuer Mark VII sind die vorhandenen offiziellen Unterlagen unten seitenweise
zugeordnet. Die projektbezogenen Bildausschnitte, Gegenansichten und Nachweise
bleiben im Katalog als offen markiert. Fuer Chief ist eine vollstaendige,
szenenkonsistente Sammlung weiterhin zu erstellen. AI-Konzeptbilder gelten
nicht als Beleg fuer Originalgeometrie.

## Mark-VII-Index fuer die vorhandenen Unterlagen

Die Seitenzahlen gelten fuer die 106-seitige
[Full-PDF](../../Resources/CosplayGuides/MK7_CosplayGuide_Full.pdf), ab Seite 1
gezaehlt. Die Kapitelzuordnung wurde aus dem PDF-Text gewonnen. Seiten 6, 34 und
83 wurden zusaetzlich visuell geprueft; dies ist kein vollstaendiger Bildaudit.

| Seiten | Inhalt | Besondere Grenze |
| --- | --- | --- |
| 6 | Digitale Material- und Farbreferenzen | Gilt fuer den gezeigten Aufbau; kein universelles Lackrezept |
| 7-12 | Gesamtansichten | Keine Koerpermasse oder Masszeichnung |
| 13-15 | Bauch-, Ruecken- und Halsstruktur | Schnittmuster und Bewegungszugaben fehlen |
| 16-26 | Helm | Optische Durchsicht eines realen Visiers nicht belegt |
| 27-33 | Torso vorne/hinten | Reale Oeffnungsmechanik ist eigene Konstruktion |
| 34-40 | UA/AGATHIUS-Schulter | Rechte Seite bezeichnet; linke Seite separat abgleichen |
| 41-47 | Oberarm | Rechte Seite bezeichnet |
| 48-54 | Unterarm | Rechte Seite bezeichnet; Anbauteile projektbezogen |
| 55-61 | Handschuh | Linke Hand bezeichnet |
| 62-68 | Handrueckenplatte | Zugehoerigkeit und Seitenlage pruefen |
| 69-75 | Huefte | Reale Beugung und Zugang zu Verschluessen pruefen |
| 76-82 | Oberschenkel | Linkes Bein bezeichnet |
| 83-89 | UA/TYPE-SA-Knie | Nicht jede Multiplayer-Knievariante ist identisch |
| 90-96 | Unterschenkel | Scharnier- und Wadenpassform fehlen |
| 97-103 | Schuh | Linker Schuh bezeichnet; normale tragbare Sohle vorsehen |

Die Farbfelder des gezeigten Mark-VII-Aufbaus sind im Katalog hinterlegt.
Fuer Chief wird daraus weder das Gruen noch eine rote Visiertoennung abgeleitet.

## Anpassung an das jeweilige Koerperprofil

Die reale Schulter- und Gelenklage bestimmt die Innengeometrie. Kopf, Torso,
Arme und Beine separat anpassen; keine uniforme Skalierung nach Koerpergroesse.
Die Aussenform wird darueber rekonstruiert. Ein engerer Taillenlook darf keine
Kompression oder Bewegungseinschraenkung erzwingen. Normales Schuhwerk bildet die
Basis. Eine fiktive Spartan-Koerpergroesse ist kein Fertigungsziel.

## Sichtbare Qualitaet und Abnahme

1. Silhouette in Front/Seite/Ruecken bei gleichem Kamerastand mit REF-01 bis 04
   vergleichen. Helm und Torso zuerst; Fehler vor dem kompletten Druck korrigieren.
2. Fugen, Befestigung und Unteranzug auch bei angehobenen Armen fotografieren.
   Gurte, Reissverschluesse und Elektronik sollen hinter den vorgesehenen Fugen liegen.
3. Farbproben auf dem echten Grundmaterial mit Grundierung und finalem Klarlack
   erstellen. Je Probe Rezept, Schichtfolge, Trockenzeit und Beleuchtung notieren.
   Die digitalen Mark-VII-Werte sind Referenzfarben, keine bestaetigte Lackrezeptur.
   Fuer Chief bleibt eine eigene Farbprobe erforderlich.
4. Aus einem Meter Entfernung: keine offenen Drucknaehte, Kleberreste, losen
   Kanten oder zufaelligen Lichtlecks. Gebrauchsspuren nach Referenz platzieren.
5. Visier von innen bei Hallenlicht, dunklerem Gang und ausgeschalteter Elektronik
   testen. Aussenwirkung und Sicht sind getrennte Abnahmepunkte.

Abweichungen werden mit Foto, Grund und Auswirkung im Bauprotokoll festgehalten.
Eine bestandene optische Pruefung ersetzt keine mechanische Pruefung.

Weiter: [Detailgestaltung und druckbares Bauteilblatt](Mjolnir-Detailgestaltung.md),
[Modellquellen und Import](../../Resources/STL-Quellen.md), [Fertigungsplan](Mjolnir-Fertigung.md), [Messanpassung](Mjolnir-Massanpassung.md),
[Abnahme](../../Tests/TestReports/Mjolnir-Abnahme.md).
