from tcp import *
from timer import Timer
import time

q = Queue()
sender = TCPSender(host = '127.0.0.1', port = 5005, q = q)
sender.start()
t = Timer()
count = 0
while t.getTime() < 10:
    message = "Message num " + str(count)
    count+=1
    q.put(message)
    print("Enqueued "+ message)
    time.sleep(0.5)

sender.stop()
sender.join()
print("client's main exited")

