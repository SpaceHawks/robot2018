#include "navigationpointer.h"
#include <QDebug>

NavigationPointer::NavigationPointer()
{
    setFlag(ItemIsMovable);
}

QRectF NavigationPointer::boundingRect() const
{
    return QRectF(0,0,20,20);
}

void NavigationPointer::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)
{
    QRectF pointer = boundingRect();
    QPen pointerPen(Qt::gray);
    pointerPen.setWidth(3);
    painter->setPen(pointerPen);
    QLine line = QLine(10,0,10,20);
    painter->drawLine(line);
    line = QLine(0,10,20,10);
    painter->drawLine(line);
}
