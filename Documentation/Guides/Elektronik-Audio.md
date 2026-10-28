# Elektronik: Sprache, Soundeffekte und Umgebungshoeren

Die Grundloesung besteht aus einem Mundmikrofon im Helm und einem nach vorne
abstrahlenden Lautsprecher hinter einem Brust- oder Kragengitter. Das schafft
Abstand zwischen Mikrofon und Lautsprecher. Ein grosser Sprachlautsprecher
unmittelbar am Ohr oder im Kinnraum ist nicht vorgesehen. Einbaupositionen und
Kabelwege stehen in [Helmintegration](Mjolnir-Helmintegration.md).

## 1. Mikrofonposition und Akustik

Ein kleines Buegelmikrofon sitzt seitlich am Mund, als erster einstellbarer
Versuchsbereich etwa 20-40 mm vom Mundwinkel entfernt. Der Wert ist eine
Positionierhilfe und wird mit dem konkreten Mikrofon ausprobiert. Eine
weiche, loesbare Aufnahme und ein geeigneter Schaumstoff-Windschutz vermindern
Koerperschall und Atemstoesse. Das Mikrofon wird weder luftdicht eingepackt noch
in den direkten Luefterstrom gesetzt.

Der Halter ist vom Lueftertraeger getrennt. Der Mikrofon-Kabelweg fuehrt an der
Wange zum seitlichen Helmstecker, mit eigener Zugentlastung. Die Kapsel sitzt
nicht an einer starren Schale, die bei jedem Schritt knarzt. Ein kurzer,
vorne erreichbarer Stummschalter oder Push-to-talk ist Teil der Bedienprobe.
Ein versehentliches Aktivieren darf keine volle Verstaerkung ausloesen.

## 2. Drei unabhaengige Ausbaustufen

| Stufe | Signalweg | Ergebnis |
| --- | --- | --- |
| Sprache | Passendes Headsetmikrofon und fertiger Sprachverstaerker | Verstaendliche direkte Stimme |
| Soundeffekte | Taster und Audiodatei-Player mit eigenem Verstaerker oder geeignetem Mischereingang | Boot-, Schild- oder Duesenklang als Datei |
| Stimmeffekt | Mikrofon, passender Audioeingang/ADC, Echtzeitverarbeitung und Audioausgang | Optionaler Funk-/Helmklang; neue Software- und Latenzpruefung |

Zwei Verstaerkerausgaenge werden nicht zusammengeschaltet. Sprache und
Soundeffekte werden entweder vor der Endstufe in einem geeigneten Mixer
kombiniert oder ueber getrennte Lautsprecher ausgegeben. Ein fertiger
Verstaerker mit dokumentiertem Mikrofon- und Line-Eingang kann den Aufbau
vereinfachen; die gleichzeitige Nutzung bleibt modellspezifisch.

### Preiswerter Einstieg

Ein komplettes Set aus kabelgebundenem Mikrofon und Sprachverstaerker minimiert
Schnittstellenprobleme. Ein konkreter Vergleichskandidat ist **SHIDU S617**:
Der Hersteller nennt 102.6 x 88 x 42.3 mm, 190 g, einen internen
3.7-V-/1800-mAh-Akku und 5-V-Ladung. Die Masse dienen zur ersten
Platzhalter-Kassette, nicht als Nachweis der Einbausituation. Herstellerangaben
zur Laufzeit gelten nicht automatisch im Helmversuch. Ein aktueller deutscher
Endpreis wurde nicht verifiziert.
[SHIDU-Produktdaten](https://en.10shidu.com/content/548.html)

Das komplette Gehaeuse bleibt erhalten, seine Bedienung erreichbar und der
Lautsprecher vor einem offenen Schallweg. Der integrierte Akku gehoert als
eigene Energiequelle in die Abschalt- und Ladeliste. Eine fest zugeklebte
Montage in Schaumstoff waere ungeeignet.

Als Entwicklungsreserve sind **40-80 EUR fuer ein vollstaendiges Sprachset**
sowie **10-25 EUR fuer Halter, Windschutz und Kabel** eine eigene
Planungsannahme, kein verifiziertes Produktangebot. Die tatsaechliche Position
wird erst mit ausgewaehltem Lieferumfang in die Projekt-BOM uebernommen.

### Eigener kompakter Lautsprecherausgang

Der **Adafruit MAX98357A** ist ein moeglicher digitaler Mono-Ausgang: I2S,
5-V-Betrieb im vorgesehenen Aufbau, Lautsprecher mit mindestens 4 Ohm.
Der Hersteller nennt 3.2 W an 4 Ohm bei 5 V und bereits 10 Prozent THD;
das ist kein sinnvoller sauberer Dauerpegel fuer Sprache. Die Produktseite
nennt 5.95 USD fuer das Board, ohne Lautsprecher, Eingang und Rechner.
[Adafruit-Produktdaten](https://www.adafruit.com/product/3006)

Die Endstufe bekommt **digitale Audiodaten**, kein analoges Mikrofon direkt an
DIN. Ausgang plus und minus fuehren ausschliesslich zum passenden
Lautsprecher; keiner davon ist Masse oder ein Line-Ausgang. Versorgung,
Stummschaltung und die passende Treiberkonfiguration werden nach dem
[Hersteller-Pinout](https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/pinouts)
ausgelegt. Der bisherige pauschale Stromwert von 0.05-0.15 A fuer einen
mehrwattigen Verstaerker ist kein belastbares Spitzenstrombudget.

## 3. Stimmeffekte ohne falsche Funktionszusage

Ein MAX4466 verstaerkt ein Mikrofonsignal, ein PAM8403 oder MAX98357A treibt
einen Lautsprecher. Diese Bauteile alleine veraendern keine Tonhoehe. Ein
Adafruit Audio FX Sound Board spielt gespeicherte WAV-/OGG-Dateien ab; es ist
kein direkter Ersatz fuer eine Echtzeit-Sprachverarbeitung.
[Audio-FX-Dokumentation](https://learn.adafruit.com/adafruit-audio-fx-sound-board/overview)

Der historische [Adafruit Wave Shield Voice Changer](https://learn.adafruit.com/wave-shield-voice-changer/overview)
verwendet dagegen einen bestimmten Aufbau und passende Software. Die Anleitung
schliesst Arduino Mega und Leonardo fuer diesen Aufbau aus. Die fruehere
unspezifische Einkaufskombination aus Uno oder Leonardo und beliebigem
Soundboard entfaellt deshalb.

Bei einem analogen Mikrofonverstaerker muessen Offset, Eingangspegel und
Koppelkondensator zur naechsten Stufe passen. Beispielsweise besitzt der
[MAX4466-Ausgang](https://www.adafruit.com/product/1063) einen Offset von VCC/2;
ob und wie AC-Kopplung erforderlich ist, entscheidet die folgende
Eingangsschaltung. Eine pauschale Kondensatorgroesse samt universellem
Schaltplan ist hier nicht festgelegt.

Ein Software-Stimmeffekt auf einem Rechner ist moeglich, aber kein hier fertig
implementierter Bestandteil. Vor Kauf sind der passende Mikrofoneingang,
Aufnahme und Ausgabe gleichzeitig, Kanalbelegung und Treiber zu pruefen. Der
Effekt muss mit laufenden Lueftern, Kamera und HUD stabil und verstaendlich
bleiben. Fuer authentischen Funkklang ist ein geringer Effektanteil sinnvoller
als eine stark verlangsamte, unverstaendliche Stimme.

## 4. Optionales Umgebungshoeren

Zunaechst werden die passiven Hoerwege des Helms erhalten und die Luefter
akustisch optimiert. Erst bei Bedarf kommen getrennte Aussenmikrofone links
und rechts und leise, offen montierte Ohrlautsprecher hinzu. Diese Funktion
bekommt einen eigenen begrenzten Pegel, eine Stummschaltung und einen Test mit
Impulsgeraeuschen. Sie bleibt ein Komfortmodul; Richtungshoeren und
Warnsignalerkennung sind durch einen Eigenbau nicht automatisch erhalten.

Der Aussenlautsprecher wird nicht auf diese Ohrlautsprecher zurueckgefuehrt.
Eine ungetestete Rueckkopplungsunterdrueckung oder automatische Verstaerkung
ersetzt weder Abstand noch vernuenftige Pegel. Bei abgeschalteter Elektronik
muss die Kommunikationsmoeglichkeit durch Oeffnen oder Abnehmen des Helms
weiter bestehen.

## 5. Konkrete Abnahmefolge

1. Sprache auf der Werkbank aufnehmen, Eingangspegel auf Uebersteuerung pruefen.
2. Geschlossener Helm ohne Soundeffekte: Gegenueber bewertet Verstaendlichkeit
   bei ruhiger Umgebung und bei reproduzierbarem Hintergrundgeraeusch.
3. Alle Luefterstufen und RGB-Modi einzeln zuschalten; Stoergeraeusche und
   Brummen aufnehmen. Keine pauschale Noise-Cancelling-Zusage.
4. Kopf drehen, Brust oeffnen und Mikrofon stummschalten; Rueckkopplung,
   Kabelzug und erreichbare Bedienung pruefen.
5. Soundeffekte waehrend eines Satzes starten; Verstaendlichkeit und
   Priorisierung der Sprache pruefen.
6. Ergebnis, Pegelstellungen, reale Stromaufnahme und Montagefotos pro
   Hardware-Revision protokollieren.
