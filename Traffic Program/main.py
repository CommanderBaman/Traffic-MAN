"""
OVERVIEW:\n
Making a trial program for assigning the red lights of the\n 
according to the inputs made by the ML division. \n\n

THEORY:
assign green light to the one which has the greatest time in\n
the array inputted\n
\n
INPUT:\n
a numpy array from ML file that contains the time required to\n
clean the intersections\n
\n
WARNING:\n
Training is turned off. Turn it on by increasing the trainLimit\n
in ml_classes file in ML folder
"""
import numpy as np 
from classes import Traffic_Light
from functions import loop_exiter, traffic_light_chooser, all_inactive_converter, time_updater, emergency_detector, get_all_traffic_times
from time import sleep
import threading
from sys import path 
from os import getcwd

# this variable sees if the project is on trial on or not
DEBUG = True

#will have to change manually to change default display images
img_dir =  'http://127.0.0.1:8000/1.jpg'
img_dir2 = 'http://127.0.0.1:8000/2.jpg'
img_dir3 = 'http://127.0.0.1:8000/3.jpg'
img_dir4 = 'http://127.0.0.1:8000/4.jpg'

# traffic_time contains all the time values 
# taking random values right now for testing

# emergency variable
emergency_loop = False

# variable for exiting the full program
exit_program = False

# defining the traffic lights Here we have to add actual links to the images
light_1 = Traffic_Light( 0, img_dir)
light_2 = Traffic_Light( 1, img_dir2)
light_3 = Traffic_Light( 2, img_dir3)
light_4 = Traffic_Light( 3, img_dir4)

intersection = [ light_1, light_2, light_3, light_4]

# getting the initial times by running the IP part
time_updater( intersection, ip_time= DEBUG)  # IP call

# making a loop that will always execute handling the operation
while( 1):
    while( not emergency_loop):

        # breaking loop if letter q is pressed and held
        if loop_exiter():
            exit_program = True
            break

        if DEBUG:
            print( 'times are: ', get_all_traffic_times( intersection))
        

        # checking if all are inactive 
        print( all_inactive_converter( intersection, DEBUG))

        # choosing the light that has max time remaining and is active
        chosen_id = traffic_light_chooser( intersection)
        chosen_traffic_light = intersection[chosen_id]
        objectsAtStart = chosen_traffic_light.objectsArray
        greenTime = chosen_traffic_light.green_time

        # showing the lights for the chosen traffic light
        light_thread = threading.Thread( target= chosen_traffic_light.show_light, args= [intersection])
        light_thread.start()

        # updating the values and using a thread to do it to leave the emergency 
        update_thread = threading.Thread( target= time_updater, args= [ intersection, True, chosen_id]) # IP call
        update_thread.start()

        # checking for emergency vehicles while showing lights
        # for now pressing button on website causes emergency
        if emergency_detector( greenTime, intersection):
            emergency_loop = True 
            break

        """
        here we need to change for real values
        """        

        # ending the light and preparing for next round of the green lights
        light_thread.join()
        update_thread.join()

        # goes into training only if limit is not passed
        if chosen_traffic_light.isTraining:
            train_thread = threading.Thread( target= chosen_traffic_light.light_trainer, args= [objectsAtStart]) # IP call
            train_thread.start()

        if DEBUG:
            print( 'loop finished')
        print( '\n\n')
    
    if exit_program:
        print( 'Exiting Program')
        break


#________________________________________________________________________________________
    # in emergency conditions this thing runs
    if DEBUG:
        print( 'emergency condition applied')
    
    # changing current green traffic light to yellow for 2 seconds
    chosen_traffic_light.change_color( 'yellow', from_emergency= True)
    sleep( 2)

    #changing all colors to red
    print( '\n\nchanging all colors to red')
    for tl in intersection:
        tl.change_color( 'red')
        
    # extracting the light number
    for indx, tl in enumerate( intersection):
        if tl.emergency:
            emer_id = indx 

    print( 'emergency at light {}'.format( emer_id))

    # choosing the light that has emergency
    emer_traffic_light = intersection[emer_id]   

    # giving input to the chosen light to stop its process
    chosen_traffic_light.was_emergency = True

    print( 'changing light {} to green-emergency'.format( emer_id))
    emer_traffic_light.change_color( 'green', emergency_loop)

    emer_timer = 0

    # checking for emergency after every second
    while( emergency_loop):
        sleep( 1)
        emer_timer += 1
        emergency_loop = emer_traffic_light.emergency 

    ip_thread = threading.Thread( target= time_updater, args=[intersection])
    ip_thread.start()

    print( 'Emergency for {} seconds'.format( emer_timer))
    print( 'changing light {} to yellow for 5 seconds-emergency'.format( emer_id))
    emer_traffic_light.change_color( 'yellow', True)
    sleep( 5)
    
    print( 'changing light {} to red-emergency'.format( emer_id))
    emer_traffic_light.change_color( 'red', True)

    print( 'resetting the traffic lights...')
    print( all_inactive_converter( intersection, DEBUG, emergency= True))

    emergency_loop = False
    ip_thread.join()

    print( '\n\n')


        


    

    




    
    



