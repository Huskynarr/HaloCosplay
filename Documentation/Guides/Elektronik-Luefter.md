# Luftfuehrung und Kuehlung in Helm und Torso

Stand: 2026-09-09. Die Komfortlueftung tauscht warme, feuchte Innenluft gegen
Aussenluft aus. Sie ist keine Klimaanlage: Lufttemperatur unter Umgebung,
beschlagfreies Visier oder eine bestimmte Tragedauer werden nicht garantiert.
LED-Kuehlkoerper, Elektronikfaecher und Nebelauslaesse bekommen getrennte Wege.

## Helm: Luft zum Visier

Arbeitsbasis sind zwei zugaengliche 40-mm-Luefter in seitlichen Kiefer-/Wangenpods.
Beide saugen frische Aussenluft durch ein geschuetztes Gitter an und schieben sie
durch kurze, breite Kanaele zur unteren Visierkante. Flache Austrittsschlitze
verteilen einen Teilstrom ueber die Visierinnenseite. Ein zweiter offener Weg
versorgt den Kopfbereich. Oben hinten treten Waerme und Feuchtigkeit aus.

Die Ansaugung liegt nicht am nebelbelasteten Ruecken und nicht direkt unter
einem LED-Kuehlkoerper. Das Mikrofon liegt ausserhalb des Luftstrahls. Polster
und Kanaele sind herausnehmbar; Haare oder Textil duerfen nicht ans Laufrad
gelangen. Die Laufradgitter bleiben auch bei abgenommenem Helm wirksam.

Enge lange Schlaeuche sind fuer kleine Axialluefter kein guenstiger Ausgangspunkt.
Ein Blower kommt erst nach Vergleich seiner Druck-/Volumenstromkennlinie infrage.
Maximalvolumenstrom und maximaler statischer Druck gelten nicht gleichzeitig.
Gitter, Filter, Biegungen und Spalte veraendern den Betriebspunkt.

## Torso: Abstandstextil und getrennte Faecher

Zwei 60-mm-Luefter sitzen versuchsweise in unteren seitlichen Einlaessen.
Abstandstextil und Luftstege halten Wege zwischen Unteranzug und Schalen frei.
Die Luft stroemt an Brust und Ruecken nach oben; Auslaesse liegen seitlich unter
den Schulterhauben. Diese muessen bei gesenkten Armen und geschlossenem Torso
frei bleiben.

Akkus, LED-Treiber und Recorder sitzen in eigenen Servicefaechern. Deren
warme Abluft wird nach aussen gefuehrt, nicht zuerst ueber den Koerper oder
ins Helmvisier. Durchgehender dicker Foam wuerde die Luftwege schliessen.
Weiche Abstandsteile duerfen nicht in Scharniere oder Schliesser geraten.

Peltiermodule sind in dieser Arbeitsbasis nicht vorgesehen: Sie verlagern
Waerme und erzeugen zusaetzliche Abwaerme auf der heissen Seite. Eine spaetere
Kuehlweste ist eine eigenstaendige Option mit neuem Masse-/Passformtest.

## Verifizierte Luefterkandidaten

| Verwendung | Kandidat | Geometrie ohne Entkoppler | Hersteller-Maximalwert | Freier Maximalvolumenstrom |
| --- | --- | --- | --- | --- |
| Helm, zweimal | Noctua NF-A4x20 **5V PWM** | 40 x 40 x 20 mm; Lochabstand 32 mm | 0,5 W / 0,1 A je Luefter | 9,4 m3/h je Luefter |
| Torso, zweimal | Noctua NF-A6x25 **5V PWM** | 60 x 60 x 25 mm; Lochabstand 50 mm | 1,3 W / 0,26 A je Luefter | 29,2 m3/h je Luefter |

[Herstellerdaten Helm-Luefter](https://www.noctua.at/en/products/nf-a4x20-5v-pwm/specifications),
[Herstellerdaten Torso-Luefter](https://www.noctua.at/en/products/nf-a6x25-5v-pwm/specifications).
Zusammen ergeben die vier Motoren nach diesen Maximalwerten 3,6 W bzw. 0,72 A
bei 5 V. Controller, Umwandlung, Einschaltverhalten und weitere Verbraucher
kommen hinzu. Die reale Kanalfoerderung wird gemessen; Hersteller-Maximalwerte
werden nicht als garantierter Helmluftwechsel addiert.

20-35 EUR je Qualitaetsluefter sind ein eigener Budgetansatz, kein abgerufenes
Angebot. Guenstigere Module sind moeglich, wenn Strom, Anlauf, Geraeusch,
Druckkennlinie und Montageabmessungen fuer die konkrete Ausfuehrung vorliegen.

## Versorgung und Drehzahl

Die 5-V-Komfortversorgung hat einen eigenen frontseitigen Schalter. Der
Effektschalter fuer RGB und Duesenluft unterbricht sie nicht. Ein Ausfall der
Komfort-Powerbank schaltet ihre Verbraucher trotzdem ab; das ist keine
redundante Versorgung. Akkus nicht parallel verdrahten.

Vierleiter-Luefter erhalten konstante geregelte 5 V am Versorgungspin und ein
separates PWM-Steuersignal. Noctua nennt 25 kHz als Ziel und 21-28 kHz als
unterstuetzten Bereich. Pegel-/Ausgangsschaltung folgen der
[Herstelleranleitung](https://www.noctua.at/en/support/faqs/microcontroller-guide-pwm-setup-and-rpm-monitoring).
Ein Zwei-Pin-Stecker fuehrt keine getrennte PWM-/Tachoschnittstelle.

Die bisherigen Arduino-Beispiele mit einfachem `analogWrite` sind nicht
automatisch fuer diese Frequenz oder Vierleiter-Luefter geeignet. Kein
Motorstrom durch einen GPIO. RPM-Signale mehrerer Luefter werden nicht
zusammengelegt. Ein Grafikrechner-Absturz darf den Komfortzweig nicht
softwareseitig ausschalten; Reset und Ausfallverhalten werden real geprueft.

## Einbauversuche

1. Luftwege im offenen Rohbau mit leichtem Prueffaehnchen sichtbar machen;
   keinen Nebler an die Atemluftfuehrung anschliessen.
2. Volumenstrom am installierten Auslass messen, Gitter und Kanaele montiert
   lassen. Geraeusch und Vibration mit/ohne Polster vergleichen.
3. Visiermuster, Brille, Atmung und Kopfbewegungen im beaufsichtigten kurzen
   Versuch pruefen. Temperatur/Feuchte innen und Umgebung dokumentieren.
4. Bei maximal geplanter Licht-/Recorderleistung pruefen, ob warme Abluft in
   einen Helmeinlass gelangt.
5. Effekt-Aus, Grafik-Neustart und Komfort-Abschaltung am Tisch pruefen.
   Beschlag, Unwohlsein oder Luftwegestoerung fuehren zum Oeffnen/Absetzen.

Der [Thermalrechner](../../Design/Thermal/README.md) berechnet die stationaere
Temperaturerhoehung durch angegebene Elektronikwaerme bei gemessenem Luftstrom.
Er modelliert weder den menschlichen Waermehaushalt noch Verdunstung oder eine
medizinisch sichere Tragedauer. Gesamtplatzierung:
[Einbauplan](Mjolnir-Einbauplan.md); Helm:
[Optik, Kamera und Audio](Mjolnir-Helmintegration.md).
