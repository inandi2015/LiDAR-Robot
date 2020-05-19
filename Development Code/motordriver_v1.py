# Python module for the Raspberry which talks to the pigpio daemon to allow
# control of the general purpose input output (GPIO)
import pigpio

WORKING_FREQUENCY = 1000 # L298N works at 1kHz

class MotorController:
	def __init__(self):
		self.controller = pigpio.pi() # access the local pi's GPIO
		# GPIO22 GPIO23 GPIO24 GPIO25
		# 1 0 1 0
		self.lastPWM1 = 0
		self.lastPWM2 = 0
		self.left_speed_table = [()]*80
		self.right_speed_table = [()]*80
		self.fill_speed_tables()
		self.controller.write(22, 1)
		self.controller.write(23, 0)
		self.controller.write(24, 1)
		self.controller.write(25, 0)
		self.controller.hardware_PWM(13, WORKING_FREQUENCY, 0) 
		self.controller.hardware_PWM(12, WORKING_FREQUENCY, 0) 
		
	def forward(self):
		if(self.lastPWM1 == 300000 and self.lastPWM2 == 300000):
			return
		self.controller.hardware_PWM(13, WORKING_FREQUENCY, 300000) 
		self.controller.hardware_PWM(12, WORKING_FREQUENCY, 300000) 
		self.lastPWM1, self.lastPWM2 = 300000, 300000
	
	def stop(self):
		if(self.lastPWM1 == 0 and self.lastPWM2 == 0):
			return
		self.controller.hardware_PWM(13, WORKING_FREQUENCY, 0) 
		self.controller.hardware_PWM(12, WORKING_FREQUENCY, 0)
		self.lastPWM1, self.lastPWM2 = 0, 0
	
	def turn_left(self, index = None):
		current_PWM1, current_PWM2 = 0, 0
		if not index:
			current_PWM1, current_PWM2 = 50000, 800000 # front too close
		else:
			current_PWM1, current_PWM2 = self.right_speed_table[index]
		if(self.lastPWM1 == current_PWM1 and self.lastPWM2 == current_PWM2):
			return
		self.controller.hardware_PWM(13, WORKING_FREQUENCY, current_PWM1) 
		self.controller.hardware_PWM(12, WORKING_FREQUENCY, current_PWM2) 
		self.lastPWM1, self.lastPWM2 = current_PWM1, current_PWM2
	
	def turn_right(self, index = None):
		current_PWM1, current_PWM2 = 0, 0
		if not index:
			current_PWM1, current_PWM2 = 800000, 50000 # front too close
		else:
			current_PWM1, current_PWM2 = self.left_speed_table[index]
		if(self.lastPWM1 == current_PWM1 and self.lastPWM2 == current_PWM2):
			return
		self.controller.hardware_PWM(13, WORKING_FREQUENCY, current_PWM1) 
		self.controller.hardware_PWM(12, WORKING_FREQUENCY, current_PWM2) 
		self.lastPWM1, self.lastPWM2 = current_PWM1, current_PWM2
		
	def fill_speed_tables(self):
		for i in range(10):
			self.left_speed_table[i] = (700000, 20000)
			self.right_speed_table[i] = (200000, 350000)
		for i in range(10, 20):
			self.left_speed_table[i] = (680000, 25000)
			self.right_speed_table[i] = (100000, 400000)
		for i in range(20, 30):
			self.left_speed_table[i] = (650000, 50000)
			self.right_speed_table[i] = (80000, 450000)
		for i in range(30, 40):
			self.left_speed_table[i] = (600000, 60000)
			self.right_speed_table[i] = (70000, 500000)
		for i in range(40, 50):
			self.left_speed_table[i] = (500000, 70000)
			self.right_speed_table[i] = (60000, 600000)
		for i in range(50, 60):
			self.left_speed_table[i] = (450000, 80000)
			self.right_speed_table[i] = (50000, 650000)
		for i in range(60, 70):
			self.left_speed_table[i] = (400000, 100000)
			self.right_speed_table[i] = (25000, 680000)
		for i in range(70, 80):
			self.left_speed_table[i] = (350000, 200000)
			self.right_speed_table[i] = (20000, 700000)

if __name__ == "__main__":
	import time
	Controller = MotorController()
	#print(len(Controller.left_speed_table))
	#print(Controller.controller.read(22), Controller.controller.read(23), 
	# Controller.controller.read(24), Controller.controller.read(25))
	#Controller.forward()
	#time.sleep(2)
	#Controller.turn_left()
	#time.sleep(2)
	#Controller.turn_right()
	#time.sleep(2)
	#Controller.stop()

