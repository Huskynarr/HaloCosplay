# Massanpassung fuer ein eigenes Projektprofil

## Messzustand und Herkunft

Alle Eingaben sind **Millimeter**. Ein [neues Profil](Mjolnir-Konfiguration.md)
beginnt ohne Koerpermasse. Koerpergroesse barfuss messen; Schalenmasse im
spaeteren Unteranzug aufnehmen. Ein bereits
montiertes Innenpolster darf nicht erneut als Zuschlag addiert werden. Schuhe
separat in ihrem tatsaechlichen Aussenmass erfassen. Alle Masse links und rechts
einzeln notieren. Jeder Messdurchgang benoetigt eine zweite Person, Datum,
Kleidung und eine Beschreibung der Endpunkte.

Fotos helfen bei Stil und Proportion, aber ohne Referenzmass, neutrale Perspektive
und definierte Pose nicht bei Fertigungsmassen. Unbekannte Messwerte bleiben
`null`. Weder Koerpergroesse, Schuhgroesse noch Fotos ersetzen die erforderlichen
Breiten, Tiefen und Umfaenge. Fuer jede Person ein eigenes Profil verwenden.

## Eingaben fuer den Generator

| Feld in measurements_mm | Messdefinition |
| --- | --- |
| height | Barfuss Boden bis Scheitel |
| shoulder_width | Gerade Aussenbreite ueber beide Deltamuskeln, Arme locker; nicht Knochenabstand |
| chest_width / chest_depth | Horizontale Gerade links/rechts bzw. vorne/hinten am groessten Brustquerschnitt, normal einatmend |
| abdomen_width / abdomen_depth | Groesste Gerade am Bauch, Maximum aus Stehen und bequemem Sitzen |
| torso_length | Senkrechte Hoehe von geplanter Schulterauflage bis Oberkante gepolstertem Hueftgurt; Endpunkte markieren |
| hip_width / hip_depth | Groesster eingeschlossener Querschnitt an Huefte/Gesaess, gerade Breite und Tiefe |
| head_width / head_depth / head_height | Maximale Breite, Stirn-Hinterkopf, Kinn-Scheitel; mit spaeterer Kopfhaube |
| upperarm_length_l/r | Schulterpunkt bis Ellbogenmitte, entlang der Oberarmachse, Arm entspannt |
| upperarm_circumference_l/r | Groesster Oberarmumfang auch bei angewinkeltem/angespanntem Arm |
| forearm_length_l/r | Ellbogenmitte bis Handgelenksfalte |
| forearm_circumference_l/r | Groesster Unterarmumfang |
| thigh_length_l/r | Seitlicher Hueftbeugepunkt bis Kniemitte; kein Schritt-Boden-Mass |
| thigh_circumference_l/r | Groesster Oberschenkelumfang im spaeteren Unteranzug |
| shin_length_l/r | Kniemitte bis Knoechelmitte |
| calf_circumference_l/r | Groesster Wadenumfang |
| boot_width_l/r / boot_length_l/r | Tatsaechliche Schuh-Aussenbreite/-laenge, keine EU-Groesse |

Gerade Breiten/Tiefen mit zwei parallelen Brettern oder Messschenkeln abnehmen,
nicht mit ueber die Haut gefuehrtem Massband. Umfang, anatomische Laenge und
freie Schalenlaenge sind verschiedene Groessen. Groessere Differenzen zwischen
Wiederholungen zuerst durch erneutes Messen klaeren, nicht einfach mitteln.

## Zusaetzliche Masse vor der Fertigung

Der Generator erstellt grobe Huellen. Fuer das eigentliche Schalenmodell fehlen
darueber hinaus: Kopf-/Halsumfang, Ohrenfreiheit, Hals-Schulter-Abstand,
Handbreite mit Handschuh, Handgelenkbreite/-tiefe, Ellbogen- und Kniequerschnitte
gebeugt, je Segment Querschnitte an Anfang/Mitte/Ende, Schuh-/Knoechelhoehe,
Rueckenform, Gurtposition und die dynamischen Freiraeume im Sitzen.

Fuer Serien-Exoskelette kommen die **herstellerspezifischen** Definitionen von
Guertelumfang, Hueftbreite, Oberschenkellaenge/-umfang und Koerpergewicht hinzu.
Eine hier gemessene maximale Hueftbreite ist nicht automatisch die im jeweiligen
Handbuch geforderte Hueftbreite. Herstellerdiagramm direkt verwenden.
Gewicht wird nicht aus Fotos oder Koerpergroesse abgeleitet.

## Zuschlaege richtig anwenden

Der Entwurf startet mit 8 mm radialem Polster und 12 mm radialem Bewegungsraum.
Beides sind einstellbare **Entwurfsannahmen**, keine garantierten Komfortwerte.
Eine Breite erhaelt den radialen Zuschlag auf beiden Seiten:

```text
Innenbreite = Koerperbreite + 2 * (Polster_radial + Freiraum_radial)
Aussenbreite = Innenbreite + 2 * Wandstaerke
```

Fuer einen Kreisquerschnitt mit Radiuszuwachs `a` waechst der Umfang um `2*pi*a`.
20 mm radialer Freiraum bedeuten somit etwa 125,7 mm Umfangszuwachs, **nicht**
20 mm. Die bisherige pauschale Empfehlung, nur 10-15 mm zum Umfang zu addieren,
bildet kein Polster von mehreren Millimetern ab und gilt hier nicht.

Aus Umfang wird im Modell ein kreisgleicher Durchmesser berechnet:
`D = Umfang/pi + 2*(Polster + Freiraum + Wand)`. Das ist nur fuer eine Testlehre
geeignet. Ein menschlicher Unterarm ist nicht kreisfoermig; Breite/Tiefe und
Querschnittsveraenderung muessen danach separat an die Schale angepasst werden.

Schalenlaengen erhalten einen einstellbaren Randabstand von anfangs 20 mm je
Ende. Diese rechnerische Verkuerzung ersetzt keine Gelenkbewegungsprobe.
Gelenkfugen werden nach dem Bewegungsraum vergroessert,
nicht durch starre prozentuale Gesamt-Skalierung ausgeglichen.

## Unterschiedliche Koerperproportionen

- Torsohoehe aus torso_length; Breite aus maximalem Brust-/Bauchquerschnitt.
- Schulterhauben folgen shoulder_width und einer separat einstellbaren optischen Zugabe.
- Seitenfuehrungen erhalten den fuer den Einstieg erforderlichen Ausfahrweg.
- Helm wird nach Kopf und Sichtlinie skaliert, nicht nach Koerpergroesse.
- Schuhcover folgen echten Schuhen; keine automatische Erhoehung oder +20-%-Vorgabe.
- Bei breiten Fuessen zuerst einen bequem passenden Schuh waehlen. EU-Groesse
  ist keine Schuhbreite; Aussenlaenge und -breite sowie spaeter Spannhoehe messen.
- Linke/rechte Gliedmassen werden nicht gegenseitig ueberschrieben.
- STL-Oberflaechen lokal schneiden und verbreitern; nicht die komplette Figur
  entlang X strecken, da sonst Visor, Schraubensitze und Gelenkanschluesse verzerren.

## Reihenfolge der Passproben

1. Torso-Querschnitt und offene Eintrittsbreite als 1:1-Kartonmodell herstellen.
2. Seitliches Ausfahren und Aufschwenken mit Unteranzug und geschlossenem Gurt testen.
3. Bauchlamellen sitzend pruefen; Brustplatte darf nicht den Hals hochschieben.
4. Oberarm-/Unterarm-Testlehren und dreipunktige Querschnitte vergleichen.
5. Oberschenkel/Schienbein mit flexiblen Gelenkzwischenraeumen testen.
6. Alle tragenden Schnittstellen und Mechanik separat abnehmen; erst dann
   die finalen sichtbaren Schalen segmentieren, drucken und lackieren.

Die Fortschritte bleiben in [Prototypen und Abnahme](../../BuildGuides/Armor/Mjolnir-Prototypen.md)
offen, bis echte Messungen und Versuche dokumentiert sind.

## Ausfuellbares Messprotokoll

[CSV-Messblatt](../../Design/Parametric/Profiles/Messprotokoll.csv) enthaelt alle
32 leeren Generatorfelder und getrennte Spalten fuer
zwei Messungen, uebernommenen Wert, Datum, Kleidung und Endpunktnotizen. Leere
Felder bleiben unbekannt. Es erfolgt kein automatischer Import ungepruefter Werte.
Die zusaetzlichen Fertigungs-/Herstellermasse aus diesem Guide separat aufnehmen.
Ausgefuellte Kopien unter `build/` lokal halten; nicht versehentlich committen.
