#include "firebase_utils.h"
#include "addons/TokenHelper.h"
#include "addons/RTDBHelper.h"

FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

void setupFirebase() {
  config.api_key = API_KEY;
  config.database_url = DATABASE_URL;

  if (Firebase.signUp(&config, &auth, "", "")) {
    Serial.println("Firebase sign-up OK");
  } else {
    Serial.printf("Firebase sign-up failed: %s\n", config.signer.signupError.message.c_str());
  }

  config.token_status_callback = tokenStatusCallback;
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);
}

void sendDataToFirebase(float vmin, float vmed, float vmax, int potValue) {
  FirebaseJson json;
  json.set("vmin", vmin);
  json.set("vmed", vmed);
  json.set("vmax", vmax);

  if (Firebase.RTDB.setTimestamp(&fbdo, "/temp/timestamp")) {
    int64_t timestamp = fbdo.intData();
    String path = "/acquisition/ESP1/" + String(timestamp);

    if (Firebase.RTDB.setJSON(&fbdo, path, &json)) {
      Serial.println("Data sent successfully!");
    } else {
      Serial.println("Failed to send data: " + fbdo.errorReason());
    }
  } else {
    Serial.println("Failed to set timestamp: " + fbdo.errorReason());
  }
}