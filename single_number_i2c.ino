#include <Wire.h>

#define SLAVE_ADDRESS 0x04
int number = 0;

void setup() {
Serial.begin(9600);
Wire.begin(SLAVE_ADDRESS);
// define callbacks for i2c communication
Wire.onReceive(receiveData);
Wire.onRequest(sendData);

Serial.println("Ready!");
}

void loop() {
delay(100);
}

// callback for received data
void receiveData(int byteCount){

while(Wire.available()) {
number = Wire.read();
Serial.print("data received: ");
Serial.println(number);

}
}

// callback for sending data
void sendData(){
Wire.write(number);
}
