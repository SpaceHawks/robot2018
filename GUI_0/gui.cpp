#include "gui.h"
#include "ui_gui.h"

// Input from LIDAR: (dist_A, dist_B, alpha, beta, robot_Theta)

GUI::GUI(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::GUI)
{
    ui->setupUi(this);

    scene = new QGraphicsScene(this);
    ui->graphicsView->setScene(scene);

    bin = new Zone(45.7,157.5, "bin");
    startArea = new Zone(150.0,378.0, "start_area");
    obstacleArea = new Zone(294.0,378.0, "obstacle_area");
    miningArea = new Zone(294.0,378.0, "mining_area");
    robot = new Robot(90.0, 75.0);
    cursor = new NavigationPointer();

    scene->addItem(bin);
    scene->addItem(startArea);
    scene->addItem(obstacleArea);
    scene->addItem(miningArea);
    scene->addItem(robot);
    scene->addItem(cursor);

    bin->setPos(0.0,110.25);
    startArea->setPos(45.7,0.0);
    obstacleArea->setPos(195.7,0.0);
    miningArea->setPos(489.7, 0.0);
    cursor->setPos(10,10);

    {
        dist_A = 157.5;
        dist_B = 157.5;
        alpha = 30.0;
        beta = -30.0;
        robot_Theta = 0.0;

        fixAlignment();
        triangulate();
        robot->setRotation(robot_Theta);
        fixRotation();
        robot->setPos(robot_X,robot_Y);
        graphicsText();
        placeObstacles(35,340,200);
       // placeScatterPoints();
        getData();
    }

}

GUI::~GUI()
{
    delete ui;
}

GUI::triangulate(){
    lambda = dist_A * qCos(qDegreesToRadians(alpha));
    robot_X = 45.7 + lambda;

    if(alpha <= 0 && beta < 0){
        robot_Y = 72.75 - (dist_A * sin(qDegreesToRadians(alpha * (-1.0))));
    }
    else if(beta >= 0 && alpha > 0){
        robot_Y = 230.25 + (dist_B * sin(qDegreesToRadians(beta)));
    }
    else if(alpha > 0 && beta < 0){
       robot_Y = 72.75 + (dist_A * sin(qDegreesToRadians(alpha)));
    }
    return 1;
}

GUI::fixAlignment(){
    alpha -= robot_Theta;
    beta -= robot_Theta;
    return 1;
}

GUI::fixRotation(){
    if(robot_Theta > 0){
        robot_X += (37.5 * qSin(qDegreesToRadians(robot_Theta)));
    }
    else if(robot_Theta < 0){
        robot_X += (37.5 * qSin(qDegreesToRadians(robot_Theta)));
    }
    robot_Y += (37.5 * (1 - qCos(qDegreesToRadians(robot_Theta))));
    return 1;
}


GUI::stayInArena(){
    if(robot->x() < 45.7){
      robot->setPos(400,robot->y());
    }
    else if(robot->x() > 783.7){
        robot->setPos(783.7,robot->y());
    }
    else if(robot->y() < 0.0){
        robot->setPos(robot->x(),0.0);
    }
    else if(robot->y() > 378.0){
        robot->setPos(robot->x(), 378.0);
    }
    return 1;
}

GUI::graphicsText(){
    if(robot->x() > 45.7 && robot->x() < 195.7){
        ui->graphicsText->setText("Robot in Start Area");
    }
    else if(robot->x() > 195.7 && robot->x() < 489.7){
        ui->graphicsText->setText("Robot in Obstacle Area");
    }
    else if(robot->x() > 489.7){
        ui->graphicsText->setText("Robot in Mining Area");
    }
    return 1;
}

GUI::placeObstacles(qreal r, qreal x, qreal y){
    rock = new Obstacle(r,x,y);
    crater = new Obstacle((r+15),(x+60),(y-140));

    scene->addItem(rock);
    scene->addItem(crater);
}

GUI::placeScatterPoints(){
    for(int i = 1; i < 20; i++){
        for(int j = 0; j < 360; j++){
            point = new ScatterPoints(600+5*i*qCos(qDegreesToRadians(float(j))),200+5*i*qSin(qDegreesToRadians(float(j))));
            scene->addItem(point);
        }
    }
    return 1;
}

GUI::getData(){
    frontLeftMotorSpeed = 50.2;
    frontRightMotorSpeed = 50.1;
    rearLeftMotorSpeed = 50.2;
    rearRightMotorSpeed = 50.1;
    accelX = 0.78;
    accelY = 0.5;
    accelZ = 1.4;
    gyroXY = 0.3;
    gyroYZ = 0.1;
    gyroXZ = 0.2;
    conveyorSpeed = 12.45;
    drillDepth = 2.65;
    timeLeftMinutes = 3;
    timeLeftSeconds = 45;
    ui->robotData->setPlainText("<<Current Task>>\n------Digging-------\n\n<<Motor Readings>>\nFront Left Motor Speed:\t"+QString::number(frontLeftMotorSpeed)+"\nFront Right Motor Speed:\t"+QString::number(frontRightMotorSpeed)+"\nRear Left Motor Speed:\t"+QString::number(rearLeftMotorSpeed)+"\nRear Right Motor Speed:\t"+QString::number(rearRightMotorSpeed)+"\n\n<<Accelerometer Readings>>\nX-axis:\t"+QString::number(accelX)+"\nY-axis\t"+QString::number(accelY)+"\nZ-axis:\t"+QString::number(accelZ)+"\n\n<<Gyroscope Readings>>\nXY plane:\t"+QString::number(gyroXY)+"\nYZ plane:\t"+QString::number(gyroYZ)+"\nXZ plane:\t"+QString::number(gyroXZ)+"\n\n<<Miscellaneous Readings>>\nConveyor Belt Speed:\t"+QString::number(conveyorSpeed)+"\nDrill Depth:\t\t"+QString::number(drillDepth)+"\n\n<<Time Left>>\n"+QString::number(timeLeftMinutes)+" mins. "+QString::number(timeLeftSeconds)+" secs.");
    return 1;
}

GUI::sendLocation(){
    x = cursor->scenePos().x() + 10;
    y = cursor->scenePos().y() + 10;
    ui->a->setPlainText(QString::number(x));
    ui->b->setPlainText(QString::number(y));
    return 1;
}

void GUI::on_pushButton_3_clicked()
{
    sendLocation();
}
