#
# Arduino related methods and attributes
#
from AI import Wheel
from AI import Drill
from AI import Conveyor
#
class Arduino:


    def __init__(self):
        self.wheels = Wheel()
        self.drill = Drill()
        self.conveyor = Conveyor()


    def resetArduino(self):
        pass
        # Reset entire Arduino system


    def lockWheels(self):
        self.wheels.enable(False)


    def unlockWheels(self):
        self.wheels.enable(True)


    def move(self):
        pass


    def lockDrill(self):
        self.drill.enable(False)


    def unlockDrill(self):
        self.drill.enable(True)


    def drill(self):
        pass


    def lockConveyor(self):
        self.conveyor.enable(False)


    def unlockConveyor(self):
        self.conveyor.enable(True)


    def start(self):
        pass


    def stop(self):
        pass

#
# End Arduino
#


#
# Tinker related methods and attributes
#
from AI import Sensor
#
class Tinker:


    def __init__(self):
        self.sensors = Sensor()


    def enableSensors(self):
        self.enableSensors()


    def disableSensors(self):
        self.disableSensors()


#
# End Tinker
#


#
# Wheel related methods and attributes
#
class Wheel:


    def __init__(self):
        self.lock = True


    def enable(self, val):
        self.lock = not val


    def moveStraight(self, isForward):
        if(self.lock == False):
            pass


    def rotate(self, isClockwise):
        if (self.lock == False):
            pass


    def moveTo(self, x,y):
        if (self.lock == False):
            pass


    def getStatus(self):
        return not self.lock

#
# End Motor
#


#
# Drill, Actuator and Slider related methods and attributes
#
class Drill:


    def __init__(self):
        self.lock = True


    def enable(self, val):
        self.lock = not val


    def getStatus(self):
        return not self.lock


    def start(self):
        if (self.lock == False):
            pass


    def stop(self):
        if (self.lock == False):
            pass


    def incline(self):
        if (self.lock == False):
            pass


    def decline(self):
        if (self.lock == False):
            pass


    def lower(self):
        if (self.lock == False):
            pass


    def higher(self):
        if (self.lock == False):
            pass

#
#   End Drill
#


#
# Conveyor related methods and attributes
#
class Conveyor:


    def __init__(self):
        self.lock = True


    def enable(self, val):
        self.lock = not val


    def getStatus(self):
        return not self.lock


    def start(self):
        if (self.lock == False):
            pass


    def stop(self):
        if (self.lock == False):
            pass

#
# End Conveyor
#


#
# Sensor related methods and attributes
#
class Sensor:


    def __init__(self):
        self.eLIDAR = False
        self.eDSensors = False


    def resetLIDAR(self):
        pass


    def resetDSensors(self):
        pass


    def enable(self):
        self.enableLIDAR(True)
        self.enableDSensors(True)


    def disable(self):
        self.enableLIDAR(False)
        self.enableDSensors(False)


    def enableLIDAR(self, val):
        self.eLIDAR = val


    def enableDSensors(self, val):
        self.eDSensors = val


    def getStatus(self):
        return self.eLIDAR


    def scan(self):
        pass
        # LIDAR


    def sense(self):
        pass
        # Distance Sensors

#
# End Sensor
#


#
# Class that controls actions of the robot
#
from AI import Pathfinding
from AI import Arduino
from AI import Tinker
class Control:


    def __init__(self):
        self.pathFinder = Pathfinding()
        self.path = [(0.0,0.0), (0.0,0.0), (0.0,0.0)]
        self.arduino = Arduino()
        self.tinker = Tinker()
        self.theta = 0.0 # Orientation angle
        self.rX = 0.0
        self.rY = 0.0
        self.task = 0


    # Path Finding/Obstacle Avoidance -> navigate()
    def navigate(self):
        pass


    # Self-alignment -> align() 40cm-80cm
    def align(self):
        pass
        # Call Self-Aligment Method


    # Fixing orientation -> orient()
    def orient(self):
        if(theta > 10):
            self.arduino.wheels.rotate(False)
            self.orient()
        elif (theta < -10):
            self.arduino.wheels.rotate(True)
            self.orient()
        # Add Timer to prevent infinite rotation


    # Check for errors/miscalculations -> inspect()
    def inspect(self):
        pass
        # if (errors == true):
        #   self.handle()


    # Fix errors -> handle()
    def handle(self):
        pass
        # if can't handle
        # self.reset()

    def goToDig(self):
        pass

    # Start-sequence (Prepare Robot to work autonomously) -> start()
    def start(self):
        self.tinker.enableSensors()
        self.arduino.unlockWheels()
        self.localize()
        self.detect() # Not needed
        self.orient()
        self.align()
        self.inspect()
        self.run()
        pass

    def run(self):
        if(self.task == 0):
            self.orient()
        elif(self.task == 1):
            while(self.rX < 1200):
                self.arduino.wheels.moveStraight(True)
                # get new data
        elif(self.task == 2):
            self.navigate() # forward
        elif(self.task == 3):
            self.goToDig()
        elif(self.task == 4):
            self.arduino.lockWheels()
            self.arduino.unlockDrill()
            self.mine()
        elif(self.task == 5):
            self.arduino.lockDrill()
            self.arduino.unlockWheels()
            while(self.rX > 4500):
                self.arduino.wheels.moveStraight(False)
                # get new data
        elif(self.task == 6):
            self.navigate() # backward
        elif(self.task == 7):
            while(self.rX > 800):
                self.arduino.wheels.moveStraight(False)
        elif(self.task == 8):
            self.align()
        elif(self.task == 9):
            self.arduino.lockWheels()
            self.arduino.unlockConveyor()
            self.dump()
        elif(self.task == 10):
            self.arduino.lockConveyor()
            self.arduino.unlockWheels()
            self.inspect()
            self.handle()

        self.task += 1
        if(self.task > 10):
            self.task = 0


    # Doomsday protocol (Switch to Manual Mode) -> switch()
    def switch(self):
        pass


    # Terminate robot operations -> shutdown()
    def shutdown(self):
        pass


    # Reset robot operations-> reset()
    def reset(self):
        pass


    # Movement (Wheels) -> move()
    def move(self,isForward, robotLoc, numPivots, obstacles):
        self.pathFinder.setData(isForward, robotLoc, numPivots, obstacles)
        self.path = self.pathFinder.getData()
        # if(path[0][0] is ahead of current location and it is safe):
        #   moveTo(path[0][0], path[0][1])
        #   memory.=addToPath(path[0][0], path[0][1])
        #   if(path[1][0] is ahead of current location and it is safe):
        #       moveTo(path[1][0],path[1][1])
        #       if(path[2][0] is ahead of current location and it is safe):
        #           moveTo(path[2][0],path[2][1])
        # else:
        #   moveStraight()


    # Mining (Drill) -> mine()
    def mine(self):
        pass


    # Dumping (Conveyor) -> dump()
    def dump(self):
        pass


    # Robot x,y,theta -> localize()
    def localize(self):
        pass


    # Obstacles x,y,r -> detect()
    def detect(self):
        pass


    # resetArduino()
    def resetArduino(self):
        pass

    # Enablers for LIDARs, DSensors, Wheels, Drill, Conveyor -> enable()
    def enableAll(self):
        self.tinker.enableSensors()
        self.arduino.unlockWheels()
        self.arduino.unlockConveyor()
        self.arduino.unlockDrill()

    # Update memory -> update()
    def update(self):
        pass

#
#  End Control
#


#
# Pathfinding Class
#
import math
#
class Pathfinding:


    def __init__(self):
        self.isForward = True
        self.r = 500.0  # radius of robot
        self.rX = 0.0  # x-coordinate of robot
        self.rY = 0.0  # y-coordinate of robot

        self.obstacles = [[0.0, 0.0],
                          [0.0, 0.0],
                          [0.0, 0.0],
                          [0.0, 0.0],
                          [0.0, 0.0]]  # holds upto 5 self.obstacles

        self.numPivots = 0  # num of relevant self.obstacles
        self.pivots = [[0.0, 0.0],
                       [0.0, 0.0]]  # works with only 2 self.obstacles at any time

        self.dirr = 1
        self.dest = 1

        self.xA = 0.0
        self.yA = 0.0
        self.xB = 0.0
        self.yB = 0.0
        self.x1 = 0.0
        self.y1 = 0.0
        self.x2 = 0.0
        self.y2 = 0.0
        self.x3 = 0.0
        self.y3 = 0.0


    def setNumPivots(self, num):
        self.numPivots = num


    def setDest(self, f):
        self.isForward = f


    def setLoc(self, x, y):
        self.rX = x
        self.rY = y


    def setObstacles(self, xA, yA, xB, yB):
        self.pivots[0][0] = xA
        self.pivots[0][1] = yA
        self.pivots[1][0] = xB
        self.pivots[1][1] = yB


    def moveStraight(self):  # moves robot forward/backward 30 cm
        if (self.isForward == True):
            self.dest = 1
            self.x1 = self.rX + 100
            self.y1 = self.rY
            self.x2 = self.rX + 200
            self.y2 = self.rY
            self.x3 = self.rX + 300
            self.y3 = self.rY
        else:
            self.dest = -1
            self.x1 = self.rX - 100
            self.y1 = self.rY
            self.x2 = self.rX - 200
            self.y2 = self.rY
            self.x3 = self.rX - 300
            self.y3 = self.rY


    def pathA(self, num):  # if self.numPivots == 1
        if (self.isForward == True):
            self.dest = 1
        else:
            self.dest = -1
        if (num == 1):
            self.xA = self.pivots[0][0]
            self.yA = self.pivots[0][1]
            if (self.yA > 0.0):
                self.dirr = -1
            else:
                self.dirr = 1
        if (num == 2):
            if ((self.pivots[0][1] + self.pivots[1][1]) / 2 > 0):
                self.dirr = -1
            else:
                self.dirr = 1
            if (self.dirr == 1):
                if (self.pivots[0][1] > self.pivots[1][1]):
                    self.xA = self.pivots[0][0]
                    self.yA = self.pivots[0][1]
                    self.xB = self.pivots[1][0]
                    self.yB = self.pivots[1][1]
                else:
                    self.xA = self.pivots[1][0]
                    self.yA = self.pivots[1][1]
                    self.xB = self.pivots[0][0]
                    self.yB = self.pivots[0][1]
            else:
                if (self.pivots[0][1] > self.pivots[1][1]):
                    self.xA = self.pivots[1][0]
                    self.yA = self.pivots[1][1]
                    self.xB = self.pivots[0][0]
                    self.yB = self.pivots[0][1]
                else:
                    self.xA = self.pivots[0][0]
                    self.yA = self.pivots[0][1]
                    self.xB = self.pivots[1][0]
                    self.yB = self.pivots[1][1]
        self.x3 = self.xA
        self.y3 = self.yA + self.dirr * (self.r + 400)
        self.x2 = self.xA - self.dest * (self.r + 400) * 2 / 3
        self.y2 = self.y3
        self.x1 = self.xA - self.dest * (self.r + 400)
        self.y1 = self.y3 - self.dirr * (self.r + 400) / 3


    def pathB(self):  # if self.numPivots == 2
        self.xA = self.pivots[0][0]
        self.yA = self.pivots[0][1]
        self.xB = self.pivots[1][0]
        self.yB = self.pivots[1][1]
        width = math.sqrt(math.pow(self.xB - self.xA, 2) + math.pow(self.yB - self.yA, 2)) - 400
        self.x1 = (self.xA + self.xB) / 2
        self.y1 = (self.yA + self.yB) / 2
        if (self.isForward == True):
            self.dest = 1
        else:
            self.dest = -1
        if (width > 2 * self.r):
            if (math.fabs(self.yA - self.yB) < 2 * self.r):
                if (self.dest * (self.xA - self.xB) < 0.0):
                    self.xA = self.pivots[1][0]
                    self.yA = self.pivots[1][1]
                    self.xB = self.pivots[0][0]
                    self.yB = self.pivots[0][1]
                if ((self.yA - self.yB) > 0.0):
                    self.dirr = -1
                else:
                    self.dirr = 1
                self.x2 = self.x1
                self.y2 = self.y1
                if (self.dest == self.dirr):
                    self.x1 = self.x2 - self.dest * 300
                    self.y1 = self.y2 - self.dest * 300
                else:
                    self.x1 = self.x2 + self.dirr * 300
                    self.y1 = self.y2 + self.dest * 300
                self.x3 = self.xA
                self.y3 = self.yA + self.dirr * (self.r + 400)
            else:
                self.x2 = self.x1
                self.y2 = self.y1
                self.x1 = self.x2 - self.dest * 200
                self.y3 = self.y2
                self.x3 = self.x2 + self.dest * 200
        else:
            self.pathA(2)  # treat the two self.obstacles as a single big one


    def setData(self, isForward, robotLoc, numPivots, obstacles):
        self.isForward = isForward
        self.rX = robotLoc[0]
        self.rY = robotLoc[1]
        self.numPivots = numPivots
        self.obstacles = obstacles
        self.filter()
        self.getPivots()
        pass


    def getData(self): # Returns path of 3 points to move to
        if (self.numPivots == 0):
            self.moveStraight()
        if (self.numPivots == 1):
            self.pathA(1)
        if (self.numPivots == 2):
            self.pathB()
        else:
            pass
        #self.check() # Allows for obstacles in 1.5m radius only
        return [(self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3)]

    def check(self):
        self.dA = math.sqrt(math.pow(self.xA - self.rX, 2) + math.pow(self.yA - self.rY, 2))
        self.dB = math.sqrt(math.pow(self.xB - self.rX, 2) + math.pow(self.yB - self.rY, 2))
        if(self.dA > 1500 or self.dB > 1500):
            self.moveStraight()

    def getPivots(self):
        d = [[0.0, 0.0],
             [0.0, 0.0],
             [0.0, 0.0],
             [0.0, 0.0],
             [0.0, 0.0]]
        if self.numPivots > 2:
            min = 100000
            minI = 100
            for i in range(self.numPivots):
                d[i] = math.sqrt(math.pow(self.obstacles[i][0] - self.rX, 2) + math.pow(self.obstacles[i][1] - self.rY, 2))
                if d[i] < min:
                    minI = i
            self.pivots[0] = (self.obstacles[minI][0], self.obstacles[minI][1])
            del self.obstacles[minI]
            self.numPivots -= 1
            min = 100000
            minI = 100
            for i in range(self.numPivots):
                d[i] = math.sqrt(math.pow(self.obstacles[i][0] - self.rX, 2) + math.pow(self.obstacles[i][1] - self.rY, 2))
                if d[i] < min:
                    minI = i
            self.pivots[1] = (self.obstacles[minI][0], self.obstacles[minI][1])
            self.numPivots = 2

        elif self.numPivots == 2:
            min = 100000
            minI = 100
            for i in range(2):
                d[i] = math.sqrt(math.pow(self.obstacles[i][0] - self.rX, 2) + math.pow(self.obstacles[i][1] - self.rY, 2))
                if d[i] < min:
                    minI = i
            self.pivots[0] = (self.obstacles[minI][0], self.obstacles[minI][1])
            del self.obstacles[minI]
            self.pivots[1] = (self.obstacles[0][0], self.obstacles[0][1])

        elif self.numPivots == 1:
            self.pivots[0] = (self.obstacles[0][0], self.obstacles[0][1])

    def filter(self):
        if(self.numPivots > 5):
            t = self.numPivots - 5
            for i in range(t):
                del self.obstacles[5]

        temp = self.obstacles
        loc = 0
        for i in range(self.numPivots):
            if (self.obstacles[i][0] > self.rX):
                temp.insert(loc, [self.obstacles[i]])
                loc += 1
        for i in range(self.numPivots):
            del temp[0]
        self.numPivots = loc
        self.obstacles = temp
#
# End Pathfinding
#