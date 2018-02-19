#include "tcpcodebuilder.h"

TCPCodeBuilder::TCPCodeBuilder()
{
    command.resize(8); // 8 bit unsigned number
    id.resize(8);   // 8 bit unsigned number
    value.resize(8); // 8 bit signed number
    checksum.resize(8); // 8 bit unsigned number
    tcpCode.resize(32); // 32 bit code to be sent via TCP

    command.fill(false);
    id.fill(true);
    value.fill(false);
    checksum.fill(true);

}

QBitArray TCPCodeBuilder::fullAdder(QBitArray a, QBitArray b){
    QBitArray carry(1);
    QBitArray sum(1);
    QBitArray result(8);
    a.resize(8);
    b.resize(8);

    int count = 0;
    for(int i=7;i > -1;i--){
        if(a.at(i))
            count++;
        if(b.at(i))
            count++;
        if(carry.at(0))
            count++;

        if(count%2 == 1){
            sum.setBit(0, true);
        }
        else
            sum.setBit(0,false);
        if(count > 1)
            carry.setBit(0,true);
        else
            carry.setBit(0,false);

        result.setBit(i,sum.at(0));
        count = 0;
    }
    return result;
}

QBitArray TCPCodeBuilder::fullSubtracter(QBitArray a, QBitArray b){
    QBitArray carry(1);
    QBitArray sum(1);
    QBitArray result(8);
    a.resize(8);
    b.resize(8);
    b = twosComplementer(b);

    int count = 0;
    for(int i=7;i > -1;i--){
        if(a.at(i))
            count++;
        if(b.at(i))
            count++;
        if(carry.at(0))
            count++;

        if(count%2 == 1){
            sum.setBit(0, true);
        }
        else
            sum.setBit(0,false);
        if(count > 1)
            carry.setBit(0,true);
        else
            carry.setBit(0,false);

        result.setBit(i,sum.at(0));
        count = 0;
    }
    if(carry.at(0) == false){
        qDebug() << carry;
        return twosComplementer(result);}
    else
        return result;
}

QBitArray TCPCodeBuilder::twosComplementer(QBitArray a){
    a.resize(8);
    QBitArray one(8);
    QBitArray result(8);
    one.setBit(7,true);
    for(int i=0;i < 8;i++){
        result.setBit(i,!a.at(i));
    }
    return fullAdder(result,one);
}

QBitArray TCPCodeBuilder::assign(QBitArray a){
    QBitArray result(8);
    for(int i=0;i<8;i++){
        result.setBit(i,a.at(i));
    }
    return result;
}

QBitArray TCPCodeBuilder::evaluateChecksum(){ // fix this
    QBitArray max(8);
    max.fill(true);
    qDebug() << max << command;
    //checksum =
            qDebug() << fullSubtracter(max,command);
   // qDebug() << checksum;
    //qDebug() << max << command;
    //checksum = fullSubtracter(checksum,id);
    //checksum = fullSubtracter(checksum,value);
    return checksum;
}

QBitArray TCPCodeBuilder::evaluateUnsigned(int a){
    QBitArray result(8);
    for(int i=0;i<8;i++){
        result.setBit(i,a%2);
        a /= 2;
    }
    return flip(result);
}

QBitArray TCPCodeBuilder::evaluateSigned(int a){
    int sign = 0;
    QBitArray result(8);
    if(a < 0){
        sign = 1;
        a = -a;
    }
    for(int i=0;i<7;i++){
        result.setBit(i,a%2);
        a /= 2;
    }
    if(sign == 1){
        result = flip(result);
        return twosComplementer(result);
    }
    else
        return flip(result);
}

QBitArray TCPCodeBuilder::flip(QBitArray a){
    QBitArray result(8);
    for(int i=0;i<8;i++){
        result.setBit(7-i,a.at(i));
    }
    return result;
}

QBitArray TCPCodeBuilder::buildCode(){
    int m = 0;
    for(int i=0;i<8;i++){
        tcpCode.setBit(m,command.at(i));
        m++;
    }
    for(int i=0;i<8;i++){
        tcpCode.setBit(m,id.at(i));
        m++;
    }
    for(int i=0;i<8;i++){
        tcpCode.setBit(m,value.at(i));
        m++;
    }
    for(int i=0;i<8;i++){
        tcpCode.setBit(m,checksum.at(i));
        m++;
    }
    return tcpCode;
}

int TCPCodeBuilder::buildCodeInt(){
    int intCode = 0;
    int temp = 0;
    buildCode();
    tcpCode.setBit(30,true);
    for(int i = 31; i>-1;i--){
        if(tcpCode.at(31-i) == true)
            temp = 1;
        else
            temp = 0;
        intCode += pow(2,i)*temp;
    }
    return intCode;
}
