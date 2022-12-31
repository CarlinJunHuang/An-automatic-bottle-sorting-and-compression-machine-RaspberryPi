import RPi.GPIO as GPIO
import time

A = 20
B = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

counter = 0 #左轮脉冲初值
counter1 = 0 #右轮脉冲初值

def my_callback(channel):#边缘检测回调函数，详情在参见链接中
    global counter#设置为全局变量
    if GPIO.event_detected(A):#检测到一个脉冲则脉冲数加1
        counter=counter+1 #这里的channel和channel1无须赋确定值，不能不写。
        print("A")

def my_callback1(channel1):
    global counter1
    if GPIO.event_detected(B):
        counter1=counter1+1
        print("B")

GPIO.add_event_detect(A,GPIO.RISING,callback=my_callback, bouncetime = 10) #在引脚上添加上升临界值检测再回调
GPIO.add_event_detect(B,GPIO.RISING,callback=my_callback1, bouncetime = 10)