import socket
import struct as Struct


TCP_IP = '192.168.0.6'
TCP_PORT = 5005
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
print("Socket listening")
while 1:
    s.listen(1)
    conn, addr = s.accept()
    print('Connection address:', addr)
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        for i in range(0, len(data), 4):
            print(Struct.unpack("BBbB", data[i: i+4]))
            #print("received data:", )
           # print(data)
    conn.close()
    print("Disconnected")
