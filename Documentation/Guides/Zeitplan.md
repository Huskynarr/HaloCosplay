# Zeitplan (Richtwerte)

> **Level:** [A] Anfaenger | [F] Fortgeschritten | [P] Profi  ·  **Varianten:** alle (V1/V2/V3)

## Gesamtdauer

| Tempo | Stunden/Woche | Gesamtdauer |
| --- | --- | --- |
| Intensiv (Vollzeit-Projekt) | 30-40 h/Woche | 3-4 Monate |
| Hobby (regelmaessig) | 10-15 h/Woche | 5-8 Monate |
| Gelegentlich | 5-8 h/Woche | 8-14 Monate |

## Phasen im Detail

| Phase | Inhalt | Dauer (Hobby) | Abhaengigkeiten |
| --- | --- | --- | --- |
| 1 | Planung, Skalierung, Bestellung | 2-4 Wochen | - |
| 2 | Unteranzug + Tragesystem | 1-2 Wochen | Phase 1 |
| 3 | 3D-Druck (H2C laeuft nebenbei) | 2-4 Wochen reine Druckzeit | Phase 1 |
| 4 | Helm-Bau + Visor | 3-6 Wochen | Phase 3 |
| 5 | Ruestung zusammenkleben + Schleifen | 4-8 Wochen | Phase 3 |
| 6 | Elektronik aufbauen + testen | 2-4 Wochen | Phase 1 |
| 7 | Lackierung + Weathering | 3-5 Wochen | Phase 4+5 |
| 8 | Befestigung + Integrationstest | 2-3 Wochen | Phase 2+5+6+7 |
| 9 | Puffer / Nacharbeit | 2-4 Wochen | - |

## Parallelisierung

Viele Phasen koennen parallel laufen — das spart erheblich Zeit:

```
Woche:  1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16
Phase 1 [===]
Phase 2    [==]
Phase 3    [==========]  (Drucker laeuft 24/7 nebenbei)
Phase 4          [=========]
Phase 5          [===============]
Phase 6    [========]  (auf dem Tisch, parallel zum Druck)
Phase 7                      [==========]
Phase 8                               [======]
Phase 9                                     [====]
                                                  ^ Convention
```

**Kritischer Pfad:** Phase 3 (Druck) -> Phase 5 (Schleifen) -> Phase 7 (Lackierung) -> Phase 8 (Integration)

## Engpaesse und Zeitfresser

| Aufgabe | Warum dauert es? | Tipp |
| --- | --- | --- |
| Schleifen/Spachteln | Wiederholend, muss trocknen zwischen Zyklen | Batch-Arbeit: heute schleifen, morgen Primer, uebermorgen schleifen |
| Lackierung | Trocknungszeiten (24-48h zwischen Schichten) | Mehrere Teile rotieren, nie warten |
| Visor-Herstellung | Vakuumformen braucht oft mehrere Versuche | 3-5 PETG-Folien kaufen, nicht nur eine |
| Passform-Korrekturen | Teile passen nicht beim ersten Mal | Testdrucke frueh machen, nicht erst am Ende |
| Elektronik-Debugging | "Funktioniert auf dem Tisch, nicht im Helm" | Frueh integrieren, nicht alles auf die letzten Wochen |

## Varianten-Abweichungen (V1 Foam / V3 Exoskelett)

Die Phasen oben beschreiben den **3D-Druck-Pfad (V2)**. Fuer die anderen Varianten
verschieben sich die Zeitfresser:

### V1 (Foam)

- **Kein Druck-Engpass** (Phase 3 entfaellt). Dafuer wird das Zuschneiden, Heat-Forming
  und vor allem das **Versiegeln** zum Zeitfresser (jede Versiegelungsschicht muss trocknen).
- Schleifen/Spachteln entfaellt weitgehend; Lackierung braucht flexible Produkte.
- Realistisch insgesamt schneller: oft **2-5 Monate** statt 4-8 (siehe
  `Documentation/Guides/Foam-Bau.md`).
- Kritischer Pfad: Schneiden/Kleben -> Versiegeln -> Lackieren -> Befestigung.

### V3 (Exoskelett)

- Zusaetzlich zur V2-Spine: **Exoskelett-Prototyp (PVC) -> Alu/Carbon-Rahmen -> Einlaufen/
  Bewegungstraining**. Plane dafuer **+4-8 Wochen** zusaetzlich ein.
- Exoskelett-Bau laeuft parallel zum Druck, der **Geh-/Lasttest** muss aber vor Lackierung
  und Integration abgeschlossen sein (Aenderungen am Rahmen sind danach teuer).
- Details: `Documentation/Guides/Exoskelett.md`.

## Meilensteine setzen

| Meilenstein | Bedeutung |
| --- | --- |
| Erstes Teil gedruckt und geschliffen | Skalierung und Workflow validiert |
| Helm fertig (Shell + Visor) | Schwerstes Einzelteil geschafft |
| Elektronik funktioniert auf dem Tisch | Software und Hardware OK |
| Erstes Ruestungsteil lackiert | Farbschema und Workflow bestaetigt |
| Volle Ruestung am Koerper (roh) | Passform und Befestigung validiert |
| Elektronik in Ruestung integriert | Alles zusammen funktioniert |
| Komplett-Anzug 1 Stunde getragen | Convention-Ready |

## Puffer

- Plane **20-30% Pufferzeit** fuer Nacharbeit und Anpassungen
- Fehldrucke passieren — kalkuliere 10-15% Nachdrucke ein
- Bestellungen brauchen Vorlauf (Elektronik aus China: 2-4 Wochen!)
- **Deadline:** Con-Datum minus 2 Wochen = eigene Deadline (letzte 2 Wochen nur Feinschliff)

## Minimalziel bei Zeitmangel

Falls die Zeit nicht reicht fuer alles:

1. **Helm + Visor** (das Highlight)
2. **Brustplatte** (definiert die Silhouette)
3. **Unterarme + Schienbeine** (komplettiert den Look)
4. Rest spaeter nachruesten

Damit sieht man sofort wie Master Chief aus und kann schrittweise aufruesten.
