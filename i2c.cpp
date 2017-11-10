#include <Wire.h>
/*
RPI               Arduino Uno		Arduino Mega
--------------------------------------------
GPIO 2 (SDA) <--> Pin A4 (SDA)		Pin 20 (SDA)	Green
GPIO 3 (SCL) <--> Pin A5 (SCL)		Pin 21 (SCL)	Yellow
Ground       <--> Ground			Ground			Black
*/

//queue variable
//I2CAddress variable
//"talk now" pin number variable
void setup()
{
	I2CSetup();
}

void loop()
{
	I2CLoop();
}

void I2CSetup()
{
	Wire.begin(I2CAddress);
	Wire.onReceive(onI2CReceive);
}
void I2CLoop() {
	
}

void onI2CReceive(int byteCount) {
}

void i2cSend()
{
	
}
