#ifndef PATHFINDING_H
#define PATHFINDING_H

#include <QtMath>
#include "grid.h"

class Pathfinding
{
public:
    Pathfinding();

    const double ROBO_RADIUS = 50.0; // in cms
    const double GAP_TOLERANCE = 125.0; // in cms
    const double SAFE_ZONE = 100.0; // in cms
    const double ROCK_DENSITY = 25.0; // in cms
    const double DIST_12 = 100.0; // in cms
    const double DIST_23 = 396.0; // in cms


    bool isBlind; // true = LIDAR can't see bin
    bool hasObstruction; // true = obstacles nearby
    bool isForward; // true = going to dig site
    bool isSafe; // true = has no obstacles in 50 cm radius (for gaps)

    double locRobot[3]; // x-coordinate, y-coordinate, orientation
    double locObstacles[50][4]; // x-coordinate of center, y-coordinate of center, radius, crater(<10) or rock(>10)
    double dSensors[7];
    double path[5][20][2]; // previous paths travelled (collection of points)

    Grid *pointList;
    Grid *nodeList;
    Grid *gapGrid;
    double nextCoordinates[2]; // x-coordinate, y-coordinate

    int pathNum; // index of path
    int pointNum; // index of point in path
    int numObstacles;

    // input methods
    void getLocation(double a, double b, double c, bool d); // update locRobot[]
    void getObstacles(double a, double b, double c, int d, int e, bool f); // update locObstacles[][]
    void getDSensors(double a, double b, double c, double d, double e, double f, double g); // update dataDSensors[]

    // motor methods
    void moveStraight(bool a); // move straight for 30 cm
    void rotate(bool a); // rotate 5 degrees
         // fix this
    void moveSlant(); // move and rotate simultaneously
    void moveTo(double x, double y); // move from present co-ordinates to next

    // task-specifivation methods
    void fixOrientation(); // make robot face forward
    void landHome(); // bring robot to the bin
    void goToDig(); // take robot to dig site
    void dig(); // dig
    void dump(); // dump

    // pathfinding functions
    void moveLoop(); // controls all robot movements
    void pathFinder(); // creates point list and implements pathfinding
    void getNumNodes(); // computes number of nodes for each point
    void nodeMaker(); // creates node list
    void gapMaker(); // creates gap grid
    void bestFit(); // returns co-ordinates of center of best suited gap

};

#endif // PATHFINDING_H
