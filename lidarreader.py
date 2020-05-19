import numpy as np
import serial
import time
import threading


class lidarReader:
	def __init__(self, port, baudrate):
	    self.serialport = serial.Serial(port=port, baudrate=baudrate)
	    self.serialport.reset_input_buffer()
	    self.serialport.reset_output_buffer()
	    self.state = 0
	    # the container stores the distance for a certain angle
	    self.container = np.zeros(360)
	    #self.container = [()]*360
	    self.index = None
	    self.speed = None
	    self.angle_180 = 30000 # 30 meters is enough to be the threshold
	    self.angle_90 = 30000
	    self.angle_270 = 30000
	    self.right_container = np.empty(80) # 95-175
	    self.left_container = np.empty(80) #185-265
	    self.right_container.fill(30000) # The maximum distance that the lidar can detect is 3 meters
	    self.left_container.fill(30000)  # Fill distance array with the maximum distance  
	    self.thread = threading.Thread(target=self.read, args=())
	    self.thread.daemon = True
	    self.thread.start()
		
	def getdata(self):
	    return list(self.container)

	def read(self):
	    while True:
		try:
		    time.sleep(0.0001) # do not hog the processor power
		    #index = None
		    if(self.state == 0):
			serial_data = ord(self.serialport.read(1))
			# start byte
			if(serial_data == 0xFA):
			    self.state = 1
			else:
			    self.state = 0
		    elif(self.state == 1):
			serial_data = ord(self.serialport.read(1))
			if (serial_data >= 0xA0 and serial_data <= 0xF9):
			    self.index = serial_data - 0xA0
			    self.state = 2
			elif(serial_data != 0xFA):
			    self.state = 0
		    elif(self.state == 2):
			data = [ord(b) for b in self.serialport.read(20)]
			# speed
			b_speed = data[:2]
			
			# data
			b_data0 = data[2:6]
			b_data1 = data[6:10]
			b_data2 = data[10:14]
			b_data3 = data[14:18]

			# checksum
			b_checksum = data[18:20]

			all_data = [ 0xFA, self.index+0xA0 ] + data[:18]

			# checksum
			incoming_checksum = int(b_checksum[0]) + (int(b_checksum[1]) << 8)

			# verify that the received checksum is equal to the one computed from the data
			if self.checksum(all_data) == incoming_checksum:        
			    #self.speed = compute_speed(b_speed)              
			    self.store(0, b_data0)
			    self.store(1, b_data1)
			    self.store(2, b_data2)
			    self.store(3, b_data3)
			self.state = 0
		    else:
			self.state = 0
		except:
		    exit(0)
			    

	def store(self, offset, data):
	    angle = self.index*4 + offset
	    x1 = data[0]
	    x2 = data[1]
	    x3 = data[2]
	    x4 = data[3]
	    dist_mm = x1 | ((x2 & 0x3f) << 8) # distance
	    quality = x3 | (x4 << 8) # quality
	    #if(quality != 0): # protect data integrity
	    if(angle >= 180):
		self.container[angle-180] = dist_mm
	    else:
		self.container[angle+180] = dist_mm
		
	    #print(angle, dist_mm, quality) # data coming back is accurate
	    if(quality != 0 and dist_mm >= 150): # protect data integrity
		
		if(angle > 185 and angle <= 265): # index:0-79
		    self.left_container[angle-186] = dist_mm
		elif(angle >= 95 and angle < 175): # index:0-79
		    self.right_container[angle-95] = dist_mm
		    
		if(angle >= 90 and angle <= 95):
		    #print(angle, dist_mm)
		    self.angle_90 = dist_mm
		elif(angle >= 175 and angle <= 185):
		    #print(angle, dist_mm)
		    self.angle_180 = dist_mm
		elif(angle >= 265 and angle <= 270):
		    #print(angle, dist_mm)
		    self.angle_270 = dist_mm
	
	def checksum(self, data):
	    # Compute and return the checksum as an int
	    data_list = []
	    for t in range(10):
		data_list.append(data[2*t] + (data[2*t+1] << 8))
	    chk32 = 0
	    for d in data_list:
		chk32 = (chk32 << 1) + d
	    
	    checksum = (chk32 & 0x7FFF) + (chk32 >> 15)
	    checksum = checksum &0x7FFF
	    return int(checksum)
	    
	def compute_speed(data):
	    speed_rpm = float( data[0] | (data[1] << 8) ) / 64.0
	    return speed_rpm
				
if __name__ == "__main__":
	reader = lidarReader('/dev/mylidar', 115200)
	while True:
	    time.sleep(0.01)
	    pass
