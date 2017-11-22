from tcp import *
from timer import Timer

q = Queue()
receiver = TCPReceiver(host = '127.0.0.1', port = 5005, q = q)
receiver.start()
t = Timer()

while t.getTime() < 10:
    if not q.empty():
        print(q.get())

receiver.stop()
receiver.join()
print("server's main exited")


