// Timer.h

#ifndef _TIMER_h
#define _TIMER_h

#if defined(ARDUINO) && ARDUINO >= 100
#include "arduino.h"
#else
#include "WProgram.h"
#endif

class Timer
{
protected:
public:
	void init();
	void reset();
	long getTime();
	long baseTime;
	Timer();
};
#endif