import RPi.GPIO as GPIO
from time import sleep

# Direction pin from controller
DIR = 18
# Step pin from controller
STEP = 12
# 0/1 used to signify clockwise or counterclockwise.
CW = 1
CCW = 0

GPIO.setwarnings(False)
# Setup pin layout on PI
GPIO.setmode(GPIO.BCM)

# Establish Pins in software
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

# Set the first direction you want it to spin
GPIO.output(DIR, CW)

try:
	# Run forever.
	while True:

		"""Change Direction: Changing direction requires time to switch. The
		time is dictated by the stepper motor and controller. """
		sleep(1)
		# Esablish the direction you want to go
		#GPIO.output(DIR,CW)

		# Run for 200 steps. This will change based on how you set you controller
		for x in range(25000):

			# Set one coil winding to high
			GPIO.output(STEP,GPIO.HIGH)
			# Allow it to get there.
			sleep(.01) # Dictates how fast stepper motor will run
			# Set coil winding to low
			GPIO.output(STEP,GPIO.LOW)
			sleep(.01) # Dictates how fast stepper motor will run
                                                                                                                                
		#"""Change Direction: Changing direction requires time to switch. The
		#time is dictated by the stepper motor and controller. """
		#sleep(1.0)
		#GPIO.output(DIR,CCW)
		#for x in range(200):
			#GPIO.output(STEP,GPIO.HIGH)
			#sleep(0.3)
			#GPIO.output(STEP,GPIO.LOW)
			#sleep(0.3)

# Once finished clean everything up
except KeyboardInterrupt:
	print("cleanup")
	GPIO.cleanup()