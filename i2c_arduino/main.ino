#include <Wire.h>

#define SLAVE_ADDRESS 0x04
int numArray1[5] = { 0,0,0,0,0 };
int numArray2[5] = { 5,4,3,2,1 };
int number = 0;

void setup() {
	Serial.begin(9600);
	Wire.begin(SLAVE_ADDRESS);
	// define callbacks for i2c communication
	Wire.onReceive(receiveSingleByte);
	Wire.onRequest(sendSingleByte);
	Serial.println("Ready!");
}

void loop() {
	delay(100);
}

// callback for received data
void receiveSingleByte(int byteCount) {
	while (Wire.available()) {
		number = Wire.read();
		Serial.print("data received: ");
		Serial.println(number);
	}
}

// callback for received data
void receiveMulBytes(int byteCount) {
	for (int i = 0; i<5; i++) {
		while (Wire.available()) {
			numArray1[i] = Wire.read();
			Serial.print("data received: ");
			Serial.println(numArray1[i]);
		}
	}
}

// callback for sending data
void sendSingleByte() {
	Wire.write(number);
}

void sendMulBytes() {
	for (int j = 0; j < 5; j++) {
		Wire.write(numArray2[j]);
		Serial.print(numArray2[j]);
	}
}
