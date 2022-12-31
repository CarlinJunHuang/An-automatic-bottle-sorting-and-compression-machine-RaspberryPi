import RPi.GPIO as GPIO
import time

IN5 = 15

bottles = 0

def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IN5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    pass

def detect():
    global bottles
    while(bottles < 8):
        if GPIO.input(IN5) == 1:
            print ("A bottle is coming in!")
            time.sleep(0.5)
            bottles += 1
        GPIO.setup(IN5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        time.sleep(3)
        
time.sleep(1)
init()
detect()
GPIO.cleanup()
