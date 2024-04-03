import RPi.GPIO as GPIO
import time

from time import sleep, perf_counter
from threading import Thread

from rpi_ws281x import *
from random import *

# LED strip configuration:
LED_COUNT      = 12      # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

#set led func
left_R = 22
left_G = 23
left_B = 24
right_R = 10
right_G = 9
right_B = 25
on = GPIO.LOW
off = GPIO.HIGH

ledfunc = ''
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
    print("%.2f cm" % distance)




def both_on():
    GPIO.output(left_R, on)
    GPIO.output(left_G, on)
    GPIO.output(left_B, on)
    GPIO.output(right_R, on)
    GPIO.output(right_G, on)
    GPIO.output(right_B, on)


def setup():  # initialization
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(left_R, GPIO.OUT)
    GPIO.setup(left_G, GPIO.OUT)
    GPIO.setup(left_B, GPIO.OUT)
    GPIO.setup(right_R, GPIO.OUT)
    GPIO.setup(right_G, GPIO.OUT)
    GPIO.setup(right_B, GPIO.OUT)
    both_off()


def both_off():
    GPIO.output(left_R, off)
    GPIO.output(left_G, off)
    GPIO.output(left_B, off)
    GPIO.output(right_R, off)
    GPIO.output(right_G, off)
    GPIO.output(right_B, off)
def side_on(side_X):
    GPIO.output(side_X, on)
def side_off(side_X):
    GPIO.output(side_X, off)
def police(police_time):
    for i in range (1,police_time):
        for i in range (1,3):
            side_on(left_R)
            side_on(right_B)
            time.sleep(0.1)
            both_off()
            side_on(left_B)
            side_on(right_R)
            time.sleep(0.1)
            both_off()
        for i in range (1,5):
            side_on(left_R)
            side_on(right_B)
            time.sleep(0.3)
            both_off()
            side_on(left_B)
            side_on(right_R)
            time.sleep(0.3)
            both_off()
def red():
    side_on(right_R)
    side_on(left_R)
def green():
    side_on(right_G)
    side_on(left_G)
def blue():
    side_on(right_B)
    side_on(left_B)

def yellow():
    red()
    green()

def pink():
    red()
    blue()

def cyan():
    blue()
    green()

def LED_seq():
    setup()
    police(4)
    both_on()
    time.sleep(1)
    both_off()
    yellow()
    time.sleep(5)
    both_off()
    pink()
    time.sleep(5)
    both_off()
    cyan()
    time.sleep(5)
    both_off()

if __name__ == '__main__':
    thr_1 = Thread(target=dist_calc)
    thr_2 = Thread(target=LED_seq)
    thr_1.start()
    thr_2.start()
    while True:
        time.sleep(1)
