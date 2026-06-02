/*
 * SensorFeeder.ino  -  Sensor-Feeder fuer den V3 AR-Helm
 *
 * Liest Bewegung (MPU6050 IMU ueber I2C) und Akkuspannung (Spannungsteiler)
 * und schickt sie als JSON-Zeilen ueber die serielle Schnittstelle an den
 * AR-Rechner (Raspberry Pi 4/5), wo ar_passthrough.py sie ins HUD einblendet.
 *
 * WICHTIG (siehe Documentation/Guides/Elektronik-AR-Display.md, Abschnitt 4):
 * Sensorik und Luefter laufen BEWUSST auf einem eigenen Mikrocontroller,
 * unabhaengig vom Grafik-Rechner. Faellt der Pi aus, laeuft dieser Controller
 * (und damit z.B. die Luefterregelung) weiter.
 *
 * Zielboard: ESP32 (empfohlen) oder Arduino Nano. Auf Arduino den ADC-Teil
 * an 10-bit ADC und 5V-Logik anpassen.
 *
 * Verkabelung (ESP32):
 *   MPU6050 SDA -> GPIO 21,  SCL -> GPIO 22,  VCC -> 3V3,  GND -> GND
 *   Akku-Spannungsteiler -> GPIO 34 (ADC1, nur Eingang)
 *
 * Ausgabe (eine Zeile, ca. 10 Hz):
 *   {"heading":123,"battery":78,"temp":41}
 *
 * Hinweis: "heading" stammt aus integrierter Gyro-Z-Rate und ist RELATIV
 * (driftet langsam). Fuer einen echten Kompass zusaetzlich ein Magnetometer
 * (z.B. HMC5883L) ergaenzen. Fuer ein Cosplay-HUD ist die relative Drehung
 * meist ausreichend.
 */

#include <Wire.h>

// ---- Konfiguration ----
const uint8_t  MPU_ADDR    = 0x68;   // MPU6050 I2C-Adresse (AD0 = GND)
const uint8_t  BATT_PIN    = 34;     // ADC-Pin am Spannungsteiler
const float    ADC_REF     = 3.30;   // ESP32 ADC-Referenz (Volt)
const int      ADC_MAX     = 4095;   // 12-bit ADC
const float    DIVIDER     = 2.0;    // Teilerfaktor (z.B. 100k/100k = 2.0)
const float    BATT_FULL   = 8.40;   // 2S LiPo voll (Volt)
const float    BATT_EMPTY  = 6.40;   // 2S LiPo leer (Volt)
const uint32_t SEND_EVERY  = 100;    // ms zwischen Ausgaben (10 Hz)

float headingDeg = 0.0;
float gyroZbias  = 0.0;
uint32_t lastSend = 0;
uint32_t lastIntegrate = 0;

void mpuWrite(uint8_t reg, uint8_t val) {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(reg);
  Wire.write(val);
  Wire.endTransmission();
}

int16_t mpuReadWord(uint8_t reg) {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(reg);
  Wire.endTransmission(false);
  Wire.requestFrom((int)MPU_ADDR, 2, true);
  int16_t hi = Wire.read();
  int16_t lo = Wire.read();
  return (hi << 8) | lo;
}

// Gyro-Z in Grad/Sekunde (Standard-Empfindlichkeit +-250 dps -> 131 LSB/dps)
float readGyroZdps() {
  return mpuReadWord(0x47) / 131.0;
}

float readTempC() {
  // MPU6050 Temperaturformel laut Datenblatt
  return mpuReadWord(0x41) / 340.0 + 36.53;
}

int batteryPercent() {
  long sum = 0;
  for (int i = 0; i < 16; i++) {
    sum += analogRead(BATT_PIN);
  }
  float adc = sum / 16.0;
  float vpin = (adc / ADC_MAX) * ADC_REF;
  float vbatt = vpin * DIVIDER;
  float pct = (vbatt - BATT_EMPTY) / (BATT_FULL - BATT_EMPTY) * 100.0;
  if (pct < 0) pct = 0;
  if (pct > 100) pct = 100;
  return (int)(pct + 0.5);
}

void calibrateGyro() {
  // Controller beim Start ruhig liegen lassen: Gyro-Z-Nullpunkt messen
  float sum = 0;
  const int n = 200;
  for (int i = 0; i < n; i++) {
    sum += readGyroZdps();
    delay(3);
  }
  gyroZbias = sum / n;
}

void setup() {
  Serial.begin(115200);
  Wire.begin();           // ESP32: SDA=21, SCL=22 (Standard)
  mpuWrite(0x6B, 0x00);   // MPU6050 aus dem Sleep wecken
  delay(100);
  analogReadResolution(12);
  calibrateGyro();
  lastIntegrate = millis();
  lastSend = millis();
}

void loop() {
  uint32_t now = millis();

  // Gyro-Z integrieren -> relative Drehung (Heading)
  float dps = readGyroZdps() - gyroZbias;
  float dt = (now - lastIntegrate) / 1000.0;
  lastIntegrate = now;
  if (dt > 0 && dt < 0.5) {
    headingDeg += dps * dt;
    while (headingDeg < 0)    headingDeg += 360.0;
    while (headingDeg >= 360) headingDeg -= 360.0;
  }

  if (now - lastSend >= SEND_EVERY) {
    lastSend = now;
    int batt = batteryPercent();
    int temp = (int)(readTempC() + 0.5);
    int head = (int)(headingDeg + 0.5);
    // JSON-Zeile fuer ar_passthrough.py
    Serial.print("{\"heading\":");
    Serial.print(head);
    Serial.print(",\"battery\":");
    Serial.print(batt);
    Serial.print(",\"temp\":");
    Serial.print(temp);
    Serial.println("}");
  }
}
