# Beleuchtete Schubdüsen & Nebel-Effekte (Jetpack)

> **Level:** [F] Fortgeschritten | [P] Profi  ·  **Varianten:** V2/V3 (Jetpack/Backpack)
> **Voraussetzungen:** Arduino IDE eingerichtet, Grundlagen Elektronik-Verdrahtung (`Documentation/Guides/Elektronik-Verdrahtung.md`), Grundlagen LED-Effekte (`Documentation/Guides/LED-Effekte.md`).

Dieses Modul beschreibt den Bau, die Verkabelung und die Programmierung von beleuchteten Schubdüsen (Thrusters) am Rückenmodul (Jetpack) des MJOLNIR-Suits, inklusive eines aktiven Nebelausstoßes für den ultimativen Show-Effekt.

---

## 1. Funktionsprinzip & Übersicht

Der Effekt besteht aus drei Säulen:
1. **Lichtquelle:** Ein programmierbarer RGB-LED-Ring (WS2812B NeoPixel) am Fuß der Düse erzeugt dynamische Flammeneffekte (Flackern, Nachbrenner-Blau, Zündungs-Orange).
2. **Diffusion:** Die Düse selbst wird aus transparentem/transluzentem Kunststoff gefertigt und angeraut. Dies streut das Licht perfekt und lässt die Düse wie eine glühende Plasma-Kammer wirken.
3. **Nebel-Effekt:** Ein kompakter 5V-Ultraschall-Vernebler verdampft Wasser im Inneren des Rucksacks. Ein kleiner Radiallüfter (Blower) drückt den kalten Dampf durch Schläuche direkt in die Schubdüsen, wo er von den LEDs beleuchtet wird.

```
+-------------------------------------------------------------+
| Rucksack / Jetpack-Gehäuse                                  |
|                                                             |
|   [Wassertank] ---> (Docht) ---> [Ultraschall-Vernebler]    |
|        ^                                 |                  |
|    [Radiallüfter 5V] (Luftstrom)         v                  |
|                                    [Nebelschlauch]          |
|                                          |                  |
+------------------------------------------|------------------+
                                           v
                             +---------------------------+
                             | Schubdüse (Transluzent)   |
                             |                           |
                             |   *(LED-Ring)*            |
                             |   ============            |
                             |   [Dampfaustritt] ==> ~~~ |
                             +---------------------------+
```

---

## 2. Benötigte Materialien

### Mechanik & Gehäuse
* **Transluzenter Kunststoff:**
  * **Für 3D-Druck:** Transparentes PETG-Filament (z. B. "PETG Clear" oder "Translucent Orange/Blue")
  * **Alternativ (analog):** Acrylglas-Rohre (Plexiglas) mit passendem Durchmesser.
* **Diffusion:** Schleifpapier (Körnung 320, 400 und 800), evtl. Diffusionsfolie oder dünner Verpackungsschaum.
* **Nebelschlauch:** Silikonschlauch (8-10 mm Innendurchmesser).
* **Wassertank:** Kleine, flache und auslaufsichere Plastikflasche (ca. 150-250 ml) mit Schraubverschluss.

### Elektronik & Nebler-Hardware
* **LED-Ringe:** 2x WS2812B RGB LED-Ringe (z. B. mit 12 oder 16 LEDs, Außendurchmesser passend zum Düseneingang).
* **Vernebler-Modul:** 5V USB Ultraschall-Vernebler-Platine (Mist Maker), wie sie in Mini-Luftbefeuchtern verbaut sind (inkl. Piezo-Keramikscheibe und Baumwoll-Docht).
* **Lüfter für Nebeltransport:** 5V DC Radiallüfter (Blower Fan, z. B. 4010 oder 5015). Wichtig: Radiallüfter bauen Druck auf, Axiallüfter (normale PC-Lüfter) sind ungeeignet!
* **Leistungstreiber (MOSFET):** IRLZ44N N-Kanal MOSFET (zum Ein-/Ausschalten des Neblers und des Lüfters über den Arduino).
* **Widerstände:** 1x 10k Ohm (Pull-Down-Widerstand für das MOSFET-Gate), 1x 220 Ohm (Gate-Widerstand), 1x 330 Ohm (LED-Datenleitung).
* **Diode:** 1x 1N4007 (Freilaufdiode für den Lüftermotor).
* **Kondensator:** 1x 1000 µF Elektrolytkondensator (Gleichrichter/Glättung).

---

## 3. Mechanischer Bau

### A. Die Schubdüsen (Diffusion)
1. **Drucken (PETG):** Drucke die Düsen-Inserts aus transparentem PETG.
   * *Tipp:* Nutze den **Vase Mode** (Spiral-Druck) für eine einzelne, durchgehende Außenwand ohne Nähte, oder drucke mit nur **1 Außenwand** und **0% Infill**. Das spart Gewicht und leitet das Licht optimal.
2. **Mattieren:** Schleife die gedruckten oder aus Acrylrohr geschnittenen Düsen von **innen und außen** gründlich mit 400er, dann mit 800er Schleifpapier nass ab. Die Oberfläche muss milchig-trüb (satiniert) werden.
3. **Alternative Diffusion:** Falls das Licht der einzelnen LEDs immer noch als "Punkte" sichtbar ist (Hotspots), klebe eine Lage Backpapier oder dünne Verpackungsfolie (Schaumfolie) in die Düse.

### B. Das Nebel-System (Tank & Lüfter)
1. **Tank vorbereiten:** Bohre zwei Löcher in den Deckel der Plastikflasche:
   * **Loch 1 (Lufteinlass):** Klebe hier den Luftauslass des 5V-Radiallüfters ein (z. B. mit Heißkleber/Epoxidharz).
   * **Loch 2 (Nebelauslass):** Klebe den Silikonschlauch ein. Er muss knapp unter dem Deckel enden und führt später zu den Düsen (Y-Verteiler nutzen für zwei Düsen).
2. **Piezo-Element montieren:** Die Ultraschall-Scheibe wird per Halterung so knapp über dem Wassertank platziert, dass der Baumwoll-Docht permanent im Wasser hängt und das Wasser per Kapillareffekt an die Unterseite der Metallscheibe saugt.
   * > [!CAUTION]
   * > Die Rückseite des Piezo-Elements (mit den Kabeln) und die Steuerplatine dürfen **niemals nass werden**! Dichte alle elektrischen Anschlüsse mit Epoxidharz oder Silikon ab.
3. **Schlauchführung:** Verlege die Silikonschläuche mit Gefälle zurück zum Tank, damit kondensiertes Wasser zurückfließen kann und den Schlauch nicht verstopft.

---

## 4. Verdrahtung & Schaltplan

Das Nebel-Modul benötigt deutlich mehr Strom als die Steuersignale des Arduino liefern können. Wir steuern den Vernebler und den Lüfter daher über einen **IRLZ44N MOSFET** an.

```
                              Powerbank +5V (GND-gemeinsam!)
                                   |
                                   +---------------------+---------------+
                                   |                     |               |
                                [Nebler +]            [Lüfter +]      [LED VCC]
                                   |                     |               |
                                   |                  [Diode] (Kathode)  |
                                   |                     |               |
                                [Nebler -]            [Lüfter -]         |
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
* **1N4007 Diode (Freilaufdiode):** Schützt den MOSFET vor Spannungsspitzen des Radiallüfters (induktive Last) beim Ausschalten. Die markierte Seite (Kathode/Ring) kommt an +5V, die andere an den Lüfter-Minuspol.
* **1000 µF Kondensator:** Parallel zu +5V und GND nahe am LED-Ring platzieren, um Spannungseinbrüche durch den Anlaufstrom des Lüfters zu puffern.

---

## 5. Software (Arduino Code)

Dieser Sketch steuert das Verhalten: Im Normalzustand (Idle) flackern die Düsen leicht bläulich-orange (Plasma-Bereitschaft). Wird ein Taster gedrückt (oder ein Signal vom I2C-Bus empfangen), zündet der Nachbrenner: Die LEDs wechseln auf helles Orange/Gelb/Weiß-Flackern und der Nebler sowie der Radiallüfter werden aktiviert.

```cpp
#include <Adafruit_NeoPixel.h>

#define LED_PIN       5    // Datenleitung LED-Ringe
#define NUM_LEDS     24    // Gesamtzahl der LEDs (z.B. 2x 12 Ringe in Reihe)
#define TRIGGER_PIN   2    // Taster für Boost-Modus (Gegen GND geschaltet)
#define MIST_PIN      9    // Gate-Steuerung des MOSFETs (Nebler + Lüfter)

#define BRIGHTNESS_IDLE 80  // Moderate Helligkeit für Idle
#define BRIGHTNESS_BOOST 255 // Volle Leistung beim Zünden

Adafruit_NeoPixel strip(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);

bool isBoosting = false;
unsigned long boostStartTime = 0;
const unsigned long BOOST_DURATION = 5000; // Boost läuft 5 Sekunden

void setup() {
  pinMode(TRIGGER_PIN, INPUT_PULLUP);
  pinMode(MIST_PIN, OUTPUT);
  digitalWrite(MIST_PIN, LOW); // Nebler aus
  
  strip.begin();
  strip.setBrightness(BRIGHTNESS_IDLE);
  strip.show();
}

void loop() {
  // Taster abfragen (LOW-aktiv)
  if (digitalRead(TRIGGER_PIN) == LOW && !isBoosting) {
    isBoosting = true;
    boostStartTime = millis();
    digitalWrite(MIST_PIN, HIGH); // Nebler und Lüfter an!
    strip.setBrightness(BRIGHTNESS_BOOST);
  }

  // Boost-Zeit abgelaufen?
  if (isBoosting && (millis() - boostStartTime > BOOST_DURATION)) {
    isBoosting = false;
    digitalWrite(MIST_PIN, LOW); // Nebler und Lüfter aus
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
      strip.setPixelColor(i, 0, baseGreen, baseBlue); // Kühles Sci-Fi-Blau
    }
  }
}

// Aggressiver Nachbrenner/Feuer-Effekt (Gelb-Orange-Weißes Flackern)
void renderBoostEffect() {
  for (int i = 0; i < NUM_LEDS; i++) {
    uint8_t r = random(200, 255);
    uint8_t g = random(80, 160);
    uint8_t b = random(0, 40);
    
    // Sehr selten ein weißer Blitz für Plasma-Eruptionen
    if (random(0, 100) > 95) {
      r = 255; g = 255; b = 255;
    }
    
    strip.setPixelColor(i, r, g, b);
  }
}
```

---

## 6. Praxis-Tipps & Convention-Sicherheit

* **Destilliertes Wasser nutzen:** Verwende im Wassertank ausschließlich destilliertes Wasser. Normales Leitungswasser hinterlässt beim Verdunsten hässliche Kalkflecken auf der mattierten Rüstung und setzt die feinen Poren der Piezo-Scheibe extrem schnell zu.
* **Dichtigkeit & Transport:** Leere den Wassertank vor jedem Transport und drehe den Deckel fest zu. Baue am besten ein kleines Ventil oder einen Absperrhahn in den Schlauch ein, falls der Rucksack hingelegt wird.
* **Convention-Regeln beachten:** Kalter Wasserdampf (Ultraschall) ist auf 99 % der Conventions erlaubt, da er keine Hitze erzeugt und rückstandsfrei verfliegt. Verwende **keine** Nebelmaschinen mit Fluiden (Glycerin/Glykol) – diese erzeugen Hitze, riechen unangenehm, verkleben die Düsen und lösen Feuermelder aus.
* **Batterielaufzeit:** Die Ultraschall-Platine zieht ca. 300-400 mA, der Radiallüfter ca. 150 mA. Zusammen mit den LEDs erhöht das den Stromverbrauch um ca. 0.6 A im Boost-Modus. Kalkuliere dies in deinem Strombudget ein (`Documentation/Guides/Elektronik-Strombudget.md`).
* **Wasserstand-Sensor:** Wenn du den Nebler trocken laufen lässt, verbrennt der Baumwoll-Docht. Nutze entweder einen durchsichtigen Sichtschlitz im Rucksack oder rüste einen einfachen digitalen Wasserstandssensor (Liquid Level Sensor) am Wassertank nach, der den MOSFET deaktiviert, wenn das Wasser leer ist.
