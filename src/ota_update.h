#ifndef OTA_UPDATE_H
#define OTA_UPDATE_H

#include <HTTPClient.h>
#include <Update.h>
#include "config.h"

void checkForUpdate();
void downloadAndUpdateFirmware();

#endif