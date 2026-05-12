#include "DHT.h"
#include <WiFi.h>
#include <HTTPClient.h>

#define DHTPIN 4
#define DHTTYPE DHT11

// const char* ssid = "RCU - DOCENTES";
const char* ssid = "prieca";
// const char* password = "DOCENTESUNSAAC2025$";
const char* password = "pc123456";
// const char* serverURL = "http://34.172.215.14:8691/temperature/api/store/";
const char* serverURL = "http://192.168.1.19:8000/temperature/api/store/";
const char* token = "mi_token_secreto";

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  WiFi.begin(ssid, password);
  Serial.print("Conectando WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" Conectado!");
  dht.begin();
}

void loop() {
  delay(2000);

  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float f = dht.readTemperature(true);

  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  float hic = dht.computeHeatIndex(t, h, false);

  Serial.print("Humidity: "); Serial.print(h);
  Serial.print("%  Temperature: "); Serial.print(t);
  Serial.print("°C  Heat index: "); Serial.println(hic);

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverURL);
    http.addHeader("Content-Type", "application/json");
    String payload = "{\"temperature\":" + String(t) + ",\"humidity\":" + String(h) + ",\"heat_index\":" + String(hic) + ",\"token\":\"" + token + "\"}";
    int httpCode = http.POST(payload);
    Serial.println("HTTP: " + String(httpCode));
    http.end();
  }
}
