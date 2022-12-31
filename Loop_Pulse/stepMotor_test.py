import RPi.GPIO as GPIO
import time

IN1 = 13
IN2 = 26
IN3 = 20
IN4 = 21

delay = 0.002 #控制转速，增大则转速变慢  最快稳定转速大概为0.0017（这个速度想要转的话需要预热，不然转不起来）
steps = 128  #控制转动时长

def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)
    
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
        
init()
time.sleep(5)
step(False)
setStep(0, 0, 0, 0)  #清零停止
time.sleep(3)
step(True)
time.sleep(3)
GPIO.cleanup()

    