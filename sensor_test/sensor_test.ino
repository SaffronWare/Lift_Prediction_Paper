#include "FastIMU.h"
#include <Wire.h>
#include <EEPROM.h>

// This relies on the FastIMU library caught  from https://github.com/LiquidCGS/FastIMU/blob/main/examples/Calibrated_sensor_output/Calibrated_sensor_output.ino

MPU6500 IMU;
AccelData accelData;
GyroData gyroData;
calData calib = { 0 };

void setup()
{
  Wire.begin();
  Wire.setClock(400000);
  Serial.begin(115200);
  while (!Serial)
  {
    ;
  }

  int err = IMU.init(calib, 0x68);
  if (err != 0) {
    Serial.print("Error initializing IMU: ");
    Serial.println(err);
    while (true) {
      ;
    }
  }

  if (err != 0) {
    Serial.print("Error Setting range: ");
    Serial.println(err);
    while (true) {
      ;
    }
  }
}

int i = 0;
void loop()
{
  if (i == 0)
  {
    delay(10000 * 12);
  }
  if ((i+1) * sizeof(float) < 256)
  {
    IMU.update(); 
    IMU.getAccel(&accelData);
    Serial.println("wow\n");
  
    EEPROM.put((i) * sizeof(float), accelData.accelX);

    Serial.println(accelData.accelX);
    Serial.println("wow\n");
  }
  delay(50);
  i+=1;
}