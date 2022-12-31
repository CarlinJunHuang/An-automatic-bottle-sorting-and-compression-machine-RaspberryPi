'''
    Driver for the motor (stepper motor).
    @author: Jingkai Zhang
    @version: 1.2
        version 1.1: add stepper motor (sofware PWM)
        version 1.2: add stepper motor (hardware PWM)
    @since: 2022
    @update: 2022-4-6
        edit in 2022-3-29: Add new stepper motor driver, based on pigpio, which is faster
        edit in 2022-4-3: Add more information if initialization is failed
        edit in 2022-4-6: fix some bugs
'''
import pigpio
import time, sys
class stepper_motor(object):
    '''
        Test script for step motor HW23-601 (https://www.mouser.com/c/?q=HW23-601) 
        with driver STR2 (https://www.applied-motion.com/products/stepper-drives/str2)
    '''
    num_of_steps_for_360 = 1600                 # this could be changed, please see the totorial of STR2/4
    resolution = num_of_steps_for_360 / 360     # resolution, how many steps would trigger 1 degree rotation
    DIR86 = 18                        # GPIO 21 for clockwise (physically connected to dir+ port in the driver)
    PUL86 = 12                       # GPIO 18 for counter clockwise (physically connected to step+ port in the driver)
    gear_ratio = 1                              # radius of the outer gear is 4 times than the radius of the inner gear
    cur_position = 0
    pwm_frequency = 2500                       # PWM frequency, the larger the faster rotation
    '''
        TODO: decide how much frequency is suitable
        Here are some frequency that I recommend:
            5000 Hz, 6250 Hz, 10000 Hz, 12500Hz, 15625 Hz, 20000 Hz
        Better choose something that can be divided by 500000.
    '''
    inner_speed = 60 * pwm_frequency / num_of_steps_for_360
    outer_speed = inner_speed / gear_ratio
    delay_micro = int(500000 / pwm_frequency)
    CCW_wave = [pigpio.pulse(1 << PUL86, 0, delay_micro), pigpio.pulse(0, 1 << PUL86, delay_micro)]
    CW_wave = [pigpio.pulse(1 << DIR86, 0, delay_micro), pigpio.pulse(0, 1 << DIR86, delay_micro)]
    waveform_id = {}
    name = 'stepper_motor'

    def __init__(self):
        
        self.pi = pigpio.pi() 
        self.pi.wave_clear()
        self.pi.set_mode(self.DIR86, pigpio.OUTPUT)
        self.pi.set_mode(self.PUL86, pigpio.OUTPUT)
        self.pi.wave_add_generic(self.CW_wave)
        self.waveform_id[self.DIR86] = self.pi.wave_create()
        self.pi.wave_add_generic(self.CCW_wave)
        self.waveform_id[self.PUL86] = self.pi.wave_create()
        # self.log.info('waveform created %s' % self.waveform_id)
        time.sleep(0.5) 
        # self.log.info("stepper motor initialization accomplished, outer speed: %d rpm, resolution: %d steps/degree" % (self.outer_speed, self.resolution))

    def __del__(self):
        self.pi = pigpio.pi()    
        self.pi.wave_tx_stop()  # stop waveform
        self.pi.wave_clear()
        self.pi.stop()

    def send_pulse(self, num_of_pulse, control_port):
        '''
            If you want to know why, please visit the following link:
            https://abyz.me.uk/rpi/pigpio/python.html#wave_chain
        '''   
        x = int(num_of_pulse) & 255
        y = int(num_of_pulse) >> 8
        chain = [255, 0, self.waveform_id[PUL86], 255, 1, x, y]  # send x + 256 * y times
        # chain = [255, 0, self.waveform_id[control_port], 255, 3]  # infinity loop, just for test
        self.pi.wave_chain(chain)
        while self.pi.wave_tx_busy():
            time.sleep(0.1)
        self.pi.wave_tx_stop() 

    def move(self, angle, direction):
        num_of_steps = self.resolution * angle * self.gear_ratio  # gear ratio is 4, so the outer speed is 1/4 of inner gear, need more pulse
        angle = -angle if direction == 'CCW' else angle           # decrease the angle if direction is CCW
        self.cur_position += angle
        if self.cur_position > 360 or self.cur_position < -360:
        #    self.log.error("rotation angle will exceeded 360 degree, wire might get twisted, current movement cancelled")
        #    self.log.info("movement: <moved %d degree, direction:%s> has been cancelled" % (angle, direction))
            self.cur_position -= angle
            return False
        else:
            if direction == 'CW':
                self.send_pulse(num_of_steps, self.DIR86)
            else:
                self.send_pulse(num_of_steps, self.PUL86)
          #  self.log.info("moved %d degree, direction:%s, current position: %d" % (abs(angle), direction, self.cur_position))
            return True
        
    def get_motor_type(self):
        return self.name

if __name__ == '__main__':
    sm86 = stepper_motor()
    sm42 = stepper_motor()
    sm42.move(180,"CW")
    #sm86.__del__()