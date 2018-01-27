// 
// 
// 

#include "Timer.h"
Timer::Timer()
{
	init();
}
void Timer::init()
{
	baseTime = millis();
}
void Timer::reset()
{
	baseTime = millis();
}
long Timer::getTime()
{
	return millis() - baseTime;
}