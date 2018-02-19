#ifndef TCPCODEBUILDER_H
#define TCPCODEBUILDER_H

#include <QBitArray>
#include <QDebug>
#include <QtMath>

class TCPCodeBuilder
{
public:
    TCPCodeBuilder();
    QBitArray command;
    QBitArray id;
    QBitArray value;
    QBitArray checksum;
    QBitArray tcpCode;
    QBitArray receivedCode;

    QBitArray fullAdder(QBitArray a, QBitArray b);
    QBitArray fullSubtracter(QBitArray a, QBitArray b); // unsigned
    QBitArray twosComplementer(QBitArray a);
    QBitArray evaluateUnsigned(int a);
    QBitArray evaluateSigned(int a);
    QBitArray flip(QBitArray a);
    QBitArray assign(QBitArray a);
    QBitArray evaluateChecksum();
    QBitArray buildCode();
    int buildCodeInt();
};

#endif // TCPCODEBUILDER_H
