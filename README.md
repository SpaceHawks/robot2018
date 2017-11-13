# Coding recommendations:
1. Collaborate with your teammates.
2. Document your codes well so other teams will understand it.
3. Make frequent Git commits.
4. Feel free to add additional functions if you need to.
5. Write your own test program.

# TCP TEAM
## Responsibilities
TCP team is responsible for the communication between all devices that are capable of TCP socket.
Your duties include:
1. Providing lightweight methods of sending and receiving data.
2. Providing a robust way to reconnect in the event of losing connections.
3. Handling all exceptions that might crash the program.

## Requirement:
1. Limit bandwidth usage to less than 50 kilobits/second. We lose 1 point for each 50 kb/s of average bandwidth.
2. Utilize multi-threading. The threads must be closed immediately if a stop signal is triggered.

## Delivery deadlines
### Friday Nov 17, 2017
Your team is expected to complete the following by this due date:
1. Push to GitHub completed server and client programs.
2. Include a test program that transmits strings of characters in both directions.
3. Handle all exceptions that might crash the program.
4. Dynamically connect/listen to a new connection if exceptions happen.

### Friday Nov 25, 2017
Your team is expected to complete the following by this due date:
1. Come up with a lightweight message structure that communicates necessary info/commands.
2. Include a test program to build the message on the sender side, and parse the message on the receiver side.