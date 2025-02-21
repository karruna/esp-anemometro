#ifndef FIREBASE_UTILS_H
#define FIREBASE_UTILS_H

#include <Firebase_ESP_Client.h>
#include "config.h"

extern FirebaseData fbdo;
extern FirebaseAuth auth;
extern FirebaseConfig config;

void setupFirebase();
void sendDataToFirebase(float vmin, float vmed, float vmax, int potValue);

#endif