"""
TCP TEAM

TCP team is responsible for the communication between all devices that are capable of TCP socket.
Your duties include:
	Providing lightweight methods of sending and receiving data.
	Providing a robust way to reconnect in the event of losing connections.
	Handling all exceptions that might crash the program.

Requrement:
	Limit bandwith usage to less than 50 kilobits/second. We lose 1 point for each 50 kb/s of average bandwith.
	Utilize multi-threading. The threads must be closed immediately if a stop signal is triggered.
	#queue is queue of messages, send the value for message dequeued
Coding notes:
	Corlaborate with your teammates.
	Document your codes well so other teams will understand it.
	Make frequent Git commits.
	Feel free to add addition functions if you need to.
	Write your own test program.
"""

import socket
import thread
class TCPReceiver(): #inherit multi-threading and socket
    """
    A thread that listens to oncoming messages.
    """
    def __init__(self, host, port, q):
        """
		        Constructor.
		        Args:
			        host: the ip address of the current devices or the target device.
			        port: The port number to connect/listen to new connections.
			        q: A shared queue containing future messages (in binary data type) from the sender.
		        """
        self.receiver_host = host
        self.receiver_port = port
        self.queue = q
		self.stop = False

    def connect(self):
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        try:
            self.sock.connect((self.receiver_host, self.receiver_port))
        except:
            print('connction failed')
    def stop():
        self.stop = True

    def run(self):
        """
        Stuff reveiced messages to the shared queue.
        Implimentation:
			            Loops until self.stop is True (never create an infinite loop)
				            Connect/Listen to a new connection. Once a connection is established...
				            Put any imcoming messages to the queue.
				            In case the connection is broken for any reason, close all existing connection, then connect/listen to another one.
        """
        thread.start_new_thread( _run )

    def _run(self)
		self.connect()
        while(not self.stop):
            
            data = self.sock.recieve()
            if(data is not None):
                self.q.enqueue(data)
            else:
                print("error occured, reconnecting...")
                self.connect(self.receiver_host, self.receiver_port)

class TCPSender(): #inherit multi-threading and socket
    """
	    A thread that send out messages.
    """
    def __init__(self, host, port, q):
        """
        Constructor.
        Args:
			            host: the ip address of the current devices or the target device.
			            port: The port number to connect/listen to new connections.
			            q: A shared queue containing messages (in binary data type) to be sent.
        """
		self.host  = host
        self.port = port
        self.queue = q
        self.stop = False

    def _bind(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(self.host, self.port)
        print('bind succesful')

    def stop():
        self.stop = True

    def run(self):
        """
        Gets messages from the shared queue and send them.
        Implimentation:
            loop until self.stop is True.
				                Connect/Listen to a new connection. Once a communicationis established.
				                loop until self.stop is True
					                loop until the queue is empty:
						                send the oldest message in the queue.
        """
        thread.start_new_thread(_run())
	
    def _run(self):
        while not self.stop:
            self._bind()
            self.sock.listen(20)
            self.sock.accept()
            while not self.stop:
                while q:
                    sock.send(q.dequeue)
            print('sender stopeed')
def main():
	pass

if __name__ == '__main__':
    main()
        