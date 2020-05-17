# Python module for the Raspberry which talks to the pigpio daemon to allow
# control of the general purpose input output (GPIO)
import pigpio

WORKING_FREQUENCY = 1000 # L298N works at 1kHz
multiplierForward = 1
multiplierTurn = 1

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
		self.controller.write(22, 1)
		self.controller.write(23, 0)
		self.controller.write(24, 1)
		self.controller.write(25, 0)
		self.controller.hardware_PWM(13, WORKING_FREQUENCY, 300000*multiplierForward) 
		self.controller.hardware_PWM(12, WORKING_FREQUENCY, 300000*multiplierForward) 
	
	def stop(self):
		self.controller.write(22, 1)
		self.controller.write(23, 0)
		self.controller.write(24, 1)
		self.controller.write(25, 0)
		self.controller.hardware_PWM(13, WORKING_FREQUENCY, 0) 
		self.controller.hardware_PWM(12, WORKING_FREQUENCY, 0)
	
	def turn_left(self, index = None):
		self.controller.write(22, 0)
		self.controller.write(23, 1)
		self.controller.write(24, 1)
		self.controller.write(25, 0)
		self.controller.hardware_PWM(13, WORKING_FREQUENCY, 700000*multiplierTurn) 
		self.controller.hardware_PWM(12, WORKING_FREQUENCY, 700000*multiplierTurn) 
	
	def turn_right(self, index = None):
		self.controller.write(22, 1)
		self.controller.write(23, 0)
		self.controller.write(24, 0)
		self.controller.write(25, 1)
		self.controller.hardware_PWM(13, WORKING_FREQUENCY, 700000*multiplierTurn) 
		self.controller.hardware_PWM(12, WORKING_FREQUENCY, 700000*multiplierTurn) 
		

if __name__ == "__main__":
	import time
	Controller = MotorController()
	#print(Controller.controller.read(22), Controller.controller.read(23), 
	# Controller.controller.read(24), Controller.controller.read(25))
	Controller.forward()
	time.sleep(1)
	Controller.turn_left()
	time.sleep(5)
	Controller.turn_right()
	time.sleep(5)
	Controller.stop()

