# Coding recommendations
1. Collaborate with your teammates.
2. Document your codes well so other teams will understand it.
3. Make frequent Git commits.
4. Feel free to add additional functions if you need to.
5. Write your own test program.

# TCP TEAM
## Responsibilities
I2C team is responsible for the wired communication between all devices that are capable of I2C, which as Arduino, Raspberry Pi, and various sensors.

Your duties include:
1. Providing methods of sending and receiving a single integer or array of integers.
2. Providing a robust way to reconnect in the event of losing connections.
3. Handling all exceptions that might crash the program.

## Requirement:
1. Use Python or C++. If you have the implementations in both languages, that's even better.
2. Utilize multi-threading in Linux devices. The threads must be closed immediately if a stop signal is triggered.
3. Master-slaves relationship: only one device will decide who is talking and when to talk.

## Delivery deadlines
### Friday Nov 17, 2017
Your team is expected to complete the following by this due date:
1. Push to GitHub completed Pythpn code in the Raspberry Pi and C++ codes in the Arduino.
2. Include a test program that transmits an array of numbers/characters in both directions.
3. Handle all exceptions that might crash the program.
4. Dynamically connect/listen to a new connection if exceptions happen.

### Friday Nov 25, 2017
Your team is expected to complete the following by this due date:
1. Come up with a message structure that communicates necessary info/commands.
2. Include a test program to build the message on the sender side, and parse the message on the receiver side.