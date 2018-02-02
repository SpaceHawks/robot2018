#ifndef NAVIGATIONPOINTER_H
#define NAVIGATIONPOINTER_H

#include <QtWidgets>

class NavigationPointer: public QGraphicsItem::QGraphicsItem
{
public:
    NavigationPointer();
    QRectF boundingRect() const;
    void paint(QPainter * painter, const QStyleOptionGraphicsItem * option, QWidget * widget);
};

#endif // NAVIGATIONPOINTER_H
