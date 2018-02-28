COMMAND_PORT = 1234
DATA_PORT = 5678
COMMAND_STRUCTURE = 'BBBBB' # Command, device, value1, value2, checksum
COMMAND_LENGTH = len(COMMAND_STRUCTURE)
DATA_STRUCTURE = 'BBBBB' # # Command, device, value1, value2, checksum
DATA_LENGTH = len(DATA_STRUCTURE)

#Commands
SYSTEM =            0
MANUAL =            1
PARTIAL_AUTO =      2
DATA =              3

#Device when command = 0
TCP_STATUS =        0

#Device when command = 0 device = 0
ALIVE =        0


#Value 1 when command = 0 Device = 0
SENDER_CONNECTED =          0
SENDER_DISCONNECTED =       1
RECEIVER_CONNECTED =        2
RECEIVER_DISCONNECTED =     3
#Value 2 when command = 0 Device = 0 is the ip address of the target device

#Manual Driving Devices when command = 1
STOP_ALL =              0
WHEEL_FRONT_RIGHT =     1
WHEEL_FRONT_LEFT =      2
WHEEL_REAR_RIGHT =      3
WHEEL_REAR_LEFT =       4
LINEAR_ACTUATOR_PAIR =  5
AUGER_SLIDER =          7
AUGER_DRILL =           8
DUMPING_CONVEYOR =      9
DRIVE_AND_TURN =        10

