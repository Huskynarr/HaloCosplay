# LED-Effekte und Programmierung

Bewaehrte LED-Muster fuer Cosplay und wie man sie programmiert.

## Empfohlene Effekte

| Effekt | Beschreibung | Einsatz | Wirkung |
| --- | --- | --- | --- |
| Breathing | Langsames sinusfoermiges Ein-/Ausblenden (2-3s Zyklus) | Visor, Brustplatte | Ruhig, lebendig, "aktive Technologie" |
| Heartbeat | Zwei schnelle Pulse + laengere Pause | Brust-Reaktor | Organisch, Power-Core |
| Static Glow | Konstantes Leuchten bei 50-70% | Allgemein | Einfach, zuverlaessig, stromsparend |
| Idle Flicker | Sehr subtile Zufalls-Variation (95-100%) | Visor | Energie-Fluktuation, lebendig |
| Chase | Laufendes Licht entlang des Strips | Schultern, Arme | Bewegung, Tech-Look |
| Boot-Up | Sweep von aus zu voll (3-5s) | Visor bei Einschalten | Dramatischer Einstieg |
| Reactive | Pulsiert mit Mikrofon-Input | Visor/Brust | Reagiert auf Stimme, sehr immersiv |

## Arduino Code-Beispiele (WS2812B / NeoPixel)

### Setup (fuer alle Beispiele)

```cpp
#include <Adafruit_NeoPixel.h>

#define LED_PIN    6
#define NUM_LEDS   10
#define BRIGHTNESS 128  // 50% = guter Convention-Wert

Adafruit_NeoPixel strip(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  strip.begin();
  strip.setBrightness(BRIGHTNESS);
  strip.show();
}
```

### Breathing (Sinuswelle)

```cpp
void loop() {
  // Sinuswelle fuer natuerliches Pulsieren
  float val = (sin(millis() / 1500.0) + 1.0) * 0.5;  // 0.0 bis 1.0
  uint8_t brightness = (uint8_t)(val * 255);

  for (int i = 0; i < NUM_LEDS; i++) {
    strip.setPixelColor(i, 0, brightness, brightness / 3);  // Gruen-Cyan
  }
  strip.show();
  delay(10);
}
```

### Heartbeat

```cpp
void heartbeat() {
  // Puls 1
  fadeTo(200, 80);
  fadeTo(0, 120);
  delay(100);
  // Puls 2
  fadeTo(255, 80);
  fadeTo(0, 150);
  // Pause
  delay(600);
}

void fadeTo(uint8_t target, uint16_t duration) {
  uint8_t current = strip.getPixelColor(0) >> 8;  // Gruen-Kanal
  int steps = duration / 10;
  for (int i = 0; i <= steps; i++) {
    uint8_t val = current + (target - current) * i / steps;
    for (int j = 0; j < NUM_LEDS; j++) {
      strip.setPixelColor(j, 0, val, val / 3);
    }
    strip.show();
    delay(10);
  }
}

void loop() {
  heartbeat();
}
```

### Idle Flicker (subtil)

```cpp
void loop() {
  for (int i = 0; i < NUM_LEDS; i++) {
    uint8_t flicker = random(230, 255);  // Nur 90-100% Variation
    strip.setPixelColor(i, 0, flicker, flicker / 3);
  }
  strip.show();
  delay(50);
}
```

### Boot-Up Sweep

```cpp
void bootSequence() {
  // Sweep von links nach rechts
  for (int i = 0; i < NUM_LEDS; i++) {
    strip.setPixelColor(i, 0, 200, 60);
    strip.show();
    delay(200);
  }
  // Aufblitzen
  for (int b = 0; b < 3; b++) {
    strip.setBrightness(255);
    strip.show();
    delay(100);
    strip.setBrightness(BRIGHTNESS);
    strip.show();
    delay(100);
  }
}

void setup() {
  strip.begin();
  strip.setBrightness(BRIGHTNESS);
  bootSequence();
}
```

### Sound-Reactive (mit MAX4466 Mikrofon)

```cpp
#define MIC_PIN A0

void loop() {
  // Mikrofon-Pegel lesen (mehrere Samples fuer Stabilitaet)
  int maxVal = 0;
  for (int i = 0; i < 50; i++) {
    int val = abs(analogRead(MIC_PIN) - 512);
    if (val > maxVal) maxVal = val;
  }

  // Auf LED-Helligkeit mappen
  uint8_t brightness = map(constrain(maxVal, 10, 300), 10, 300, 30, 255);

  for (int i = 0; i < NUM_LEDS; i++) {
    strip.setPixelColor(i, 0, brightness, brightness / 3);
  }
  strip.show();
  delay(20);
}
```

## Farb-Empfehlungen

| Einsatz | Farbe | RGB-Werte | Wirkung |
| --- | --- | --- | --- |
| Visor (klassisch) | Warm-Gold/Amber | R:255, G:180, B:20 | Ikonischer Master Chief Look |
| Visor (Cortana) | Kuehles Blau | R:0, G:100, B:255 | Cortana-Effekt |
| Ruestungs-Akzente | Gruen-Cyan | R:0, G:200, B:60 | MJOLNIR Tech-Glow |
| Alarm/Damage | Orange-Rot | R:255, G:60, B:0 | Schild-Alarm |

**Hinweis:** Reines Weiss vermeiden — sieht durch goldene Visor-Toenung verwaschen aus. Warme Toene (Amber, Gold) wirken durch den Visor am besten.

## Praktische Tipps

### Helligkeit

- **50% Helligkeit** fuer Convention-Innenraeume (helle Hallen)
- **100%** nur fuer Outdoor-Fotoshootings oder dunkle Raeume
- **25%** fuer Nacht-Events (Augen der Betrachter angepasst)
- Helligkeits-Umschaltung per Taster am Arduino einbauen

### PWM-Frequenz (Foto-kompatibel)

Standard-Arduino `analogWrite` laeuft bei 490 Hz — kann sichtbare Streifen in Fotos erzeugen.

Loesung: Timer-basiertes PWM oder NeoPixel-Library (diese nutzt eigenes Timing und ist foto-sicher).

### Stromsparen

- LEDs bei 50% Helligkeit brauchen nur ~25% des Stroms von voller Helligkeit
- Nicht alle LEDs gleichzeitig auf Maximum — 60 LEDs weiss bei 100% = 3.6 A!
- Gruenes Einzelkanal-Leuchten braucht nur 1/3 des Stroms von Weiss

### Convention-Realitaet

- In einer hell beleuchteten Halle sind subtile Effekte (Idle Flicker, leichtes Pulsieren) kaum sichtbar
- Fuer Convention: lieber **konstant hell** oder **deutliches Breathing** statt zu subtile Muster
- Komplexe Muster fuer **Fotoshootings und dunkle Raeume** aufheben

## Weiterführend

- **LED-Visor-Forschung (Diffusion, Foto-Probleme, COB Strips, 9mm-Regel):** `Documentation/Guides/LED-Visor-Forschung.md`
- **Helm LED-Controller Code:** `Code/HelmetControl/HelmetMultiEffects.ino`
- **Ruestung LED-Controller Code:** `Code/ArmorControl/MultiEffects.ino`
