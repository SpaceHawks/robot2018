#ifndef PROTO_GUI_H
#define PROTO_GUI_H

#include <QMainWindow>
#include <QtCore>
#include <QtGui>
#include <QtWidgets>
#include "joystick.h"

namespace Ui {
class Proto_GUI;
}

class Proto_GUI : public QMainWindow
{
    Q_OBJECT

public:
    explicit Proto_GUI(QWidget *parent = 0);
    ~Proto_GUI();

private:
    Ui::Proto_GUI *ui;
    QGraphicsScene *scene;
    QGraphicsRectItem *rect;
    Joystick *joystick;
    int turn;
    int drive;
public slots:
    void getJoystickPosition();
signals:
    void hi();

};

#endif // PROTO_GUI_H
