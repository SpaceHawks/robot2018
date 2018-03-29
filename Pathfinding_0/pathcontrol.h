#ifndef PATHCONTROL_H
#define PATHCONTROL_H

#include <QDebug>
#include "grid.h"
#include "pathfinding.h"

class PathControl
{
public:
    PathControl();

    Pathfinding *path;

    bool isBlind; // true = LIDAR can't see bin
    bool hasObstruction; // true = obstacles nearby
    bool isForward; // true = going to dig site

    int numObstacles;

    double dataLIDAR[3]; // x-coordinate, y-coordinate, orientation
    double dataKINECT[50][4]; // x-coordinate of center, y-coordinate of center, radius, crater(<10) or rock(>10)
    double dataDSensors[7]; // distances

    void sendLocation(double a, double b, double c);
    void sendObstacles(int a);
    void sendDSensors(double a, double b, double c, double d, double e, double f, double g);
    void update();
    void execute();

};

#endif // PATHCONTROL_H
