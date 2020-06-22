import numpy as np
from os import getcwd
from sys import path 
# modules imported

# getting database functions
path.append( getcwd() + '\\Database Functions')
from db_functions import getLastPoint

# Write your code below

"""
defining a class for traffic model 
"""

class TrafficModel:

    def __init__( self, lr= 0.001):
        """
        initialising class
        weight and bias contain the ML parameters for the Traffic light model
        """
        self.weight= np.ones( (9, 1)) # both these are already initialised using the pre trained model
        self.bias= 1
        self.inTraining = True
        self.trainedOn = 0
        self.lr = lr
        self.trainLimit = 2
    
    @property
    def isTraining( self):
        return self.trainedOn < self.trainLimit


    def __repr__(self):
        return 'Traffic Model ML builder object'
    
    def timeVal( self, objectsArray):
        """
        Returns the red time of the light
        """
        if objectsArray == None:
            return 0
            
        return float( np.matmul( objectsArray, self.weight) + self.bias)
    
    def train( self, objectsArray, timeArray, batchSize= 1):
        """
        trains the model \n
        using Stochastic Gradient Descent (SGD) algorithm to train the model\n
        objectsArray contains the data about the number of vehicles at the light. It must a m X n array.
        where m is the number of training examples and n is the dimension of the array.\n
        timeArray contains the output value for the model. It must be a m X 1 array. 
        """
        nExamples = len( timeArray)
        t = 0 # this is a pointer on where we are on the array

        if not self.isTraining:
            # if the number of training examples given to the light are too many 
            # it won't train to avoid overfitting
            print( 'training limit surpassed')
            return None

        # below while loop handles all the gradient calculation
        while( t < nExamples):
            weightGradient = 0
            biasGradient = 0

            # this loop handles the gradient calculation
            for i in range( batchSize):
                indx = t + i

                if nExamples <= indx:
                    # break loop if going out of array
                    break 
                
                # calculating gradients
                biasGradient += ( timeArray[indx] - self.timeVal( objectsArray)) / batchSize
                weightGradient += (( timeArray[indx] - self.timeVal( objectsArray)) * objectsArray[indx].T) / batchSize
            
            t += batchSize  #increasing the pointer after calculating through 1 batch

            # We have already taken the negative factor in account by 
            # doing y - w x rather than w x - y
            weightGradient = weightGradient.reshape( -1, 1)
            
            self.weight += self.lr * weightGradient
            self.bias += self.lr * biasGradient
        
        self.trainedOn += nExamples

        return self.weight, self.bias
    
    def calcError( self, objectsArray, timeArray):
        """
        returns the mean squared error on the given input values\n
        """
        # calculating prediction values
        predArray = self.timeVal( objectsArray)
        errorArray = timeArray - predArray

        # calculating the error values
        meanSqError = np.matmul( errorArray.T, errorArray) / len( timeArray)

        return meanSqError
    

    
    


