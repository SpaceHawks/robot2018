from arduino import *
from distance_sensor import *
from PID import PID

pid = PID(0.3, 0.1, 0.1)
pid.SetPoint=200
pid.setSampleTime(0.02)
#hieu
#s = DistanceSensors([29,31,33,35])
s = DistanceSensors([29])
arduino = Arduino("/dev/ttyS1")

while (True):
    try:
        s.update()
        #print(s.distances)
        dist = s.distances[0]
        if dist > 8000:
            print("No object seen")
            arduino.drive(0,0)
        elif dist <= 0:
            print("Sensor fail")
            arduino.drive(0,0)
        elif dist < 1000:
            pid.update(dist)
            drive = int(pid.output)
            if drive > 70:
                drive = 70
            if drive < -70:
                drive = -70
            drive = - drive
            if drive < 0:
                drive = drive%256
            if drive >= 0 and drive < 256:
                print(dist, drive)
                arduino.drive(drive, 0)
        else:
            pass
    except KeyboardInterrupt:
        arduino.drive(0,0)
        print("custom keyboard interupt")
        s.stop()
        break
    


