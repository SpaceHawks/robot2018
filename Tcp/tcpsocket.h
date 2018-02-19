#ifndef TCPSOCKET_H
#define TCPSOCKET_H

#include <QObject>
#include <QTcpSocket>
#include <QDebug>
#include "tcpcodebuilder.h"

class TcpSocket: public QObject
{
    Q_OBJECT
public:
    TCPCodeBuilder code;
    explicit TcpSocket(QObject *parent = 0);
    void connect();
    QBitArray compute(int command, int id, int value);
    void send(int command, int id, int value);
    void receive();

private:
    QTcpSocket *socket;
    int command;
    int id;
    int value;
};

#endif // TCPSOCKET_H
