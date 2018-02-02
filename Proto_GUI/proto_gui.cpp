#include "proto_gui.h"
#include "ui_proto_gui.h"
#include <QDebug>

Proto_GUI::Proto_GUI(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::Proto_GUI)
{
    ui->setupUi(this);
    scene = new QGraphicsScene(this);
    ui->graphicsView->setScene(scene);


    QBrush brush(Qt::black);
    scene->setBackgroundBrush(brush);

    QPen pen(Qt::red);
    pen.setWidth(3);
    QLine line = QLine(0,0,400,0);
    scene->addLine(line,pen);
    line = QLine(0,400,400,400);
    scene->addLine(line,pen);
    line = QLine(0,0,0,400);
    scene->addLine(line,pen);
    line = QLine(400,0,400,400);
    scene->addLine(line,pen);

    pen.setColor(Qt::blue);
    line = QLine(200,0,200,400);
    scene->addLine(line,pen);
    line = QLine(0,200,400,200);
    scene->addLine(line,pen);
    pen.setWidth(1);
    pen.setColor(Qt::white);
    for(int i = 0; i < 39; i++){
       line = QLine(185,10+(10*i),215,10+(10*i));
       scene->addLine(line,pen);
    }
    for(int i = 0; i < 39; i++){
       line = QLine(10+(10*i),185,10+(10*i),215);
       scene->addLine(line,pen);
    }

   joystick = new Joystick();
   scene->addItem(joystick);
   joystick->setPos(165,165);

   getJoystickPosition();
}


Proto_GUI::~Proto_GUI()
{
    delete ui;
}

void Proto_GUI::getJoystickPosition()
{
    //qDebug() << "called";

}

QVariant Joystick::itemChange(GraphicsItemChange change, const QVariant &value)
{
    if (330 < value.toPointF().x())
        setX(330);
    if (330 < value.toPointF().y())
        setY(330);
    if(change == ItemPositionChange && scene()){
       QPoint newPos = value.toPoint();
       QRectF rect = scene()->sceneRect();
       drive = 82 - (newPos.y())/2;
       turn =  (newPos.x())/2 - 82;
       qDebug() << drive << turn;

       if (!rect.contains(newPos)) {


                    if (rect.left() > newPos.x())
                         newPos.setX(rect.left());


                     if (rect.top() > newPos.y())
                         newPos.setY(rect.top());

                     return newPos;
                 }
    }
   return QGraphicsItem::itemChange(change, value);
}
