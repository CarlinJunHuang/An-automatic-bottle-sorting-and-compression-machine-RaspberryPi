import RPi.GPIO as GPIO
import time

SM42freq = 19
SM42dirc = 26
SM86freq = 20
SM86dirc = 21
Inductive = 15
Infrared = 23
PulserA = 5
PulserB = 6
   
freq_StepMotor42 = 100
freq_StepMotor86 = 0
bottles = 0
mode = 0

def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Infrared, GPIO.IN)
    GPIO.setup(Inductive, GPIO.IN)
    GPIO.setup(SM42freq, GPIO.OUT)
    GPIO.setup(SM42dirc, GPIO.OUT)
    GPIO.setup(SM86freq, GPIO.OUT)
    GPIO.setup(SM86dirc, GPIO.OUT)

    GPIO.setup(PulserA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PulserB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    pass

def detect():
    global bottles, mode
    while(bottles < 8):     # 控制最大容量，8只是测试值
        if GPIO.input(Infrared) == 0:    # 红外传感器，检测到瓶子投入
            time.sleep(1)
            bottles += 1
            print ("A bottle is coming in!")
            if GPIO.input(Inductive) == 0:
                mode = 1
            else:
                mode = 0
                
def sorting():
    global mode
    
def motor(freq, dirc, SMfreq, SMdirc):
    