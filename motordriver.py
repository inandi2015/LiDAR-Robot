# Python module for the Raspberry which talks to the pigpio daemon to allow
# control of the general purpose input output (GPIO)
import pigpio

WORKING_FREQUENCY = 1000 # L298N works at 1kHz
multiplierForward = 1.2
multiplierTurn = 1.2

class MotorController:
	def __init__(self):
		self.controller = pigpio.pi() # access the local pi's GPIO
		# GPIO22 GPIO23 GPIO24 GPIO25
		# 1 0 1 0
		self.lastPWM1 = 0
		self.lastPWM2 = 0
		self.speed_table = [()]*80
		self.fill_speed_tables()
		self.moving_forward = False
		self.controller.write(22, 1)
		self.controller.write(23, 0)
		self.controller.write(24, 1)
		self.controller.write(25, 0)
		self.controller.hardware_PWM(13, WORKING_FREQUENCY, 0) 
		self.controller.hardware_PWM(12, WORKING_FREQUENCY, 0) 
		
	def forward(self):
		if(not self.moving_forward):
			self.controller.write(22, 1)
			self.controller.write(23, 0)
			self.controller.write(24, 1)
			self.controller.write(25, 0)
			self.controller.hardware_PWM(13, WORKING_FREQUENCY, 300000*multiplierForward) 
			self.controller.hardware_PWM(12, WORKING_FREQUENCY, 300000*multiplierForward) 
			self.lastPWM1, self.lastPWM2 = 300000*multiplierForward, 300000*multiplierForward
		self.moving_forward = True
	
	def backward(self):
		self.moving_forward = False
		self.controller.write(22, 0)
		self.controller.write(23, 1)
		self.controller.write(24, 0)
		self.controller.write(25, 1)
		self.controller.hardware_PWM(13, WORKING_FREQUENCY, 300000*multiplierForward) 
		self.controller.hardware_PWM(12, WORKING_FREQUENCY, 300000*multiplierForward) 
		self.lastPWM1, self.lastPWM2 = 0, 0
	
	def stop(self):
		self.moving_forward = False
		if(self.lastPWM1 == 0 and self.lastPWM2 == 0):
			return
		self.controller.write(22, 1)
		self.controller.write(23, 0)
		self.controller.write(24, 1)
		self.controller.write(25, 0)
		self.controller.hardware_PWM(13, WORKING_FREQUENCY, 0) 
		self.controller.hardware_PWM(12, WORKING_FREQUENCY, 0)
		self.lastPWM1, self.lastPWM2 = 0, 0
	
	def turn_left(self, index = None):
		self.moving_forward = False
		current_PWM1, current_PWM2 = 0, 0
		self.controller.write(22, 0)
		self.controller.write(23, 1)
		self.controller.write(24, 1)
		self.controller.write(25, 0)
		if not index:
			current_PWM1, current_PWM2 = 600000*multiplierTurn, 780000*multiplierTurn # front too close
		else:
			current_PWM2, current_PWM1 = self.speed_table[index]
			#current_PWM1, current_PWM2 = current_PWM1 * multiplierTurn, current_PWM2 * multiplierTurn
		if(self.lastPWM1 == current_PWM1 and self.lastPWM2 == current_PWM2):
			return
		self.controller.hardware_PWM(13, WORKING_FREQUENCY, current_PWM1) 
		self.controller.hardware_PWM(12, WORKING_FREQUENCY, current_PWM2) 
		self.lastPWM1, self.lastPWM2 = current_PWM1, current_PWM2
	
	def turn_right(self, index = None):
		self.moving_forward = False
		current_PWM1, current_PWM2 = 0, 0
		self.controller.write(22, 1)
		self.controller.write(23, 0)
		self.controller.write(24, 0)
		self.controller.write(25, 1)		
		if not index:
			current_PWM1, current_PWM2 = 780000*multiplierTurn, 600000*multiplierTurn # front too close
		else:
			current_PWM1, current_PWM2 = self.speed_table[len(self.speed_table)-1-index]
		if(self.lastPWM1 == current_PWM1 and self.lastPWM2 == current_PWM2):
			return
		self.controller.hardware_PWM(13, WORKING_FREQUENCY, current_PWM1) 
		self.controller.hardware_PWM(12, WORKING_FREQUENCY, current_PWM2) 
		self.lastPWM1, self.lastPWM2 = current_PWM1, current_PWM2
		
	def fill_speed_tables(self):
		
		for i in range(10):
			self.speed_table[i] = (580000, 360000)
		for i in range(10, 20):
			self.speed_table[i] = (650000, 380000)
		for i in range(20, 30):
			self.speed_table[i] = (670000, 400000)
		for i in range(30, 40):
			self.speed_table[i] = (720000, 420000)
		for i in range(40, 50):
			self.speed_table[i] = (730000, 430000)
		for i in range(50, 60):
			self.speed_table[i] = (735000, 435000)
		for i in range(60, 70):
			self.speed_table[i] = (790000, 490000)
		for i in range(70, 80):
			self.speed_table[i] = (800000, 500000)
			
	def shutdown(self):
		self.stop()
		self.controller.write(22, 0)
		self.controller.write(23, 0)
		self.controller.write(24, 0)
		self.controller.write(25, 0)
		# Release pigpio resources
		self.controller.stop()
		

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

