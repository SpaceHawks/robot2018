#ifndef ROBOT_H
#define ROBOT_H

#include <QtWidgets>

#define NAME 1

class Robot :public QGraphicsItem::QGraphicsItem
{
public:
    Robot(qreal width, qreal height);
    QRectF boundingRect() const;
    void paint(QPainter * painter, const QStyleOptionGraphicsItem * option, QWidget * widget);
    bool Pressed;
    qreal width; // Centimeters
    qreal height; //Centimeters
private:
    void mousePressEvent(QGraphicsSceneMouseEvent *event);
    void mouseReleaseEvent(QGraphicsSceneMouseEvent *event);
};

#endif // ROBOT_H
