#ifndef ZONE_H
#define ZONE_H

#include "robot.h"

#include <QtWidgets>

class Zone: public QGraphicsItem::QGraphicsItem
{
public:
    Zone(qreal width, qreal height, QString name);
    QRectF boundingRect() const;
    void paint(QPainter * painter, const QStyleOptionGraphicsItem * option, QWidget * widget);
    bool hasRobot;
    qreal width;  // Centimeters
    qreal height; // Centimeters
};

#endif // ZONE_H
