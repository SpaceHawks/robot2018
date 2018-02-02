#include "joystick.h"

#include <QDebug>

Joystick::Joystick()
{
    setFlag(ItemIsMovable);
    setFlag(ItemSendsScenePositionChanges);
    setData(1, "joystick");
}

QRectF Joystick::boundingRect() const
{
    return QRectF(0,0,70,70);
}

void Joystick::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)
{
    QRectF rect = boundingRect();

        QPen pen(Qt::black, 3);
        QBrush brush(Qt::gray);
        QBrush brush2(Qt::white);
        painter->setPen(pen);
        painter->setBrush(brush);
        painter->drawEllipse(rect);
        QPoint center = QPoint(35,35);
        painter->setBrush(brush2);
        painter->drawEllipse(center,10,10);

}

void Joystick::mousePressEvent(QGraphicsSceneMouseEvent *event)
{
   isSelected = true;
   QGraphicsItem::mousePressEvent(event);
}

void Joystick::mouseReleaseEvent(QGraphicsSceneMouseEvent *event)
{
    setX(165);
    setY(165);
    QGraphicsItem::mouseReleaseEvent(event);
}

