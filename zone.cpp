#include "zone.h"

Zone::Zone(qreal width, qreal height, QString name)
{
    hasRobot = false;
    this->width = width;
    this->height = height;
    setData(NAME, name);
}

QRectF Zone::boundingRect() const
{
    return QRectF(0,0,width,height);
}

void Zone::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)
{
    QRectF rect = boundingRect();
    if(hasRobot)
    {
        QPen pen(Qt::green, 3);
        painter->setPen(pen);
        painter->drawRect(rect);
    }
    else
    {
        QPen pen(Qt::black, 3);
        painter->setPen(pen);
        painter->drawRect(rect);
    }

    QList<QGraphicsItem *> areas = scene()->collidingItems(this);
    hasRobot = false;
    for(int i = 0; i < areas.count(); i++)
    {
        if(areas[i]->data(NAME) == "robot")
        {
            hasRobot = true;
        }
    }
    update();
}

void Zone::mousePressEvent(QGraphicsSceneMouseEvent *event)
{
}

void Zone::mouseReleaseEvent(QGraphicsSceneMouseEvent *event)
{
}
