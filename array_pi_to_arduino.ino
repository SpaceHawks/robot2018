#include <Wire.h>

#define SLAVE_ADDRESS 0x04
int number[5] = {0,0,0,0,0};
int number_2[5]={5,4,3,2,1};

void setup() {
Serial.begin(9600); // start serial for output
// initialize i2c as slave
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
for(int i=0;i<5;i++){
while(Wire.available()) {
number[i] = Wire.read();
Serial.print("data received: ");
Serial.println(number[i]);
}
}
}

// callback for sending data
void sendData(){
for(int j=0;j<5;j++)

Wire.write(number_2[j]);
Serial.print(number_2[j]);
}
}
