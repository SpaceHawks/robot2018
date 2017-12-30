#include "nav.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    nav w;
    w.show();

    return a.exec();
}
