#ifndef GUI_H
#define GUI_H

#include <QMainWindow>
#include <QtCore>
#include <QtGui>
#include <QtWidgets>
#include <QtMath>
#include <cstdlib>
#include "robot.h"
#include "zone.h"
#include "obstacle.h"
#include "scatterpoints.h"
#include "navigationpointer.h"

namespace Ui {
class GUI;
}

class GUI : public QMainWindow
{
    Q_OBJECT

public:
    explicit GUI(QWidget *parent = 0);
    ~GUI();

private slots:
    void on_pushButton_3_clicked();

private:
    Ui::GUI *ui;

    QGraphicsScene *scene;
    QGraphicsTextItem *text;
    Zone *bin;
    Zone *startArea;
    Zone *obstacleArea;
    Zone *miningArea;
    Robot *robot;
    Obstacle *rock;
    Obstacle *crater;
    ScatterPoints *point;
    NavigationPointer *cursor;

    double dist_A;
    double dist_B;
    double alpha;
    double beta;
    double lambda;

    double robot_X;
    double robot_Y;
    double robot_Theta;

    int x;
    int y;
    double frontLeftMotorSpeed;
    double frontRightMotorSpeed;
    double rearLeftMotorSpeed;
    double rearRightMotorSpeed;
    double accelX;
    double accelY;
    double accelZ;
    double gyroXY;
    double gyroYZ;
    double gyroXZ;
    double conveyorSpeed;
    double drillDepth;
    int timeLeftMinutes;
    int timeLeftSeconds;


    int triangulate();
    int fixAlignment();
    int fixRotation();
    int stayInArena();
    int graphicsText();
    int placeObstacles(qreal r, qreal x, qreal y);
    int placeScatterPoints();
    int getData();
    int sendLocation();
};

#endif // GUI_H
