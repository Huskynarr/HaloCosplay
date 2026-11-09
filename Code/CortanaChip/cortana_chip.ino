// Cortana-Chip Firmware - ESP32-S3 (Arduino).
// Stellt Charakter-Daten per BLE bereit und zeigt Status auf dem OLED.
// Bibliotheken: Adafruit SSD1306, Adafruit GFX, BLEDevice (ESP32-Core).
//
// Verhalten:
//  - Charakter-Daten (cortana_v1.json / husky_v1.json) aus LittleFS lesen
//  - BLE-Service mit Charakteristic fuer Charakter-ID + Status-JSON
//  - OLED zeigt ID, Status und BLE-Status
//  - Taster (GPIO 0 = BOOT) wechselt zwischen Statusseiten
//
// Konvention: Alle Werte sind Konzeptwerte; keine Freigabe fuer den
// Tragebetrieb. Vor dem ersten Einsatz Strombudget und Sicherheit pruefen.

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <ArduinoJson.h>
#include <LittleFS.h>

// ---- Display ----
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define OLED_ADDR 0x3C
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// ---- Pins ----
#define PIN_PAGE_BTN 0   // BOOT-Taster wechselt die Seite
#define PIN_STATUS_LED 48 // Onboard-RGB (optional)

// ---- BLE ----
#define SERVICE_UUID "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHAR_ID_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"
#define CHAR_DATA_UUID "beb5483f-36e1-4688-b7f5-ea07361b26a8"

BLEServer* pServer = nullptr;
BLECharacteristic* pIdChar = nullptr;
BLECharacteristic* pDataChar = nullptr;
bool deviceConnected = false;

// ---- Charakter-Daten ----
struct Character {
  String id;
  String name;
  String status;
  int shield;
  int energy;
  String mode;
};
Character character;

// ---- Seiten ----
int page = 0;
const int PAGE_COUNT = 3;

void loadCharacter(const char* path) {
  File f = LittleFS.open(path, "r");
  if (!f) {
    Serial.println("Fehler: Charakter-Datei nicht gefunden");
    character.id = "UNKNOWN";
    character.name = "UNBEKANNT";
    character.status = "offline";
    character.shield = 0;
    character.energy = 0;
    character.mode = "standby";
    return;
  }
  JsonDocument doc;
  DeserializationError err = deserializeJson(doc, f);
  f.close();
  if (err) {
    Serial.println("Fehler: JSON ungueltig");
    return;
  }
  character.id = doc["id"].as<String>();
  character.name = doc["name"].as<String>();
  character.status = doc["status"].as<String>();
  character.shield = doc["shield"] | 100;
  character.energy = doc["energy"] | 100;
  character.mode = doc["mode"].as<String>();
}

void setupBLE() {
  BLEDevice::init(character.id.c_str());
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new ServerCallbacks());
  BLEService* pService = pServer->createService(SERVICE_UUID);
  pIdChar = pService->createCharacteristic(
      CHAR_ID_UUID, BLECharacteristic::PROPERTY_READ);
  pDataChar = pService->createCharacteristic(
      CHAR_DATA_UUID, BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY);
  pIdChar->setValue(character.id.c_str());
  updateDataChar();
  pService->start();
  pServer->getAdvertising()->start();
  Serial.println("BLE gestartet");
}

void updateDataChar() {
  JsonDocument doc;
  doc["id"] = character.id;
  doc["name"] = character.name;
  doc["status"] = character.status;
  doc["shield"] = character.shield;
  doc["energy"] = character.energy;
  doc["mode"] = character.mode;
  String out;
  serializeJson(doc, out);
  pDataChar->setValue(out.c_str());
  pDataChar->notify();
}

class ServerCallbacks : public BLEServerCallbacks {
  void onConnect(BLEServer* s) override { deviceConnected = true; }
  void onDisconnect(BLEServer* s) override {
    deviceConnected = false;
    pServer->getAdvertising()->start();
  }
};

void drawPage() {
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);
  if (page == 0) {
    display.setCursor(0, 0);
    display.println(character.name);
    display.setCursor(0, 16);
    display.println("Status: " + character.status);
    display.setCursor(0, 28);
    display.println("Schild: " + String(character.shield) + "%");
    display.setCursor(0, 40);
    display.println("Energie: " + String(character.energy) + "%");
    display.setCursor(0, 52);
    display.println("Modus: " + character.mode);
  } else if (page == 1) {
    display.setCursor(0, 0);
    display.println("BLE: " + String(deviceConnected ? "verbunden" : "wartet"));
    display.setCursor(0, 16);
    display.println("ID: " + character.id);
    display.setCursor(0, 32);
    display.println("Daten aktiv, bereit");
  } else {
    display.setCursor(0, 0);
    display.println("CORTANA CHIP v1");
    display.setCursor(0, 16);
    display.println("Konzept-Prototyp");
    display.setCursor(0, 32);
    display.println("Keine Freigabe");
  }
  display.display();
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_PAGE_BTN, INPUT_PULLUP);
  Wire.begin(6, 7);  // SDA=6, SCL=7 (ESP32-S3 Standard)
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
    Serial.println("OLED nicht gefunden");
  }
  if (!LittleFS.begin(true)) {
    Serial.println("LittleFS nicht initialisierbar");
  }
  loadCharacter("/cortana_v1.json");
  setupBLE();
  drawPage();
}

void loop() {
  static unsigned long lastBtn = 0;
  if (digitalRead(PIN_PAGE_BTN) == LOW && millis() - lastBtn > 300) {
    page = (page + 1) % PAGE_COUNT;
    lastBtn = millis();
    drawPage();
  }
  // Demo: Schild langsam regenerieren
  static unsigned long lastTick = 0;
  if (millis() - lastTick > 5000) {
    if (character.shield < 100) {
      character.shield += 5;
      updateDataChar();
      drawPage();
    }
    lastTick = millis();
  }
}
