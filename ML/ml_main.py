import numpy as np
from time import perf_counter
# modules imported
from ml_classes import TrafficModel

# This is not final and not made 
# this is just a demo that everything works properly
t1 = TrafficModel( lr_obj= 0.03)
ncars = np.array( [[1,2,3,4,5,6,7]])
nthresh = np.array([1,1,0,0,2,1,1])

print( t1.timeVal( nthresh), ncars.shape, t1.weight.shape)

for _ in range( 100):
    t1.train_with_object( nthresh, np.array([48]))
    print( t1.timeVal( nthresh), ncars.shape, t1.weight.shape)

print( t1.weight, t1.bias, t1.isTraining)
