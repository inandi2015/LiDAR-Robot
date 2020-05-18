import numpy as np
from lidar_data import lidarReader
from motordriver_v3 import MotorController
import threading
import time
MAP_SIZE_PIXELS         = 500
MAP_SIZE_METERS         = 20
from roboviz import MapVisualizer
from breezyslam.algorithms import RMHC_SLAM
from breezyslam.sensors import XVLidar as LaserModel

class Robot:
	def __init__(self):
		# Connect to Lidar unit
		self.lidar = lidarReader('/dev/mylidar', 115200)
		self.mover = MotorController()
		# Create an RMHC SLAM object with a laser model and optional robot model
		self.slam = RMHC_SLAM(LaserModel(), MAP_SIZE_PIXELS, MAP_SIZE_METERS)
		# Set up a SLAM display
		self.viz = MapVisualizer(MAP_SIZE_PIXELS, MAP_SIZE_METERS, 'SLAM')
		# Initialize empty map
		self.mapbytes = bytearray(MAP_SIZE_PIXELS * MAP_SIZE_PIXELS)
		self.left_distance_table = np.zeros(80)
		self.right_distance_table = np.zeros(80)
		self.thread = threading.Thread(target=self.navigate, args=())
		self.thread.start()
		
	def constructmap(self):
		while True:
			time.sleep(0.0001)
			# Update SLAM with current Lidar scan, using first element of (scan, quality) pairs
			self.slam.update(self.lidar.getdata())
			# Get current robot position
			x, y, theta = self.slam.getpos()
			# Get current map bytes as grayscale
			self.slam.getmap(self.mapbytes)
			# Display map and robot pose, exiting gracefully if user closes it
			if not self.viz.display(x/1000., y/1000., theta, self.mapbytes):
				break
				exit(0)
		
	def navigate(self):
		while True:
			time.sleep(0.01) # (yield) allowing reading data from the serailport
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
				self.mover.backward()
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
			
			print(front_too_close, left_too_close, right_too_close, self.lidar.angle_180)
			
			
			

if __name__ == "__main__":
	robot = Robot()
	robot.constructmap()
