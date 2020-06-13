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
"""
import numpy as np 
from classes import Traffic_Light
from functions import loop_exiter, traffic_light_chooser, all_inactive_converter, time_updater, emergency_updater
from time import sleep
import threading

# this variable sees if the project is on trial on or not
DEBUG = True

def nothing():
    pass

# traffic_time contains all the time values 
# taking random values right now for testing
if DEBUG:
    traffic_time= np.random.randint( 10, size= 4)
else:
    traffic_time= np.random.randint( 100, size= 4)
print( 'Initial times are: ', traffic_time)

# emergency variable
emergency = False
emergency_value = 5 # contains the id of the traffic at which emergecy comes

# variable for exiting the full program
exit_program = False

light_1 = Traffic_Light( 0, traffic_time[0])
light_2 = Traffic_Light( 1, traffic_time[1])
light_3 = Traffic_Light( 2, traffic_time[2])
light_4 = Traffic_Light( 3, traffic_time[3])

intersection = [ light_1, light_2, light_3, light_4]

# making a loop that will always execute handling the operation
while( 1):
    while( not emergency):

        # breaking loop if letter q is pressed and held
        if loop_exiter( 'q', DEBUG):
            exit_program = True
            break

        if DEBUG:
            print( 'times are: ', traffic_time)
        
        # updating the times
        time_updater( intersection, traffic_time)

        # checking if all are inactive 
        print( all_inactive_converter( intersection, DEBUG))

        # choosing the light that has max time remaining and is active
        chosen_id = traffic_light_chooser( intersection)
        chosen_traffic_light = intersection[chosen_id]

        # showing the lights for the chosen traffic light
        light_thread = threading.Thread( target= chosen_traffic_light.show_light)
        light_thread.start()

        # checking for emergency vehicles while showing lights
        # for now pressing e causes emergency
        if emergency_updater( chosen_traffic_light.green_time, 'e'):
            emergency = True 
            del light_thread
            print( 'light thread deactivated:', not light_thread.is_alive())
            break

        """
        here we need to change for real values
        """
        if DEBUG:
            traffic_time= np.random.randint( 10, size= 4)
        else:
            traffic_time= np.random.randint( 100, size= 4)

        # traffic_time = [ 0, 0, 0, 0]
        # updating the times
        time_updater( intersection, traffic_time)
        

        # ending the light and preparing for next round of the green lights
        light_thread.join()

        if DEBUG:
            print( 'loop finished')
        print( '\n\n')
    
    if exit_program:
        print( 'Exiting Program')
        break


#________________________________________________________________________________________
    # in emergency conditions this runs
    if DEBUG:
        print( 'emergency condition applied')

    #changing all colors to red
    print( '\n\nchanging all colors to red')
    for tl in intersection:
        tl.change_color( 'red')
        
    """
    here we need to change for real case scenario. 
    right now choosing random values 
    """
    emergency_value = np.random.randint( 4)
    print( 'emergency at light {}'.format( emergency_value))

    # choosing the light that has emergency
    emer_id = emergency_value
    emer_traffic_light = intersection[chosen_id]   

    while( emergency):
            
        print( 'changing light {} to green-'.format( emer_id))
        emer_traffic_light.change_color( 'green')

        """
        here is another change 
        we will update emergency values here but now assigning True after 20 seconds
        we are thinking of updating after 1 second that is why there is a while loop
        """
        sleep( 20)
        emergency = False

    print( 'changing light {} to yellow for 4 seconds-'.format( emer_id))
    emer_traffic_light.change_color( 'yellow')
    sleep( 4)

    
    print( 'changing light {} to red-'.format( emer_id))
    emer_traffic_light.change_color( 'red')

    print( 'resetting the traffic lights...')
    print( all_inactive_converter( intersection, DEBUG, emergency= True))

    print( '\n\n')


        


    

    




    
    



