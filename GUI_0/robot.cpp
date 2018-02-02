#include "robot.h"
#include <QDebug>
Robot::Robot(qreal width, qreal height)
{
    isSelected = false;
    setFlag(ItemIsMovable);
    this->width = width;
    this->height = height;
    setData(1, "robot");
}

QRectF Robot::boundingRect() const
{
    return QRectF(0,0,width,height);
}

void Robot::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)
{
    QRectF rect = boundingRect();
    if(isSelected)
    {
        QPen robotLine(Qt::blue, 3);
        QBrush robotFill(Qt::blue);
        painter->setPen(robotLine);
        painter->setBrush(robotFill);
        painter->drawRect(rect);
    }
    else
    {
        QPen robotLine(Qt::black, 3);
        QBrush robotFill(Qt::black);
        painter->setPen(robotLine);
        painter->setBrush(robotFill);
        painter->drawRect(rect);
    }
}

void Robot::mousePressEvent(QGraphicsSceneMouseEvent *event)
{
    isSelected = true;
    update();
    QGraphicsItem::mousePressEvent(event);
}

void Robot::mouseReleaseEvent(QGraphicsSceneMouseEvent *event)
{
    isSelected = false;
    update();
    QGraphicsItem::mouseReleaseEvent(event);
}

