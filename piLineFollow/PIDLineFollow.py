#==============================================================
# Import python library 
import numpy as np
from threading import Thread

#==============================================================
# Import our robot library

import motor
import irSensor
import keyboardInput
import PID

# initialize PID constant variable
global P
global I
global D

P = 0.0
I = 0.0 
D = 0.0

# initialize pid class
pid = PID.PID(P,I,D)
pid.SetPoint = 0.0
pid.setSampleTime(0.0)

# initialize motor class
motor = motor.motor()

# initialize keyboard input class
userInput = keyboardInput.keyboardInput()

# initialize irSensor class
lineSensor = irSensor.irSensor(11,9,10,22,27)

# initialize pid data variable
global PD_value
global error

PD_value = 0
error = 0

# initialize sensor data variable
global s1
global s2
global s3
global s4
global s5
global hold
hold = False

s1 = 0
s2 = 0
s3 = 0
s4 = 0
s5 = 0

# initialize motor data variable
global leftMotorSpeed
global rightMotorSpeed
global initialMotorSpeed
global maxSpeed

leftMotorSpeed = 0.0
rightMotorSpeed = 0.0
initialMotorSpeed = 40
maxSpeed = 100

# initialize other variable
global EXIT
global char
EXIT = False
char = ''




#==================================================================
# Function for line follow

def getSensors():
    global error
    global s1
    global s2
    global s3
    global s4
    global s5
    global initialSpeed
    global hold

    lineSensor.update()

    sensorsData = lineSensor.output

    s1 = sensorsData[0]
    s2 = sensorsData[1]
    s3 = sensorsData[2]
    s4 = sensorsData[3]
    s5 = sensorsData[4]

    #print(str(s1) + " " + str(s2) + " " + str(s3) + " " + str(s4) + " " + str(s5))

    while hold:
        if s3 == 1:
            hold = False
            break

    if not s1 and not s2 and s3 and not s4 and not s5:
        error = 0
    elif not s1 and not s2 and s3 and s4 and not s5:
        error = 2
    elif not s1 and not s2 and s3 and s4 and s5:
        error = 5
       # hold=True
    elif not s1 and s2 and s3 and s4 and s5:
        error = 5
       # hold=True
    elif not s1 and not s2 and not s3 and s4 and not s5:
        error = 2
    elif not s1 and not s2 and not s3 and s4 and s5:
        error = 3
    elif not s1 and not s2 and not s3 and not s4 and s5:
        error = 4
    elif not s1 and s2 and s3 and not s4 and not s5:
        error = -1
    elif s1 and s2 and s3 and not s4 and not s5:
        error = -5
       # hold=True
    elif s1 and s2 and s3 and s4 and not s5:
        error = -5
       # hold=True
    elif not s1 and s2 and not s3 and not s4 and not s5:
        error = -2
    elif s1 and s2 and not s3 and not s4 and not s5:
        error = -3
    elif s1 and not s2 and not s3 and not s4 and not s5:
        error = -4
    elif not s1 and not s2 and not s3 and not s4 and not s5:
        if error > 0:
            error = 4
        else:
            error = -4

 

def pidCalculation():
    global error
    global PD_value

    pid.update(error)
    PD_value = pid.output

def motorControl():
    global leftMotorSpeed
    global initialMotorSpeed
    global PD_value
    global rightMotorSpeed
    leftMotorSpeed = initialMotorSpeed - PD_value;
    rightMotorSpeed = initialMotorSpeed + PD_value;

    #leftMotorSpeed = leftMotorSpeed + 10

    leftMotorSpeed = np.clip(leftMotorSpeed, 0, maxSpeed)
    rightMotorSpeed = np.clip(rightMotorSpeed, 0, maxSpeed)

    motor.setLeftMotorSpeed(leftMotorSpeed)
    motor.setRightMotorSpeed(rightMotorSpeed)
    motor.move()
 
#==================================================================
# Function and classes for multithread

def lineFollowRoutine():
    getSensors()
    pidCalculation()
    motorControl()

class lineFollowProgram:
    def __init__(self):
        self._running = True

    def terminate(self):
        motor.clear()
        self._running = False

    def run(self):
        while self._running:
            lineFollowRoutine()

def manualTuningRoutine():

    global EXIT
    global P
    global D
    global I
    global leftMotorSpeed
    global rightMotorSpeed

    keyp = userInput.readkey()

    if keyp == 'q':
        EXIT = True
    elif keyp == 'p':
        P = P + 0.5
        pid.setKp(P)
        print("P = " + str(P) + "\tI = " + str(I) + "\tD = " + str(D))
    elif keyp == 'o':
        P = P - 0.5
        pid.setKp(P)
        print("P = " + str(P) + "\tI = " + str(I) + "\tD = " + str(D))
    elif keyp == 'k':
        D = D - 0.5
        pid.setKd(D)
        print("P = " + str(P) + "\tI = " + str(I) + "\tD = " + str(D))
    elif keyp == 'l':
        D = D + 0.5
        pid.setKd(D)
        print("P = " + str(P) + "\tI = " + str(I) + "\tD = " + str(D))
    elif keyp == 'n':
        I = I - 0.01
        pid.setKi(I)
        print("P = " + str(P) + "\tI = " + str(I) + "\tD = " + str(D))
    elif keyp == 'm':
        I = I + 0.01
        pid.setKi(I)
        print("P = " + str(P) + "\tI = " + str(I) + "\tD = " + str(D))

class manualTuningProgram():
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        while self._running:
            manualTuningRoutine()
lineFollow = lineFollowProgram()
manualTuning = manualTuningProgram()
def startLineFollowThread():
    #lineFollow = lineFollowProgram()
    lineFollowThread = Thread(target=lineFollow.run)
    lineFollowThread.start()

def startManualTuningThread():
    #manualTuning = manualTuningProgram()
    manualTuningThread = Thread(target=manualTuning.run)
    manualTuningThread.start()

#==================================================================
# main while loop


startLineFollowThread()
startManualTuningThread()


while not EXIT:
    #print(str(leftMotorSpeed) + "\t" + str(rightMotorSpeed))
    pass

lineFollow.terminate()
manualTuning.terminate()
motor.clear()


