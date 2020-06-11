import pandas as pd 
import numpy as np
from cv2 import cv2
import matplotlib.pyplot as plt

img = black_img = np.zeros( ( 768, 1366, 3), np.uint8) # full black image
cv2.namedWindow('image')

def change_color( x):
	if cv2.getTrackbarPos( switch, 'image') == 0:
		return
	img[:] = [ cv2.getTrackbarPos( 'B', 'image'), cv2.getTrackbarPos( 'G', 'image'), cv2.getTrackbarPos( 'R', 'image')]
	return


switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'image',0,1, change_color)

cv2.createTrackbar('B','image',0,255, change_color)
cv2.createTrackbar('G','image',0,255, change_color)
cv2.createTrackbar('R','image',0,255, change_color)

while( 1):
	cv2.imshow( 'image', black_img)

	k = cv2.waitKey( 1) & 0xFF
	if k == 27:
		break

cv2.destroyWindow( 'image')