//#include "Sabertooth.ino"
void setup() {

	//motorSetup();
	//kSetup();
	pinMode(4, OUTPUT);
	digitalWrite(4, HIGH);
	Serial.begin(9600);
	aSetup();
	i2cSetup();

}
void loop() {
	//motorLoop();
	//kLoop();
	digitalWrite(4, LOW);
	aLoop();
	digitalWrite(4, HIGH);
	delay(100);
	//Serial.println("Hello");
}

