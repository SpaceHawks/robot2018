#include "RMCKangaroo1.h"

RMCKangaroo1::RMCKangaroo1(int rxPin, int txPin, String channelList, String channelType)
{
	this->channelList = channelList;
	this->channelType = channelType;
	SerialPort = new SoftwareSerial(rxPin, txPin);
	K = new KangarooSerial(*SerialPort);
	
	for (int i = 0; i < channelList.length(); i++) {
		channel[i] = new KangarooChannel(*K, channelList[i]);
		channelIndex[(int)(channelList[i]-49)] = i; //if channel is 1, index is 0
	}
}

void RMCKangaroo1::loop()
{
	for (int i = 0; i < channelList.length(); i++) {
		if (channelType[i] == 'l') {		
			if (targetVal[i] != lastVal[i] || linearActuatorSpeed[i] != lastSpeed[i]) {
				channel[i]->p(targetVal[i], linearActuatorSpeed[i]);
				lastVal[i] = targetVal[i];
				lastSpeed[i] = linearActuatorSpeed[i];
			}

			status[i] = channel[i]->getP();
			if (status[i].done())
				channel[i]->powerDown();
		}

		else if (channelType[i] == 'm') {

			if (targetVal[i] != lastVal[i]) {
				channel[i]->s(targetVal[i]);
				lastVal[i] = targetVal[i];
			}

			status[i] = channel[i]->getS();
		}

	}

}

void RMCKangaroo1::begin() {
	SerialPort->begin(9600);
	SerialPort->listen();
	
	for(int i=0; i< channelList.length(); i++)
		channel[i]->start();

	for (int i = 0; i < channelList.length(); i++) {
		if (channelType[i] == 'l') {
			long absMin = channel[i]->getMin().value();
			long absMax = channel[i]->getMax().value();
			long safeBound = (absMax - absMin)*0.02;
			min[i] = (absMin + safeBound);
			max[i] = absMax - safeBound;
			maxSpeed[i] = 0.1 * (absMax - absMin);
			setSpeed((int)(channelList[i] -48), 50);
		}
	}
}

void RMCKangaroo1::setTargetPos(int channelName, long val) {
	int index = getChannelIndex(channelName);
	if (val >= min[index] && val <= max[index]) {
		targetVal[index] = val;
		
	}
}

void RMCKangaroo1::setTargetSpeed(int channelName, long val) {
	int index = getChannelIndex(channelName);
	targetVal[index] = val;

}

void RMCKangaroo1::setSpeed(int channelName, long speed) //speed:0-100%
{
	int index = getChannelIndex(channelName);
	if (speed >= 0 && speed <= maxSpeed[index]) {
		lastSpeed[index] = speed;
		linearActuatorSpeed[index] = map(speed, 0, 100, 1, maxSpeed[index]);
	}
}

int RMCKangaroo1::getChannelIndex(int channelName) {
	
	return channelIndex[channelName-1];
}