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

speed = 99

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
        keyp = readkey()
        print(keyp)
        if keyp == 'w':
            motorForward(speed)
        elif keyp == 's':
            motorReverse(speed)
        elif keyp == 'a':
            motorLeft(speed)
        elif keyp == 'd':
            motorRight(speed)
        elif keyp == '.' or keyp == '>':
            speed = min(100, speed+10)
            print 'Speed+', speed
        elif keyp == ',' or keyp == '<':
            speed = max(0, speed-10)
            print 'Speed-', speed
        elif keyp == ' ':
            motorStop()
            print 'Stop'
        elif keyp == 'q':
            break

except KeyboardInterrupt:
    pass

finally:
    pass



