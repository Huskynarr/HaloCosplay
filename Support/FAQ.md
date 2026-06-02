# FAQ (Haeufig gestellte Fragen)

## Einstieg

**Wie starte ich am besten?**
- Lies `Documentation/Guides/Start-Hier.md` und waehle eine Variante (`Varianten.md`). Fuer das erste Cosplay V1 (Foam) oder V2 (3D-Druck mit H2C).

**Welche Variante soll ich waehlen?**
- V1 fuer den Einstieg (Foam, guenstig, schnell)
- V2 fuer detaillierte Builds mit HUD und 3D-Druck (empfohlen mit Bambu Lab H2C)
- V3 fuer Showpiece-Exoskelette (Profi-Level)

**Wo finde ich die TODO-Liste fuer das ganze Projekt?**
- `Documentation/TODO.md` — 9 Phasen mit Checkboxen von Planung bis Convention.

## Kosten und Zeit

**Was kostet das Ganze?**
- V1: 800-2.700 EUR, V2: ~680-1.140 EUR Materialkosten (ohne Tools/Fehlversuche), V3: 615-1.630 EUR (Exo+Ruestung). Realistisch: 1.5-2x der Materialkosten.
- Detaillierte Aufstellung: `Documentation/Guides/Kosten.md` und `Materials/ShoppingList.md`

**Wie lange dauert es?**
- Hobby-Tempo (10-15h/Woche): 5-8 Monate fuer V2
- Intensiv (30-40h/Woche): 3-4 Monate
- Details und Parallelisierungstipps: `Documentation/Guides/Zeitplan.md`

**Was brauche ich mindestens fuer eine Convention?**
- Helm + Brustplatte + Unterarme + Schienbeine — damit sieht man sofort wie Master Chief aus.

## 3D-Druck

**Welches Filament soll ich nehmen?**
- **PETG** fuer tragbare Ruestung (schlagfest, hitzebestaendig bis ~80 C)
- **PLA+** fuer Prototypen und feine Details
- Details: `Documentation/Guides/3D-Druck.md`

**Wie viel Filament brauche ich?**
- Komplettes Set: ca. 2.250-3.650 g (3-4 kg). Kosten: 50-90 EUR (PETG).

**Passt der Helm in den Bambu Lab H2C?**
- Nicht am Stueck. Mit dem Cut Tool (Taste C) in 2-3 Teile splitten. Details: `Documentation/Guides/3D-Druck.md`

**Was ist das beste STL-Set?**
- Kostenpflichtig: **Galactic Armory** (~60 USD, 76 vorgeschnittene Teile)
- Kostenlos: **MakerWorld MJOLNIR GEN3** (Timberlake Creations, hoch detailliert)
- Uebersicht: `Resources/STL-Quellen.md`

## Elektronik

**Wie schwer ist die Ruestung?**
- V1 ca. 8-15 kg, V2 ca. 12-20 kg, V3 variabel (Ziel unter 25 kg).

**Kann ich das HUD auch guenstig bauen?**
- Ja, ein einfarbiger LED-Akzent im Visor wirkt bereits stark, kostet <20 EUR und spart Strom. Das volle OLED-HUD kostet ca. 85-115 EUR an Elektronik.

**Wie lange haelt der Akku?**
- PiSugar 3 Plus (5000 mAh) allein: ca. 3.3 Stunden
- Mit 2x 10.000 mAh Powerbank: 13+ Stunden — mehr als genug fuer eine Convention
- Details: `Documentation/Guides/Elektronik-Batterie.md`

**Brauche ich Arduino UND Raspberry Pi?**
- Pi fuer HUD-Display (braucht Grafik-Library). Arduino fuer LEDs (braucht Echtzeit-Timing). I2C-Verbindung zwischen beiden. Details: `Documentation/Guides/Elektronik-HUD.md`

## Convention

**Brauche ich einen Handler?**
- Fuer V2 mit eingeschraenkter Helm-Sicht: empfohlen. Fuer V3 oder Exo: **Pflicht**.

**Darf ich eine Prop-Waffe mitbringen?**
- Kommt auf die Convention an. **Gamescom verbietet ALLE Waffen-Props.** DoKomi/MCC erlauben Foam/Kunststoff mit Einschraenkungen. Props IMMER in blickdichter Tasche transportieren (Waffengesetz!). Details: `Documentation/Guides/Convention-Regeln.md`

**Wie gehe ich auf Toilette in voller Ruestung?**
- Helm ab, Handschuhe ab, Codpiece ab (Quick-Release!). Plane 10-15 Minuten ein. Handler wartet mit den Teilen. Details: `Documentation/Guides/Convention-Alltag.md`

**Wie trinke ich im Helm?**
- CamelBak-Trinkblase mit Schlauch zum Helm-Kinn. Zu Hause vorher testen! Details: `Documentation/Guides/Convention-Alltag.md`

## Hilfe und Community

**Wo finde ich Hilfe?**
- **405th Infantry Division** (https://www.405th.com/) — DIE Halo-Cosplay-Community
- Weitere Quellen: `Resources/Community.md`

**Gibt es deutsche Cosplay-Communities?**
- Animexx.de, Cosplay.de, Cosplay Corner Germany (Facebook). Kamui Cosplay (YouTube) ist Deutschland-basiert. Details: `Resources/Community.md`
