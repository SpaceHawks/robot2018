#include "pathfinding.h"

Pathfinding::Pathfinding()
{
    // initialize variables
    isBlind = true;
    hasObstruction = false;
    isForward = true;
    isSafe = true;
    locRobot[0] = 0.0;
    locRobot[1] = 0.0;
    locRobot[2] = 0.0;
    for(int i=0;i<50;i++){
        for(int j=0;j<4;j++){
            locObstacles[i][j] = 0.0;
        }
    }
    for(int i=0;i<7;i++){
        dSensors[i] = 0.0;
    }
    for(int i=0;i<5;i++){
        for(int j=0;j<20;j++){
            path[i][j][0] = 0.0;
            path[i][j][1] = 0.0;
        }
    }
    pointList = new Grid();
    nodeList = new Grid();
    gapGrid = new Grid();
    nextCoordinates[0] = 0.0;
    nextCoordinates[1] = 0.0;
    pathNum = 0;
    pointNum = 0;
    numObstacles = 0;
}

void Pathfinding::getLocation(double a, double b, double c, bool d)
{
    locRobot[0] = a;
    locRobot[1] = b;
    locRobot[2] = c;
    isBlind = d;
}

void Pathfinding::getObstacles(double a, double b, double c, int d, int e, bool f)
{
    locObstacles[d-1][0] = a;
    locObstacles[d-1][1] = b;
    locObstacles[d-1][2] = c;
    numObstacles = e;
    hasObstruction = f;
}

void Pathfinding::getDSensors(double a, double b, double c, double d, double e, double f, double g)
{
    dSensors[0] = a;
    dSensors[1] = b;
    dSensors[2] = c;
    dSensors[3] = d;
    dSensors[4] = e;
    dSensors[5] = f;
    dSensors[6] = g;
}

void Pathfinding::moveStraight(bool a)
{
    // move straight for 30 cm
}

void Pathfinding::rotate(bool a)
{
    // rotate 5 degrees
}

void Pathfinding::moveSlant()
{
    // move and rotate simultaneously
}

void Pathfinding::moveTo(double x, double y)
{
    // move from present co-ordinates to next
}

void Pathfinding::fixOrientation()
{
    if(isBlind){
        // rotate();
        fixOrientation();
        // if 360 degrees try fail-safe
    }
    else{
        if(locRobot[2] < 177 && locRobot[2] > 183){
          //  rotate();
            fixOrientation();
        }
    }
}

void Pathfinding::landHome(){
    moveSlant(); //  backwards, till y = 0
    fixOrientation();
    moveStraight(false);
    dump();
}

void Pathfinding::goToDig()
{
    // find place to dig
    dig();
}

void Pathfinding::dig()
{
    // dig
    isForward = false;
    pointNum = 0;
    pathNum++;
}

void Pathfinding::dump()
{
    // dump
    isForward = true;
    pointNum = 0;
    pathNum++;
}

void Pathfinding::moveLoop()
{
        if(locRobot[0] < DIST_12 && isForward) // in start area
            moveStraight(true);
        else if(locRobot[0] < DIST_12){
            landHome();
        }
        else if(locRobot[0] > DIST_23 && isForward){ // in mining area
            goToDig();
        }
        else if(locRobot[0] > DIST_23){
            moveStraight(false);
        }
        else{ // in obstacle area
            pathFinder();
        }
}

void Pathfinding::pathFinder()
{
    if(hasObstruction){
        pointList->clear();
        for(int i=0;i<numObstacles;i++){ // creates point list
            for(int j=0;j<4;j++){
               pointList->insert(locObstacles[i][j],pointList->getIndex(),j);
            }
            pointList->incrementIndex();
        }
        getNumNodes(); // adds number of nodes to point list
        nodeMaker(); // creates node list
        gapMaker(); // creates gap grid
        bestFit(); // computes next coordinates
        moveTo(nextCoordinates[0],nextCoordinates[1]);
    }
    else
        moveStraight(isForward);
}

void Pathfinding::getNumNodes()
{
    double x1 = 0.0;
    double x2 = 0.0;
    double y1 = 0.0;
    double y2 = 0.0;
    double temp1 = 0.0;
    double temp2 = 0.0;

    for(int i=0;i<pointList->getIndex();i++){
        pointList->insert(15.0,i,4); // 15 -> 2 nodes (>10)
        for(int j=0;j<pointList->getIndex();j++){
            if(j!=i){
                x1 = pointList->get(i,0);
                x2 = pointList->get(j,0);
                if((x2-x1) < 50 || (x2-x1) > -50){ // 0 or 1 nodes
                    pointList->insert(5.0,i,4); // 5 -> 1 node (>0 & <10)
                    y1 = pointList->get(i,1);
                    y2 = pointList->get(j,1);
                    temp1 = pointList->get(i,5);
                    temp2 = pointList->get(i,6);
                    if(y2>y1)
                        temp2 += 15.0;
                    else
                        temp2 += 15.0;
                    pointList->insert(temp1,i,5);
                    pointList->insert(temp2,i,6);
                }
            }
        }
    }

    for(int i=0;i<pointList->getIndex();i++){
        if(pointList->get(i,4) < 10.0){
            if(pointList->get(i,5) > 10.0 && pointList->get(i,6) > 10.0){ // 0 nodes
                pointList->insert(-5.0,i,4);
                pointList->insert(0.0,i,5);
                pointList->insert(0.0,i,6);
            }
            else if(pointList->get(i,5) < 10.0 && pointList->get(i,6) > 10.0){ // 1 node
                pointList->insert(5.0,i,4);
                pointList->insert(-5.0,i,5);
                pointList->insert(0.0,i,6);
            }
            else if(pointList->get(i,5) > 10.0 && pointList->get(i,6) < 10.0){ // 1 node
                pointList->insert(5.0,i,4);
                pointList->insert(5.0,i,5);
                pointList->insert(0.0,i,6);
            }
            else{
                pointList->insert(15.0,i,4); // 2 nodes
                pointList->insert(0.0,i,5);
                pointList->insert(0.0,i,6);
            }
        }
    }
}

void Pathfinding::nodeMaker()
{
    nodeList->clear();
    for(int i=0;i<pointList->getIndex();i++){
        if(pointList->get(i,4) > 0.0 && pointList->get(i,4) < 10.0){ // 1 node
            if(pointList->get(i,5) > 2.0){
                nodeList->insert(pointList->get(i,0),2*i,0);
                nodeList->insert(0.0,2*i,1); // node at top
            }
            else if(pointList->get(i,5) < -2.0){
                nodeList->insert(pointList->get(i,0),2*i,0);
                nodeList->insert(378.0,2*i,1); // node at bottom
            }
            nodeList->insert(5.0,2*i,2); // radius
        }
        else if (pointList->get(i,4) > 10.0){ // 2 nodes
            nodeList->insert(pointList->get(i,0),2*i,0);
            nodeList->insert(0.0,2*i,1);
            nodeList->insert(pointList->get(i,0),(2*i)+1,0);
            nodeList->insert(378.0,(2*i)+1,1);
            nodeList->insert(5.0,2*i,2);   // radius
            nodeList->insert(5.0,(2*i)+1,2);   // radius
        }
    }
}

void Pathfinding::gapMaker()
{
    double x1 = 0.0;
    double x2 = 0.0;
    double y1 = 0.0;
    double y2 = 0.0;
    double c1 = 0.0;
    double c2 = 0.0;
    double temp = 0.0;

    gapGrid->clear();

    // point-to-point
    for(int i=0;i<pointList->getIndex()-1;i++){
        for(int j=i+1;j<pointList->getIndex();j++){
            x1 = pointList->get(i,0);
            x2 = pointList->get(j,0);
            y1 = pointList->get(i,1);
            y2 = pointList->get(j,1);
            c1 = (x1+x2)/2;
            c2 = (y1+y2)/2;
            temp = qSqrt(qPow(x2-x1,2)+qPow(y2-y1,2))-pointList->get(i,2)-pointList->get(j,2); // width
            gapGrid->insert(temp,gapGrid->getIndex(),0); // width
            gapGrid->insert(c1,gapGrid->getIndex(),1);   // center-x
            gapGrid->insert(c2,gapGrid->getIndex(),2);   // center-y
            temp = qSqrt(qPow(c1-locRobot[0],2)+qPow(c2-locRobot[1],2));
            gapGrid->insert(temp,gapGrid->getIndex(),3); // distance
          /*  if(pointList->get(i,3) < 10 && pointList->get(j,3) < 10)
                gapGrid->insert(5.0,gapGrid->getIndex(),4); // type
            else if((pointList->get(i,3) < 10 && pointList->get(j,3) > 10) || (pointList->get(i,3) > 10 && pointList->get(j,3) < 10))
                gapGrid->insert(15.0,gapGrid->getIndex(),4); // type
            else if(pointList->get(i,3) > 10 && pointList->get(j,3) < 10)
                gapGrid->insert(25.0,gapGrid->getIndex(),4); // type*/
            // 1 more slot for each gap: validity
            gapGrid->incrementIndex();
        }
    }

    // point-to-node
    for(int i=0;i<pointList->getIndex();i++){
        if(pointList->get(i,4) > 0 && pointList->get(i,4) < 10){ // 1 node
                x1 = pointList->get(i,0);
                x2 = nodeList->get(2*i,0);
                y1 = pointList->get(i,1);
                y2 = nodeList->get(2*i,1);
                c1 = (x1+x2)/2;
                c2 = (y1+y2)/2;
                temp = qSqrt(qPow(x2-x1,2)+qPow(y2-y1,2))-pointList->get(i,2);// width
                gapGrid->insert(temp,gapGrid->getIndex(),0); // width
                gapGrid->insert(c1,gapGrid->getIndex(),1);   // center-x
                gapGrid->insert(c2,gapGrid->getIndex(),2);   // center-y
                temp = qSqrt(qPow(c1-locRobot[0],2)+qPow(c2-locRobot[1],2));
                gapGrid->insert(temp,gapGrid->getIndex(),3); // distance
                if(pointList->get(i,3) < 10)
                    gapGrid->insert(35.0,gapGrid->getIndex(),4); // type
                else if(pointList->get(i,3) > 10)
                    gapGrid->insert(45.0,gapGrid->getIndex(),4); // type
                // 1 more slot for each gap: validity
                gapGrid->incrementIndex();
        }
        else if(pointList->get(i,4) > 10){ // 2 nodes
            for(int j=2*i;j<2*(i+1);j++){
                x1 = pointList->get(i,0);
                x2 = nodeList->get(j,0);
                y1 = pointList->get(i,1);
                y2 = nodeList->get(j,1);
                c1 = (x1+x2)/2;
                c2 = (y1+y2)/2;
                temp = qSqrt(qPow(x2-x1,2)+qPow(y2-y1,2))-pointList->get(i,2);// width
                gapGrid->insert(temp,gapGrid->getIndex(),0); // width
                gapGrid->insert(c1,gapGrid->getIndex(),1);   // center-x
                gapGrid->insert(c2,gapGrid->getIndex(),2);   // center-y
                temp = qSqrt(qPow(c1-locRobot[0],2)+qPow(c2-locRobot[1],2));
                gapGrid->insert(temp,gapGrid->getIndex(),3); // distance
                if(pointList->get(i,3) < 10)
                    gapGrid->insert(35.0,gapGrid->getIndex(),4); // type
                else if(pointList->get(i,3) > 10)
                    gapGrid->insert(45.0,gapGrid->getIndex(),4); // type
                // 1 more slot for each gap: validity
                gapGrid->incrementIndex();
            }
        }
    }
}

void Pathfinding::bestFit()
{
    int bestFit = -1;
    double temp = 0.0;
    for(int i=0;i<gapGrid->getIndex();i++){
        if(gapGrid->get(i,3) < SAFE_ZONE){
            if((gapGrid->get(i,2) - locRobot[1]) < (ROBO_RADIUS + 10) && (gapGrid->get(i,2) - locRobot[1]) > -(ROBO_RADIUS + 10))
                isSafe = false;
            break;
        }
        else
            isSafe = true;
    }
    if(isSafe == true)
        moveStraight(isForward);
    else{
        // eliminate unsuitable gaps
        for(int i=0;i<gapGrid->getIndex();i++){
            //eliminate gaps with x coordinates less than robot's
            if(gapGrid->get(i,1) < locRobot[0])
                gapGrid->insert(-10.0,i,5);
            //eliminate gaps with width less than GAP-TOLERANCE
            if(gapGrid->get(i,0) < GAP_TOLERANCE)
                gapGrid->insert(-10.0,i,5);
            //eliminate gaps with unsuitable centers
            for(int j = 0; j<gapGrid->getIndex();j++){
                if(j != i){
                    temp = qSqrt(qPow(gapGrid->get(i,1)-gapGrid->get(j,1),2)+qPow(gapGrid->get(i,2)-gapGrid->get(j,2),2));
                    if(temp < ROBO_RADIUS)
                        gapGrid->insert(-10.0,i,5);
                }
            }
        }
        // select closest gap
        temp = 100000.0;
        for(int i=0;i<gapGrid->getIndex();i++){
            if(gapGrid->get(i,5) > -1){
                if(gapGrid->get(i,0) < temp){
                    temp = gapGrid->get(i,0);
                    bestFit = i;
                }
            }
        }
        if(bestFit == -1){
            // no suitable gap
        }
        else{
            nextCoordinates[0] = gapGrid->get(bestFit,1);
            nextCoordinates[1] = gapGrid->get(bestFit,2);
            path[pathNum][pointNum][0] = nextCoordinates[0];
            path[pathNum][pointNum][1] = nextCoordinates[1];
            pointNum++;
        }
    }
}
