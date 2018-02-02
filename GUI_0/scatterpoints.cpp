#include "scatterpoints.h"
#include <QDebug>

ScatterPoints::ScatterPoints(qreal x, qreal y)
{
    this->x = x;
    this->y = y;
    setData(3, "point");
}

QRectF ScatterPoints::boundingRect() const
{
    return QRectF(0,0,0,0);
}

void ScatterPoints::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)
{
    QPoint point(x,y);
    QPen pointPen(Qt::yellow);
    painter->setPen(pointPen);
    painter->drawPoint(point);
    update();
}
