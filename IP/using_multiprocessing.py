import numpy as np
from cv2 import cv2
from time import perf_counter 
from os import getcwd
import multiprocessing 

from image_functions import detect_class_in_img

img_dir = getcwd() + '\\IP\\sample images\\1.jpg'
img_dir2 = getcwd() + '\\IP\\sample images\\2.jpg'
img_dir3 = getcwd() + '\\IP\\sample images\\3.jpg'
img_dir4 = getcwd() + '\\IP\\sample images\\4.jpg'

img = cv2.imread( img_dir, 1)
img2 = cv2.imread( img_dir2, 1)
img3 = cv2.imread( img_dir3, 1)
img4 = cv2.imread( img_dir4, 1)

if __name__ == '__main__':
    start = perf_counter()


    # # this is via multiprocessing
    # process1 = multiprocessing.Process( target= detect_class_in_img, args= [img, 1])
    # process2 = multiprocessing.Process( target= detect_class_in_img, args= [img2, 1])
    # process3 = multiprocessing.Process( target= detect_class_in_img, args= [img2, 1])
    # process4 = multiprocessing.Process( target= detect_class_in_img, args= [img2, 1])

    # process1.start()
    # process2.start()
    # process3.start()
    # process4.start()


    # process1.join()
    # process2.join()
    # process3.join()
    # process4.join()

    # this is direct (comes out to be faster -?)
    print( detect_class_in_img( img, 1))
    print( detect_class_in_img( img2, 1))
    print( detect_class_in_img( img3, 1))
    print( detect_class_in_img( img4, 1))


    """
    although the multiprocessing is slower here, we need to check for the board too
    not giving more time in it 
    """

    end = perf_counter()

    print( 'time taken is ', ( end - start))
