# Tests

## MJOLNIR-Entwicklung

Physische Kriterien: [Prototypen und Abnahme](../BuildGuides/Armor/Mjolnir-Prototypen.md). Berechnungspruefung: `python3 -m unittest discover -s Tests/Automation -v`. Softwaretests ersetzen keine Pass-/Lastprobe.

Vorlagen fuer physische Anprobe- und Funktionstests. Vor jeder Convention
mindestens einen vollstaendigen Tragetest dokumentieren (siehe auch
`Documentation/Guides/Checklisten.md`).

## TestReports

- `TestReports/Test1.md` und `Test2.md` sind **Vorlagen** - pro Test kopieren und ausfuellen.
- Sinnvolle Zeitpunkte: nach der ersten kompletten Anprobe, nach Elektronik-Einbau
  (Laufzeit-/Hitzetest) und als Generalprobe 1-2 Wochen vor der Convention.
- Was gemessen wird: Passform, Bewegungsfreiheit, Sichtfeld, Tragedauer,
  Temperatur, Akkulaufzeit, Schwachstellen.
