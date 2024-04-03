# Day2 project 4-1
import RPi.GPIO as GPIO
import time
from time import sleep, perf_counter
from threading import Thread

# 초음파 센서 설정
Tr = 11
Ec = 8

# Line tracking 센서 설정
line_pin_right = 19
line_pin_middle = 16
line_pin_left = 20

# LED 설정
pin_led_1 = 5
pin_led_2 = 6
pin_led_3 = 13

def setup():
    GPIO.setwarnings(False)
    # 초음파
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Tr, GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(Ec, GPIO.IN)
    # Line tracer
    GPIO.setup(line_pin_right,GPIO.IN)
    GPIO.setup(line_pin_middle,GPIO.IN)
    GPIO.setup(line_pin_left,GPIO.IN)
    # LED
    GPIO.setup(pin_led_1, GPIO.OUT)
    GPIO.setup(pin_led_2, GPIO.OUT)
    GPIO.setup(pin_led_3, GPIO.OUT)

def checkdist():
    while True:
        GPIO.output(Tr, GPIO.LOW)
        sleep(0.000002)
        GPIO.output(Tr, GPIO.HIGH)
        sleep(0.000015)
        GPIO.output(Tr, GPIO.LOW)
        while not GPIO.input(Ec):
            pass
        t1 = time.time()
        while GPIO.input(Ec):
            pass
        t2 = time.time()
        dist = (t2 - t1) * 340 / 2
        print("Distance: %.2f cm" % (dist * 100))
        sleep(1)

def checkdist():
    while True:
        GPIO.output(Tr, GPIO.LOW)
        sleep(0.000002)
        GPIO.output(Tr, GPIO.HIGH)
        sleep(0.000015)
        GPIO.output(Tr, GPIO.LOW)
        while not GPIO.input(Ec):
            pass
        t1 = time.time()
        while GPIO.input(Ec):
            pass
        t2 = time.time()
        dist = (t2 - t1) * 340 / 2
        print("Distance: %.2f cm" % (dist * 100))
        sleep(1)

def led_control():
    soft_pwm = GPIO.PWM(pin_led_1, 100)
    soft_pwm.start(50)
    while True:
        soft_pwm.ChangeDutyCycle(100)
        sleep(1)
        soft_pwm.ChangeDutyCycle(50)
        sleep(1)
        soft_pwm.ChangeDutyCycle(0)
        sleep(1)

if __name__ == '__main__':
    try:
        setup()
        t1 = Thread(target=checkdist)
        t2 = Thread(target=line_tracking)
        t3 = Thread(target=led_control)
        
        t1.start()
        t2.start()
        t3.start()
        
        t1.join()
        t2.join()
        t3.join()
        
    except KeyboardInterrupt:
        GPIO.cleanup()

