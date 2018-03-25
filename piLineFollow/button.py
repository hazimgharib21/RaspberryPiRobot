import RPi.GPIO as GPIO
import time
import os

buttonPin = 5
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
last_state = True
input_state = True
while True:
    input_state = GPIO.input(buttonPin)
    if(not input_state):
        print("Shutdown")
        time.sleep(0.05)

GPIO.cleanup()
