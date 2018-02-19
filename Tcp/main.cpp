#include <QCoreApplication>
#include "tcpsocket.h"
int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);
    TcpSocket s;
    s.connect();
    return a.exec();
}
