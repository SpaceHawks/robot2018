#ifndef OBSTACLE_H
#define OBSTACLE_H

#include <QtWidgets>

class Obstacle : public QGraphicsItem::QGraphicsItem
{
public:
    Obstacle(qreal radius, qreal x, qreal y);
    QRectF boundingRect() const;
    void paint(QPainter * painter, const QStyleOptionGraphicsItem * option, QWidget * widget);
    qreal radius;
    qreal x;
    qreal y;
};

#endif // OBSTACLE_H
