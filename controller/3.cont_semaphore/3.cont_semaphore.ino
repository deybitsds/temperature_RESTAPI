#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "RCU - DOCENTES";
const char* password = "DOCENTESUNSAAC2025$";
const char* apiURL = "http://34.172.215.14:8691/temperature/api/semaphore/";

#define LED_R 12
#define LED_Y 14
#define LED_G 27

void setup() {
  Serial.begin(9600);
  pinMode(LED_R, OUTPUT);
  pinMode(LED_Y, OUTPUT);
  pinMode(LED_G, OUTPUT);
  digitalWrite(LED_R, LOW);
  digitalWrite(LED_Y, LOW);
  digitalWrite(LED_G, LOW);

  WiFi.begin(ssid, password);
  Serial.print("WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" OK");
}

void loop() {
  delay(2000);

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi lost");
    return;
  }

  HTTPClient http;
  http.begin(apiURL);
  http.addHeader("Accept", "application/json");
  int code = http.GET();
  String body = http.getString();
  http.end();

  if (code != 200) {
    Serial.println("HTTP " + String(code));
    return;
  }

  bool r = body.indexOf("\"red\":true") >= 0;
  bool y = body.indexOf("\"yellow\":true") >= 0;
  bool g = body.indexOf("\"green\":true") >= 0;

  digitalWrite(LED_R, r ? HIGH : LOW);
  digitalWrite(LED_Y, y ? HIGH : LOW);
  digitalWrite(LED_G, g ? HIGH : LOW);

  Serial.println("R:" + String(r) + " Y:" + String(y) + " G:" + String(g));
}
