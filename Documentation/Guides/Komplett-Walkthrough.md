# Komplett-Walkthrough (Anfaenger bis Profi)

Der **rote Faden** durch das ganze Projekt: ein durchgehender, geordneter Weg von der
ersten Entscheidung bis zum Auftritt auf der Convention. Jeder Schritt verlinkt den
passenden Detail-Guide und ist markiert nach Schwierigkeit und Variante.

Wenn du nur EINE Datei liest, lies diese - und springe von hier aus in die Tiefe.

## Legende

- **Level:** [A] Anfaenger · [F] Fortgeschritten · [P] Profi
- **Variante:** (V1) Foam/guenstig · (V2) 3D-Druck/H2C + HUD · (V3) Profi/Exoskelett/AR
- (alle) = gilt fuer jede Variante

Variantenvergleich und Auswahl: `Documentation/Guides/Varianten.md`.
Begriffe unklar? `Documentation/Guides/Glossar.md`.

## Phase 0 - Entscheidung und Planung (alle, [A])

1. [A] Variante waehlen: `Documentation/Guides/Varianten.md`
2. [A] Ziel setzen (Con-Datum oder Foto-Shoot) und realistisch gegen den Zeitplan pruefen:
   `Documentation/Guides/Zeitplan.md`
3. [A] Budget abstecken: `Documentation/Guides/Kosten.md`
4. [A] Die 15 haeufigsten Anfaengerfehler lesen (spart Wochen): `Documentation/Guides/Anfaengerfehler.md`
5. [A] Authentischen Look festlegen (Halo Infinite): `Documentation/Guides/Authentizitaet-Referenz.md`
6. [A] Werkzeug- und Materialueberblick: `Documentation/Guides/Materialien.md`

## Phase 1 - Vermessung und Skalierung (alle, [A])

1. [A] Koerpermasse nehmen (mit Unteranzug, zweite Person): `Documentation/Guides/Messblatt.md`
2. [A]/(V2,V3) STL-Set waehlen und auf die Masse skalieren: `Resources/STL-Quellen.md`,
   `BuildGuides/Armor/Step1.md`
3. [A]/(V1) Foam-Templates (Pepakura/Patterns) auf die Masse skalieren:
   `Documentation/Guides/Foam-Bau.md`
4. [A] Tragesystem grob planen (Last auf die Huefte): `BuildGuides/Armor/Step1.md`,
   `Documentation/Guides/Unteranzug-Befestigung.md`

## Phase 2 - Beschaffung (alle, [A])

1. [A] Detaillierte Einkaufsliste durchgehen und bestellen: `Materials/ShoppingList.md`
2. [A] Elektronik mit Vorlauf bestellen (Lieferzeit!): `Documentation/Guides/ElectronicsGuide.md`
3. [A]/(V2,V3) Filament bestellen; Druck-Setup vorbereiten: `Documentation/Guides/3D-Druck.md`
4. [A]/(V1) Foam, Kontaktkleber, Versiegelung, Klingen: `Documentation/Guides/Foam-Bau.md`

## Phase 3 - Korpus bauen

Hier trennen sich die Wege je nach Variante - das Ergebnis (Rohteile am Koerper) ist gleich.

### (V1) Foam-Weg [A]

1. [A] Lernteil bauen (Unterarm/Schienbein): `Documentation/Guides/Foam-Bau.md`
2. [A] Kleber richtig waehlen: `Documentation/Guides/Klebetechniken.md`
3. [A] Restliche Teile schneiden, formen (Heat-Forming), kleben, versiegeln:
   `Documentation/Guides/Foam-Bau.md`

### (V2,V3) 3D-Druck-Weg [F]

1. [F] Druckeinstellungen, Splitting, Orientierung (Bambu Lab H2C): `Documentation/Guides/3D-Druck.md`
2. [F] Druck-Reihenfolge und Skalierung: `BuildGuides/Armor/Step1.md`
3. [F] Drucken, zusammenkleben (CA/Epoxy), Passform-Test: `BuildGuides/Armor/Step2.md`,
   `Documentation/Guides/Klebetechniken.md`

## Phase 4 - Helm und Visor (alle)

1. [A]/(V1) Foam-Helm (Pepakura-Schalen) oder Fertighelm + einfache getoente Visor-Folie:
   `Documentation/Guides/Foam-Bau.md` (Abschnitt 11 "Helm aus Foam")
2. [F]/(V2,V3) Helm-Shell und Innenraum: `BuildGuides/Helmet/Step1.md`
3. [F]/(V2,V3) Visor herstellen (Vakuumformen, faerben, verspiegeln):
   `Documentation/Guides/Lackierung-Finishing.md` (Abschnitt Visor) +
   `BuildGuides/Helmet/Step1.md`
4. [F] Visor-Probleme loesen (Beschlag, Kratzer, Toenung): `Documentation/Guides/Lackierung-Finishing.md`
   (Visor-Troubleshooting), `Documentation/Guides/Praxis-Tipps-Fortgeschritten.md`
5. [F]/(V2,V3) Helm-Elektronik/-Finish vorbereiten: `BuildGuides/Helmet/Step2.md`

## Phase 5 - Finishing und Lackierung (alle, [F])

1. [F]/(V2,V3) Schleifen, spachteln, grundieren (Layer Lines weg):
   `Documentation/Guides/Lackierung-Finishing.md`
2. [A]/(V1) Foam **flexibel** versiegeln und grundieren (kein harter Primer!):
   `Documentation/Guides/Lackierung-Finishing.md` (Abschnitt Foam-Finishing)
3. [F] Master-Chief-Gruen lackieren (Halo Infinite): `Documentation/Guides/Lackierung-Finishing.md`
4. [F] Weathering (Wash, Dry Brushing, Battle Damage) - Logik nach `Authentizitaet-Referenz.md`
5. [F] Matter Klarlack als Schutz: `Documentation/Guides/Lackierung-Finishing.md`

## Phase 6 - Elektronik (Modul fuer Modul)

Reihenfolge strikt einhalten: erst Strom, dann Module einzeln. Uebersicht und
Modulmatrix (was pro Variante sinnvoll ist): `Documentation/Guides/ElectronicsGuide.md`.

1. [F] Strombudget rechnen: `Documentation/Guides/Elektronik-Strombudget.md`
2. [F] Batterie/Stromverteilung waehlen: `Documentation/Guides/Elektronik-Batterie.md`
3. [F] Verdrahtung und Power-Verteilung (Sicherung, Stecker): `Documentation/Guides/Elektronik-Verdrahtung.md`
4. [A]/(V1) Einfache LEDs; [F]/(V2,V3) adressierbare LED-Effekte: `Documentation/Guides/LED-Effekte.md`,
   `Code/` (Arduino-Sketches)
5. [F] Helm-Belueftung (Luefter gegen Beschlag/Hitze): `Documentation/Guides/Elektronik-Luefter.md`
6. [F]/(V2,V3) Transparentes OLED-HUD + Pi-Software: `Documentation/Guides/Elektronik-HUD.md`,
   `Code/HelmetControl/hud_display.py`
7. [F] Autostart einrichten (systemd): `Documentation/Guides/Elektronik-Autostart.md`
8. [F] Audio/Voice-Changer (optional): `Documentation/Guides/Elektronik-Audio.md`
9. [F] Visor-LED-Diffusion/Foto-Tauglichkeit verstehen: `Documentation/Guides/LED-Visor-Forschung.md`

## Phase 7 - Unteranzug und Befestigung (alle, [F])

1. [F] Unteranzug, Magnete, Klett, Harness: `Documentation/Guides/Unteranzug-Befestigung.md`
2. [F] Teile am Tragesystem befestigen, Polsterung einkleben: `BuildGuides/Armor/Step2.md`

## Phase 8 - Profi-Ausbau (nur V3, [P])

1. [P] Exoskelett bauen, auf der Ruestung montieren, Geh-/Lasttest: `Documentation/Guides/Exoskelett.md`
2. [P] AR-Display planen (Stufen A/B/C, Sicherheit): `Documentation/Guides/Elektronik-AR-Display.md`
3. [P] AR-Passthrough-Code aufsetzen und testen: `Code/HelmetControl/AR/README.md`

## Phase 9 - Integration und Tests (alle, [F])

1. [F] Software/Hardware integrieren, Dauertest: `BuildGuides/Electronics/Step2.md`
2. [F] Komplettanzug anziehen (mit Handler), Sicht-/Beweglichkeitstest: `Documentation/TODO.md` (Phase 8)
3. [F] **Sicherheit**: Hitze, Sichtfeld, Notausstieg, LiPo: `Documentation/Guides/Sicherheit.md`
4. [F] Fehler systematisch beheben: `Documentation/Guides/Fehlerbehebung.md`

## Phase 10 - Convention (alle, [A])

1. [A] Pack- und Reparatur-Checklisten: `Documentation/Guides/Checklisten.md`
2. [A] Con-Regeln und Waffengesetz (Props!): `Documentation/Guides/Convention-Regeln.md`
3. [A] Transport der Ruestung: `Documentation/Guides/Transport.md`
4. [A] Con-Alltag (Essen, Trinken, Pausen, Hitze): `Documentation/Guides/Convention-Alltag.md`
5. [A] Fotoshooting: `Documentation/Guides/Fotoshooting.md`

## Nach der Con

- [A] Pflege, Wartung, Reparatur, Lagerung: `Documentation/Guides/Pflege-Wartung.md`
- [F] Upgrade-Pfad V1 -> V2 -> V3: `Documentation/Guides/Varianten.md`
- [A] Best Practices verinnerlichen: `Documentation/Guides/Best-Practices.md`
- [A] Austausch in der Community: `Resources/Community.md`

## Wenn du nicht weiterkommst

- Begriffe: `Documentation/Guides/Glossar.md`
- Haeufige Fragen: `Support/FAQ.md`
- Fehlerbehebung: `Documentation/Guides/Fehlerbehebung.md`
- Anfaengerfehler vermeiden: `Documentation/Guides/Anfaengerfehler.md`
