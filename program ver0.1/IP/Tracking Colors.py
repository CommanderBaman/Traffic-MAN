import pandas as pd 
import numpy as np
from cv2 import cv2
import matplotlib.pyplot as plt

def object_tracker_by_color( colors= ['take_value'], lower_val= np.array([0,0,0]), upper_val= np.array([178,255,255]),
							 show_mask= False, show_original= True):
	"""
	Captures and shows a video and displays chosen color = 'blue', 'green' and 'red'\n
	INPUT:\n
	Colors (list) should be the names of the color to be tracked. supported: 'blue', 'green' and 'red'\n
	For specific colors type the lower and upper values in the lower_val and upper_val, in HSV format as numpy arrays\n
	show_mask (bool), if set True, will display what portions of video are being shown\n
	show_original (bool), if set True will display the original image.\n
	OUTPUT:\n
	A video named 'tracker' showing the objects being tracked\n
	"""
	cap = cv2.VideoCapture(0)
	
	while(1):
		_, frame = cap.read()
		img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		mask = cv2.inRange( img_hsv, lower_val, upper_val)

		# define range of color in HSV
		if len( colors) == 1:
			if colors[0] == 'red':	
				lower_val = np.array([-10,100,100])
				upper_val = np.array([10,255,255])
			elif colors[0] == 'blue':
				lower_val = np.array([110,100,100])
				upper_val = np.array([130,255,255])
			elif colors[0] == 'green':
				lower_val = np.array([50,100,100])
				upper_val = np.array([70,255,255])
			
			# Threshold the HSV image to get only selected colors
			mask = cv2.inRange( img_hsv, lower_val, upper_val)
		
		else: 
			for i in colors:
				if i == 'red':	
					lower_val = np.array([-10,100,100])
					upper_val = np.array([10,255,255])
				elif i == 'blue':
					lower_val = np.array([110,100,100])
					upper_val = np.array([130,255,255])
				elif i == 'green':
					lower_val = np.array([50,100,100])
					upper_val = np.array([70,255,255])

				mask = cv2.bitwise_or( mask, cv2.inRange( img_hsv, lower_val, upper_val))

		# Bitwise-AND mask and original image
		res = cv2.bitwise_and( frame, frame, mask= mask)

		if show_original:
			cv2.imshow( 'original', frame)
		if show_mask:
			cv2.imshow( 'mask', mask)

		cv2.imshow( 'tracker', res)

		#exit strategy
		k = cv2.waitKey(100) & 0xFF
		if k == 27:
			break

	return None

object_tracker_by_color( colors= ['red', 'green', 'blue'])
cv2.destroyAllWindows()