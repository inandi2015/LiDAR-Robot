
import numpy as np
import serial
import threading
from motordriver_v2 import *
import time

class lidarReader:
	def __init__(self, port, baudrate):
		self.serialport = serial.Serial(port=port, baudrate=baudrate)
		self.mover = MotorController()
		# the container stores the distance for a certain angle
		self.container = np.zeros(360)
		self.serialport.reset_input_buffer()
		self.serialport.reset_output_buffer()
		#self.thread = threading.Thread(target=self.read, args=())
		#self.thread.daemon = True
		#self.thread.start()
	
	def is_number(self, n):
		try:
			int(n)   # Type-casting the string to `float`.
					   # If string is not a valid `float`, 
					   # it'll raise `ValueError` exception
		except ValueError:
			return False
		return True
	
	def prepare(self):
		#self.serialport.write(b'RelayOff\n')
		while(len(self.serialport.readline().split(",")) != 4): # "A" sign, distance, angle, quality
			self.serialport.write(b'ShowDist\n')

	def read(self):
		self.prepare()
		self.mover.stop()
		time.sleep(1)
		self.mover.forward()
		
		turning = 0
		while True:
			line = self.serialport.readline()   # read a '\n' terminated line 
			data = line.split(",")
			# ~ print(data[1])
			if(data[1].isdigit() and data[2].isdigit() and int(data[1]) < 360): # shouldn't be false, put here just in case of transimisson error
				self.container[int(data[1])] = int(data[2])
				if int(data[1]) == 0 and turning == 0:
					angle_0 = int(data[2])
					# ~ print(angle_0)
					if(angle_0 >= 100 and angle_0 <= 400):
						angle_90, angle_270 = self.container[90], self.container[270]
						# ~ print("Too close", angle_0)
						if(angle_90 > angle_270):
							self.mover.turn_left()
						else:
							self.mover.turn_right()
						turning = 1
			if turning == 1: # State while in the middle of turning
				# ~ print("Mid turning", angle_0)
				angle_0, angle_90, angle_270 = self.container[0], self.container[90], self.container[270]
				if angle_0 > 500 and angle_90 > 450 and angle_270 > 450:
					turning = 0
			if turning == 0:
				self.mover.forward()
				
			# ~ print(data)
			
if __name__ == "__main__":
	reader = lidarReader('/dev/mylidar', 115200)
	reader.read()
