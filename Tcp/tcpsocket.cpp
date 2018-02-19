#include "tcpsocket.h"

TcpSocket::TcpSocket(QObject *parent): QObject(parent)
{ 
    command = 0;
    id = 0;
    value = 0;
}

QBitArray TcpSocket::compute(int command, int id, int value){
    code.command = code.evaluateUnsigned(command);
    code.id = code.evaluateUnsigned(id);
    code.value = code.evaluateSigned(value);
    code.checksum = code.evaluateChecksum();
    return code.buildCode();
}

void TcpSocket::send(int command, int id, int value){
    compute(command, id, value); // Send this
    socket->write("Hello server\r\n\r\n");
    socket->waitForBytesWritten(1000);
}

void TcpSocket::connect()
{
    socket = new QTcpSocket(this);

    socket->connectToHost("192.168.2.104", 1234);

    if(socket->waitForConnected(5000))
    {
        qDebug() << "Connected!";
        send(1,3,50);
        receive();
        socket->close();
    }
    else
    {
        qDebug() << "Not connected!";
    }
}

void TcpSocket::receive(){
    socket->waitForReadyRead(3000);
    qDebug() << "Reading: " << socket->bytesAvailable();
    qDebug() << socket->readAll(); // put this in code.receivedCode
}
