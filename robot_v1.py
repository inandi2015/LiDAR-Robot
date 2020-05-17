import numpy as np
from lidar_data import lidarReader
from motordriver_v3 import MotorController
import threading
import time

class Robot:
	def __init__(self):
		self.lidar = lidarReader('/dev/mylidar', 115200)
		self.mover = MotorController()
		self.left_distance_table = np.zeros(80)
		self.right_distance_table = np.zeros(80)
		self.thread = threading.Thread(target=self.navigate, args=())
		self.thread.start()
		
	def navigate(self):
		while True:
			time.sleep(0.1) # (yield) allowing reading data from the serailport
			front_too_close, left_too_close, right_too_close = False, False, False
			if(self.lidar.angle_180 < 400):
				front_too_close = True
			left_angle = np.argmin(self.lidar.left_container)
			right_angle = np.argmin(self.lidar.right_container)
			if(self.lidar.left_container[left_angle] < 250):
				left_too_close = True
			if(self.lidar.right_container[right_angle] < 250):
				right_too_close = True
			if(front_too_close and left_too_close and right_too_close):
				self.mover.stop()
			elif(front_too_close):
				if(self.lidar.angle_270 > self.lidar.angle_90):
					self.mover.turn_left()
				else:
					self.mover.turn_right()
			elif(left_too_close or right_too_close):
				if(left_too_close):
					self.mover.turn_right(left_angle)
				else:
					self.mover.turn_left(right_angle)
			else:
				self.mover.forward()
				
			#print(front_too_close, left_too_close, right_too_close)
			
			

if __name__ == "__main__":
	robot = Robot()
	while True:
		time.sleep(10)
