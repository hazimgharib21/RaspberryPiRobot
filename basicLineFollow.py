#==============================================================
# Import use to read character
import sys
import tty
import termios

#==============================================================
# Import use for GPIO
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#==============================================================
# Setup motor
pwm2 = 13
pwm1 = 12
dir2 = 24
dir1 = 26

GPIO.setup(pwm2, GPIO.OUT)
GPIO.setup(pwm1, GPIO.OUT)
GPIO.setup(dir2, GPIO.OUT)
GPIO.setup(dir1, GPIO.OUT)

sleep(1)
motor1 = GPIO.PWM(pwm1, 100)
motor1.start(0)
motor1.ChangeDutyCycle(0)

motor2 = GPIO.PWM(pwm2, 100)
motor2.start(0)
motor2.ChangeDutyCycle(0)

#==============================================================
# Setup IR sensor
sensor1 = 11
sensor2 = 9
sensor3 = 10
sensor4 = 22
sensor5 = 27

GPIO.setup(sensor1, GPIO.IN)
GPIO.setup(sensor2, GPIO.IN)
GPIO.setup(sensor3, GPIO.IN)
GPIO.setup(sensor4, GPIO.IN)
GPIO.setup(sensor5, GPIO.IN)

#==============================================================
# Read single character

def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if ch == '0x03':
        raise KeyboardInterrupt
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65) # 16=Up, 17=Down, 18=Right, 19=Left

speed = 10

#================================================================
# Motor direction function

def motorRight(spd):
    GPIO.output(dir1, GPIO.LOW)
    GPIO.output(dir2, GPIO.LOW)
    motor1.ChangeDutyCycle(spd)
    motor2.ChangeDutyCycle(spd)
    
def motorLeft(spd):
    GPIO.output(dir1, GPIO.HIGH)
    GPIO.output(dir2, GPIO.HIGH)
    motor1.ChangeDutyCycle(spd)
    motor2.ChangeDutyCycle(spd)

def motorForward(spd):
    GPIO.output(dir1, GPIO.LOW)
    GPIO.output(dir2, GPIO.HIGH)
    motor1.ChangeDutyCycle(spd)
    motor2.ChangeDutyCycle(spd)

def motorForward(spdLeft,spdRight):
    GPIO.output(dir1, GPIO.LOW)
    GPIO.output(dir2, GPIO.HIGH)
    motor1.ChangeDutyCycle(spdLeft + speed)
    motor2.ChangeDutyCycle(spdRight + speed)

def motorReverse(spd):
    GPIO.output(dir1, GPIO.HIGH)
    GPIO.output(dir2, GPIO.LOW)
    motor1.ChangeDutyCycle(spd)
    motor2.ChangeDutyCycle(spd)

def motorStop():
    GPIO.output(dir1, GPIO.LOW)
    GPIO.output(dir2, GPIO.LOW)
    motor1.ChangeDutyCycle(0)
    motor2.ChangeDutyCycle(0)

#==================================================================
# main while loop

try:
    while True:
        #keyp = readkey()
        #if keyp == 'q':
        #    break

        s1 = GPIO.input(sensor1)
        s2 = GPIO.input(sensor2)
        s3 = GPIO.input(sensor3)
        s4 = GPIO.input(sensor4)
        s5 = GPIO.input(sensor5)

        #print(str(s1) + " " + str(s2) + " " + str(s3) + " " + str(s4) + " " + str(s5))

 
        if s1 and not s2 and not s3 and not s4 and not s5:
            print("left 1")
            motorForward(0,40)
        elif s1 and s2 and not s3 and not s4 and not s5:
            print("left 2")
            motorForward(5,40)
        elif s1 and s2 and s3 and not s4 and not s5:
            print("left 3")
            motorForward(7.5,40)
        elif not s1 and s2 and not s3 and not s4 and not s5:
            print("left 4")
            motorForward(9,40)
        elif not s1 and s2 and s3 and not s4 and not s5:
            print("left 5")
            motorForward(14,40)
        elif not s1 and not s2 and not s3 and not s4 and s5:
            print("right 1")
            motorForward(40,0)
        elif not s1 and not s2 and not s3 and s4 and s5:
            print("right 2")
            motorForward(40,5)
        elif not s1 and not s2 and s3 and s4 and s5:
            print("right 3")
            motorForward(40,7.5)
        elif not s1 and not s2 and not s3 and s4 and not s5:
            print("right 4")
            motorForward(40,9)
        elif not s1 and not s2 and s3 and s4 and not s5:
            print("right 5")
            motorForward(40,14)
        elif not s1 and not s2 and s3 and not s4 and not s5:
            print("straight 1")
            motorForward(40,40)
        elif not s1 and s2 and s3 and s4 and not s5:
            print("straight 2")
            motorForward(40,40)

except KeyboardInterrupt:
    pass

finally:
    pass



