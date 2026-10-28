# Parametrische Komponentenproben

Dieser Baukasten liefert editierbare Pass- und Materialproben fuer den Innenausbau.
Die fuenf Modelle sind eigene generische Konstruktionen. Sie enthalten keine
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
```

Die Beispielparameter der Quelldatei sind unabhaengige Tischproben. Der
projektbezogene Export enthaelt zusaetzlich `Config.json`, `Manifest.json`,
`BOM.json`, eine Uebersicht und je Komponente eine konkrete Passprobenanleitung.
Das Manifest speichert SHA-256 von Profil, CAD-Quelle und optionaler Konfiguration.
Direkte Aenderungen in `Parameters.scad` veraendern die Geometrie, aktualisieren
aber nicht diese Provenienz; fuer dokumentierte Revisionen erneut exportieren.

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
