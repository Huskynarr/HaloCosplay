# Beleuchtete Schubduesen & Nebel-Effekte (Jetpack)

> **Level:** [F] Fortgeschritten | [P] Profi  |  **Varianten:** V2/V3 (Jetpack/Backpack)
> **Voraussetzungen:** Arduino IDE eingerichtet, Grundlagen Elektronik-Verdrahtung (`Documentation/Guides/Elektronik-Verdrahtung.md`), Grundlagen LED-Effekte (`Documentation/Guides/LED-Effekte.md`).

Dieses Modul beschreibt den Bau, die Verkabelung und die Programmierung von beleuchteten Schubduesen (Thrusters) am Rueckenmodul (Jetpack) des MJOLNIR-Suits, inklusive eines aktiven Nebelausstosses fuer den ultimativen Show-Effekt.

---

## 1. Funktionsprinzip & Uebersicht

Der Effekt besteht aus drei Saeulen:
1. **Lichtquelle:** Ein programmierbarer RGB-LED-Ring (WS2812B NeoPixel) am Fuss der Duese erzeugt dynamische Flammeneffekte (Flackern, Nachbrenner-Blau, Zuendungs-Orange).
2. **Diffusion:** Die Duese selbst wird aus transparentem/transluzentem Kunststoff gefertigt und angeraut. Dies streut das Licht perfekt und laesst die Duese wie eine gluehende Plasma-Kammer wirken.
3. **Nebel-Effekt:** Ein kompakter 5V-Ultraschall-Vernebler verdampft Wasser im Inneren des Rucksacks. Ein kleiner Radialluefter (Blower) drueckt den kalten Dampf durch Schlaeuche direkt in die Schubduesen, wo er von den LEDs beleuchtet wird.

```
+-------------------------------------------------------------+
| Rucksack / Jetpack-Gehaeuse                                  |
|                                                             |
|   [Wassertank] ---> (Docht) ---> [Ultraschall-Vernebler]    |
|        ^                                 |                  |
|    [Radialluefter 5V] (Luftstrom)         v                  |
|                                    [Nebelschlauch]          |
|                                          |                  |
+------------------------------------------|------------------+
                                           v
                             +---------------------------+
                             | Schubduese (Transluzent)   |
                             |                           |
                             |   *(LED-Ring)*            |
                             |   ============            |
                             |   [Dampfaustritt] ==> ~~~ |
                             +---------------------------+
```

---

## 2. Benoetigte Materialien

### Mechanik & Gehaeuse
* **Transluzenter Kunststoff:**
  * **Fuer 3D-Druck:** Transparentes PETG-Filament (z. B. "PETG Clear" oder "Translucent Orange/Blue")
  * **Alternativ (analog):** Acrylglas-Rohre (Plexiglas) mit passendem Durchmesser.
* **Diffusion:** Schleifpapier (Koernung 320, 400 und 800), evtl. Diffusionsfolie oder duenner Verpackungsschaum.
* **Nebelschlauch:** Silikonschlauch (8-10 mm Innendurchmesser).
* **Wassertank:** Kleine, flache und auslaufsichere Plastikflasche (ca. 150-250 ml) mit Schraubverschluss.

### Elektronik & Nebler-Hardware
* **LED-Ringe:** 2x WS2812B RGB LED-Ringe (z. B. mit 12 oder 16 LEDs, Aussendurchmesser passend zum Dueseneingang).
* **Vernebler-Modul:** 5V USB Ultraschall-Vernebler-Platine (Mist Maker), wie sie in Mini-Luftbefeuchtern verbaut sind (inkl. Piezo-Keramikscheibe und Baumwoll-Docht).
* **Luefter fuer Nebeltransport:** 5V DC Radialluefter (Blower Fan, z. B. 4010 oder 5015). Wichtig: Radialluefter bauen Druck auf, Axialluefter (normale PC-Luefter) sind ungeeignet!
* **Leistungstreiber (MOSFET):** IRLZ44N N-Kanal MOSFET (zum Ein-/Ausschalten des Neblers und des Luefters ueber den Arduino).
* **Widerstaende:** 1x 10k Ohm (Pull-Down-Widerstand fuer das MOSFET-Gate), 1x 220 Ohm (Gate-Widerstand), 1x 330 Ohm (LED-Datenleitung).
* **Diode:** 1x 1N4007 (Freilaufdiode fuer den Lueftermotor).
* **Kondensator:** 1x 1000 uF Elektrolytkondensator (Gleichrichter/Glaettung).

---

## 3. Mechanischer Bau

### A. Die Schubduesen (Diffusion)
1. **Drucken (PETG):** Drucke die Duesen-Inserts aus transparentem PETG.
   * *Tipp:* Nutze den **Vase Mode** (Spiral-Druck) fuer eine einzelne, durchgehende Aussenwand ohne Naehte, oder drucke mit nur **1 Aussenwand** und **0% Infill**. Das spart Gewicht und leitet das Licht optimal.
2. **Mattieren:** Schleife die gedruckten oder aus Acrylrohr geschnittenen Duesen von **innen und aussen** gruendlich mit 400er, dann mit 800er Schleifpapier nass ab. Die Oberflaeche muss milchig-trueb (satiniert) werden.
3. **Alternative Diffusion:** Falls das Licht der einzelnen LEDs immer noch als "Punkte" sichtbar ist (Hotspots), klebe eine Lage Backpapier oder duenne Verpackungsfolie (Schaumfolie) in die Duese.

### B. Das Nebel-System (Tank & Luefter)
1. **Tank vorbereiten:** Bohre zwei Loecher in den Deckel der Plastikflasche:
   * **Loch 1 (Lufteinlass):** Klebe hier den Luftauslass des 5V-Radialluefters ein (z. B. mit Heisskleber/Epoxidharz).
   * **Loch 2 (Nebelauslass):** Klebe den Silikonschlauch ein. Er muss knapp unter dem Deckel enden und fuehrt spaeter zu den Duesen (Y-Verteiler nutzen fuer zwei Duesen).
2. **Piezo-Element montieren:** Die Ultraschall-Scheibe wird per Halterung so knapp ueber dem Wassertank platziert, dass der Baumwoll-Docht permanent im Wasser haengt und das Wasser per Kapillareffekt an die Unterseite der Metallscheibe saugt.
   * > [!CAUTION]
   * > Die Rueckseite des Piezo-Elements (mit den Kabeln) und die Steuerplatine duerfen **niemals nass werden**! Dichte alle elektrischen Anschluesse mit Epoxidharz oder Silikon ab.
3. **Schlauchfuehrung:** Verlege die Silikonschlaeuche mit Gefaelle zurueck zum Tank, damit kondensiertes Wasser zurueckfliessen kann und den Schlauch nicht verstopft.

---

## 4. Verdrahtung & Schaltplan

Das Nebel-Modul benoetigt deutlich mehr Strom als die Steuersignale des Arduino liefern koennen. Wir steuern den Vernebler und den Luefter daher ueber einen **IRLZ44N MOSFET** an.

```
                              Powerbank +5V (GND-gemeinsam!)
                                   |
                                   +---------------------+---------------+
                                   |                     |               |
                                [Nebler +]            [Luefter +]      [LED VCC]
                                   |                     |               |
                                   |                  [Diode] (Kathode)  |
                                   |                     |               |
                                [Nebler -]            [Luefter -]         |
                                   |                     |               |
                                   +----------+----------+               |
                                              |                          |
                                        (Drain Pin 2)                    |
                                              |                          |
   Arduino Pin 9 ---[220R]---+-----------(Gate Pin 1)                    |
                             |                |                          |
                          [10k Ohm]     (Source Pin 3)                   |
                             |                |                          |
   Arduino GND --------------+----------------+--------------------------+
                                              |
   Arduino Pin 5 ---[330R]--------------------+-----------------------> LED DATA IN
```

* **10k Ohm Widerstand (Pull-Down):** Zieht das Gate des MOSFETs auf GND, wenn der Arduino bootet, damit der Nebler nicht unkontrolliert startet.
* **1N4007 Diode (Freilaufdiode):** Schuetzt den MOSFET vor Spannungsspitzen des Radialluefters (induktive Last) beim Ausschalten. Die markierte Seite (Kathode/Ring) kommt an +5V, die andere an den Luefter-Minuspol.
* **1000 uF Kondensator:** Parallel zu +5V und GND nahe am LED-Ring platzieren, um Spannungseinbrueche durch den Anlaufstrom des Luefters zu puffern.

---

## 5. Software (Arduino Code)

Dieser Sketch steuert das Verhalten: Im Normalzustand (Idle) flackern die Duesen leicht blaeulich-orange (Plasma-Bereitschaft). Wird ein Taster gedrueckt (oder ein Signal vom I2C-Bus empfangen), zuendet der Nachbrenner: Die LEDs wechseln auf helles Orange/Gelb/Weiss-Flackern und der Nebel wird aktiviert.

Der Code spricht **beide Nebel-Stufen** an: `MIST_PIN` schaltet den Ultraschall-Vernebler + Radialluefter (Stufe 1), `FOGGER_PIN` triggert einen beheizten Micro-Fogger (Stufe 2, siehe Abschnitt 7). Du verkabelst nur den Pin der Stufe, die du nutzt - der jeweils andere bleibt einfach frei. Ueber `FOGGER_MOMENTARY` waehlst du, ob der Fogger per Dauerpegel (USB-C-Trigger) oder per kurzem Impuls (Optokoppler ueber die Fernbedienung) angesteuert wird.

```cpp
#include <Adafruit_NeoPixel.h>

#define LED_PIN       5    // Datenleitung LED-Ringe
#define NUM_LEDS     24    // Gesamtzahl der LEDs (z.B. 2x 12 Ringe in Reihe)
#define TRIGGER_PIN   2    // Taster fuer Boost-Modus (Gegen GND geschaltet)
#define MIST_PIN      9    // MOSFET-Gate: Ultraschall-Vernebler + Luefter (Stufe 1)
#define FOGGER_PIN    8    // Trigger fuer beheizten Micro-Fogger (Stufe 2)

// Trigger-Art des Foggers (siehe Abschnitt 7):
//   false = Pegel/Hold: Pin bleibt HIGH waehrend des Boosts
//           (z.B. USB-C-Trigger oder Relais auf eine Trigger-Leitung)
//   true  = Momentan: kurzer Impuls zum Starten UND Stoppen
//           (z.B. Optokoppler ueber die Tasten-Pads der Fernbedienung)
#define FOGGER_MOMENTARY false
#define FOGGER_PULSE_MS  120   // Impulslaenge bei FOGGER_MOMENTARY

#define BRIGHTNESS_IDLE 80  // Moderate Helligkeit fuer Idle
#define BRIGHTNESS_BOOST 255 // Volle Leistung beim Zuenden

Adafruit_NeoPixel strip(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);

bool isBoosting = false;
unsigned long boostStartTime = 0;
const unsigned long BOOST_DURATION = 5000; // Boost laeuft 5 Sekunden

// Beheizten Fogger triggern (Stufe 2). on=true startet, on=false stoppt.
void setFogger(bool on) {
  if (FOGGER_MOMENTARY) {
    // kurzer "Tastendruck" - sowohl zum Starten als auch zum Stoppen (Toggle)
    digitalWrite(FOGGER_PIN, HIGH);
    delay(FOGGER_PULSE_MS);
    digitalWrite(FOGGER_PIN, LOW);
  } else {
    digitalWrite(FOGGER_PIN, on ? HIGH : LOW); // Pegel halten
  }
}

void setup() {
  pinMode(TRIGGER_PIN, INPUT_PULLUP);
  pinMode(MIST_PIN, OUTPUT);
  pinMode(FOGGER_PIN, OUTPUT);
  digitalWrite(MIST_PIN, LOW);   // Vernebler aus
  digitalWrite(FOGGER_PIN, LOW); // Fogger-Trigger inaktiv

  strip.begin();
  strip.setBrightness(BRIGHTNESS_IDLE);
  strip.show();
}

void loop() {
  // Taster abfragen (LOW-aktiv)
  if (digitalRead(TRIGGER_PIN) == LOW && !isBoosting) {
    isBoosting = true;
    boostStartTime = millis();
    digitalWrite(MIST_PIN, HIGH); // Stufe 1: Vernebler + Luefter an
    setFogger(true);              // Stufe 2: beheizten Fogger zuenden
    strip.setBrightness(BRIGHTNESS_BOOST);
  }

  // Boost-Zeit abgelaufen?
  if (isBoosting && (millis() - boostStartTime > BOOST_DURATION)) {
    isBoosting = false;
    digitalWrite(MIST_PIN, LOW); // Stufe 1 aus
    setFogger(false);            // Stufe 2 aus
    strip.setBrightness(BRIGHTNESS_IDLE);
  }

  // Effekte rendern
  if (isBoosting) {
    renderBoostEffect();
  } else {
    renderIdleEffect();
  }
  
  strip.show();
  delay(20); // ca. 50 FPS
}

// Subtiler Plasma-Idle Effekt (pulsierendes Blau mit leichtem orange-rotem Kern)
void renderIdleEffect() {
  float pulse = (sin(millis() / 800.0) + 1.0) * 0.5; // 0.0 bis 1.0
  uint8_t baseBlue = 100 + (pulse * 80);
  uint8_t baseGreen = 20 + (pulse * 30);

  for (int i = 0; i < NUM_LEDS; i++) {
    // Jede dritte LED flackert leicht orange
    if (i % 3 == 0) {
      uint8_t flicker = random(30, 80);
      strip.setPixelColor(i, flicker, flicker / 3, 0); // Warmes Orange
    } else {
      strip.setPixelColor(i, 0, baseGreen, baseBlue); // Kuehles Sci-Fi-Blau
    }
  }
}

// Aggressiver Nachbrenner/Feuer-Effekt (Gelb-Orange-Weisses Flackern)
void renderBoostEffect() {
  for (int i = 0; i < NUM_LEDS; i++) {
    uint8_t r = random(200, 255);
    uint8_t g = random(80, 160);
    uint8_t b = random(0, 40);
    
    // Sehr selten ein weisser Blitz fuer Plasma-Eruptionen
    if (random(0, 100) > 95) {
      r = 255; g = 255; b = 255;
    }
    
    strip.setPixelColor(i, r, g, b);
  }
}
```

---

## 6. Praxis-Tipps & Convention-Sicherheit

* **Destilliertes Wasser nutzen:** Verwende im Wassertank ausschliesslich destilliertes Wasser. Normales Leitungswasser hinterlaesst beim Verdunsten haessliche Kalkflecken auf der mattierten Ruestung und setzt die feinen Poren der Piezo-Scheibe extrem schnell zu.
* **Dichtigkeit & Transport:** Leere den Wassertank vor jedem Transport und drehe den Deckel fest zu. Baue am besten ein kleines Ventil oder einen Absperrhahn in den Schlauch ein, falls der Rucksack hingelegt wird.
* **Convention-Regeln beachten:** Kalter Wasserdampf (Ultraschall) ist auf 99 % der Conventions erlaubt, da er keine Hitze erzeugt und rueckstandsfrei verfliegt. Verwende **keine** Nebelmaschinen mit Fluiden (Glycerin/Glykol) im Con-Alltag - diese erzeugen Hitze, riechen, verkleben die Duesen und loesen Feuermelder aus. Fuer Photoshoots/Outdoor gibt es trotzdem einen dichteren Effekt - siehe Abschnitt 7.
* **Batterielaufzeit:** Die Ultraschall-Platine zieht ca. 300-400 mA, der Radialluefter ca. 150 mA. Zusammen mit den LEDs erhoeht das den Stromverbrauch um ca. 0.6 A im Boost-Modus. Kalkuliere dies in deinem Strombudget ein (`Documentation/Guides/Elektronik-Strombudget.md`).
* **Wasserstand-Sensor:** Wenn du den Nebler trocken laufen laesst, verbrennt der Baumwoll-Docht. Nutze entweder einen durchsichtigen Sichtschlitz im Rucksack oder rueste einen einfachen digitalen Wasserstandssensor (Liquid Level Sensor) am Wassertank nach, der den MOSFET deaktiviert, wenn das Wasser leer ist.

---

## 7. Alternative: Beheizter Micro-Fogger (dichter Rauch, nur kontrolliert)

Der Ultraschall-Kaltnebel aus Abschnitt 1-6 ist con-tauglich, aber duenn und
"wabernd". Wer fuer **Photoshoots, Outdoor oder Buehne** dichten, dramatischen
Rauch will (wie ein echter Triebwerksausstoss), nutzt einen **beheizten
Glycerin-Fogger**. Genau das sind die kompakten Foto-Geraete:

| Geraet | Typ | Laufzeit (Dauerbetrieb) | Hinweis |
| --- | --- | --- | --- |
| Vosentech MicroFogger 5 Pro | **zum Einbauen** | ca. 30 min (mittel) | Fernsteuerung 30 m, wechselbarer Akku - **die Maker-Wahl** |
| PMI Smoke Ninja / Pro | Handgeraet | ~15 min (Pro: kurze Stoesse) | sehr effizientes "Clean Fog"-Fluid, aber versiegelt |
| Ulanzi FM01 Filmog Ace | Handgeraet | ~15-20 min | 40 W, ~366 g, Veggie-Glycerin |
| LensGo Smoke B | Handgeraet | ~18 min | 40 W |

### Warum der MicroFogger fuer den Suit

Smoke Ninja, Ulanzi und LensGo sind **versiegelte Foto-Handgeraete** - schlecht
ins Jetpack zu integrieren. Der **Vosentech MicroFogger 5 Pro** ist explizit zum
**Einbau in Props** gebaut (Fernsteuerung, wechselbarer Akku, food-grade
Glycerin/PG). Das ist die sinnvolle Basis fuer eine "eigene Version", statt ein
Foto-Geraet auszuschlachten. Der Nebel wird wie in Abschnitt 3 ueber einen
Radialluefter + Schlauch zu den Duesen gefuehrt.

### Ehrliche Grenzen (vor dem Kauf lesen)

- **Hitze:** Heizelement (~40 W). Nicht direkt an Foam/Kleber/Akku fuehren,
  Schlauch und Auslass werden warm.
- **Feuermelder:** echter Rauch kann Melder ausloesen. **Nicht** in geschlossenen
  Hallen / auf der Con-Flaeche. Nur Outdoor oder mit Erlaubnis des Veranstalters.
- **Rueckstand:** Glycerin hinterlaesst mit der Zeit einen feinen Film - Duesen
  und Umgebung gelegentlich reinigen.
- **Strombudget:** ein 40-W-Fogger zieht viel mehr als die Ultraschall-Loesung.
  Bester Trick: den MicroFogger auf seinem **eigenen wechselbaren Akku** laufen
  lassen und vom Suit nur das Trigger-Signal geben - so bleibt die Heizlast
  komplett aus deinem Strombudget (Entkopplung wie in `V3-Systemarchitektur.md`).
  Eigener Akku haelt ca. 14 min (voll) / 30 min (mittel) - Ersatzakku einpacken.

### MicroFogger 5 Pro: Steuerung per Arduino

Der MicroFogger laesst sich neben dem Knopf ueber die **mitgelieferte Funk-
Fernbedienung (4 Kanaele)** ODER ueber den **USB-C-Port als Steuer-/Trigger-
Schnittstelle** ansteuern. Drei Wege, von elegant zu pragmatisch:

1. **USB-C-Steuerport (sauberste Loesung):** Vosentech bewirbt den Port explizit
   zum Anbinden an ein eigenes Trigger-System. Wenn Pinout/Protokoll dokumentiert
   sind, haengt der Arduino direkt dran - kein Funk noetig. **Zuerst bei Vosentech
   / im Manual abklaeren** (exaktes Pinout war oeffentlich nicht auffindbar).
2. **Vorhandene Fernbedienung "druecken" lassen:** Statt einen neuen RF-Sender zu
   bauen (Frequenz + Codierung des Fobs treffen = fummelig), einen **Optokoppler
   oder Transistor ueber die Tasten-Pads der Original-Fernbedienung** loeten. Der
   Arduino schaltet den Optokoppler, die echte Fernbedienung sendet - originale
   Funkpaarung bleibt erhalten, ~2 Bauteile pro Taste. Robust und simpel.
3. **Servo/Solenoid auf den Geraeteknopf:** Mikro-Servo drueckt physisch den
   Hauptknopf. Protokoll-unabhaengig, aber klobig - nur als Fallback.

So oder so triggert am Ende ein **GPIO-Pin** des Schubduesen-Arduino den Fogger -
gekoppelt an denselben Boost-Taster, der auch die LEDs auf volle Helligkeit setzt
(Abschnitt 5). Ein Boost = Licht + Rauch gleichzeitig.

### Sauberer Einbau ins Jetpack

- **Eigener Akku, nur Trigger vom Suit** (siehe Strombudget oben) - das ist der
  sauberste Schnitt: ein einziges Signalkabel statt Heizstrom durch den Suit.
- **Hitze isolieren:** Heizteil/Auslass werden heiss. In eine belueftete Kammer
  mit Abstand zu Foam, Kleber und LiPo setzen; Halterung aus Metall/Hochtemp-Kunststoff.
- **Lage:** Fogger halbwegs aufrecht/eben halten (Fluid-Zufuhr) - nicht kippen.
- **Refill-/Akku-Klappe:** Tank reicht nur ~7-15 min. Eine **gut erreichbare
  Klappe** am Rucksack einplanen (Fluid nachfuellen UND Akku wechseln), nicht
  hinter verklebten Platten vergraben.
- **Nebelfuehrung:** Auslass per Silikonschlauch + Radialluefter und Y-Verteiler
  zu den zwei Duesen - identisch zur Ultraschall-Variante (Abschnitt 3).

### Empfehlung: zwei Stufen

1. **Con-Alltag:** Ultraschall-Kaltnebel (Abschnitt 1-6) - sicher, erlaubt.
2. **Beast Mode (Photoshoot/Outdoor):** MicroFogger - dichter Rauch, kontrollierte
   Umgebung, mit Handler.

Kauflinks und Bezugsquellen gehoeren in `Materials/Einkaufsliste-Links.md`,
falls du dich fuer ein Geraet entscheidest.
