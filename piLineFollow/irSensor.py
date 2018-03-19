import time
import RPi.GPIO as GPIO

class irSensor:

    def __init__(self,sensor1=11,sensor2=9,sensor3=10,sensor4=22,sensor5=27):

        self.s1 = sensor1
        self.s2 = sensor2
        self.s3 = sensor3
        self.s4 = sensor4
        self.s5 = sensor5

        self.sample_time = 0.00
        self.current_time = time.time()
        self.last_time = self.current_time

        self.ds1 = 0
        self.ds2 = 0
        self.ds3 = 0
        self.ds4 = 0
        self.ds5 = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        time.sleep(1)

        GPIO.setup(4,GPIO.OUT)
        GPIO.setup(self.s1, GPIO.IN)
        GPIO.setup(self.s2, GPIO.IN)
        GPIO.setup(self.s3, GPIO.IN)
        GPIO.setup(self.s4, GPIO.IN)
        GPIO.setup(self.s5, GPIO.IN)
        GPIO.output(4,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(4,GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(4,GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(4,GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(4,GPIO.HIGH)
        
        self.delta_time = 0.0

        self.output = [self.ds1,self.ds2,self.ds3,self.ds4,self.ds5]

    def update(self):

        self.current_time = time.time()
        self.delta_time = self.current_time - self.last_time

        if(self.delta_time >= self.sample_time):
            
            self.last_time = self.current_time

            self.ds1 = GPIO.input(self.s1)
            self.ds2 = GPIO.input(self.s2)
            self.ds3 = GPIO.input(self.s3)
            self.ds4 = GPIO.input(self.s4)
            self.ds5 = GPIO.input(self.s5)

            self.output = [self.ds1,self.ds2,self.ds3,self.ds4,self.ds5]

    def setSampleTime(self, sampleTime):
        self.sample_time = sampleTime





