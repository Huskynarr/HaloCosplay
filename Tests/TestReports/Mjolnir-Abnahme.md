# V4: Abnahmevorlage fuer reale Prototypen

**Leere Vorlage, kein bestandener Test.** Pro Durchgang eine eigene Datei mit
Revision, Datum, pruefender Person, Aufbau, Messmitteln und Fotos anlegen.
Koerperdaten und personenbezogene Nachweise standardmaessig lokal halten.

## Kopf des Protokolls

- Test-ID / Baugruppen-ID / CAD-Revision / Firmware-Revision:
- Datum / Pruefperson / Umgebung / Bekleidung / eingesetztes Exoskelett:
- Ist-Masse und Schwerpunkt / Messmittel / Fotos oder Video mit Zeitmarken:
- Vorbedingungen / vereinbarte Grenzwerte / Abbruchkriterien:
- Einzelmessungen / Beobachtungen / bestanden oder fehlgeschlagen:
- Maengel / Korrektur / betroffene Nachpruefungen / verantwortliche Freigabe:

## Nachweismatrix

| Gate | Versuch | Erforderlicher Nachweis |
| --- | --- | --- |
| REF | Referenzvergleich | Acht Ansichten erfasst, Variantenabweichungen bewertet |
| FIT | Messung und Passprobe | Offene Eingaben geklaert, dynamische Freiraeume, linke/rechte Seite |
| CAD | Detail- und Fertigungspruefung | Keine Platzhalter, Teilzeichnungen, Montage und Materialwahl |
| MECH | Tischversuch / Rohbau | Lastannahmen, Lagerung, Anschlaege, Verschluesse, Kabelwege |
| EXIT | Stromloser Ausstieg | Drei Durchgaenge mit Handschuhen, Helfer und Zeitmessung |
| VISION | Sicht / Beschlag / Audio | Test bei heller/dunkler Umgebung und Stromausfall |
| THERMAL | Gestufter Trageversuch | Dauer, Umgebung, Messposition, Beschwerden und Abbruchzeit |
| POWER | Elektrische Pruefung | Verbraucher, Spitzen, Absicherung, Laufzeit und Ausfallverhalten |
| FINISH | Optische Abnahme | Referenzvergleich, Nah-/Fernansichten, Farbproben |
| STAND | Ungetragenes Exponat | Gesamtlast, Schwerpunkt, Kippsicherheit und Publikumsabstand |
| DEMO | Wiederholte Vorfuehrung | Reale Zyklenzahl, Stoerungen, Wiederanlauf ohne Eigenbewegung |
| EVENT | Konkreter Veranstaltungseinsatz | Ausgabe, Betriebsart, Unterlagen, Bedingungen/Rueckmeldung |

Ziele aus dem Konzept (Anziehen <5 min, Ausstieg <60 s, Basismasse <12 kg) sind
keine Grenzwerte einer Norm und keine erreichten Ergebnisse. Eine Ueberschreitung
fuehrt zur Neubewertung; ein unterschrittener Zeitwert allein beweist keine Sicherheit.
Lasten, Pruefkraefte, Temperatur- und elektrische Grenzen vor dem jeweiligen
Versuch aus realem Aufbau und Fachpruefung festlegen, nicht nachtraeglich passend waehlen.

## Dokumentationsstatus per Werkzeug

`python3 tools/suit_readiness.py` erzeugt den aktuellen Nachweisbericht.
`--require wearable` bzw. `--require exhibition` liefert Exitcode 2, solange
Nachweise fehlen. Das prueft Dokumentvollstaendigkeit, keine reale Sicherheit.
Eine Vorlage, ein CAD-Render und bestandene Softwaretests sind keine Hardwareabnahme.

[Nachweisregister](../../Progress/Mjolnir-Readiness.json) enthaelt anfangs nur offene
Gates. Fuer reale Ergebnisse eine private Kopie `build/readiness.local.json`
verwenden; Nachweise mit SHA-256, Datum, Revision und Pruefperson registrieren.

## Separate Projekte und Profilrevisionen

Ein neues Register entsteht ohne bestandene Gates:

```bash
python3 tools/suit_readiness.py --init build/SuitA/readiness.local.json --project SuitA --revision r1 --profile build/SuitA.local.json
python3 tools/suit_readiness.py --manifest build/SuitA/readiness.local.json --out build/SuitA/Readiness.local.md
```

Das Profil muss bereits existieren. Standardwurzel fuer Profil-/Nachweisdateien
ist das Repository; `--root` erlaubt eine eigene Projektwurzel. Alle referenzierten
Dateien muessen darin liegen. Die optionale Profilbindung speichert SHA-256:
Aenderungen an Mass- oder Baukonfiguration machen vorhandene Nachweise unvollstaendig,
bis diese fuer die neue Revision bewertet werden. Keine bestehenden Register
werden durch `--init` ueberschrieben. Pruefdatum als UTC-Kalendertag dokumentieren.
