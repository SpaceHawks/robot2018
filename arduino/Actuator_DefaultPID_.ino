#include <SoftwareSerial.h>
#include <Kangaroo.h>
#define TX_PIN 11
#define RX_PIN 10

// Independent mode channels on Kangaroo are, by default, '1' and '2'.
SoftwareSerial  SerialPort(RX_PIN, TX_PIN);
KangarooSerial  K(SerialPort);
KangarooChannel K1(K, '1');
KangarooChannel K2(K, '2');
KangarooStatus absP;
int Pos = 200;
long maximum;
long minimum;

void aSetup()
{
	SerialPort.begin(9600);
	SerialPort.listen();

	K1.start();
	K1.home().wait();
//	Serial.begin(9600);

}

void aLoop()
{
//	minimum = K1.getMin().value();
//	maximum = K1.getMax().value();
	K1.p(Pos).wait();
//	K1.p(Pos, 30).wait();
//	int position = digitalRead(A0);
//	Serial.println(absP);
	absP = K1.getP();
	Serial.println(absP.value());
	delay(500);
		
	//{@Plot.Position.SetPosition.Red Pos}, {@Plot.Position.CurrentPosition.Green absP.value()}, Pos is {Pos =?}
}