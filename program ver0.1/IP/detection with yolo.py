# importing required files
import numpy as np 
from cv2 import cv2 
from time import time
import os 

print( 'program started')
start = time()

# for displaying images
def see_img_shape( directory, is_array = True, frame_name= 'frame'):
	"""
	INPUT:\n
	directory is the string that contains the directory of image\n
	if already loaded then pass True in is_array.\n
	OUTPUT:\n
	Image in another window\n
	INSTRUCTIONS:\n
	Press any key to close image\n
	"""
	if not is_array:
		img = cv2.imread( directory, 1)
	else:
		img = directory
	print( img.shape)

	cv2.imshow( frame_name, img)
	cv2.waitKey( 0)
	cv2.destroyWindow( frame_name)
	return None

# variables having effect on output
DEBUG= True # decides if we want to show the time intervals between different blocks, also if we want the classified image
show_imgs= False # decides if you want to view the input image, debug needs to be true for classified image
class_confidence_thresh = 0.5
nms_thresh_val = 0.4
required_classes= [ 2, 3, 5, 7] 
other_classes= [ 0, 1, 9, 11, 12]
classes_to_identify = [ 0, 1, 2, 3, 5, 7, 9, 11, 12]


# important directories
main_folder_dir = os.getcwd() + '\\Summer Holidays \'20\\Image_Processing'
this_folder_dir = main_folder_dir + '\\ITSP'
yolo_folder = main_folder_dir + '\\yolo files'
picture_folder = this_folder_dir + '\\Images'

# importing required files for using yolo
yolo_classes_file = yolo_folder + '\\yolov3.txt'
yolo_weights_file = yolo_folder + '\\yolov3.weights'
yolo_config_file = yolo_folder + '\\yolov3.cfg'

if DEBUG:
    end1 = time()
    print( 'time taken to assign variables =', np.round( end1 - start, 3))

# importing image
image = cv2.imread( picture_folder + '\\1.jpg')
if show_imgs:
        see_img_shape( image, frame_name= 'original image')

#importing names of classes
with open( yolo_classes_file, 'r') as ycf:
    yolo_classes = ycf.read().splitlines()


if DEBUG:
    end2 = time()
    print( 'time taken to load files= ', np.round( end2 - end1, 3))

"""
Image Preprocessing
"""
# reading pre-trained model and config file (yolo)
net = cv2.dnn.readNet( yolo_weights_file, yolo_config_file)

# creating input blob
scale = 0.00392 # deifnes the scale of the image
blob = cv2.dnn.blobFromImage(image, scale, (416,416), swapRB= True, crop= False)

# getting the layer names that we need from YOLO
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# setting blob as input
net.setInput( blob)

end3 = time()
if DEBUG:
    print( 'time taken for YOLO setup = ', np.round( end3 - end2, 3))

# running YOLO and getting outputs
layerOutputs = net.forward( ln)
end_yolo = time()
print( 'time taken by YOLO = ', np.round( end_yolo - end3, 2))

# making required lists for obtaining data
pred_confidences = []
pred_classIDs = []
pred_boxes = []
height, width = image.shape[:2]
box_def_array = np.array([width, height, width, height])


# extracting data from layerOutputs list
for output in layerOutputs:
    for detection in output:

        # extracting probabilities and classes assigned from current object
        scores = detection[5:]
        classID = np.argmax(scores)
        confidence = scores[classID]

        # filtering out classes that have lowest confidences
        if confidence > class_confidence_thresh:

            if classID in classes_to_identify:
                # adding the required information
                pred_confidences.append( float( confidence))
                pred_classIDs.append( classID)

                # creating boxes 
                # YOLO gives info about the centres and the height and width of box 
                temp_box= detection[0:4] * box_def_array
                (centerX, centerY, width, height) = temp_box.astype("int") 

                # defining coordinates of top left corner of the box
                X = int( centerX - ( width / 2))
                Y = int( centerY - ( height / 2))

                pred_boxes.append( [X, Y, int( width), int( height)])

if DEBUG:
    end4 = time()
    print( 'time taken to extract info = ', np.round( end4 - end_yolo, 3))

# applying non-maxima suppression to rule out the unwanted boxes
if len( pred_boxes) > 0:
    indexes_to_keep = cv2.dnn.NMSBoxes( pred_boxes, pred_confidences, class_confidence_thresh, nms_thresh_val)
else:
    print( 'no classes identified')

if DEBUG:
    for i in indexes_to_keep.flatten():
        # taking out the required values for 
        ( X, Y, W, H) = pred_boxes[i]

        # assigning different colors to important and non important classes
        if pred_classIDs[i] in required_classes:
            color = ( 0, 0, 255)
        else:
            color = ( 0, 0, 0)

        # drawing bounding box
        cv2.rectangle( image, ( X, Y), ( X+W, Y+H), color)
        # writing class name
        cv2.putText( image, yolo_classes[pred_classIDs[i]], ( X-10, Y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    end5 = time()
    print( 'time taken to draw boxes = ', np.round( end5 - end4, 3))

    if show_imgs:
        see_img_shape( image, frame_name= 'classified image with boxes')

print( 'program ended')
print( 'time taken to run program = ', np.round( time() - start, 3))