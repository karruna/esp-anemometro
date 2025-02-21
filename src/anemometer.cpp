#include "anemometer.h"
#include "config.h"

float vmin = 70.0, vmed = 0.0, vmax = 0.0;
int conta = 0;
long tempoa = millis();
long tempob = 0;

void IRAM_ATTR isr() {
  tempob = millis() - tempoa;
  tempoa = millis();
  float rpm = 60000.0 / tempob;
  float vento = ((4 * 3.14159265 * 147 * rpm) / 60) / 1000;

  if (vento < vmin) vmin = vento;
  if (vento > vmax) vmax = vento;
  conta++;
}

void setupAnemometer() {
  pinMode(giro, INPUT_PULLUP);
  attachInterrupt(giro, isr, FALLING);
}

void calculateWindSpeed() {
  vmed = ((4 * 3.14159265 * 147 * conta) / 60) / 1000;
  conta = 0;
}