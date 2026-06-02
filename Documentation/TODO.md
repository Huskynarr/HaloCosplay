# Master Chief MJOLNIR Build — TODO

Hauptliste aller offenen Aufgaben, gegliedert nach Phasen. Hake ab was erledigt ist.

**Varianten-Hinweis:** Diese Liste ist fuer den **3D-Druck-Pfad (V2)** geschrieben.
- **V1 (Foam):** Ersetze Phase 2 "3D-Druck" durch den Foam-Bau (`Documentation/Guides/Foam-Bau.md`):
  Templates skalieren, schneiden, Heat-Forming, kleben, **flexibel** versiegeln. Phase 3/4
  (Finishing/Lack) sinngemaess mit flexiblen Produkten, siehe Lackierung-Finishing Abschnitt
  "Foam-Finishing". Elektronik/Befestigung/Convention identisch.
- **V3 (Exoskelett + AR):** Zusaetzlich zu allem unten: Exoskelett bauen, auf der Ruestung
  montieren und Geh-/Lasttest bestehen (`Documentation/Guides/Exoskelett.md`); AR-Display
  planen (`Documentation/Guides/Elektronik-AR-Display.md`). Beides VOR der Integration (Phase 8).

## Phase 1: Planung und Vorbereitung

- [ ] Variante festlegen (V2 empfohlen mit H2C + Loetkolben)
- [ ] Ziel-Con oder Ziel-Datum festlegen
- [ ] Koerpermessungen nehmen (Brust, Taille, Huefte, Armlaenge, Bein-Innenlaenge, Kopfumfang)
- [ ] STL-Set auswaehlen und herunterladen (siehe `Resources/STL-Quellen.md`)
  - [ ] Galactic Armory oder MakerWorld MJOLNIR GEN3 evaluieren
  - [ ] Testdruck eines kleinen Teils zur Qualitaetspruefung
- [ ] Budget erstellen (siehe `Documentation/Guides/Kosten.md`)
- [ ] Con-Regeln der Ziel-Convention pruefen (siehe `Documentation/Guides/Convention-Regeln.md`)
- [ ] Elektronik-Komponenten bestellen (Vorlaufzeit beachten)
- [ ] Filament bestellen (mind. 4 kg PETG)

## Phase 2: 3D-Druck

- [ ] Bambu Studio Projekt anlegen mit Multi-Plate Setup
- [ ] STLs auf Koerper skalieren
- [ ] Teile die nicht passen im Cut Tool splitten
- [ ] **Helm** drucken (Prioritaet — laengste Nachbearbeitung)
  - [ ] Helm-Haelften
  - [ ] Visier-Buck fuer Vakuumformen
  - [ ] Interne Halterungen (OLED, Luefter, Pi-Mount)
- [ ] **Brustplatte** drucken (vorne + hinten)
- [ ] **Schulter-Pauldrons** drucken (L+R)
- [ ] **Unterarme** drucken (L+R)
- [ ] **Oberschenkel** drucken (L+R)
- [ ] **Schienbeine/Knieschutz** drucken (L+R)
- [ ] **Handplatten** drucken
- [ ] **Hueft-/Codpiece** drucken
- [ ] **Stiefelcover** drucken
- [ ] **Detailteile** drucken (Lueftungsgitter, Akzente, Schnallen-Halter)
- [ ] Alle Teile zusammenkleben (CA + Epoxy)
- [ ] Passform-Test mit allen Rohteilen

## Phase 3: Oberflaechenbearbeitung

- [ ] Schleifen: 120er > 240er > Filler Primer > 320er (2-3 Durchgaenge)
- [ ] Naehte und Luecken spachteln (Bondo / XTC-3D)
- [ ] Letzte Grundierung auftragen
- [ ] Finish-Schliff 400-600er

## Phase 4: Lackierung

- [ ] Rust-Oleum Oregano (Satin) als Hauptfarbe kaufen (mehrere Dosen!)
- [ ] Schwarze Farbe fuer Gelenke/Vertiefungen
- [ ] Gunmetal/Silber fuer mechanische Details
- [ ] Grundfarbe auftragen (3-4 duenne Schichten)
- [ ] Panel Lines mit schwarzer Wash vertiefen
- [ ] Dry Brushing: Schwarz auf Kanten, dann Silber
- [ ] Battle Damage / Abplatzer (Metallic Pen)
- [ ] Schwammtechnik fuer Schmutz/Grime
- [ ] Matte Klarlack-Versiegelung (3-4 Schichten)

## Phase 5: Visor

- [ ] PETG-Folie besorgen (0.75-1 mm)
- [ ] Visor-Buck drucken
- [ ] Vakuumform-Setup bauen/organisieren
- [ ] Visor formen und zuschneiden
- [ ] iDye Poly Gold faerben
- [ ] Krylon Looking Glass innen verspiegeln
- [ ] In Helm einpassen und befestigen

## Phase 6: Elektronik

- [ ] Raspberry Pi Zero 2 W einrichten
  - [ ] Pi OS Lite flashen
  - [ ] I2C aktivieren
  - [ ] Python + luma.oled installieren
  - [ ] HUD-Software testen (siehe `Code/HelmetControl/hud_display.py`)
  - [ ] Autostart-Service einrichten (systemd)
  - [ ] Stromspar-Optimierungen in config.txt
- [ ] OLED-Display testen (i2cdetect -y 1)
- [ ] Arduino Nano flashen
  - [ ] LED-Steuerung (WS2812B)
  - [ ] Luefter-PWM
  - [ ] I2C-Slave fuer Pi-Kommunikation
- [ ] LEDs verloeten und testen
  - [ ] Helm-Visor LEDs (6-10 Stueck)
  - [ ] Brustplatte LEDs (8-12 Stueck)
  - [ ] Weitere Zonen nach Bedarf
- [ ] Luefter einbauen und testen (2x 40 mm)
- [ ] Batterie-Setup zusammenstellen
  - [ ] PiSugar 3 Plus montieren
  - [ ] Powerbank fuer LEDs/Luefter
  - [ ] Laufzeittest (mind. 4 Stunden Dauertest)
- [ ] Verkabelung mit JST/XT30 Steckern
- [ ] Quick-Disconnect am Helm-Nacken
- [ ] Alle Elektronik ausserhalb der Ruestung testen
- [ ] Optional: Voice Changer / Lautsprecher

## Phase 7: Unteranzug und Befestigung

- [ ] Unteranzug auswaehlen/bestellen (Morphsuit oder Dive Skin)
- [ ] Klettergurt oder MOLLE-Guertel besorgen
- [ ] Neodym-Magnete bestellen (10x3 mm oder 12x3 mm)
- [ ] Klett-Punkte auf Unteranzug naehen
- [ ] Magnet-Halter 3D-drucken und einkleben
- [ ] Gurte und Schnallen an schweren Teilen befestigen
- [ ] Polsterung in alle Ruestungsteile einkleben
- [ ] Helm-Padding-Kit einbauen + Kinnriemen
- [ ] Kabelwege im Unteranzug anlegen (Spiralschlauch)

## Phase 8: Integration und Test

- [ ] Komplettanzug anziehen (mit Handler!)
- [ ] Sichtfeld-Test (Treppen, Tueren, Engstellen)
- [ ] Beweglichkeitstest (Sitzen, Drehen, Heben, Hocken)
- [ ] Toiletten-Zugaenglichkeit pruefen
- [ ] Elektronik-Gesamttest (HUD + LEDs + Luefter)
- [ ] Laufzeittest Elektronik (mind. 4 Stunden)
- [ ] Temperatur messen (Helm-Innentemperatur mit/ohne Luefter)
- [ ] Gewicht wiegen (Ziel: unter 15-20 kg gesamt)
- [ ] Notausstieg testen (Schnellverschluesse, Quick-Release)
- [ ] Fotos machen und ggf. an Con senden fuer Vorab-Freigabe

## Phase 9: Convention-Vorbereitung

- [ ] Reparatur-Kit packen (siehe Checklisten)
- [ ] Ersatz-Akkus/Powerbanks laden
- [ ] Transport-Boxen mit Polsterung vorbereiten
- [ ] Handler briefen
- [ ] CamelBak/Trinkblase fuellen
- [ ] Con-Regeln nochmal pruefen
- [ ] Props in blickdichte Taschen (Waffengesetz!)
- [ ] Anreise-Route und Parkplatz planen

## Notizen

- Fertigungszeit: Poste-Processing (Schleifen/Lackieren) braucht oft genauso lang wie der Druck selbst
- Helm zuerst fertigstellen — er ist das Herzstueck und braucht am meisten Iterationen
- Immer erst Passform, dann Details
- Elektronik modular halten — wenn etwas ausfaellt, muss der Rest trotzdem funktionieren
