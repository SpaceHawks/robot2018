#include "pathcontrol.h"

PathControl::PathControl()
{
    isBlind = true;
    hasObstruction = false;
    isForward = true;
    numObstacles = 0;
    for(int i=0;i<5;i++){
            dataLIDAR[i] = 0.0;
        }
    for(int i=0;i<50;i++){
        for(int j=0;j<4;j++){
                dataKINECT[i][j] = 0.0;
        }
    }
    for(int i=0;i<7;i++){
        dataDSensors[i] = 0.0;
    }

    path = new Pathfinding();
    path->pointList->display();
}

void PathControl::sendLocation(double a, double b, double c)
{
    path->getLocation(a,b,c,isBlind);
}

void PathControl::sendObstacles(int a)
{
    for(int i=a;i>0;i--){
        path->getObstacles(dataKINECT[i-1][0],dataKINECT[i-1][1],dataKINECT[i-1][2],i,a,hasObstruction);
    }
}

void PathControl::sendDSensors(double a, double b, double c, double d, double e, double f, double g)
{
    path->getDSensors(a,b,c,d,e,f,g);
}

void PathControl::update()
{
    // give new values for robot & obstacles locations
}

void PathControl::execute() // 1 lap of the arena
{
    sendLocation(dataLIDAR[0],dataLIDAR[1],dataLIDAR[2]);
    path->fixOrientation();
    update();
    sendLocation(dataLIDAR[0],dataLIDAR[1],dataLIDAR[2]);
    sendObstacles(numObstacles);
    sendDSensors(dataDSensors[0],dataDSensors[1],dataDSensors[2],dataDSensors[3],dataDSensors[4],dataDSensors[5],dataDSensors[6]);
    while(isForward == true){
        path->moveLoop();
        update();
    }
    while(isForward == false){
        path->moveLoop();
        update();
    }
}
