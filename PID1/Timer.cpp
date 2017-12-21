// 
// 
// 

#include "Timer.h"
TimerClass::TimerClass()
{
	init();
}
void TimerClass::init()
{
	baseTime = millis();
}
void TimerClass::reset()
{
	baseTime = millis();
}
long TimerClass::getTime()
{
	return millis() - baseTime;
}
TimerClass Timer;