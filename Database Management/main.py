import numpy as np
from os import getcwd
from time import sleep
# modules imported

from functions import getAllData, insertData, createConnection, createTable, getLastPoint
"""
This contains all the code for creating the table and must only be run once
"""
# creating a database to store all the output from IP
vehicle_db_dir = getcwd() + '//ML//vehicleData.db'
createConnection( vehicle_db_dir)
# database created

# creating a database to store all the time output from ML
time_db_dir = getcwd() + '//Traffic Program//timeData.db'
createConnection( time_db_dir)
# database created


# creating tables in the database 
# every light has a id which will be used to create a table and all the values will be stored there
