import RPi.GPIO as GPIO
import time

class motorTwo:

    def __init__(self, motorDir1=26, motorDir2=24, motorPWM1=12, motorPWM2=13):

        self.pwm1 = motorPWM1
        self.pwm2 = motorPWM2
        self.dir1 = motorDir1
        self.dir2 = motorDir2

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        time.sleep(1)

        GPIO.setup(4,GPIO.OUT)
        GPIO.setup(self.pwm2, GPIO.OUT)
        GPIO.setup(self.pwm1, GPIO.OUT)
        GPIO.setup(self.dir1, GPIO.OUT)
        GPIO.setup(self.dir2, GPIO.OUT)
        GPIO.output(4,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(4,GPIO.LOW)
    

        self.motorSpeedLeft = 0.0
        self.motorSpeedRight = 0.0

        self.motor1 = GPIO.PWM(self.pwm1, 100)
        self.motor1.start(0)
        self.motor1.ChangeDutyCycle(0)

        self.motor2 = GPIO.PWM(self.pwm2, 100)
        self.motor2.start(0)
        self.motor2.ChangeDutyCycle(0)

        GPIO.output(self.dir1, GPIO.LOW)
        GPIO.output(self.dir2, GPIO.HIGH)



    def move(self):
            self.motor1.ChangeDutyCycle(self.motorSpeedLeft)
            self.motor2.ChangeDutyCycle(self.motorSpeedRight)

    def setLeftMotorSpeed(self, leftSpeed):

        self.motorSpeedLeft = leftSpeed

    def setRightMotorSpeed(self, rightSpeed):

        self.motorSpeedRight = rightSpeed

    def clear(self):
        self.motor1.ChangeDutyCycle(0)
        self.motor2.ChangeDutyCycle(0)
        GPIO.cleanup()




