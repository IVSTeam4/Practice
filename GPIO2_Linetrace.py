import RPi.GPIO as GPIO

line_pin_right = 19
line_pin_middle = 16
line_pin_left = 20
def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(line_pin_right,GPIO.IN)
    GPIO.setup(line_pin_middle,GPIO.IN)
    GPIO.setup(line_pin_left,GPIO.IN)
def run():
    status_right = GPIO.input(line_pin_right)
    status_middle = GPIO.input(line_pin_middle)
    status_left = GPIO.input(line_pin_left)
    print('LF3: %d LF2: %d LF1: %d\n'%(status_right,status_middle,status_left))
if __name__ == '__main__':
    try:
        setup()
        while 1:
            run()
        pass
    #키보드 입력 발생 시 종료
    except KeyboardInterrupt:
        GPIO.cleanup()