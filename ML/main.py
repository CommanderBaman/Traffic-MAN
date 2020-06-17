import numpy as np
from time import perf_counter
# modules imported
from classes import TrafficModel

# This is not final and not made 
# this is just a demo that everything works properly
t1 = TrafficModel( 1, 0.2)
ncars = np.array( [[1,2,3,4,5,6,7,8,9]])

print( t1.timeVal( ncars), ncars.shape, t1.weight.shape)

ncars = np.array( [[1,2,3,4,5,6,7,8,9]])
t1.train( ncars, np.array([54]))


print( t1.weight, t1.bias, t1.isTraining)
