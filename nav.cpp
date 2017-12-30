#include "nav.h"
#include "ui_nav.h"


nav::nav(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::nav)
{
    ui->setupUi(this);
    scene = new QGraphicsScene(this);
   // scene->setSceneRect(-arenaWidth/2,arenaHeight/2,arenaWidth,arenaHeight);
    scene->setSceneRect(0,0,ARENA_WIDTH,ARENA_HEIGHT);
    ui->graphicsView->setScene(scene);
    QPen wallPen = QPen(Qt::red);

    QLineF lineTop = QLineF(scene->sceneRect().topLeft(),scene->sceneRect().topRight());
    QLineF lineBottom = QLineF(scene->sceneRect().bottomLeft(),scene->sceneRect().bottomRight());
    QLineF lineLeft = QLineF(scene->sceneRect().topLeft(),scene->sceneRect().bottomLeft());
    QLineF lineRight = QLineF(scene->sceneRect().topRight(),scene->sceneRect().bottomRight());

    scene->addLine(lineTop, wallPen);
    scene->addLine(lineBottom, wallPen);
    scene->addLine(lineLeft, wallPen);
    scene->addLine(lineRight, wallPen);

    robot =         new Robot(ROBOT_WIDTH, ROBOT_HEIGHT);
    bin =           new Zone(COLLECTION_BIN_WIDTH,COLLECTION_BIN_HEIGHT, "bin");
    dumpArea =      new Zone(ARENA_WIDTH,DUMP_AREA_HEIGHT, "dump");
    obstacleField = new Zone(ARENA_WIDTH,OBSTACLE_FIELD_HEIGHT, "obstacle");
    digArea =       new Zone(ARENA_WIDTH,DIG_AREA_HEIGHT, "dig");


    scene->addItem(bin);
    scene->addItem(dumpArea);
    scene->addItem(obstacleField);
    scene->addItem(digArea);
    scene->addItem(robot);


    robot->setPos(90,90);
    bin->setPos((ARENA_WIDTH-COLLECTION_BIN_WIDTH)/2,- COLLECTION_BIN_HEIGHT);
    dumpArea->setPos(0,0);
    obstacleField->setPos(0,DUMP_AREA_HEIGHT);
    digArea->setPos(0, DUMP_AREA_HEIGHT + OBSTACLE_FIELD_HEIGHT);
}

nav::~nav()
{
    delete ui;
}

void nav::initLidar()
{
    const char * opt_com_path = NULL;
    _u32         opt_com_baudrate = 115200;
    u_result     op_result;
    opt_com_path = "/dev/ttyUSB0";
    RPlidarDriver * drv = RPlidarDriver::CreateDriver(RPlidarDriver::DRIVER_TYPE_SERIALPORT);
}
