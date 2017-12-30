#ifndef NAV_H
#define NAV_H

#include <QMainWindow>
#include <QtCore>
#include <QtGui>
#include <QtWidgets>
#include "robot.h"
#include "zone.h"
#include "lidar/include/rplidar.h"

#define ARENA_HEIGHT 738 //centimeters
#define ARENA_WIDTH 378 //centimeters
#define DUMP_AREA_HEIGHT 150 //centimeters
#define OBSTACLE_FIELD_HEIGHT 294 //centimeters
#define DIG_AREA_HEIGHT 294 //centimeters
#define COLLECTION_BIN_HEIGHT 45.7 //centimeters
#define COLLECTION_BIN_WIDTH 157.5 //centimeters
#define ROBOT_WIDTH 75 //centimeters
#define ROBOT_HEIGHT 90 //centimeters

#include <stdio.h>
#include <stdlib.h>
#ifndef _countof
#define _countof(_Array) (int)(sizeof(_Array) / sizeof(_Array[0]))
#endif

#ifdef _WIN32
#include <Windows.h>
#define delay(x)   ::Sleep(x)
#else
#include <unistd.h>
static inline void delay(_word_size_t ms){
    while (ms>=1000){
        usleep(1000*1000);
        ms-=1000;
    };
    if (ms!=0)
        usleep(ms*1000);
}
#endif
using namespace rp::standalone::rplidar;

namespace Ui {
class nav;
}

class nav : public QMainWindow
{
    Q_OBJECT

public:
    explicit nav(QWidget *parent = 0);
    ~nav();

private:
    Ui::nav *ui;
    QGraphicsScene *scene;
    Robot *robot;
    Zone *bin;
    Zone *dumpArea;
    Zone *obstacleField;
    Zone *digArea;
    void initLidar();
};

#endif // NAV_H
