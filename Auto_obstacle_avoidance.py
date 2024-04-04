# Auto Obstacle Avoidance PiCar-B 
# Adeept - https://youtu.be/lUN6xrSA3BE?feature=shared

import ultra
import move
import time
import Adafruit_PCA9685
import RPIservo
import os

curpath = os.path.realpath(__file__)
thisPath = '/' + os.path.dirname(curpath)

def num_import_int(initial):
    global r
    with open(thisPath+"/RPIservo.py") as f: #RPIservo.py 파일은 확인해봐야 함 -> 우리가 가지고 있는 servo.py 사용?
        for line in f.readlines():
            if(line.find(initial) == 0):
                r = line
    begin = len(list(initial))
    snum = r[begin:]
    n = int(sum)
    return n


# pwm 
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

pwm0_direction = 1
pwm0_init = num_import_int('init_pwm0 = ')
pwm0_max = 520  # 상황에 따라 변경?
pwm0_min = 100  # 상황에 따라 변경?
pwm0_pos = pwm0_init

pwm1_direction = 1
pwm1_init = num_import_int('init_pwm1 = ')
pwm1_max = 520  # 상황에 따라 변경?
pwm1_min = 100  # 상황에 따라 변경?
pwm1_pos = pwm1_init

pwm2_direction = 1
pwm2_init = num_import_int('init_pwm2 = ')
pwm2_max = 520  # 상황에 따라 변경?
pwm2_min = 100  # 상황에 따라 변경?
pwm2_pos = pwm2_init


scGear = RPIservo.ServoCtrl() # Initialize the servo control object scGear
scanNum = 3     # Number of sections for scanning
scanPos = 1     # 초음파 스캐닝에서 next position을 위한 기준
scanDir = 1     # Direction for robot scanning (1: left, -1: right)
scanList = []   # Distance of obstacles in 3 directions
scanServo = 1   # serial number of the servo
scanRange = 100 # Angle range for servo scanning
rangeKeep = 0.7 # Threshold of obstacle 거리

while True:
    # rotation - left, right, center 
    if scanPos == 1:
        pwm.set_pwm(scanServo, 0, pwm1_init + scanRange)
        time.sleep(0.3)
        scanList[0] = ultra.checkdist()
    elif scanPos == 2:
        pwm.set_pwm(scanServo, 0, pwm1_init + scanRange)
        time.sleep(0.3)
        scanList[1] = ultra.checkdist()
    elif scanPos == 3:
        pwm.set_pwm(scanServo, 0, pwm1_init + scanRange)
        time.sleep(0.3)
        scanList[2] = ultra.checkdist()

    # 초음파 센서 - 장애물과의 거리 scanning
    scanPos += scanDir # Update scanPos

    if scanPos > scanNum or scanPos < 1: # -1인가..?
        # Replace the scan direction
        if scanDir == 1: scanDir = -1
        elif scanDir == -1: scanDir = 1

        # Restore scanned location
        scanPos += scanDir*2
    print(scanList)

    # If the distance of the nearest obstacle in front is less than the threshold
    if min(scanList) < rangeKeep:
        # 왼쪽 장애물
        if scanList.index(min(scanList)) == 0:
            # Turn right
            scGear.moveAngle(2, -30)
        # 정면 장애물
        if scanList.index(min(scanList)) == 1:
            # 어느쪽으로 더 큰지 확인
            if scanList[0] < scanList[2]:
                # Go to right
                scGear.moveAngle(2, -45)
            else:
                # Go to left
                scGear.moveAngle(2, 45)
        # 오른쪽 장애물
        elif scanList.index(min(scanList)) == 2:
            # Turn left
            scGear.moveAngle(2, 30)
        # 뒤로 가기
        if max(scanList) < rangeKeep or min(scanList) < rangeKeep/3:
            move.motor_left(1, 1, 80)
            move.motor_right(1, 1, 80)
        else:
            # move along
            move.motor_left(1, 0, 80)
            move.motor_right(1, 0, 80)

       

