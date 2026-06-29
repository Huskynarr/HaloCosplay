# 3D-Modell fuer den Ruestungs-Viewer

Der interaktive 3D-Viewer (im Web-Guide unter **Visualisierung -> 3D-Ruestungsmodell**)
laedt ein Modell aus diesem Ordner:

```
web/models/spartan.glb
```

Solange diese Datei fehlt, zeigt der Viewer automatisch ein **Platzhalter-Modell**
(Googles "Astronaut", CC-BY) und blendet einen Hinweis ein. Sobald `spartan.glb`
vorhanden ist, wird sie automatisch verwendet.

## Empfohlenes Modell (kostenlos, CC-BY)

**Spartan Armour MKV - Halo Reach** von **McCarthy3D**
- Lizenz: **CC-BY 4.0** (Namensnennung erforderlich, kommerziell erlaubt)
- Komplette Figur, ca. 42.600 Dreiecke - gut fuer das Web geeignet
- Quelle: https://sketchfab.com/3d-models/spartan-armour-mkv-halo-reach-57070b2fd9ff472c8988e76d8c5cbe66

### So holst du die Datei (einmalig, ca. 2 Minuten)

1. Kostenloses Sketchfab-Konto anlegen / einloggen (Downloads brauchen einen Login).
2. Modellseite oeffnen (Link oben) -> Button **Download 3D Model**.
3. Format **glTF** (oder "Autoconverted glTF") waehlen und herunterladen.
4. Aus dem ZIP die `.glb` (oder `scene.gltf` + Texturen) entpacken.
5. Die `.glb` nach `web/models/spartan.glb` kopieren (genau dieser Name).
6. Committen und pushen - GitHub Pages liefert sie dann automatisch aus.

> Hinweis: Falls das Modell als `.gltf` + separate Texturen kommt, am einfachsten
> vorher zu einer einzelnen `.glb` zusammenpacken (z. B. mit `gltf-pipeline`:
> `npx gltf-pipeline -i scene.gltf -o spartan.glb -b`).

## Eigenes Modell verwenden

Du kannst jedes `.glb` nehmen - auch aus deinen eigenen Druck-STLs
(in Blender importieren und als glTF/GLB exportieren). Nenne es `spartan.glb`.

Nach dem Tausch passen die Marker-Positionen evtl. nicht mehr exakt:
Im Viewer den Button **"Kalibrieren"** aktivieren, auf das gewuenschte Bauteil
klicken - die ausgegebenen `pos`/`normal`-Werte in `web/app.js` beim passenden
`ARMOR_PARTS`-Eintrag eintragen.

## Lizenz / Namensnennung

Bei CC-BY ist die Namensnennung Pflicht. Der Viewer zeigt die Quelle automatisch
unter dem Modell an. Bitte diese Angabe nicht entfernen. Beachte ausserdem, dass
"Halo", "Master Chief" und "MJOLNIR" Marken von Microsoft/343 Industries sind -
die Nutzung hier erfolgt als nicht-kommerzielles Fan-Projekt.
