"""
I2C TEAM

I2C team is responsible for the wired communication between all devices that are capable of I2C, which as Arduino, Raspberry Pi, and various sensors.
Your duties include:
	Providing methods of sending and receiving an single integer or array of integers.
	Providing a robust way to reconnect in the event of losing connections.
	Handling all exceptions that might crash the program.

Requrement:
	Use Python or C++. If you have implimentation in both languages, that's even better.
	Utilize multi-threading in Linux devices. The threads must be closed immediately if a stop signal is triggered.
	Master-slaves relationship: only one device will decide who is talking and when to talk.
	
Coding notes:
	Corlaborate with your teammates.
	Document your codes well so other teams will understand it.
	Make frequent Git commits.
	Feel free to add addition functions if you need to.
	Write your own test program.
"""

class I2CReceiver(): #inherit multi-threading and socket
    """
	A thread on Raspberry Pi that listen always listen to messages from the master, which will then be added to a queue.
    """
    def __init__(self, address, targetAddress, q):
        """
		Constructor.
		Args:
			address: The i2c address of the host device.
			targetAddress: The i2c address of the target device.
			q: a shared queue containing received messages (integer or array of integers).
		"""
		pass

    def run(self):
        """
        Stuff reveiced messages to the shared queue.
        Implimentation:
			Loops until self.stop is True (never create an infinite loop)
				Connect/Listen to a new connection. Once a connection is established...
				Put any imcoming messages to the queue.
				In case the connection is broken for any reason, close all existing connection, then connect/listen to another one.
        """
        #your codes
		

class I2CSender(): #inherit multi-threading and socket
    """
	Always listen to the "talk now" signal from the master, then send all items in its queue.
    """
    def __init__(self, address, targetAddress, signalPin, q):
        """
        Constructor.
        Args:
			address: The i2c address of the host device.
			targetAddress: The i2c address of the target device.
			signalPin: an GPIO pin that when it's on means "talk now".
			q: A shared queue containing messages (integer or array of integers) to be sent.
        """
		pass
      
    def run(self):
        """
        Gets messages from the shared queue and send them.
        Implimentation:
            loop until self.stop is True.
				Connect/Listen to a new connection. Once a communicationis established.
				loop until self.stop is True:
					if signalPin is HIGH:
						send all messages
        """
		pass
		
	def send(data):
		"""
		Send data to targetAddress.
		Args:
			data: an integer or an array of integers containing useful info.
		"""
		pass

def main():
	pass

if __name__ == '__main__':
    main()
        