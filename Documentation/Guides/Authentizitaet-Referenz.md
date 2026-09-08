# Ruestungsreferenz und optische Abnahme

Die Ruestungsreferenz wird im [Projektprofil](Mjolnir-Konfiguration.md) bewusst
gewaehlt. Ein Referenzpaket gehoert zu genau einem Spiel, Ruestungstyp und
Aussehen. Die mechanische Oeffnung ist eine eigene Interpretation und soll
die geschlossene Silhouette der gewaehlten Vorlage erhalten.

| Profilwert | Bezug | Benoetigte Festlegung |
| --- | --- | --- |
| chief-infinite | Master Chief, Halo Infinite Kampagne, Mark VI GEN3 | Kampagnenansichten, Markierungen und Farb-/Visiermuster |
| mark-vii | Halo Infinite Multiplayer, Mark VII GEN3 | Konkrete Helm-/Schulterkonfiguration und Farbgebung |
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
- Abrufstand: 2026-09-08. Bilder/Spielmodelle wurden nicht als eigene Werke
  uebernommen. Nutzungsrechte jeder spaeteren Modelldatei separat festhalten.

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

Diese Ansichten sind Beschaffungsaufgaben, keine bereits vollstaendige Sammlung.
AI-Konzeptbilder gelten nicht als Beleg fuer Originalgeometrie.

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
   Kein RGB-/Pantonewert ist hier als offiziell bestaetigte Lackrezeptur belegt.
4. Aus einem Meter Entfernung: keine offenen Drucknaehte, Kleberreste, losen
   Kanten oder zufaelligen Lichtlecks. Gebrauchsspuren nach Referenz platzieren.
5. Visier von innen bei Hallenlicht, dunklerem Gang und ausgeschalteter Elektronik
   testen. Aussenwirkung und Sicht sind getrennte Abnahmepunkte.

Abweichungen werden mit Foto, Grund und Auswirkung im Bauprotokoll festgehalten.
Eine bestandene optische Pruefung ersetzt keine mechanische Pruefung.

Weiter: [Fertigungsplan](Mjolnir-Fertigung.md), [Messanpassung](Mjolnir-Massanpassung.md),
[Abnahme](../../Tests/TestReports/Mjolnir-Abnahme.md).
