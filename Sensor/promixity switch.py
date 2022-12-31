import RPi.GPIO as GPIO
import time

promixity_switch = 14

count = 0

def cnt(ev=None):
	global count
	count += 1
	print ('Received infrared. cnt = ', count)


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# GPIO.setup(promixity_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.add_event_detect(promixity_switch, GPIO.FALLING, callback=cnt)
GPIO.setup(promixity_switch, GPIO.IN)
if GPIO.input(promixity_switch) == 0:
    cnt()
time.sleep(1)
GPIO.cleanup()



