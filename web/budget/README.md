# Stuecklisten- und Budgeteditor

Im Repository-Hauptverzeichnis einen lokalen Server starten:

```bash
python3 -m http.server 8080
```

Danach `http://localhost:8080/web/budget/` oeffnen. Der Editor verwendet keine
externen Skripte, Schriftarten oder Dienste. Nach dem Laden ist keine
Internetverbindung erforderlich. Das optionale Konzeptbeispiel wird ueber
denselben lokalen Server aus `Materials/Mjolnir-BOM.json` geladen. Bei direktem
Oeffnen als Datei kann der Browser diesen Abruf blockieren; JSON-Import ist die
Alternative.

## Eigene Liste

- Der Startzustand ist leer. Das Plan-Massenziel beginnt bei 0 g und ist passend
  zum eigenen Projekt einzutragen; es beschreibt keine persoenliche Belastbarkeit.
- Mengen sind positive ganze Zahlen. Preise gelten je Einheit als EUR-Bereich.
- Die optionale Planmasse gilt ebenfalls je Einheit. Ein leeres Feld wird als
  `null` exportiert und bleibt unbekannt. Der Wert 0 ist dagegen eine explizite
  Planmasse von 0 g.
- Alle Positionen tragen zum Budget bei. Nur als getragen markierte Positionen
  tragen zur bekannten getragenen Planmasse bei. Fehlende Massen getragener
  Positionen werden mit ihrer ID ausgewiesen.
- Das Konzeptbeispiel enthaelt unbestaetigte Budget- und Massenansaetze. Durch das
  Laden entsteht keine Kaufempfehlung oder Bestaetigung einer bestimmten Bauweise.
- Die Reserve erhoeht nur den Kostenrahmen.

JSON explizit herunterladen, bevor die Seite geschlossen wird. Es erfolgt keine
automatische Speicherung. Neue Listen und Imports ersetzen nach Rueckfrage
vorhandene Aenderungen. Ein langsamer Ladevorgang darf neuere Eingaben nicht
ueberschreiben. Exportdateien erhalten den Namen `Cosplay-BOM.local.json` und
werden durch die bestehende Git-Regel fuer `*.local.json` nicht versehentlich
mit eingecheckt.

## Kompatibilitaet und Pruefung

Schema 1, Waehrung EUR; Export und Import verwenden dasselbe Datenformat wie
`tools/suit_budget.py`. Zusaetzliche JSON-Metadaten bleiben beim Import erhalten.

```bash
python3 tools/suit_budget.py --bom pfad/zur/Cosplay-BOM.local.json
node --test Tests/Automation/budget.test.cjs
```

Die Tests pruefen unter anderem Referenzsummen, die Behandlung unbekannter
getragener Massen, den Unterschied zwischen Kosten- und Massensumme sowie
ungueltige Werte. Daraus folgt keine Hardware- oder Tragbarkeitsfreigabe.

## Nebel als Zusatzmodul

Die Schaltflaeche Nebelmodul ergaenzen fuegt die PMI-Beispielpositionen hinzu. Vorhandene Positionen, Reserve und Zielmasse bleiben erhalten; doppelte IDs werden abgelehnt. Massen bleiben unbekannt. Das ist keine automatische Kopplung an die Profilwahl. Bereits vorhandene Lichttechnik, Ausschluesse und Zusatzkosten separat pruefen.
