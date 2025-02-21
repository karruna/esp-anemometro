#include "ota_update.h"
#include "firebase_utils.h"

String Update_Version = "";
String Firebase_Firmawre_Update_URL = "";

void downloadAndUpdateFirmware() {
  HTTPClient http;
  http.begin(Firebase_Firmawre_Update_URL);
  int httpCode = http.GET();

  if (httpCode == HTTP_CODE_OK) {
    WiFiClient &client = http.getStream();
    int firmwareSize = http.getSize();

    if (Update.begin(firmwareSize)) {
      size_t written = Update.writeStream(client);

      if (Update.size() == written) {
        Serial.println("Update successfully completed. Rebooting...");
        if (Update.end()) {
          ESP.restart();
        }
      }
    }
  }
  http.end();
}

void checkForUpdate() {
  if (Firebase.ready()) {
    if (Firebase.RTDB.getString(&fbdo, "/update/ESP1/version")) {
      Update_Version = fbdo.stringData();
      int update = Update_Version.compareTo(CURRENT_FIRMWARE_VERSION);

      if (update > 0) {
        if (Firebase.RTDB.getString(&fbdo, "/update/ESP1/url")) {
          Firebase_Firmawre_Update_URL = fbdo.stringData();
          downloadAndUpdateFirmware();
        }
      }
    }
  }
}