import RPi.GPIO as GPIO
import time

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
recentLog = "/home/huangjun/Desktop/rl.txt"
logg = "/home/huangjun/Desktop/l.txt"

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
    while(bottles < 8):     # 控制最大容量，8只是测试值
        if GPIO.input(IN6) == 0:    # 红外传感器，检测到瓶子投入
            time.sleep(0.05)
            bottles += 1
            print ("A bottle is coming in!")
            interval = True                 # 开始计时
            begin = time.time()             # 当前时刻
            while interval == True:         # 1秒的计时循环
                if GPIO.input(IN5) == 1:    # 1秒内，若金属传感器检测到金属
                    mode = 1                # 切换到金属处理模式
                if time.time() - begin >= 1:  # 循环时间到达1秒后
                    interval = False        # 结束循环
            sortingAction(mode)
            mode = 0
           
        
def setStep(h1, h2, h3, h4):
    GPIO.output(IN1, h1)
    GPIO.output(IN2, h2)
    GPIO.output(IN3, h3)
    GPIO.output(IN4, h4)
    
def stop():
    setStep(0,0,0,0)
    
def step(direction, step):
    global recentLog
    if direction == 1:      # 控制顺时针转
        for i in range(0, step):
            setStep(1, 0, 0, 0)
            time.sleep(delay)
            setStep(0, 1, 0, 0)
            time.sleep(delay)
            setStep(0, 0, 1, 0)
            time.sleep(delay)
            setStep(0, 0, 0, 1)
            time.sleep(delay)
            with open(recentLog,'w') as recent_log:
                recent_log.write("1\n")
                recent_log.write(str(i+1))
    else:                   # 控制逆时针转
        for i in range(0, step):
            setStep(0, 0, 0, 1)
            time.sleep(delay)
            setStep(0, 0, 1, 0)
            time.sleep(delay)
            setStep(0, 1, 0, 0)
            time.sleep(delay)
            setStep(1, 0, 0, 0)
            time.sleep(delay)
            with open(recentLog,'w') as recent_log:
                recent_log.write("0\n")
                recent_log.write(str(i+1))
            
def sortingAction(mode):
    global steps, recentLog, logg
    with open(logg, 'a') as log:
        if mode == 1:
            print ("This is a Pop Can")
            step(False, steps)     # 控制逆时针转
            time.sleep(1)
            step(True, steps)      # 控制顺时针转
            time.sleep(0.1)
            GPIO.setup(IN5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            time.sleep(0.1)
            log.write(time.strftime("%Y-%m-%d %H:%M:%S, PopCan", time.localtime())+"\n")
        else:
            print ("This is a PET Bottle")
            step(True, steps)     # 控制顺时针转
            time.sleep(1)
            step(False, steps)      # 控制逆时针转
            time.sleep(0.1)
            log.write(time.strftime("%Y-%m-%d %H:%M:%S, PET", time.localtime())+"\n")
    
def restartCheck():
    global steps, recentLog, logg
    with open(recentLog,'r') as recent_log:
        time.sleep(0.1)
        direction = recent_log.readline(1)
        recent_log.seek(2,0)
        read_data = recent_log.readline()
        if int(read_data) != steps:
            step(False if direction == 1 else True, int(read_data))     # 复位
            with open(logg, 'a') as log:
                time.sleep(0.2)
                log.write("PopCan " if direction == 0 else "PET "
                          + time.strftime("%Y-%m-%d %H:%M:%S, ", time.localtime())    # 数据与急停记录
                          + "Emergency STOP!\n")
        print("Everything is ready")

time.sleep(0.5)
init()
restartCheck()
time.sleep(0.5)
detect()
GPIO.cleanup()
