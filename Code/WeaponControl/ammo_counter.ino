// Benötigte Bibliotheken für das OLED-Display
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Button.h> // Hinweis: Die spezifische mochoy-Button-Bibliothek verwenden!

// Display-Spezifikationen
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET 4
#define TEXT_SIZE 8

// Pin-Belegung für den Arduino
#define TRIGGER_BTN_PIN 2     // Mikroschalter am Abzug
#define RELOAD_BTN_PIN 4      // Sensor/Schalter im Magazinschacht (z.B. Hall-Effekt)
#define MAG_SZ_TOG_BTN_PIN 5  // Optional: Knopf zum Wechseln der Magazingröße

// Button-Parameter (Pullup-Widerstand nutzen, invertiert, Debounce in ms)
#define INVERT true
#define PULLUP true
#define DEBOUNCE_MS 20

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Buttons initialisieren
Button triggerBtn(TRIGGER_BTN_PIN, PULLUP, INVERT, DEBOUNCE_MS); 
Button reloadBtn(RELOAD_BTN_PIN, PULLUP, INVERT, DEBOUNCE_MS); 
Button magSzTogBtn(MAG_SZ_TOG_BTN_PIN, PULLUP, INVERT, DEBOUNCE_MS); 

// Halo Sturmgewehr (MA40/MA5) Magazingrößen (Standard: 32 oder 36)
byte magSizeArr[] = {32, 36, 60}; 
byte currentMagSize = 0; 
byte maxAmmo = magSizeArr[currentMagSize]; 
byte currentAmmo = maxAmmo; 

void setup() {
  Serial.begin(9600);
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C); // I2C Adresse für das Display
  initDisplayAmmo(); 
}

void loop() {
  countAmmo();  // Schüsse zählen
  reload();     // Magazinwechsel prüfen
  toggleMags(); // Magazingröße wechseln (optional)
}

// Funktion: Munition auf dem OLED zentriert anzeigen
void displayAmmo(String ammoToDisplay) {
  display.clearDisplay(); 
  display.setTextSize(TEXT_SIZE); 
  display.setTextColor(WHITE); 
  // Text zentrieren
  display.setCursor((SCREEN_WIDTH/2) - ((ammoToDisplay.length()*2) * (TEXT_SIZE * 1.5)), (SCREEN_HEIGHT/2) - (TEXT_SIZE * 3)); 
  display.print(ammoToDisplay); 
  display.display(); 
}

// Funktion: Führende Null bei einstelligen Zahlen hinzufügen (z.B. "04")
void initDisplayAmmo() {
  String ammoToDisplay = currentAmmo < 10 ? ("0" + (String)currentAmmo) : (String)currentAmmo;
  displayAmmo(ammoToDisplay); 
}

// Funktion: Schuss-Logik
void countAmmo() {
  triggerBtn.read(); 
  if (triggerBtn.wasPressed()) { 
    if (currentAmmo > 0) { 
      currentAmmo--; // Munition um 1 reduzieren
      // HIER KÖNNTE AUCH DER SOUND-Befehl für das Soundboard stehen!
    }
    initDisplayAmmo(); 
  }
}

// Funktion: Nachlade-Logik
void reload() {
  reloadBtn.read(); 
  if (reloadBtn.wasPressed()) { 
    currentAmmo = maxAmmo; // Munition auf Maximum zurücksetzen
    initDisplayAmmo(); 
  }
}

// Funktion: Magazingröße durchschalten
void toggleMags() {
  magSzTogBtn.read(); 
  if (magSzTogBtn.wasPressed()) { 
    currentMagSize = (currentMagSize < (sizeof(magSizeArr)/sizeof(magSizeArr[0]) - 1)) ? currentMagSize + 1 : 0;
    maxAmmo = magSizeArr[currentMagSize];
    currentAmmo = maxAmmo;
    initDisplayAmmo(); 
  }
}
