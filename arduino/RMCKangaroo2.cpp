#include "RMCKangaroo2.h"


RMCKangaroo1::RMCKangaroo1(int rxPin, int txPin, String channelList, String channelType)
{
	this->channelList = channelList;
	this->channelType = channelType;
	SerialPort = new SoftwareSerial(rxPin, txPin);
	K = new KangarooSerial(*SerialPort);
	
	for (int i = 0; i < channelList.length(); i++) {
		channel[i] = new LinearActuatorPair(*K, channelList[i]);
		channelIndex[(int)(channelList[i]-49)] = i; //if channel is 1, index is 0
	}
}

void RMCKangaroo1::loop()
{
	channel[0]->loop();
	//for (int i = 0; i < 1; i++) {
	//	int tempTargetVal = targetVal[i];
	//	int tempLASpeed = linearActuatorSpeed[i];
	//	if (channelType[i] == 'l')
	//	{
	//		
	//		//if ((tempTargetVal >= min[i] && tempTargetVal <= max[i]) && (tempTargetVal != lastVal[i] || tempLASpeed != lastSpeed[i])) {
	//		//	channel[i]->p(tempTargetVal, tempLASpeed);
	//		//	lastVal[i] = tempTargetVal;
	//		//	lastSpeed[i] = tempLASpeed;
	//		//}

	//		//status[i] = channel[i]->getP();
	//		//if (status[i].done()) {
	//		//	channel[i]->powerDown();
	//		//}
	//	}
	//	else if (channelType[i] == 'm') {

	//		//if (tempTargetVal != lastVal[i]) {
	//		//	channel[i]->s(tempTargetVal);
	//		//	delay(10);
	//		//	lastVal[i] = tempTargetVal;
	//		//}

	//		//status[i] = channel[i]->getS();
	//	}

	//}

}

void RMCKangaroo1::begin() {
	SerialPort->begin(9600);
	SerialPort->listen();
	
	for(int i=0; i< channelList.length(); i++)
		channel[i]->begin();

	for (int i = 0; i < channelList.length(); i++) {
		if (channelType[i] == 'l') {
		}
		else if (channelType[i] == 'm') {
			/*long absMin = channel[i]->getMin().value();
			long absMax = channel[i]->getMax().value();
			long safeBound = (absMax - absMin)*0.02;
			min[i] = (absMin + safeBound);
			max[i] = absMax - safeBound;
			maxSpeed[i] = 0.1 * (absMax - absMin);*/
			//setSpeed((int)(channelList[i] - 48), 50);
		}
	}
}

void RMCKangaroo1::setTargetVal(int channelName, long val) { //val = 0% to 100%
	//int index = getChannelIndex(channelName);
	
	//channel[0]->setTargetVal(val);
	//channel[1]->setTargetVal(val);
	//channel[index]->setTargetVal(val);

	//if (val >= 0 && val <= 100) {
	//	targetVal1 = map(val, 0, 100, channel[0]->min, channel[0]->max);
	//}
	channel[0]->setTargetPos(val);
}

LinearActuator::LinearActuator(KangarooSerial& K, char name):KangarooChannel(K, name)
{
}
void LinearActuator::begin() {

	start();
	getExtremes();
}
void LinearActuator::loop()
{
	if ((targetVal >= min && targetVal <= max) && (targetVal != lastVal || speed != lastSpeed)) {
		p(targetVal, speed);
		lastVal = targetVal;
		lastSpeed = speed;
	}

	status = getP();
	if (status.done()) {
		powerDown();
	}
}
void LinearActuator::getExtremes()
{
		long absMin = getMin().value();
		long absMax = getMax().value();
		long safeBound = (absMax - absMin)*0.02;
		min = (absMin + safeBound);
		max = absMax - safeBound;
		maxSpeed = 0.1 * (absMax - absMin);
}
void LinearActuator::setTargetVal(long pos, long newSpeed) { //val = 0% to 100%
	setTargetPos(pos);
	setSpeed(newSpeed);
}
void LinearActuator::setTargetPos(long pos) { //val = 0% to 100%
	if (pos >= 0 && pos <= 100) {
		targetVal = map(pos, 0, 100, min, max);
	}
}
void LinearActuator::setSpeed(long newSpeed) { //val = 0% to 100%
	if (newSpeed >= 0 && speed <= maxSpeed) {
		lastSpeed = newSpeed;
		speed = map(newSpeed, 0, 100, 1, maxSpeed);
	}
}
long LinearActuator::getCurrentVal()
{
	return status.value();
}


LinearActuatorPair::LinearActuatorPair(KangarooSerial & K, char name)
{
	channel[0] = new LinearActuator(K, name);
	channel[1] = new LinearActuator(K, name+1);
}
long * LinearActuatorPair::getCurrentVal()
{
	return nullptr;
}
void LinearActuatorPair::setTargetVal(long pos, long newSpeed)
{
	Serial.println("LAPair setTargetVal is empty.");

}
void LinearActuatorPair::setSpeed(long newSpeed)
{
	if (newSpeed != lastSpeed && newSpeed >= 0 && newSpeed <= 100)
	{
		channel[0]->setSpeed(newSpeed);
		channel[1]->setSpeed(newSpeed);
		lastSpeed = newSpeed;
	}
}
void LinearActuatorPair::setTargetPos(long pos)
{
	targetVal = pos;
}
void LinearActuatorPair::loop()
{
	long tempTargetVal = targetVal;
	channel[0]->setTargetPos(tempTargetVal);
	channel[1]->setTargetPos(tempTargetVal);
	channel[0]->loop();
	channel[1]->loop();
	sync();
}
void LinearActuatorPair::begin()
{
	channel[0]->begin();
	channel[1]->begin();
}

void LinearActuatorPair::sync()
{
	long la1 = targetVal - map(channel[0]->getP().value(), channel[0]->min, channel[0]->max, 0, 100);
	long la2 = targetVal - map(channel[1]->getP().value(), channel[1]->min, channel[1]->max, 0, 100);
	long gap = la1 - la2;
	Serial.println(gap);
	while (abs(gap) > 3)
	{
		if (la1 > la2)
			channel[0]->powerDown();
		if (la1 < la2)
			channel[1]->powerDown();

	}	
}
