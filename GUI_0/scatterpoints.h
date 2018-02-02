#ifndef SCATTERPOINTS_H
#define SCATTERPOINTS_H

#include <QtWidgets>

class ScatterPoints: public QGraphicsItem::QGraphicsItem
{
public:
    ScatterPoints(qreal x, qreal y);
    QRectF boundingRect() const;
    void paint(QPainter * painter, const QStyleOptionGraphicsItem * option, QWidget * widget);
    qreal x;
    qreal y;
};

#endif // SCATTERPOINTS_H
