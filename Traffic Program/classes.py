"""
OVERVIEW:
This file contains all the classes built in order to handle the 
traffic program.  

"""
import numpy as np 
from time import sleep

#assining values to colors
color_to_num = { 'red': 0, 'yellow':1, 'green': 2}
num_to_color = { 0: 'red', 1: 'yellow', 2: 'green'}


# class Intersection:
#     """
#     making a class to handle an intersection
#     """

#     def __init__( self, num_lights= 4):
#         """
#         Variables:\n
#         \tnum_lights contains the number of lights in the intersection.
#         """
#         self.num_lights = num_lights 

#     def __str__( self):
#         return 'This is an intersection containing {} traffic lights'.format( self.num_lights)
    
#     def __repr__( self):
#         return 'intersection object. Number of lights: {}'.format( self.num_lights)


class Traffic_Light:
    """
    making a class for handling each light
    """

    def __init__( self, tl_id, time_val, color= 'red', inactive= False):
        """
        Variables:\n\ttime_val consists the time allotted to the light\n
        \tcolor represents the color that is allotted to each light.\n
        \tid is a unique value allotted to recognise the light.\n
        \tinactive is a variable that decides whether to change color of light to green or not.\n
        """
        self.id = tl_id
        self.time_val = time_val 
        self.color = color 
        self.inactive = inactive
    
    def __str__( self):
        return 'This is a traffic light with color {} waiting for {} seconds'.format( self.color, self.time_val)
    
    def __repr__( self):
        return 'Traffic Light object. ID: {}, Time: {}, Color: {}'.format( self.id, self.time_val, self.color)

    @property
    def yellow_time( self):
        """calculates the yellow time of the light"""
        return max( 2, min( self.time_val * 0.1, 5))
    
    @property
    def green_time( self):
        """calculates the yellow time of the light""" 
        return max( self.time_val - self.yellow_time, 0)

    # making functions for handling variables
    def assign_time( self, time):
        """time is an integer"""
        self.time_val = time 
    
    def change_color( self, color):
        """color is either a string or a number"""
        if type( color) == str:
            self.color = color
        elif type( color) == int:
            self.color = num_to_color[color]
        else:
            raise NotImplementedError
    
    def wait( self, light_time):
        """sleeping the program for the required amount of time"""
        sleep( light_time)
        return 'slept for {} seconds'.format(light_time)
    
    def show_light( self):
        """this shows the complete yellow and green light sequence"""

        # checking for damages in light
        if self.color != 'red' or self.time_val == 0:
            print( 'Bad Light {} time: {}  color: {}'.format( self.id, self.time_val, self.color))
            return 'Bad Light'
        
        # changing color to green 
        print( 'changing color of light {} to green for {} seconds'.format( self.id, self.green_time))
        self.change_color( 'green')
        self.wait( self.green_time)
        
        # changing color to yellow
        print( 'changing color of light {} to yellow for {} seconds'.format( self.id, self.yellow_time))
        self.change_color( 'yellow')
        self.wait( self.yellow_time)

        #changing color to red
        print( 'changing color of light {} to red'.format( self.id))
        self.change_color( 'red')
        self.inactive = True
        self.assign_time( 0)

        return 'light {} handled'.format( self.id)     
        
    



   

    

