#include <QCoreApplication>
#include "pathcontrol.h"
int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);
    PathControl *p = new PathControl();
    p->execute();
    p->path->pathFinder();
    p->path->pointList->display();
    return a.exec();
}
