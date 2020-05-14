import sys
import thread
sys.path.append('/home/pi/Final Project') # where I store the lidarreader.py file
from lidarreader import *
#from motors import *

class Robot:
	def __init__(self):
		# lidar object
		self.data_reader = lidarReader('/dev/ttyACM0', 115200)
		thread.start_new_thread(self.desicion, ())
		
	def desicion(self):
		# moving dicision based on the distance value
		while True:
			angle_0, angle_90, angle_270 = self.data_reader.container[0], self.data_reader.container[90], self.data_reader.container[270]
			print(angle_0)
			if(angle_0 >= 150 and angle_0 <= 250):
				print("Too close", angle_0)
				if(angle_90 > angle_270):
					print("Moving left")
				else:
					print("Moving right")

if __name__ == "__main__":
	robot = Robot()
	c = raw_input("What's up")
	
	
