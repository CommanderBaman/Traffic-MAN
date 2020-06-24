"""
OVERVIEW:
This file contains all the classes built in order to handle the 
traffic program.  

"""
import numpy as np 
from time import sleep
from os import getcwd
from sys import path 
import requests
# ML class from superclass of the traffic light
path.append( getcwd() + '/ML')
from ml_classes import TrafficModel

# getting database functions
path.append( getcwd() + '/Database Management')
from db_functions import getLastPoint

# getting IP functions
path.append( getcwd() + '/IP')
from ip_functions import detect_class_in_img


#assining values to colors
color_to_num = { 'red': 0, 'yellow':1, 'green': 2}
num_to_color = { 0: 'red', 1: 'yellow', 2: 'green'}

# directory for the vehicle and time database
vehicle_db_dir = getcwd() + '/ML/vehicleData.db'
time_db_dir = getcwd() + '/Traffic Program/timeData.db'


class Traffic_Light( TrafficModel):
    """
    making a class for handling each light
    """

    def __init__( self, tl_id, img_link, color= 'red', inactive= False):
        """
        Variables:\n
        \tcolor represents the color that is allotted to each light.\n
        \tid is a unique value allotted to recognise the light.\n
        \tinactive is a variable that decides whether to change color of light to green or not.\n
        """
        TrafficModel.__init__( self)
        self.id = tl_id
        self.color = color 
        self.inactive = inactive
        self.img_link = img_link
        requests.put('http://127.0.0.1:8000/tl/'+str(self.id),data={'color':self.color})

    def __str__( self):
        return 'This is a traffic light with color {} waiting for {} seconds'.format( self.color, self.time_val)
    
    def __repr__( self):
        return 'Traffic Light object. ID: {}, Time: {}, Color: {}'.format( self.id, self.time_val, self.color)

    @property
    def yellow_time( self):
        """calculates the yellow time of the light"""
        yt = max( 2, min( self.time_val * 0.1, 5))
        requests.put('http://127.0.0.1:8000/tl/'+str(self.id),data={'yellowTime':yt})
        return yt
    
    @property
    def green_time( self):
        """calculates the yellow time of the light""" 
        gt = max( self.time_val - self.yellow_time, 0)
        requests.put('http://127.0.0.1:8000/tl/'+str(self.id),data={'greenTime':gt})
        return gt

    @property
    def objectsArray( self):
        """
        returns the latest objects array stored in the database
        """
        return np.array( getLastPoint( db_dir= vehicle_db_dir, table_name= self.id, if_id= True))
    
    @property
    def time_val( self):
        """time_val consists the time allotted to the light\n"""
        return self.timeVal( self.objectsArray)
    
    def change_color( self, color):
        """color is either a string or a number"""
        if type( color) == str:
            self.color = color
        elif type( color) == int:
            self.color = num_to_color[color]
        else:
            raise NotImplementedError
        requests.put('http://127.0.0.1:8000/tl/'+str(self.id),data={'color':self.color})   


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

        return 'light {} handled'.format( self.id)     
    
    def img_updater( self):
        """
        updates the image link stored in the class
        """        
        r = requests.get('http://127.0.0.1:8000/current/1',headers= {'Content-type': 'application/json'})
        r = r.json()
        self.img_link = 'http://127.0.0.1:8000/' + str(r['img' + str(self.id)]) + '.jpg'
   
        return 'image updated'

    def light_trainer( self, objectsAtStart):
        """
        It trains the light variables for each point
        """
        self.img_updater()
        detect_class_in_img( self.img_link, self.id, is_url= True)
        self.train_with_object( self.threshold_decider( objectsAtStart), self.time_val)
        return None 
    
    def threshold_decider( self, objectsArray):
        """
        it gives a threshold for the current light
        """
        # write over 
        return objectsArray / 10
    
    


   

    

