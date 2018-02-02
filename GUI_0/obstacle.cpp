#include "obstacle.h"
#include <QDebug>

Obstacle::Obstacle(qreal radius, qreal x, qreal y)
{
    this->radius = radius;
    this->x = x;
    this->y = y;
    setData(2, "obstacle");
}

QRectF Obstacle::boundingRect() const
{
    return QRectF(x,y,radius,radius);
}

void Obstacle::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)
{
    QRectF circ = boundingRect();
    QPen obstacleLine(Qt::black, 3);
    QBrush obstacleFill(QColor::fromRgb(128,0,0));
    painter->setPen(obstacleLine);
    painter->setBrush(obstacleFill);
    painter->drawEllipse(circ);
    update();
}
