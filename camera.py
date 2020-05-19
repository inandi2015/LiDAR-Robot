import cv2
import threading
from multiprocessing import Queue, Value, Lock
import time

CV_CAP_PROP_FRAME_WIDTH = 3
CV_CAP_PROP_FRAME_HEIGHT = 4

class Camera(object):
	def __init__(self):
		self.videoCap = cv2.VideoCapture(0)
		if(not self.videoCap.isOpened()):
			print("Cannot find Pi Camera")	
		self.videoCap.set(3, 320)
		self.videoCap.set(4, 240)
		self.threshold = 0.4
		self.recognized_state = 0
		self.template_size = (64, 64)
		self.recording_size = (160, 120)
		self.width = None
		self.height = None
		self.stop_template = cv2.imread('./stop.png', cv2.IMREAD_GRAYSCALE)
		self.turn_right_template = cv2.imread('./turn_right.png', cv2.IMREAD_GRAYSCALE)
		self.turn_left_template = cv2.imread('./turn_left.png', cv2.IMREAD_GRAYSCALE)
		self.preprocess()
		
	def preprocess(self):
		resized_stop_template = cv2.resize(self.stop_template, self.template_size)
		resized_turn_right_template = cv2.resize(self.turn_right_template, self.template_size)
		resized_turn_left_template = cv2.resize(self.turn_left_template, self.template_size)
		self.stop_template = cv2.Laplacian(resized_stop_template, cv2.CV_8U)
		self.turn_right_template = cv2.Laplacian(resized_turn_right_template, cv2.CV_8U)
		self.turn_left_template = cv2.Laplacian(resized_turn_left_template, cv2.CV_8U)
		# Check the results from the Laplacian transformation on templates
		#cv2.imshow("stop template", self.stop_template)
		#cv2.imshow("turn_right_template", self.turn_right_template)
		#cv2.imshow("turn_left_template", self.turn_left_template)
		
	def matching(self, lock, frame_resize, frame, template, template_id):
		match_res = cv2.matchTemplate(frame, template, cv2.TM_CCORR_NORMED)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_res)
		#print(max_val)
		if(max_val > self.threshold):
			top_left = max_loc
			bottom_right = (top_left[0] + self.template_size[0], top_left[1] + self.template_size[1])
			cv2.rectangle(frame_resize, top_left, bottom_right, (0,0,255), 2)
			lock.acquire()
			#print(template_id)
			self.recognized_state = template_id
			lock.release()
			
	def recording(self, running_state, message):
		while running_state.value:
			returnBool, frame = self.videoCap.read()
			frame_resize = cv2.resize(frame, self.recording_size)
			frame_gray = cv2.cvtColor(frame_resize, cv2.COLOR_BGR2GRAY)
			laplacian_frame = cv2.Laplacian(frame_gray, cv2.CV_8U)
			#print(laplacian_frame.shape)
			
			lock = threading.Lock() # shouldn't be useful in case the threshold is not proper
			
			thread1 = threading.Thread(target=self.matching, args=(lock, frame_resize, laplacian_frame, self.stop_template, 1))
			thread2 = threading.Thread(target=self.matching, args=(lock, frame_resize, laplacian_frame, self.turn_right_template, 2))
			thread3 = threading.Thread(target=self.matching, args=(lock, frame_resize, laplacian_frame, self.turn_left_template, 3))
			thread1.start()
			thread2.start()
			thread3.start()
			thread1.join()
			thread2.join()
			thread3.join()
			cv2.imshow('recording', frame_resize)
			if(self.recognized_state != 0):
				message.put(self.recognized_state) # put value into the message queue
				time.sleep(2) # avoid detection once again, stop updating for 2 secs
				self.recognized_state = 0
			
		    #A keyboard binding function. Its argument is the time in milliseconds. 
            #The function waits for specified milliseconds for any keyboard event. 
            #If you press any key in that time, the program continues. 
            #If 0 is passed, it waits indefinitely for a key stroke. 
			if cv2.waitKey(1) == ord('q'):			
				running_state.value = False
				break
		self.videoCap.release()
		cv2.destroyAllWindows() # Destroy the window created using imshow
		
if __name__ == "__main__":
	running = Value('b', True)
	camera = Camera()
	camera.recording(running, Queue())
