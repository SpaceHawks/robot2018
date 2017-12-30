#include "robot.h"
#include <QDebug>
Robot::Robot(qreal width, qreal height)
{
    Pressed = false;
    setFlag(ItemIsMovable);
    this->width = width;
    this->height = height;
    setData(NAME, "robot");
}

QRectF Robot::boundingRect() const
{
    return QRectF(0,0,width,height);
}

void Robot::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)
{
    QRectF rect = boundingRect();
    if(Pressed)
    {
        QPen pen(Qt::red, 3);
        painter->setPen(pen);
        painter->drawEllipse(rect);
    }
    else
    {
        QPen pen(Qt::black, 3);
        painter->setPen(pen);
        painter->drawRect(rect);

        static const QPointF points[3] = {
            QPointF(0, 0),
            QPointF(width, 0),
            QPointF(width/2, height),
        };
        painter->drawPolygon(points, 3);
    }
}

void Robot::mousePressEvent(QGraphicsSceneMouseEvent *event)
{
    Pressed = true;
    update();
    QGraphicsItem::mousePressEvent(event);
}

void Robot::mouseReleaseEvent(QGraphicsSceneMouseEvent *event)
{
    Pressed = false;
    update();
    QGraphicsItem::mouseReleaseEvent(event);
}
