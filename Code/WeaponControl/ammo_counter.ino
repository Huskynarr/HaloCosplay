// Benoetigte Bibliotheken fuer das OLED-Display
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <JC_Button.h> // Library "JC_Button" (ueber den Arduino Library Manager installierbar)

// Display-Spezifikationen
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET 4
#define TEXT_SIZE 8

// Pin-Belegung fuer den Arduino
#define TRIGGER_BTN_PIN 2     // Mikroschalter am Abzug
#define RELOAD_BTN_PIN 4      // Sensor/Schalter im Magazinschacht (z.B. Hall-Effekt)
#define MAG_SZ_TOG_BTN_PIN 5  // Optional: Knopf zum Wechseln der Magazingroesse

// Button-Debounce in ms (interner Pull-Up und Invertierung sind JC_Button-Standard)
#define DEBOUNCE_MS 20

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Buttons initialisieren
Button triggerBtn(TRIGGER_BTN_PIN, DEBOUNCE_MS);
Button reloadBtn(RELOAD_BTN_PIN, DEBOUNCE_MS);
Button magSzTogBtn(MAG_SZ_TOG_BTN_PIN, DEBOUNCE_MS);

// Halo Sturmgewehr (MA40/MA5) Magazingroessen (Standard: 32 oder 36)
byte magSizeArr[] = {32, 36, 60}; 
byte currentMagSize = 0; 
byte maxAmmo = magSizeArr[currentMagSize]; 
byte currentAmmo = maxAmmo; 

void setup() {
  Serial.begin(9600);
  triggerBtn.begin();
  reloadBtn.begin();
  magSzTogBtn.begin();
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C); // I2C Adresse fuer das Display
  initDisplayAmmo();
}

void loop() {
  countAmmo();  // Schuesse zaehlen
  reload();     // Magazinwechsel pruefen
  toggleMags(); // Magazingroesse wechseln (optional)
}

// Funktion: Munition auf dem OLED zentriert anzeigen
void displayAmmo(String ammoToDisplay) {
  display.clearDisplay(); 
  display.setTextSize(TEXT_SIZE); 
  display.setTextColor(WHITE); 
  // Text zentrieren (Standard-Font: 6x8 Pixel pro Groessenstufe)
  display.setCursor((SCREEN_WIDTH - ammoToDisplay.length() * 6 * TEXT_SIZE) / 2,
                    (SCREEN_HEIGHT - 8 * TEXT_SIZE) / 2);
  display.print(ammoToDisplay); 
  display.display(); 
}

// Funktion: Fuehrende Null bei einstelligen Zahlen hinzufuegen (z.B. "04")
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
      // HIER KOeNNTE AUCH DER SOUND-Befehl fuer das Soundboard stehen!
    }
    initDisplayAmmo(); 
  }
}

// Funktion: Nachlade-Logik
void reload() {
  reloadBtn.read(); 
  if (reloadBtn.wasPressed()) { 
    currentAmmo = maxAmmo; // Munition auf Maximum zuruecksetzen
    initDisplayAmmo(); 
  }
}

// Funktion: Magazingroesse durchschalten
void toggleMags() {
  magSzTogBtn.read(); 
  if (magSzTogBtn.wasPressed()) { 
    currentMagSize = (currentMagSize < (sizeof(magSizeArr)/sizeof(magSizeArr[0]) - 1)) ? currentMagSize + 1 : 0;
    maxAmmo = magSizeArr[currentMagSize];
    currentAmmo = maxAmmo;
    initDisplayAmmo(); 
  }
}
