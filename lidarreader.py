import numpy as np
import serial
import threading

        

class lidarReader:
	def __init__(self, port, baudrate):
		self.serialport = serial.Serial(port=port, baudrate=baudrate)
		# the container stores the distance for a certain angle
		self.container = np.zeros(360)
		self.serialport.reset_input_buffer()
		self.serialport.reset_output_buffer()
		self.thread = threading.Thread(target=self.read, args=())
		#self.thread.daemon = True
		self.thread.start()
	
	def prepare(self):
		while(len(self.serialport.readline().split(",")) != 4): # "A" sign, distance, angle, quality
			self.serialport.write(b'ShowDist\n')

	def read(self):
		self.prepare()
		while True:
			line = self.serialport.readline()   # read a '\n' terminated line 
			data = line.split(",")
			if(data[1].isdigit() and int(data[1]) < 360): # shouldn't be false, put here just in case of transimisson error
				self.container[int(data[1])] = int(data[2])
			#print(angle, distance)
			
if __name__ == "__main__":
	reader = lidarReader('/dev/ttyACM0', 115200)
