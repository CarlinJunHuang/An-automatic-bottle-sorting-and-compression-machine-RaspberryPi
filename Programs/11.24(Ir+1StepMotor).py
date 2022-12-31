import RPi.GPIO as GPIO
import time

# 红外+树莓派步进电机

IN1 = 19
IN2 = 26
IN3 = 20
IN4 = 21
IN5 = 15
IN6 = 23

    
delay = 0.002 #控制转速，增大则转速变慢  最快稳定转速大概为0.0017（这个速度想要转的话需要预热，不然转不起来）
steps = 128  #控制转动时长
bottles = 0
mode = 0

def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)
    GPIO.setup(IN6, GPIO.IN)
    GPIO.setup(IN5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    pass

def detect():
    global bottles, mode
    while(bottles < 8):
        if GPIO.input(IN5) == 0:    
            print ("hahah")
            time.sleep(1)
        
        
        
        
def setStep(h1, h2, h3, h4):
    GPIO.output(IN1, h1)
    GPIO.output(IN2, h2)
    GPIO.output(IN3, h3)
    GPIO.output(IN4, h4)
    
def stop():
    setStep(0,0,0,0)
    
def step(direction):
    if direction == 1:
        for i in range(0, steps):
            setStep(1, 0, 0, 0)
            time.sleep(delay)
            setStep(0, 1, 0, 0)
            time.sleep(delay)
            setStep(0, 0, 1, 0)
            time.sleep(delay)
            setStep(0, 0, 0, 1)
            time.sleep(delay)
    else:
        for i in range(0, steps):
            setStep(0, 0, 0, 1)
            time.sleep(delay)
            setStep(0, 0, 1, 0)
            time.sleep(delay)
            setStep(0, 1, 0, 0)
            time.sleep(delay)
            setStep(1, 0, 0, 0)
            time.sleep(delay)
        
        
time.sleep(1)
init()
detect()
GPIO.cleanup()
