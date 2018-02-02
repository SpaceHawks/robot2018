#include "zone.h"

Zone::Zone(qreal width, qreal height, QString name)
{
    hasRobot = false;
    this->width = width;
    this->height = height;
    setData(1, name);
}

QRectF Zone::boundingRect() const
{
    return QRectF(0,0,width,height);
}

void Zone::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)
{
    QRectF zone = boundingRect();
    if(hasRobot)
    {
        QPen zoneLine(Qt::black, 3);
        QBrush zoneFill(QColor::fromRgb(210,180,140));
        painter->setPen(zoneLine);
        painter->setBrush(zoneFill);
        painter->drawRect(zone);
    }
    else
    {
        QPen zoneLine(Qt::black, 3);
        QBrush zoneFill(QColor::fromRgb(200,64,63));
        painter->setPen(zoneLine);
        painter->setBrush(zoneFill);
        painter->drawRect(zone);
    }

    QList<QGraphicsItem *> areas = scene()->collidingItems(this);
    hasRobot = false;
    for(int i = 0; i < areas.count(); i++)
    {
        if(areas[i]->data(1) == "robot")
        {
            hasRobot = true;
        }
    }
    update();
}
