# Armor Step 1: Planung, Skalierung, Unteranzug

## Ziele

- Richtige Passform und Bewegungsfreiheit sichern
- Ruestung auf den eigenen Koerper skalieren
- Tragesystem planen

## 1. Koerpermessungen nehmen

Miss folgende Masse und notiere sie (alle in cm):

| Messung | Wert | Hinweis |
| --- | --- | --- |
| Brustumfang | ___ | Massband um breiteste Stelle |
| Taillenumfang | ___ | Natuerliche Taille |
| Hueftumfang | ___ | Breiteste Stelle |
| Schulterbreite | ___ | Knochen zu Knochen |
| Armlaenge | ___ | Schulter bis Handgelenk |
| Oberarmumfang | ___ | Bizeps, angespannt |
| Unterarmumfang | ___ | Breiteste Stelle |
| Oberschenkelumfang | ___ | Breiteste Stelle |
| Wadenumfang | ___ | Breiteste Stelle |
| Bein-Innenlaenge | ___ | Schritt bis Boden |
| Koerpergroesse | ___ | Gesamt |
| Kopfumfang | ___ | Ueber Stirn und Hinterkopf |

**Tipp:** Lass jemanden helfen, allein messen ist ungenau. Trage dabei das, was du unter der Ruestung tragen wirst (Morphsuit + Klettergurt).

## 2. STLs skalieren

### Methode A: Prozentuale Skalierung

Die meisten STL-Sets sind fuer eine Standard-Koerpergroesse erstellt:
- Galactic Armory: 183 cm, 91 kg
- MoeSizzlac: 178 cm, 84 kg

**Skalierungsformel (grob):**
```
Skalierung = Eigene Koerpergroesse / Standard-Koerpergroesse
Beispiel: 175 cm / 183 cm = 0.956 = 95.6%
```

**ACHTUNG:** Nur Groesse reicht nicht! Schulterbreite, Brustumfang und Hueftumfang sind genauso wichtig. Immer Testdruck machen.

### Methode B: Armorsmith (Software)

- Armorsmith Designer (Windows, ca. $25) — speziell fuer Ruestungsskalierung
- Eigene Masse eingeben, 3D-Modell des Koerpers wird erstellt
- STLs importieren und am virtuellen Koerper positionieren
- Zeigt sofort wo Teile zu gross/klein sind
- Exportiert skalierte STLs pro Koerperregion

### Methode C: Testdruck und Anpassen

1. Ein Teil drucken (z.B. Unterarm — schnell, sichtbares Ergebnis)
2. Anhalten, Passform pruefen
3. Skalierung anpassen (meist 2-5% Schritte)
4. Wiederholen bis es sitzt
5. Skalierungsfaktor auf alle Teile der gleichen Region anwenden

**Wichtig:** Verschiedene Koerperregionen koennen unterschiedliche Skalierungen brauchen! Arme passen vielleicht bei 96%, aber die Brust braucht 100%.

## 3. Unteranzug auswaehlen

Der Unteranzug ist die Basis fuer alles. Siehe `Documentation/Guides/Unteranzug-Befestigung.md` fuer Details.

**Kurzversion:**
- Schwarzer Morphsuit oder Kompressions-Suit (feuchtigkeitsableitend!)
- Unter dem Morphsuit: Klettergurt oder MOLLE-Guertel fuer Lastverteilung
- Klett-Punkte und Magnet-Positionen auf dem Morphsuit markieren

## 4. Tragesystem planen

### Gewichtsverteilung

- **Huefte traegt die Last** — Klettergurt oder gepolsterter MOLLE-Guertel
- Schultergurte nur zur Stabilisierung, nicht als Hauptlast
- Brustplatte und Rueckenpanzer haengen am Guertel-System, nicht an den Schultern

### Befestigungspunkte planen

Bevor du druckst, plane wo jedes Teil befestigt wird:

| Teil | Befestigung | An was? |
| --- | --- | --- |
| Brustplatte | Gurte + Schnallen | Klettergurt/Harness |
| Rueckenpanzer | Gurte + Schnallen | Klettergurt/Harness |
| Schultern | Klett + Magnete | Schulterriemen |
| Oberarme | Klett + Magnete | Morphsuit |
| Unterarme | Klett + Gummiband | Morphsuit |
| Oberschenkel | Gurte + Schnallen | Guertel + Beinschlaufen |
| Schienbeine | Klett + Gummiband | Morphsuit |
| Handplatten | Magnete | Handschuhe |
| Hueft-/Codpiece | Schnalle | Guertel |

## 5. Reihenfolge der Teile festlegen

Nicht alles auf einmal drucken! Reihenfolge nach Prioritaet:

1. **Helm** — laengste Nachbearbeitung, bestes Lern-Stueck
2. **Unterarme (L+R)** — klein, schnell gedruckt, gut zum Testen der Skalierung
3. **Schienbeine (L+R)** — einfache Form, fruehe Passformtests
4. **Brustplatte** — grosses Stueck, definiert den Look
5. **Rueckenpanzer** — passt zur Brustplatte
6. **Schultern** — nach Brust, fuer korrekte Ausrichtung
7. **Oberschenkel** — nach Brust/Guertel, fuer Befestigungstest
8. **Hueft-/Codpiece** — nach Guertel-System
9. **Handplatten, Stiefelcover** — zuletzt, kleine Details

## 6. Erster Passform-Test (Karton/Rohteile)

Bevor du in teurem Filament druckst:

1. **Papier-/Karton-Mockups** der groessten Teile (Brust, Oberschenkel) ausschneiden
2. Am Koerper halten — stimmen die Proportionen?
3. Kann man sich bewegen? Sitzen? Arme heben?
4. **Armloecke testen:** Koennen die Arme durch die Schulter-/Brustplatte hindurch?
5. Erst wenn Karton-Mockups passen: echte Drucke starten

## Checkliste Phase 1

- [ ] Alle Koerpermasse genommen und notiert
- [ ] STL-Set heruntergeladen
- [ ] Skalierung berechnet/getestet
- [ ] Unteranzug bestellt/vorhanden
- [ ] Klettergurt/Guertel beschafft
- [ ] Befestigungspunkte geplant
- [ ] Testdruck gemacht (Unterarm passt)
- [ ] Karton-Mockup fuer Brustplatte passt
- [ ] Druck-Reihenfolge festgelegt
