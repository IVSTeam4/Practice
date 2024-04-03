import RPi.GPIO as GPIO
import time
Tr = 11
Ec = 8

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(Tr, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Ec, GPIO.IN)

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
        dist = (t2-t1)*340/2
        if dist > 9 and i < 4:
            continue
        else:
            return (t2-t1)*340/2

if __name__ == '__main__':
    while True:
        distance = checkdist()*100
        print("%.2f cm" %distance)
        time.sleep(1)
