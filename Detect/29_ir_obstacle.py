#!/usr/bin/env python3
import RPi.GPIO as GPIO

ObstaclePin = 21

def setup():
	GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
	GPIO.setup(21,GPIO.IN)

def loop():
	while True:
		if (0 == GPIO.input(ObstaclePin)):
			print ("Detected Barrier!")
			

def destroy():
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

