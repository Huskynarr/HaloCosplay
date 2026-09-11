# Einbauplan: Akkus, Licht, Luft und aufklappbare Schalen

Stand: 2026-09-09. Der Entwurf sieht vollstaendig oeffnende Arm-/Beinmodule,
getrennte Komfort-/Effektversorgung und zugaengliche technische Kassetten vor.
Ziel ist das selbststaendige An- und Ablegen nach bestandenen Gesamtproben.
Die folgenden Zonen sind noch keine gemessenen dreidimensionalen Freiraeume.

## Einbauorte

| Baugruppe | Vorgesehene Zone | Funktion und Zugang |
| --- | --- | --- |
| Komfort-Powerbank | Tief an linker Flanke am Huefttraeger | Nach vorn/seitlich wechselbar; eigener Schalter vorne links |
| Effekt-Powerbank | Tief an rechter Flanke am Huefttraeger | Gewicht verteilen; eigener Schalter vorne rechts |
| LED-Treiber und Controller | Seitliches trockenes Servicefach, vom Akku getrennt | Waerme nach aussen; Kanaele und Stecker beschriften |
| Nebler | Originalhuelle an eigener erreichbarer Traegerkassette | OEM-Betriebslage und Direktbedienung erhalten; Fernbedienung nur Ergaenzung |
| Helmlampen | Links/rechts aussen in Licht-/Sensorpods | Metallkernplatine auf echtem Kuehlkoerper; Lichtfenster nach vorn, Entblendung und Beruehrschutz |
| Helm-Frischluft | Seitliche Wangen-/Kieferkanaele | Luft an innere Visierflaeche; Abluft oben hinten |
| Torso-Frischluft | Untere seitliche Einlaesse | Abstandstextil fuehrt Luft nach oben; Elektronikabluft getrennt |
| Kamera | Stirn-/Sensorblock mit eigenem klarem Fenster | Nicht hinter Goldvisier; Fenster, Streulicht und Sichtfeld pruefen |
| Optionales HUD | Seitlich oberhalb eines Auges, umklappbar | Kleine Optik, direkte Hauptsicht bleibt frei; Bildgeber in naher Servicekassette |
| Mikrofon | Seitlich am Mund, entkoppelt | Abstand zu Luftstrahl, Kontaktgeraeuschen und Lautsprecher |
| Sprachlautsprecher | Vorderer Brust-/Kragengrill | Sprache nach aussen, frontseitige Lautstaerke/Stummschaltung |
| Duesen-RGB | Trockene Umrandung beider Auslaesse | Licht in ausgetretenen Nebel; OEM-Austritt bleibt frei |
| Effektluefter | Eigener trockener Kanal neben jedem Auslass | Zusatzluft fuer Startwirkung, kein Eingriff in Nebelschlauch |

Flankenkassetten duerfen beim Sitzen, Armabsenken, Drehen und Oeffnen nicht
in Huefte, Rippen oder Oberschenkel druecken. Kein harter Akkublock am Sternum
oder direkt auf der Wirbelsaeule. Gewicht traegt der Gurt-/Rahmenaufbau, keine
duenne aufklappende Brustzierplatte. Beim Serien-Exoskelett bleiben dessen
Gurte, Bedienelemente und Bewegungsraum eigenstaendig erreichbar.

## Stromkreise und Kabelbaum

**Komfort:** geregelte 5 V als Entwurfsbasis fuer passende Luefter und
Kleinmodule. HUD, Kamera/Recorder und Sprachsystem nur nach verifizierter
Schnittstelle anschliessen. Ein fertiger Sprachverstaerker mit eigenem Akku
bleibt stattdessen ein eigenes System und wird in der Projektbilanz umgetragen.

**Effekte:** Die untersuchte Konstantstrom-RGB-Loesung verwendet 15 V als
Entwurfsziel. Die konkrete Powerbank braucht ein entsprechendes USB-PD-Profil
und ein geeignetes Ausgangsmodul, das dieses Profil aktiv aushandelt. Ein
passives Kabel erzeugt keine 15 V. Controller und trockene 5-V-Duesenluefter
bekommen einen eigenen geregelten 5-V-Abgang; dort duerfen keine 15 V anliegen.

**Nebel und kommerzielles Exoskelett:** bleiben auf den vorgesehenen
Herstellerakkus. Gleiche Stecker bedeuten keine gleiche Versorgung. Auch
Powerbank-Ausgaenge werden nicht miteinander verbunden. Der Effektschalter
unterbricht die Komfortversorgung nicht; deren eigener Ausfall bleibt moeglich.

Ausgangsleistung, Kabel, Stecker und Sicherung folgen der gemessenen Maximal-
und Einschaltlast, Leitung und Herstellerdaten. An Mehrport-Powerbanks pruefen,
ob Zu-/Abstecken anderer Verbraucher Spannung oder PD-Aushandlung neu startet.
Kapazitaet in Wh und nutzbare Ausgangsenergie erfassen; eine mAh-Angabe allein
bestimmt keine Laufzeit am 5-/15-V-Verbraucher.

Kabel bleiben bevorzugt am festen Traeger. Jede bewegte Klappe bekommt eine
zugentlastete, gefuehrte Bewegungsschlaufe ohne Hals-/Handgelenksring und eine
erreichbare Service-Trennstelle. Helmstecker sind mit Handschuhen erreichbar;
betroffene Stromkreise vor dem Trennen ausschalten. Kodierung unterscheidet
5 V, 15 V, Konstantstrom-LED-Ausgaenge und Signale.

Im [Lichtguide](Mjolnir-Lichtmodule.md) liegen je zwei gleiche Farbchips in
Reihe. Die drei RGB-Strange bekommen getrennte Treiberausgaenge, keine
gemeinsame LED-Rueckleitung zur Versorgungsmasse. Die NeoPixel-Sketches und
das einfache Luefter-`analogWrite` sind dafuer keine passende Gesamtsteuerung.

## Oeffnen statt Durchschluepfen

Oberarm, Unterarm, Oberschenkel und Wade erhalten je Seite eigene aufklappbare
Schalen. Fusscover legen sich um normale Schuhe; Handruecken und Halsabschluss
oeffnen ebenfalls. Auch innere Gurte, Kabel und flexible Abdeckungen werden an
der Oeffnung geteilt oder vollstaendig geloest. Ein offener Panzer mit
geschlossenem Innengurt waere weiterhin ein Durchschluepfteil.

Verschluesse liegen vorne oder vorne/innen und werden mit der Gegenhand
bedient. Die letzte Armschale wird mit bereits gepanzerter Gegenhand geprueft.
Handschuhe/Handruecken kommen spaet, der Helm zuletzt. Schulterlaschen werden
zur Brust gefuehrt. Details: [Selbstanziehen](Mjolnir-Selbstanziehen.md).

Das [Clamshell-CAD](../../Design/Clamshell/README.md) stellt acht getrennte
Bauraumhuellen mit gespiegelter Bewegung bereit. Echte Scharniere, Anschlaege,
Verschluesse, Fugen und originale Aussenkonturen werden je Teil angepasst.
Ein Durchmesser aus einem Umfang ist nur eine kreisfoermige Planhuelle,
keine gemessene anatomische Querschnittskontur.

## Fotografischer Startablauf

Ein Tasterplatz liegt vorne an der Flanke. Gestalterische Folge: RGB einschalten,
trockene Luft hochfahren, kurzen OEM-Nebelimpuls separat ausloesen, Nebel stoppen,
Licht/Luft ausklingen lassen. Komfortluefter laufen unabhaengig weiter.
Das ist ein Ablaufplan, keine bereits implementierte synchrone Steuerung.
Originalbedienung und Geraeteschutz behalten ihre Funktion.

Zusatzluft kann Nebel auch zerstreuen. Winkel, Drehzahl und Belichtung werden
mit der tatsaechlichen Kamera getestet. LDD-Licht-PWM kann Banding erzeugen;
hohe LED-Leistung bedeutet nicht automatisch Fototauglichkeit. Die
[Duesenanleitung](Elektronik-Schubduesen.md) beschreibt Aufbau und Abbruch.

## Konfigurierbares Baupaket

Der Generator uebernimmt Licht, HUD, Audio und Nebel aus dem Profil. Bei
Beleuchtung ist die neue Helm-Arbeitsbasis `power-rgb`; mit ausgewaehltem Nebel
kommen Duesen-RGB und trockene Effektluefter hinzu. Kamera beginnt mit `none`.
Technische Leistungen, Waermegrenzen, Masse und Bauraummasse bleiben unbekannt.

Eine eigene JSON-Datei kann einzelne Optionen ueberschreiben:

```json
{
  "camera": "usb-uvc",
  "helmet_light": "power-rgb",
  "helmet_ventilation": "dual-40mm",
  "torso_ventilation": "dual-60mm",
  "nozzle_light": "power-rgb",
  "nozzle_air": "dry-dual-40mm"
}
```

Beispielsweise unter `build/Integration.local.json` speichern und verwenden:

```bash
python3 tools/suit_project.py --profile build/MySuit.local.json --integration build/Integration.local.json --out build/MySuit-r2
```

Synthetische/unvollstaendige Profile benoetigen `--concept`. Licht-, HUD- und
Audiooptionen verlangen die entsprechende aktive Profilausstattung;
Widersprueche werden abgewiesen. Kamera und Startluft sind eigene Optionen.
Duesenlicht/-luft ohne Nebel sind als reiner optischer Effekt moeglich.

| Option | Werte |
| --- | --- |
| `helmet_light` | `none`, `pixel`, `power-rgb` |
| `nozzle_light` | `none`, `power-rgb` |
| `helmet_ventilation` | `passive`, `dual-40mm` |
| `torso_ventilation` | `passive`, `dual-60mm` |
| `nozzle_air` | `none`, `dry-dual-40mm` |
| `hud` | `none`, `combiner` |
| `camera` | `none`, `usb-uvc`, `csi-local` |
| `audio` | `none`, `chest-speaker` |

`Integration.json/.md` fuehren Einbauzonen und Stromkreise.
`integration.local.json` sichert die gewaehlten Optionen.
`engineering.local.json` enthaelt die dazugehoerigen Verbraucher;
`thermal.local.json` trennt LED-Kuehlkoerper, Farbchips und Luftwege.
Diese Dateien werden mit echten Messdaten ausgefuellt. Recorder-/Hostleistung
nicht nochmals inklusive bereits getrennt erfasster Kamera/Displays eintragen;
eine gemeinsame Eingangsmessung wird als eine Verbraucherbaugruppe erfasst.

Eine geaenderte Integrationsauswahl erzeugt eine neue Revision. Die Budgetvorlage
wird nicht automatisch umgerechnet: [Licht-Einkauf](../../Materials/Mjolnir-Licht-Einkauf.md)
und bestehende BOM positionsweise abgleichen; FOG-Licht-/Versorgungsposten
gegebenenfalls ersetzen. Alte Nachweise werden nicht als neue Proben uebernommen.

## Naechste reale Einbauprobe

Zuerst Helmrohbau mit Visier, Luftwegen und einem vollstaendigen RGB-Paar
testen. Flankenkassetten mit gewogenen Ersatzmassen auf Sitzen, Zugang und
Lastverteilung pruefen. Eine komplette Arm-/Beinkassette mit Gegenhandbedienung
folgt vor den Gegenseiten. Erst dann finale Halter, Leitungslaengen und
LED-Betriebsstroeme festlegen. [Helm-Optik und Audio](Mjolnir-Helmintegration.md),
[Luftfuehrung](Elektronik-Luefter.md) und
[Thermalrechnung](../../Design/Thermal/README.md) enthalten die Detailproben.
