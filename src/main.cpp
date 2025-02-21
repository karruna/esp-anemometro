#include <Arduino.h>
#include <WiFi.h>
#include <Firebase_ESP_Client.h>
#include <HTTPClient.h>
#include <Update.h>
#include "config.h"
#include "wifi_utils.h"
#include "firebase_utils.h"
#include "anemometer.h"
#include "ota_update.h"

unsigned long sendDataPrevMillis = 0;
int count = 0;
bool signupOK = false;

void setup() {
  Serial.begin(115200);
  setupWiFi();
  setupFirebase();
  setupAnemometer();
}

void loop() {
  if (millis() >= sendDataPrevMillis + 60000) {
    calculateWindSpeed();
    sendDataToFirebase(vmin, vmed, vmax, analogRead(dir));
    sendDataPrevMillis = millis();
  }

  checkForUpdate();
  delay(50);
}