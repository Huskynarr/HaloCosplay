# Parametrische Komponentenproben

Dieser Baukasten liefert editierbare Pass- und Materialproben fuer den Innenausbau.
Die sechs Modelle sind eigene generische Konstruktionen. Sie enthalten keine
originalgetreuen Halo-Aussenschalen und ersetzen keine reale Pass-, Temperatur-,
Bewegungs- oder Festigkeitspruefung. Alle Ausgaben bleiben
**COMPONENT_PROTOTYPES_NOT_VALIDATED** und `fabrication_approved: false`.

## Enthaltene Komponenten

| Selector | Modell | Entscheidungszweck |
| --- | --- | --- |
| `visor_retainer` | Drei gebogene U-Leisten mit unterschiedlichen Nutspielen | Visiermaterial einfuehren, loesen und auf Abrieb pruefen |
| `fan_bracket` | Montageplatte mit vier Luefterbohrungen und zwei geschlitzten Laschen | Kaufteil-Lochbild und erreichbare, loesbare Montage pruefen |
| `seam_coupon` | Drei Feder-/Nut-Plattenpaare | Fugenpassung vor und nach Schleifen/Lackieren vergleichen |
| `joint_cover` | Flache gerippte flexible Probe | Biegung, Rueckstellung, Optik und Stoffkontakt vergleichen |
| `hinge_coupon` | Drei Stifthuelsen, Schraubenbohrungen und ein loser Vergleichsstift | Reales Stiftspiel und Schraubenkopf-Freiraum messen |
| `magnet_mount` | Zwei Magnettraeger mit verschraubten Lochdeckeln, Fuehrungsstiften und Textilschlitz | Leichte Teile ansetzen, seitlich fuehren und mit Handschuhen abheben |

Die Visiersegmente und Fugenpaare sind entlang der positiven Y-Achse angeordnet;
die Huelsen und Schraubenbohrungen entlang der positiven X-Achse. In dieser
Reihenfolge gilt die Liste `clearances_mm`, standardmaessig 0.2 / 0.4 / 0.6 mm.
Der Wert ist das **Gesamtspiel**, nicht der Zuschlag je Seite. Ein gedruckter
Vergleichsstift hat selbst Fertigungstoleranz; fuer die Auswahl zaehlt das reale
Kaufteil. Kein Coupon stellt ein lasttragendes Scharnier dar.

## Profilbezogener Export

Aus dem Repository-Stamm:

```bash
python3 tools/suit_components.py --demo --concept --out build/Demo-Components-r1
python3 tools/suit_components.py --profile build/Suit-A/profile.json --out build/Suit-A/Components-r1
```

Ohne `--out` liegt das Paket unter `build/<Profilname>/Components`.
Synthetische und unvollstaendige Profile benoetigen ausdruecklich `--concept`.
Ein vorhandener Ausgabeordner wird nicht ueberschrieben. Fuer Aenderungen einen
neuen Revisionsordner waehlen. Vorlagen bleiben unveraendert.

Fuer eine Kaufteilanpassung `ExampleConfig.json` kopieren und Werte ersetzen.
Die Konfiguration darf auch nur einzelne Parameter enthalten:

```json
{
  "visor_sheet_mm": 1.2,
  "visor_radius_mm": 140,
  "fan_size_mm": 40,
  "fan_hole_pitch_mm": 32,
  "clearances_mm": [0.2, 0.4, 0.6]
}
```

Diese Zahlen sind Probenwerte, keine Zusicherung eines bestimmten Kaufteils.
Anschliessend beispielsweise:

```bash
python3 tools/suit_components.py --demo --concept --config build/Components-r2.json --out build/Demo-Components-r2
```

Die Profilkopplung bestimmt ohne explizite Vorgabe nur den Visierradius als halbe
Helmhuellenbreite. Das ist ein Startwert fuer eine gebogene Passprobe, keine
abgeleitete optische Visierform. Luefter, Befestiger und Fuehrungsspiele werden
nicht aus Koerpergroesse skaliert. Der Materialpfad des Profils waehlt kein
automatisch nachgewiesenes Druckmaterial.

## Bearbeitung und Einzelteile

`ComponentKit.scad` laedt die benachbarte `Parameters.scad`; beide Dateien werden
in das Projektpaket kopiert und funktionieren gemeinsam ohne das Repository.
`component` waehlt ein Modell. `layout` ist eine Uebersicht, kein kollisionsfrei
gepacktes Druckplattenlayout. Einzelteile exportieren und im Slicer ausrichten.

```bash
openscad --hardwarnings -D 'component="visor_retainer"' -o build/VisorRetainer.stl Design/Components/ComponentKit.scad
openscad --hardwarnings -D 'component="fan_bracket"' -o build/FanBracket.stl Design/Components/ComponentKit.scad
openscad --hardwarnings -D 'component="seam_coupon"' -o build/SeamCoupon.stl Design/Components/ComponentKit.scad
openscad --hardwarnings -D 'component="joint_cover"' -o build/JointCover.stl Design/Components/ComponentKit.scad
openscad --hardwarnings -D 'component="hinge_coupon"' -o build/HingeCoupon.stl Design/Components/ComponentKit.scad
openscad --hardwarnings -D 'component="magnet_mount"' -D 'magnet_part="base"' -o build/MagnetBase.stl Design/Components/ComponentKit.scad
```

Die Beispielparameter der Quelldatei sind unabhaengige Tischproben. Der
projektbezogene Export enthaelt zusaetzlich `Config.json`, `Manifest.json`,
`BOM.json`, eine Uebersicht und je Komponente eine konkrete Passprobenanleitung.
Das Manifest speichert SHA-256 von Profil, CAD-Quelle und optionaler Konfiguration.
Direkte Aenderungen in `Parameters.scad` veraendern die Geometrie, aktualisieren
aber nicht diese Provenienz; fuer dokumentierte Revisionen erneut exportieren.

## Magnetpaar zum leichteren Anlegen

`component="magnet_mount"` ergaenzt eine universelle, noch ungepruefte
Schnittstelle fuer leichte Kosmetikplatten oder die Ausrichtung einer Kassette.
Das Modell ist separat von der Halo-Aussenhaut; Einbauorte und verstaerkte
Montageflaechen muessen am gewaehlten Schalenmodell angepasst werden.
Bei Arm-/Beinkassetten bleiben Scharnier und mechanischer Verschluss erhalten.

| `magnet_part` | Druckteil / Ansicht | Funktion |
| --- | --- | --- |
| `base` | Traeger mit zwei nach oben offenen Magnettaschen | Montageohren an den kurzen Enden; geschlossener Boden |
| `base_lid` | Lochdeckel mit zwei konischen Fuehrungsstiften | Kleinere Fenster halten die Magnete gefangen |
| `mate` | Gegenhalter mit zwei Magnettaschen und Fuehrungsaufnahmen | Seitliche Montageohren und Schlitz fuer die Zugschlaufe |
| `mate_lid` | Lochdeckel mit Fuehrungs- und Textiloeffnungen | Verschraubte Rueckhaltung der gegenueberliegenden Magnete |
| `layout` | Vier auseinandergelegte Teile, voreingestellt | Uebersicht der Druckteile, alle Unterseiten auf Z=0 |
| `assembly` | Paar in geschlossener Einbaulage | Montagevorschau; nicht als ein Teil drucken |

Standard: vier axial magnetisierte Magnete mit **10 x 3 mm**, zwei je Haelfte.
`magnet_clearance_mm=0.3` ist das gesamte diametrale Taschenspiel;
`magnet_axial_clearance_mm=0.2` ist die zusaetzliche Taschentiefe.
Die 1-mm-Lochdeckel decken die aeussere Magnetkante um 0.8 mm radial ab.
Damit bleiben die Magnete ohne Einkleben im verschraubten Traeger. Die beiden
Kontaktseiten liegen mindestens 2 mm auseinander; am Taschenboden sitzende
Magnete haben 2.4 mm Abstand. Die reale Haltekraft bei diesem Abstand ist zu messen.

Die beiden Schrauben je Haelfte halten zugleich Deckel und Traeger am
verstaerkten Untergrund. Mit passenden breiten Scheiben und Muttern montieren;
die Bohrung von 3.4 mm ist ein Startwert fuer eine M3-Passprobe. Schraubenlaenge
nach Materialstaerke des Untergrunds und realen Kaufteilen bestimmen.
Die Montageohren sind gegeneinander versetzt, damit die Schraubkoepfe ausserhalb
der gegenueberliegenden Kontaktplatte liegen. Die Schrauben-/Scheibenkontur
dennoch am eigenen Aufbau auf Freigang pruefen.

Alle vier Teile liegen mit ihrer ebenen Unterseite auf dem Druckbett; Taschen,
Fenster und Stifte zeigen nach oben. Magnete erst **nach** dem Druck und nach
Polprobe einsetzen. Die Deckel jeweils auf den passenden Traeger schrauben.
Vor dem Verschrauben in gewendeter Einbaulage pruefen, dass beide Magnetpaare
sich anziehen, und die zusammengehoerenden Kontaktpole markieren.
Durch den gemeinsamen Schlitz von `mate` und `mate_lid` eine greifbare
Textilschlaufe faedeln und vernaehen. Zum Zusammenfuegen `mate` samt Deckel
um 180 Grad um X wenden, dann die Stifte in die Aufnahmen fuehren. Die Schlaufe
hebt beim Oeffnen eine Kante ab; sie entriegelt keinen Kassettenverschluss.

10-mm-Probenpaket erzeugen und alle vier Teile einzeln exportieren:

```bash
python3 tools/suit_components.py --demo --concept --out build/Magnet10-r1
for part in base base_lid mate mate_lid; do
  openscad --hardwarnings -D 'component="magnet_mount"' -D "magnet_part=\"${part}\"" -o "build/Magnet10-r1/magnet_${part}.stl" build/Magnet10-r1/ComponentKit.scad
done
```

Fuer 12 x 3 mm denselben Baukasten mit der
[partiellen Vergleichskonfiguration](Magnet12Config.json) exportieren und die
Einzelteilbefehle auf den neuen Ordner anwenden:

```bash
python3 tools/suit_components.py --demo --concept --config Design/Components/Magnet12Config.json --out build/Magnet12-r1
```

Magnetdurchmesser und -dicke bleiben Kaufteilmasse und werden nicht aus der
Koerpergroesse skaliert. Die generierte `magnet_mount.md` enthaelt Stueckbedarf,
alle Einzelteilbefehle, Kontaktabstand und Montage-/Passproben. Zuerst die
Taschenpassung und mechanische Rueckhaltung pruefen, dann Halte-, Verschiebe-
und Abhebekraft messen. Es folgen 50 ungetragene Oeffnungszyklen und die
[beidseitige Handschuhprobe](../../Documentation/Guides/Unteranzug-Befestigung.md#erste-anlegeprobe).
Magnet/Stahl ist eine eigene Passprobe; der aktuelle Satz verwendet vier Magnete.

Mit installiertem OpenSCAD prueft
`python3 -m unittest discover -s Tests/Automation -p test_components.py -v`
die acht Einzelteil-STLs fuer 10/12 mm auf geschlossene, konsistent orientierte
Kanten und beide zusammengefuegten Haelften auf gegenseitige Volumenueberschneidung.
Ohne OpenSCAD wird nur dieser Geometrietest als uebersprungen gemeldet.

## Grenzen und Protokoll

Die numerischen Grenzen und Geometriebedingungen verhindern offensichtliche
Ueberschneidungen und nichtpositive Querschnitte. Sie sind keine zertifizierten
Material-, Last- oder Temperaturgrenzen. Druckbare Netzgeometrie beweist keine
Funktion am Koerper. Preise, reale Massen, Schraubenlaengen, Klebstoffe,
Beruehrschutz und endgueltige Einbaupunkte bleiben projektspezifisch.

Vor der Integration sind Istmasse, Druckorientierung, Materialcharge, Finish,
Tischprobe und Ergebnis je Komponente zu dokumentieren. Visierleiste und
Gelenkabdeckung zunaechst ohne Koerperkontakt pruefen. Der Luefterrahmen enthaelt
keinen Rotor-Beruehrschutz. Fugenfedern dienen nur der Ausrichtung. Fuer alle
Komponenten gilt: kein Beleg fuer menschliche Lastaufnahme oder Notausstieg.
