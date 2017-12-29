#pragma once
#include <SoftwareSerial.h>
#include <Kangaroo.h>

class RMCKangaroo1
{
protected:
	long targetVal1;
	long targetVal2;
	long lastVal1;
	long lastVal2;

	//Only for Linear Actuator
	int speed1 = 1;
	int speed2 = 1;
	int maxSpeed1;
	int maxSpeed2;
	int lastSpeed1;
	int lastSpeed2;

	KangarooChannel *channel1;
	KangarooChannel *channel2;
	SoftwareSerial *SerialPort;
	KangarooSerial  *K;

public:
	long max1;
	long min1;
	long max2;
	long min2;
	RMCKangaroo1(int rxPin, int txPin);
	void loopP();
	void loopS();
	void begin();
	void setTargetVal1(long val);
	void setTargetVal2(long val);
	void setSpeed1(long speed);
	void setSpeed2(long speed);
	KangarooStatus *status1;
	KangarooStatus *status2;
};

