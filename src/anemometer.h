#ifndef ANEMOMETER_H
#define ANEMOMETER_H

#include <Arduino.h>

extern float vmin, vmed, vmax;
extern int conta;

void setupAnemometer();
void calculateWindSpeed();

#endif