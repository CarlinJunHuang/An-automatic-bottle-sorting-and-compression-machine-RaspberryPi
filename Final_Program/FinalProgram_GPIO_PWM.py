# HUANG JUN
import RPi.GPIO as GPIO
import time

IrPin  = 21
count = 0
countPC = 0
DIR86 = 18
PUL86 = 12
promixity_switchPin = 20

# 别问我这里为什么是2085不是1600，我也很纳闷，试了很久，发现这个频率才刚好转够一圈 > . <
speed86 = 2085


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)      # Numbers GPIOs by physical location
GPIO.setup([PUL86, DIR86], GPIO.OUT)
pwmPUL = GPIO.PWM(PUL86, 10*speed86) 

def setup():
    GPIO.setup(IrPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(promixity_switchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    pwmPUL.start(0)


def cnt(ev=None):
	global count
	count += 1
	print ('Received infrared. cnt = ', count)
	GPIO.add_event_detect(promixity_switchPin, GPIO.FALLING, callback=promixityCallback)
	promixityDetect()
	

def rotate(time86, direction):
    GPIO.remove_event_detect(IrPin)
    """
    旋转操作，需要指定旋转角度和方向
    :param angle: 正整型数据，旋转角度
    :param direction: 字符串数据，旋转方向，取值为："ccw"或"cw".ccw:逆时针旋转，cw:顺时针旋转
    :return:None
    """
    if direction == "ccw":
        GPIO.output(DIR86, GPIO.LOW)
    elif direction == "cw":
        GPIO.output(DIR86, GPIO.HIGH)
    else:
        return
    pwmPUL.ChangeDutyCycle(50)
    time.sleep(time86)
    pwmPUL.ChangeDutyCycle(0)
    GPIO.add_event_detect(IrPin, GPIO.FALLING, callback=cnt)
    
def promixityDetect():
    
    GPIO.remove_event_detect(IrPin)
    GPIO.output(DIR86, GPIO.LOW)     # "ccw"
    pwmPUL.ChangeDutyCycle(50)
    time.sleep(5)
    pwmPUL.ChangeDutyCycle(0)
    GPIO.add_event_detect(IrPin, GPIO.FALLING, callback=cnt)
    GPIO.remove_event_detect(promixity_switchPin)
    
def compressPrepared():
    rotate(4, "cw")
    
def promixityCallback():
    GPIO.remove_event_detect(promixity_switchPin)
    global countPC
    countPC += 1
    print ('Received promixity. cnt = ', count)
    compressPrepared()
    
def loop():
	GPIO.add_event_detect(IrPin, GPIO.FALLING, callback=cnt) # wait for falling
	while True:
		pass   # Don't do anything

def destroy():
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()



