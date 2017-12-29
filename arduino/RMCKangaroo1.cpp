#include "RMCKangaroo1.h"

RMCKangaroo1::RMCKangaroo1(int rxPin, int txPin)
{
	SerialPort = new SoftwareSerial(rxPin, txPin);
	K = new KangarooSerial(*SerialPort);
	channel1 = new KangarooChannel(*K, '1');
	channel2 = new KangarooChannel(*K, '2');

	
}

void RMCKangaroo1::loopP()
{
	if (targetVal1 != lastVal1 || speed1 != lastSpeed1) {
		channel1->p(targetVal1, speed1);
		lastVal1 = targetVal1;
	}

	if (targetVal2 != lastVal2 || speed2 != lastSpeed2) {
		channel2->p(targetVal2, speed2);
		lastVal2 = targetVal2;
	}

	status1 = &channel1->getP();
//	status2 = &channel2->getP();
	//We need sensor for channel 2

	if (status1->done())
		channel1->powerDown();
	/*if (status2->done())
		channel2->powerDown();*/
	//{@Plot.Position.SetPosition.Red Pos}, {@Plot.Position.CurrentPosition.Green absP.value()}, Pos is {Pos =?}, Speed is {Speed =?}
}

void RMCKangaroo1::begin() {
	SerialPort->begin(9600);
	SerialPort->listen();
	channel1->start();
	channel2->start();

	long absMin1 = channel1->getMin().value();
	long absMax1 = channel1->getMax().value();
	long safeBound1 = (absMax1 - absMin1)*0.02;
	min1 = absMin1 + safeBound1;
	max1 = absMax1 - safeBound1;

	long absMin2 = channel2->getMin().value();
	long absMax2 = channel2->getMax().value();
	long safeBound2 = (absMax2 - absMin2)*0.02;
	min2 = absMin2 + safeBound2;
	max2 = absMax2 - safeBound2;
	setTargetVal1(min1);
	setTargetVal2(min2);
	maxSpeed1 = 0.1 * (absMax1 - absMin1);
	maxSpeed2 = 0.1 * (absMax2 - absMin2);
	speed1 = maxSpeed1 / 2;
	speed2 = maxSpeed2 / 2;

}

void RMCKangaroo1::setTargetVal1(long val) {
	if (val >= min1 && val <= max1)
		targetVal1 = val;

}

void RMCKangaroo1::setTargetVal2(long val) {
	if (val >= min2 && val <= max2)
		targetVal2 = val;

}

void RMCKangaroo1::setSpeed1(long speed)
{
	if (speed >= 0 && speed <= maxSpeed1) {
		lastSpeed1 = speed1;
		speed1 = map(speed, 0, 100, 1, maxSpeed1);
	}
}

void RMCKangaroo1::setSpeed2(long speed)
{
	
	if (speed >= 0 && speed <= maxSpeed2) {
		lastSpeed2 = speed2;
		speed2 = map(speed, 0, 100, 1, maxSpeed2);
	}
}
