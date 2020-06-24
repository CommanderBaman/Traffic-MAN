import numpy as np 
from time import sleep, perf_counter
import threading
import requests
from sys import path 
from os import getcwd

# getting IP functions
path.append( getcwd() + '/IP')
from ip_functions import detect_class_in_img

def loop_exiter( intersection= 0):
    """returns True if key_stroke is pressed in the computer"""
    
    if intersection != 0:
        for tl in intersection:
            if tl.emergency:
                return True
        
        return False

    else:
        r = requests.get('http://127.0.0.1:8000/currentimages/1/',headers= {'Content-type': 'application/json'})
        r = r.json()
        if not r['programStarted'] :
            # print('loop_exiter is true')
            return True

    return False

def traffic_light_chooser( intersection):
    traffic_times = {} # contains all the ids and the time values for comparison
    
    for tl in intersection:
        if tl.inactive: 
            continue
        traffic_times.update( {tl.time_val : tl.id})
    
    # if no light is found then changing 
    if len( traffic_times) == 0:
        print( 'no light found')
        return 'no light found'

    # returnin the id of the traffic light chosen
    tl_chosen = max( traffic_times.keys())
    return( traffic_times[ tl_chosen])

def all_inactive_converter( intersection, DEBUG= False, emergency= False):
    """
    changes all the traffic lights to active if all are inactive\n
    else remains the same\n
    if the emergency condition is there then it is also reset\n
    """
    all_inactive = True

    for index, tl in enumerate( intersection):
        all_inactive = all_inactive and tl.inactive 
        if DEBUG:
            print( '|', index, tl.inactive, end= '|  ')
    
    if all_inactive or emergency:
        for tl in intersection:
            tl.inactive = False 
        return 'changed all to inactive'
    
    return 'some are active'


def time_updater( intersection, in_loop= False, chosen_id= 5, ip_time= False):
    """
    updates the time for all the lights by running the IP program\n
    if its is in loop then sleeps for green time - 3 seconds\n
    """

    # checking if its in the main loop 
    if in_loop:
        # just final checking
        if chosen_id > 3:
            print( 'Provided ID is wrong')
        else:
            chosen_traffic_light = intersection[ chosen_id]
            sleep_time = max( 0, chosen_traffic_light.green_time - 4)
            sleep( sleep_time)
    
    start = perf_counter()
    # running IP for the intersection
    for tl in intersection:
        tl.img_updater()
        detect_class_in_img( tl.img_link, tl.id, is_url= True)
    end = perf_counter()

    if ip_time:
        print( 'IP run in {} seconds'.format( np.round( end - start, 3)))

    return 'time updated'

def emergency_detector( check_time, intersection):
    """
    Detects if there is any emergency in the system by regularly checking the system
    """
    for _ in range( 30):
        # detecting the emergency for 30 times in a progra, 
        if loop_exiter( intersection):
            return True

        # sleeping for the rest of the time
        sleep( check_time/30)
    
    return False


def get_all_traffic_times( intersection):
    """
    gets all the traffic values from the intersection
    """

    ret_list= []

    # getting all the values
    for tl in intersection:
        ret_list.append( tl.time_val)
    
    return ret_list
