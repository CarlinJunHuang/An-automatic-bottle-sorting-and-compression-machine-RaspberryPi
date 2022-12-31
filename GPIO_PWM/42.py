import RPi.GPIO as GPIO
import time

DIR42 = 19
PUL42 = 13


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup([PUL42, DIR42], GPIO.OUT)


# 别问我这里为什么是2085不是1600，我也很纳闷，试了很久，发现这个频率才刚好转够一圈 > . <
pwmPUL42 = GPIO.PWM(PUL42, 2085)  
pwmPUL42.start(0)

def rotate42(time42, direction):
    """
    旋转操作，需要指定旋转角度和方向
    :param angle: 正整型数据，旋转角度
    :param direction: 字符串数据，旋转方向，取值为："ccw"或"cw".ccw:逆时针旋转，cw:顺时针旋转
    :return:None
    """
    if direction == "left":
        GPIO.output(DIR42, GPIO.LOW)
    elif direction == "right":
        GPIO.output(DIR42, GPIO.HIGH)
    else:
        return
    pwmPUL42.ChangeDutyCycle(50)
    time.sleep(time42)
    pwmPUL42.ChangeDutyCycle(0)

time.sleep(1)
rotate42(3.7, "right")
# rotate42(1.7, "left")

pwmPUL42.stop()
GPIO.cleanup()
