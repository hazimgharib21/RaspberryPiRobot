# Import and initialize our robot library
import RPi.GPIO as GPIO
import time
import os
buttonPin = 5
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
input_state = True
import numpy as np
Kp = 25.0
Kd = 50.0
Ki = 0.0

lost = False
previousAvgSensor = 0.0
deviation = 4.0
error = 0.0
previousError = 0.0
totalError = 0.0

pwmLeft = 0.0
pwmRight = 0.0

maxSpeed = 30

import motor
import irSensor

import PID

motor = motor.motor()
lineSensor = irSensor.irSensor(11,9,10,22,27)
lineSensor.setSampleTime(0.01)
pid = PID.PID(Kp,Ki,Kd)
pid.setPoint(4.0)
pid.setSampleTime(0.01)

try:
    while input_state:

        input_state = GPIO.input(buttonPin)

        activeSensor = 0.0
        totalSensor = 0
    
        #Get sensor data
        lineSensor.update()
        sensors = lineSensor.output

        #loop through the sensor
        i = 0
        for sensor in sensors:
            i += 1
            if sensor == 1:
                activeSensor += 1
            totalSensor += sensor * (i+1)

        if activeSensor != 0:
            maxSpeed = 70
            pid.setKp(25.0)
            pid.setKd(50.0)

            deviation = 4.0
            avgSensor = totalSensor/activeSensor
            lost = False
        else:
            
            
            if lost == False:



                #motor.setLeftMotorSpeed(0)
                #motor.setRightMotorSpeed(0)
                #motor.move()
                #time.sleep(1)

                if previousError < 0:
                    deviation = 4.0
                else:
                    deviation = -4.0

                maxSpeed = 20
                pid.setKp(5.0)
                pid.setKd(00.0)


                
                lost = True
            avgSensor = 0
        
    
        deltaError = error - previousError
        previousError = error # save previous error for differential
        error = avgSensor - deviation # Count how much robot deviate from center
            
        pid.setPoint(deviation)
        pid.update(avgSensor)
        power = pid.output

        #power = (Kp * error) + (Kd * deltaError)
       # if( power > maxSpeed):
       #     power = maxSpeed
       # if( power < -maxSpeed):
       #     power = -maxSpeed

        if(power<0):
            pwmRight = maxSpeed - abs(power)
            pwmLeft = maxSpeed + abs(power)
        else:
            pwmRight = maxSpeed + power
            pwmLeft = maxSpeed - power
    
        pwmRight = pwmRight + 3

        if(pwmRight > 100):
            pwmRight = 100
        elif(pwmRight < -100):
            pwmRight = -100
        if(pwmLeft > 100):
            pwmLeft = 100
        elif(pwmLeft < -100):
            pwmLeft = -100
            
        #print str(pwmLeft) + "\t" + str(pwmRight) + "\t" + str(power) + "\t" + str(lost)

        motor.setLeftMotorSpeed(pwmLeft)
        motor.setRightMotorSpeed(pwmRight)

        motor.move()



finally:
    print "Goodbye :)"
    motor.clear()
    os.system('sudo halt')
    time.sleep(0.05)
