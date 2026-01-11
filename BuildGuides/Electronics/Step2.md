# Electronics Step 2: Software, Tests, Integration

## Schritte

1. Raspberry Pi OS Lite installieren
2. I2C aktivieren und OLED testen
3. Dependencies installieren (siehe `Code/HelmetControl/requirements.txt`)
4. HUD-Software starten (siehe `Code/HelmetControl/hud_display.py`)
5. Konfig anpassen (siehe `Code/HelmetControl/config.example.json`)
6. Optional: Arduino fuer LED/Luefter anbinden
7. Dauerlauf-Test (2-4 Stunden) ausserhalb der Ruestung
8. Finaler Einbau und Kabelsicherung

## Fehleranalyse

- Display dunkel: I2C-Adresse pruefen
- Pi rebootet: Akku/Spannung pruefen
- LEDs flackern: Masse verbinden, Data-Leitung schirmen
