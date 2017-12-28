// 
// 
// 

#include "RMCKangaroo.h"

void RMCKangaroo::init()
{


}

RMCKangaroo::RMCKangaroo(txPin, rxPin)
{
	SoftwareSerial  SerialPort(txPin, rxPin);
	KangarooSerial  K(SerialPort);

	K1 = KangarooChannel(K, '1');
	K2 = KangarooChannel(K, '2');

	KangarooStatus currentVal1;
	KangarooStatus currentVal2;

	SerialPort.begin(9600);
	SerialPort.listen();

	K1.start();
	K2.start();

	min1 = K1.getMin().value();
	max1 = K1.getMax().value();

	min2 = K2.getMin().value();
	max2 = K2.getMax().value();

}

void RMCKangaroo::loop()
{
	if (targetVal1 != lastVal1) {
		K1.p(targetVal1, speed1);
		lastVal1 = targetVal1;
	}
	status1 = K1.getP();
	if (status1->done())
		K1.powerDown();
	//{@Plot.Position.SetPosition.Red Pos}, {@Plot.Position.CurrentPosition.Green absP.value()}, Pos is {Pos =?}, Speed is {Speed =?}
}
