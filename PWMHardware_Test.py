import time 
import RPi.GPIO as GPIO
import sys
import subprocess # to call echo

import pigpio

GPIO.setmode(GPIO.BCM) # Set for broadcom numbering not board numbers...

pi_hw = pigpio.pi() # connect to pi gpio daemon

rest13 = 71800 # 71.8% rest center duty cycle for red mount servo
rest12 = 72500 # 72.5% rest center duty cycle for blue mount servo
turnSpeed = 14000

pi_hw.hardware_PWM(13, 46.5, rest13) 
pi_hw.hardware_PWM(12, 46.5, rest12) 

time.sleep(5)

# Duty cycles arejust based on rest duty cycles observed above approximate center rest point (75% and 25% is one direction and flipped is the other direction)

pi_hw.hardware_PWM(13, 46.5, rest13 + turnSpeed) 
pi_hw.hardware_PWM(12, 46.5, rest12 - turnSpeed) 

time.sleep(5)

pi_hw.hardware_PWM(13, 46.5, rest13 - turnSpeed) 
pi_hw.hardware_PWM(12, 46.5, rest12 + turnSpeed)

time.sleep(5)

pi_hw.hardware_PWM(13, 0, 0) # 0 Hz, 0% duty cycle - stop the servo!
pi_hw.hardware_PWM(12, 0, 0) # 0 Hz, 0% duty cycle - stop the servo!

pi_hw.stop() # close pi gpio DMA resources
