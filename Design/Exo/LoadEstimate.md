# X01: Lastabschaetzung der Konzeptgeometrie

**Erzeugt von `tools/suit_loads.py`; nicht von Hand aendern.** Eingaben:
[Parameters.scad](Parameters.scad) und [LoadCase.json](LoadCase.json).

Status: `ROUGH_ESTIMATE_NOT_A_STRENGTH_APPROVAL`. Balken- und Schraubenformeln am
Nennquerschnitt mit angenommenen Werkstoffwerten. Nicht enthalten: Ermuedung,
Kerbwirkung, Schweiss- und Klebestellen, Knicken und Beulen, Lasten quer zur
Bewegungsebene, Sturz, Fertigungsfehler und jede Messung. Eine Auslastung unter 1
heisst nur, dass diese eine Rechnung den Querschnitt nicht ausschliesst.

Lastfall: 22 Nm Spitzenmoment an einem Hueftantrieb, Sicherheitsfaktor 3 gegen
die Streckgrenze, Stossfaktor 2 am Anschlag. Auslastung = Spannung mal
Sicherheitsfaktor durch Streckgrenze (bei Scherung 0,58 davon).

## Querschnitte

| ID | Teil | Nachweis | Spannung MPa | EN AW-6061-T6 | S235 | PETG gedruckt (Annahme, quer zur Schicht) |
| --- | --- | --- | --- | --- | --- | --- |
| E01 | Abtriebsarm | Biegung am Nabenrand | 24.4 | 0.3 | 0.31 | **3.66** |
| E02 | Abtriebsarm | Biegung im Lochquerschnitt | 24.7 | 0.31 | 0.32 | **3.7** |
| E03 | Strebe | Biegung im Lochquerschnitt | 29.6 | 0.37 | 0.38 | **4.44** |
| E04 | Anschlagblock | Scherung am Fuss, mit Stossfaktor | 20.7 | 0.45 | 0.46 | **5.35** |
| E08 | Strebe | Lochleibung an den Strebenschrauben | 27.5 | 0.34 | 0.35 | **4.12** |
| E09 | Motorplatte | Biegung im Hals unter dem Gelenkblock | 29.3 | 0.37 | 0.37 | **4.4** |
| E10 | Gabel am Seitenarm | Lochleibung am Gelenkbolzen | 9.0 | 0.11 | 0.11 | **1.35** |
| E12 | Seitenarm | Biegung hochkant | 7.3 | 0.09 | 0.09 | **1.09** |
| E13 | Rueckenrohr | Torsion, duennwandig | 7.0 | 0.15 | 0.15 | **1.81** |

## Schrauben (Festigkeitsklasse 8.8)

| ID | Schraube | Nachweis | Spannung MPa | Auslastung |
| --- | --- | --- | --- | --- |
| E05 | Flanschschrauben M4 | Scherung je Schraube | 29.8 | 0.24 |
| E06 | Gehaeuseschrauben M3 | Scherung je Schraube | 12.9 | 0.1 |
| E07 | Strebenschrauben M6 | Scherung je Schraube, Kraeftepaar im Lochraster | 43.8 | 0.35 |
| E11 | Gelenkbolzen M8 | Scherung je Gabelohr | 15.8 | 0.13 |
| E14 | Schrauben Rohreinsatz M6 | Scherung je Schraube | 60.5 | 0.49 |

Fett: Auslastung ueber 1, der Querschnitt reicht in dieser Rechnung nicht.

## Verformung und Kraefte

| ID | Groesse | Werkstoff | Wert |
| --- | --- | --- | --- |
| I01 | Verdrehung des Rueckenrohrs bei Spitzenmoment, Grad | EN AW-6061-T6 | 0.42 |
| I02 | Zum Vergleich: Flachstab gleicher Hoehe statt Rohr, Grad | EN AW-6061-T6 | 7.37 |
| I03 | Durchbiegung der Strebe an der Manschette in Bewegungsrichtung, mm | EN AW-6061-T6 | 1.03 |
| I04 | Seitliche Auslenkung der Strebe an der Manschette je 10 N Querkraft, mm | EN AW-6061-T6 | 5.6 |
| I01 | Verdrehung des Rueckenrohrs bei Spitzenmoment, Grad | S235 | 0.13 |
| I02 | Zum Vergleich: Flachstab gleicher Hoehe statt Rohr, Grad | S235 | 2.37 |
| I03 | Durchbiegung der Strebe an der Manschette in Bewegungsrichtung, mm | S235 | 0.34 |
| I04 | Seitliche Auslenkung der Strebe an der Manschette je 10 N Querkraft, mm | S235 | 1.8 |
| I01 | Verdrehung des Rueckenrohrs bei Spitzenmoment, Grad | PETG gedruckt (Annahme, quer zur Schicht) | 14.55 |
| I02 | Zum Vergleich: Flachstab gleicher Hoehe statt Rohr, Grad | PETG gedruckt (Annahme, quer zur Schicht) | 255.46 |
| I03 | Durchbiegung der Strebe an der Manschette in Bewegungsrichtung, mm | PETG gedruckt (Annahme, quer zur Schicht) | 35.49 |
| I04 | Seitliche Auslenkung der Strebe an der Manschette je 10 N Querkraft, mm | PETG gedruckt (Annahme, quer zur Schicht) | 191.7 |
| I05 | Kraft der Manschette am Oberschenkel bei Spitzenmoment, N | - | 66.7 |
| I06 | Mittlerer Druck unter der Manschette bei Spitzenmoment, kPa | - | 7.4 |
| I07 | Kraft am Anschlag ohne Stossfaktor, N | - | 786 |

## Einhaengelaschen der Ruestungsmodule

Zug im Restquerschnitt neben dem Gurtschlitz (2 x 6 mm breit, 6 mm dick) mit
angenommener Modulmasse, dynamischem Faktor und angenommener Festigkeit des
Drucks quer zur Schicht. Kriechen, Schlag und Schichtlage sind nicht erfasst.

| Modul | Masse kg | Spannung MPa | Auslastung |
| --- | --- | --- | --- |
| Beinmodul | 3.0 | 1.23 | 0.25 |
| Armmodul | 1.1 | 0.45 | 0.09 |
