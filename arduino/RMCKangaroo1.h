#pragma once
#include <SoftwareSerial.h>
#include <Kangaroo.h>
#define DEFAULT_NUMBER_OF_CHANNEL 10
class RMCKangaroo1
{
protected:
	long targetVal[DEFAULT_NUMBER_OF_CHANNEL];
	long lastVal[DEFAULT_NUMBER_OF_CHANNEL];
	
	//Only for Linear Actuator
	int linearActuatorSpeed[DEFAULT_NUMBER_OF_CHANNEL];
	int maxSpeed[DEFAULT_NUMBER_OF_CHANNEL];
	int lastSpeed[DEFAULT_NUMBER_OF_CHANNEL];
	int channelIndex[DEFAULT_NUMBER_OF_CHANNEL];
	KangarooChannel* channel[DEFAULT_NUMBER_OF_CHANNEL];
	SoftwareSerial* SerialPort;
	KangarooSerial* K;
	String channelList;
	String channelType;

public:
	long max[DEFAULT_NUMBER_OF_CHANNEL];
	long min[DEFAULT_NUMBER_OF_CHANNEL];
	RMCKangaroo1(int rxPin, int txPin, String channelList, String channelType);
	void loop();

	void begin();
	void setTargetPos(int channelName, long val);
	void setTargetSpeed(int channelName, long val);
	void setSpeed(int channelName, long speed);

	int getChannelIndex(int channelName);
	KangarooStatus status[DEFAULT_NUMBER_OF_CHANNEL];
	
};

