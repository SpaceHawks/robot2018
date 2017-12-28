#include "RMCKangaroo1.h"

RMCKangaroo1::RMCKangaroo1(int txPin, int rxPin)
{
	SoftwareSerial  SerialPort(txPin, rxPin);
	KangarooSerial  K(SerialPort);

	channel1 =new KangarooChannel(K, '1');
	channel2 = new KangarooChannel(K, '2');

	SerialPort.begin(9600);
	SerialPort.listen();

	channel1->start();
	channel2->start();

	//min1 = channel1->getMin().value();
	//max1 = channel1->getMax().value();

	//min2 = channel2->getMin().value();
	//max2 = channel2->getMax().value();

	targetVal1 = 1000;
	speed1 = 500;

	channel1->p(targetVal1, speed1);
}

void RMCKangaroo1::loop()
{
	//if (targetVal1 != lastVal1) {
	//	channel1->p(targetVal1, speed1);
	//	lastVal1 = targetVal1;
	//}

	//status1 = &(channel1->getP());
	//if (status1->done())
	//	channel1->powerDown();
	////{@Plot.Position.SetPosition.Red Pos}, {@Plot.Position.CurrentPosition.Green absP.value()}, Pos is {Pos =?}, Speed is {Speed =?}
}
