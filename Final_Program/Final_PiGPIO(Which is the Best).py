'''
    Stepper motor driving Reference @author: Jingkai Zhang
'''
import pigpio
import time, sys
import RPi.GPIO as GPIO
import os 

PrmxtPin = 14
IrPin = 15

logg = "/home/huangjun/Desktop/l.txt"

PETcount = 0
POPCANcoutn = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class stepper_motor42(object):
    num_of_steps_for_360 = 1600                 # this could be changed, please see the totorial of STR2/4
    resolution = num_of_steps_for_360 / 360     # resolution, how many steps would trigger 1 degree rotation
    DIR = 19                        # GPIO 18 for clockwise (physically connected to dir+ port in the driver)
    PUL = 13                        # GPIO 12 for counter clockwise (physically connected to step+ port in the driver)
    gear_ratio = 1                              # radius of the outer gear is 4 times than the radius of the inner gear
    cur_position = 0
    pwm_frequency = 3125                        # PWM frequency, the larger the faster rotation
    GPIO.setup(DIR, GPIO.OUT)
    '''
        TODO: decide how much frequency is suitable
        Here are some frequency that recommended:
            5000 Hz, 6250 Hz, 10000 Hz, 12500Hz, 15625 Hz, 20000 Hz
        Better choose something that can be divided by 500000.
    '''
    inner_speed = 60 * pwm_frequency / num_of_steps_for_360
    outer_speed = inner_speed / gear_ratio
    delay_micro = int(500000 / pwm_frequency)
    CCW_wave = [pigpio.pulse(1 << PUL, 0, delay_micro), pigpio.pulse(0, 1 << PUL, delay_micro)]
    CW_wave = [pigpio.pulse(1 << DIR, 0, delay_micro), pigpio.pulse(0, 1 << DIR, delay_micro)]
    waveform_id = {}
    name = 'stepper_motor'

    def __init__(self):
        self.pi = pigpio.pi() 
        self.pi.wave_clear()
        self.pi.set_mode(self.PUL, pigpio.OUTPUT)
        self.pi.wave_add_generic(self.CCW_wave)
        self.waveform_id[self.PUL] = self.pi.wave_create()
        
    def __del__(self):
        self.pi = pigpio.pi()    
        self.pi.wave_tx_stop()  # stop waveform
        self.pi.wave_clear()
        self.pi.stop()

    def send_pulse(self, num_of_pulse, direction):
        '''
            If you want to know why, please visit the following link:
            https://abyz.me.uk/rpi/pigpio/python.html#wave_chain
        '''   
        x = int(num_of_pulse) & 255
        y = int(num_of_pulse) >> 8
        if direction == "left":
            GPIO.output(self.DIR, GPIO.LOW)
        elif direction == "right":
            GPIO.output(self.DIR, GPIO.HIGH)
        chain = [255, 0, self.waveform_id[self.PUL], 255, 1, x, y]  # send x + 256 * y times
        # chain = [255, 0, self.waveform_id[control_port], 255, 3]  # infinity loop, just for test
        self.pi.wave_chain(chain)
        while self.pi.wave_tx_busy():
            time.sleep(0.1)
        self.pi.wave_tx_stop() 

    def move(self, angle, direction):
        self.__init__()
        num_of_steps = self.resolution * angle * self.gear_ratio  # gear ratio is 3, so the outer speed is 1/4 of inner gear, need more pulse
        angle = -angle if direction == 'left' else angle           # decrease the angle if direction is CCW
        self.cur_position += angle
        print(self.cur_position)
        
        if self.cur_position > 10000 or self.cur_position < -10800:
            # self.log.error("rotation angle will exceeded 360 degree, wire might get twisted, current movement cancelled")
            # self.log.info("movement: <moved %d degree, direction:%s> has been cancelled" % (angle, direction))
            self.cur_position -= angle
            return False
        else:
            if direction == 'right':
                self.send_pulse(num_of_steps, "right")
            else:
                self.send_pulse(num_of_steps, "left")
            # self.log.info("moved %d degree, direction:%s, current position: %d" % (abs(angle), direction, self.cur_position))
            return True
        
    def get_motor_type(self):
        return self.name
    
class stepper_motor86(object):
    num_of_steps_for_360 = 1600                 # this could be changed, please see the totorial of STR2/4
    resolution = num_of_steps_for_360 / 360     # resolution, how many steps would trigger 1 degree rotation
    DIR = 18                        # GPIO 18 for clockwise (physically connected to dir+ port in the driver)
    PUL = 12                        # GPIO 12 for counter clockwise (physically connected to step+ port in the driver)
    gear_ratio = 3                              # radius of the outer gear is 4 times than the radius of the inner gear
    cur_position = 0
    pwm_frequency = 5000                        # PWM frequency, the larger the faster rotation
    GPIO.setup(DIR, GPIO.OUT)
    '''
        TODO: decide how much frequency is suitable
        Here are some frequency that I recommend:
            5000 Hz, 6250 Hz, 10000 Hz, 12500Hz, 15625 Hz, 20000 Hz
        Better choose something that can be divided by 500000.
    '''
    inner_speed = 60 * pwm_frequency / num_of_steps_for_360
    outer_speed = inner_speed / gear_ratio
    delay_micro = int(500000 / pwm_frequency)
    CCW_wave = [pigpio.pulse(1 << PUL, 0, delay_micro), pigpio.pulse(0, 1 << PUL, delay_micro)]
    CW_wave = [pigpio.pulse(1 << DIR, 0, delay_micro), pigpio.pulse(0, 1 << DIR, delay_micro)]
    waveform_id = {}
    name = 'stepper_motor'

    def __init__(self):
        self.pi = pigpio.pi() 
        self.pi.wave_clear()
        self.pi.set_mode(self.PUL, pigpio.OUTPUT)
        self.pi.wave_add_generic(self.CCW_wave)
        self.waveform_id[self.PUL] = self.pi.wave_create()
        
    def __del__(self):
        self.pi = pigpio.pi()    
        self.pi.wave_tx_stop()  # stop waveform
        self.pi.wave_clear()
        self.pi.stop()

    def send_pulse(self, num_of_pulse, direction):
        '''
            If you want to know why, please visit the following link:
            https://abyz.me.uk/rpi/pigpio/python.html#wave_chain
        '''   
        x = int(num_of_pulse) & 255
        y = int(num_of_pulse) >> 8
        if direction == "up":
            GPIO.output(self.DIR, GPIO.LOW)
        elif direction == "down":
            GPIO.output(self.DIR, GPIO.HIGH)
        chain = [255, 0, self.waveform_id[self.PUL], 255, 1, x, y]  # send x + 256 * y times
        # chain = [255, 0, self.waveform_id[control_port], 255, 3]  # infinity loop, just for test
        self.pi.wave_chain(chain)
        while self.pi.wave_tx_busy():
            time.sleep(0.1)
        self.pi.wave_tx_stop() 

    def move(self, angle, direction):
        self.__init__()
        num_of_steps = self.resolution * angle * self.gear_ratio  # gear ratio is 3, so the outer speed is 1/4 of inner gear, need more pulse
        angle = -angle if direction == 'up' else angle           # decrease the angle if direction is CCW
        self.cur_position += angle
        print(self.cur_position)
        
        if self.cur_position > 10800 or self.cur_position < -10800:
            # self.log.error("rotation angle will exceeded 360 degree, wire might get twisted, current movement cancelled")
            # self.log.info("movement: <moved %d degree, direction:%s> has been cancelled" % (angle, direction))
            self.cur_position -= angle
            return False
        else:
            if direction == 'down':
                self.send_pulse(num_of_steps, "down")
            else:
                self.send_pulse(num_of_steps, "up")
            # self.log.info("moved %d degree, direction:%s, current position: %d" % (abs(angle), direction, self.cur_position))
            return True
        
    def get_motor_type(self):
        return self.name
    
def setup():
    GPIO.setup(IrPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PrmxtPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    open_io="sudo pigpiod"
    os.system(open_io)
    time.sleep(1)
    pi = pigpio.pi()  # Set up the pigpio`
    
def loop():     # main Loop
    global IrPin
    while True:
        if (0 == GPIO.input(IrPin)):
            metal_detect()
    
def metal_detect(): # The command when metal bottle is detected
    global PETcount, sm42, sm86
    PETcount += 1
    time.sleep(2.5)
    sm86.move(3000, "down")
    time.sleep(0.2)
    sm86.move(3000, "down")
    time.sleep(0.3)
    sm42.move(150, "right")
    time.sleep(0.8)
    if GPIO.input(PrmxtPin) == 0:
        compress()
    else:
        sm42.move(450, "right")
        time.sleep(0.3)
        sm42.move(600, "left")
    sm86.move(3000, "up")
    time.sleep(0.2)
    sm86.move(3000, "up")
    time.sleep(0.1)
        
        
def compress(): # Use 86 step motot to compress the metal bottle
    global sm42, sm86
    sm42.move(775, "left") # middlize
    time.sleep(0.2)
    sm42.move(65, "right")
    time.sleep(0.3)
    
    sm86.move(3000, "up")  # compressing
    time.sleep(0.3)
    sm86.move(3000, "up")  
    time.sleep(0.15)
    sm86.move(3000, "up")  
    time.sleep(0.15)
    sm86.move(3000, "up")  
    time.sleep(0.5)
    sm86.move(3000, "down")
    time.sleep(0.3)
    sm86.move(3000, "down")
    time.sleep(0.15)
    sm86.move(3000, "down")
    time.sleep(0.15)
    sm86.move(3000, "down")
    time.sleep(0.2)
    
    sm42.move(750, "left") # back
    time.sleep(0.5)
    sm42.move(1310, "right")
    


if __name__ == '__main__':
    global sm86, sm42
    setup()
    sm86 = stepper_motor86()
    sm42 = stepper_motor42()
    
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        GPIO.clearup()
