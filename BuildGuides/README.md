# Build Guides

Schritt-fuer-Schritt Anleitungen fuer den Bau der MJOLNIR-Ruestung. Jeder Bereich hat 2 Schritte.

## Welcher Pfad gilt fuer mich? (Varianten)

Die Step-by-Step-Anleitungen unten (`Armor/`, `Helmet/`, `Electronics/`) beschreiben den
**3D-Druck-Pfad (V2)** im Detail. Je nach Variante (siehe `Documentation/Guides/Varianten.md`)
ist dein Einstieg leicht anders:

- **V1 (Einsteiger, Foam):** Folge statt 3D-Druck dem kompletten Foam-Weg in
  `Documentation/Guides/Foam-Bau.md` (Templates, Schneiden, Heat-Forming, Versiegeln) und
  `Documentation/Guides/Klebetechniken.md`. Helm-, Befestigungs- und Elektronik-Schritte
  unten gelten sinngemaess; Finishing fuer Foam: `Documentation/Guides/Lackierung-Finishing.md`
  (Abschnitt "Foam-Finishing").
- **V2 (Fortgeschritten, 3D-Druck/H2C):** Folge dieser Spine 1:1 (Helm -> Ruestung ->
  Elektronik), Druckdetails in `Documentation/Guides/3D-Druck.md`.
- **V3 (Profi, Exoskelett + AR):** Wie V2, zusaetzlich Exoskelett-Aufbau und -Montage in
  `Documentation/Guides/Exoskelett.md` sowie AR-Display in
  `Documentation/Guides/Elektronik-AR-Display.md`.

Alle drei Varianten enden im selben Convention-Abschluss: `Documentation/Guides/Checklisten.md`,
`Documentation/Guides/Transport.md`, `Documentation/Guides/Convention-Regeln.md`.

## Reihenfolge (empfohlen)

1. **Helm** — laengste Nachbearbeitung, Herzstueck des Builds
2. **Ruestung** — groesstes Volumen, definiert die Silhouette
3. **Elektronik** — parallel zum Bau auf dem Tisch aufbauen

## Helm

- `Helmet/Step1.md` — Shell, Visor, Innenraum (Skalierung, Druck, Vakuumformen, Polsterung)
- `Helmet/Step2.md` — Elektronik, Lackierung, Finish (OLED, Luefter, Lack, Endmontage)

## Ruestung

- `Armor/Step1.md` — Planung, Skalierung, Unteranzug (Koerpermasse, STL-Skalierung, Befestigung)
- `Armor/Step2.md` — Druck, Zusammenbau, Finish, Montage (Workflow, Lackierung, An-/Ausziehen)

## Elektronik

- `Electronics/Step1.md` — Systemplanung und Verkabelung (Komponentenliste, Strombudget, Loeten)
- `Electronics/Step2.md` — Software, Tests, Integration (Pi Setup, Arduino, LED-Effekte, Dauertest)

## Weitere Guides

Ergaenzende Details in `Documentation/Guides/`:
- 3D-Druck Einstellungen: `Documentation/Guides/3D-Druck.md`
- Lackierung/Weathering: `Documentation/Guides/Lackierung-Finishing.md`
- Elektronik-Details: `Documentation/Guides/Elektronik-HUD.md` und weitere
- Befestigungssystem: `Documentation/Guides/Unteranzug-Befestigung.md`
