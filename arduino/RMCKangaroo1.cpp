#include "RMCKangaroo1.h"

RMCKangaroo1::RMCKangaroo1(int txPin, int rxPin)
{
	SoftwareSerial  SerialPort(txPin, rxPin);
	KangarooSerial  K(SerialPort);

	KangarooChannel K1(K, '1');
	KangarooChannel K2(K, '2');

	SerialPort.begin(9600);
	SerialPort.listen();

	K1.start();
	K2.start();

	min1 = K1.getMin().value();
	max1 = K1.getMax().value();

	min2 = K2.getMin().value();
	max2 = K2.getMax().value();
	targetVal1 = 1000;
	speed1 = 500;
	K1.p(targetVal1, speed1);
}

void RMCKangaroo1::loop()
{
	if (targetVal1 != lastVal1) {
		K1.p(targetVal1, speed1);
		lastVal1 = targetVal1;
	}
	status1 = K1.getP();
	if (status1.done())
		K1.powerDown();
	////{@Plot.Position.SetPosition.Red Pos}, {@Plot.Position.CurrentPosition.Green absP.value()}, Pos is {Pos =?}, Speed is {Speed =?}
}
