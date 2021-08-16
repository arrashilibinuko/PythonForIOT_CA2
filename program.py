import RPI.GPIO as GPIO
from time import sleep
import time
from timeit import default_timer as timer
import requests
from datetime import datetime

# LED Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(24, GPIO.OUT)

# PIR setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.IN)
sleep(5)
PIR_state = 0

# DC motor setup
GPIO.setmode(GPIO.BCM)  
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.OUT)  
PWM1 = GPIO.PWM(23, 100)

# Buzzer Setup
GPIO.setmode(GPIO.BCM)  
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)  
PWM2 = GPIO.PWM(18, 100)  

#Defining variable
buzzCount = 0
start = 0

while (True):
    if GPIO.input(17):
        if PIR_state == 0:
            print('no person detected')
            # Start off
            PWM1.start(0)
            PWM2.start(0)
            GPIO.output(24, 0)
            if(buzzCount == 1):
                print(timer() - start)
                now = datetime.now()
                dt_string = now.strftime("%d%m%Y %H:%M%S")
                usage = timer()-start
                #Should send request to thingspeak here
                buzzCount = 0
            # End off
            PIR_state = 1
    else:
        if PIR_state == 1:
            print('person detected')
            # Start on
            PWM1.start(100)
            if(buzzCount == 0):
                PWM2.start(80)
                start = timer()
                sleep(0.2)
                PWM2.start(0)
                buzzCount = 1
            # End on
            PIR_state = 0
    sleep(0.2)
