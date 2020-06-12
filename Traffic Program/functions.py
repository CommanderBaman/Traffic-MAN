import numpy as np 
from time import sleep
import threading
import msvcrt
import keyboard


def loop_exiter( key_stroke, wait):
    """returns True if key_stroke is pressed in the computer"""
    if wait:
        sleep( 1)
    if keyboard.is_pressed( key_stroke):
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
    changes all the traffic lights to active if all are inactive
    else remains the same
    if the emergency condition is there then it is also reset
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


def time_updater( intersection, time_values):
    """updates the time for all the lights"""
    
    for index, tl in enumerate( intersection):
        tl.assign_time( time_values[index])
    
    return 'time updated'

def emergency_updater( check_time, key_stroke):

    for _ in range( 100):
        # detecting the emergency only when e is pressed
        if loop_exiter( key_stroke, False):
            return True
        
        # sleeping for the rest of the time
        sleep( check_time/100)
    
    return False


