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
	int speed1 = 500;
	int speed2 = 500;
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
	void begin();
	void setTargetVal1(long val);
	void setTargetVal2(long val);
	KangarooStatus *status1;
	KangarooStatus *status2;
};

