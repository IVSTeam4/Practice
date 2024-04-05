import RPi.GPIO as GPIO
import time

from time import sleep, perf_counter
from threading import Thread

from rpi_ws281x import *
from random import *

Tr = 11
Ec = 8

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(Tr, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Ec, GPIO.IN)


#set dist func
def checkdist():
    for i in range(5):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Tr, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(Ec, GPIO.IN)
        GPIO.output(Tr, GPIO.LOW)
        time.sleep(0.000002)
        GPIO.output(Tr, GPIO.HIGH)
        time.sleep(0.000015)
        GPIO.output(Tr, GPIO.LOW)
        while not GPIO.input(Ec):
            pass
        t1 = time.time()
        while GPIO.input(Ec):
            pass
        t2 = time.time()
        dist = (t2 - t1) * 340 / 2
        if dist > 9 and i < 4:
            continue
        else:
            return (t2 - t1) * 340 / 2

def dist_calc():
    distance = checkdist() * 100
    return distance
    %print("%.2f cm" % distance)

#Test Code - Thread
#thr_1 = Thread(target=dist_calc)
#thr_1.start()
#time.sleep(1)
