# Python module for the Raspberry which talks to the pigpio daemon to allow
# control of the general purpose input output (GPIO)
import pigpio

WORKING_FREQUENCY = 1000 # L298N works at 1kHz

class MotorController:
	def __init__(self):
		self.controller = pigpio.pi() # access the local pi's GPIO
		# GPIO22 GPIO23 GPIO24 GPIO25
		# 1 0 1 0
		self.controller.write(22, 1)
		self.controller.write(23, 0)
		self.controller.write(24, 1)
		self.controller.write(25, 0)
		self.controller.hardware_PWM(13, WORKING_FREQUENCY, 0) 
		self.controller.hardware_PWM(12, WORKING_FREQUENCY, 0) 
		
	def forward(self):
		self.controller.hardware_PWM(13, WORKING_FREQUENCY, 350000) 
		self.controller.hardware_PWM(12, WORKING_FREQUENCY, 350000) 
	
	def stop(self):
		self.controller.hardware_PWM(13, WORKING_FREQUENCY, 0) 
		self.controller.hardware_PWM(12, WORKING_FREQUENCY, 0)
	
	def turn_left(self):
		self.controller.hardware_PWM(13, WORKING_FREQUENCY, 50000) 
		self.controller.hardware_PWM(12, WORKING_FREQUENCY, 600000) 
	
	def turn_right(self):
		self.controller.hardware_PWM(13, WORKING_FREQUENCY, 600000) 
		self.controller.hardware_PWM(12, WORKING_FREQUENCY, 50000) 
		

if __name__ == "__main__":
	import time
	Controller = MotorController()
	#print(Controller.controller.read(22), Controller.controller.read(23), 
	# Controller.controller.read(24), Controller.controller.read(25))
	Controller.forward()
	time.sleep(2)
	Controller.turn_left()
	time.sleep(2)
	Controller.turn_right()
	time.sleep(2)
	Controller.stop()

