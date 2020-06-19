import numpy as np
from os import getcwd
from time import sleep
# modules imported

from functions import getAllData, insertData, createConnection, createTable
"""
This contains all the code for creating the table and must only be run once
"""
# creating a database to store all the output from IP
# createConnection( getcwd() + '//ML//vehicleData.db')
# database created
vehicle_db_dir = getcwd() + '//ML//vehicleData.db'

# creating a database to store all the time output from ML
# createConnection( getcwd() + '//Traffic Program//timeData.db')
# database created
time_db_dir = getcwd() + '//Traffic Program//timeData.db'






vehicler = np.zeros( 7, dtype= 'int')
timer = [8.7]

# trial code
# creating a trial database
createConnection( 'trial.db')
createTable( 'trial.db', 'first', 'time')
# database created
insertData( 'trial.db', 'first', timer, 'time')
print( getAllData( 'trial.db', 'first'))



# createConnection( 'trial.db')
createTable( 'trial.db', 'second', 'vehicle')
# database created
insertData( 'trial.db', 'second', vehicler, 'vehicle')
print( getAllData( 'trial.db', 'second'))
