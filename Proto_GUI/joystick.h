#ifndef JOYSTICK_H
#define JOYSTICK_H

#include <QtWidgets>

class Joystick: public QGraphicsItem::QGraphicsItem
{
public:
    Joystick();
    QRectF boundingRect() const;
    void paint(QPainter * painter, const QStyleOptionGraphicsItem * option, QWidget * widget);
    bool isSelected;
    int drive = 0;
    int turn = 0;
private:
    QVariant itemChange(GraphicsItemChange change, const QVariant &value);
    void mousePressEvent(QGraphicsSceneMouseEvent *event);
    void mouseReleaseEvent(QGraphicsSceneMouseEvent *event);
signals:
    void joystickMoved();
};

#endif // JOYSTICK_H
