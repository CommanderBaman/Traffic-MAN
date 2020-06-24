import numpy as np
from os import getcwd
from sys import path 
# modules imported

# Write your code below

"""
defining a class for traffic model 
"""

class TrafficModel:

    def __init__( self, lr_time= 0.003, lr_obj= 0.03):
        """
        initialising class
        weight and bias contain the ML parameters for the Traffic light model
        """
        self.weight= np.ones( (7, 1)) # both these are already initialised using the pre trained model
        self.bias= 1
        self.trainedOn = 0
        self.lr_time = lr_time
        self.lr_obj = lr_obj
        self.trainLimit = 0
    
    @property
    def isTraining( self):
        return self.trainedOn < self.trainLimit


    def __repr__(self):
        return 'Traffic Model ML builder object'
    
    def timeVal( self, objectsArray):
        """
        Returns the red time of the light
        """
        return float( np.matmul( objectsArray, self.weight) + self.bias)
    
    def train_with_time( self, objectsArray, timeArray, batchSize= 1):
        """
        trains the model given a perfect input of time\n
        using Stochastic Gradient Descent (SGD) algorithm to train the model\n
        objectsArray contains the data about the number of vehicles at the light. It must a m X n array.
        where m is the number of training examples and n is the dimension of the array.\n
        timeArray contains the output value for the model. It must be a m X 1 array.\n
        """
        nExamples = len( timeArray)
        t = 0 # this is a pointer on where we are on the array

        if not self.isTraining:
            # if the number of training examples given to the light are too many 
            # it won't train to avoid overfitting
            print( 'training limit surpassed')
            return None
        
        # reshaping objectsArray and timeArray so that they don't cause us problems
        objectsArray = np.array( objectsArray)
        objectsArray = np.reshape( objectsArray, ( -1, 7))
        timeArray = np.array( timeArray)
        timeArray = np.reshape( timeArray, ( -1, 1))

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
                biasGradient += ( timeArray[indx] - self.timeVal( objectsArray[indx])) / batchSize
                weightGradient += (( timeArray[indx] - self.timeVal( objectsArray[indx])) * objectsArray[indx].T) / batchSize
            
            t += batchSize  #increasing the pointer after calculating through 1 batch

            # We have already taken the negative factor in account by 
            # doing y - w x rather than w x - y
            weightGradient = weightGradient.reshape( -1, 1)
            
            self.weight += self.lr_time * weightGradient
            self.bias += self.lr_time * biasGradient
        
        self.trainedOn += nExamples

        return self.weight, self.bias

    def train_with_object( self, objectThreshold, timeArray, batchSize= 1):
        """
        trains the model after each traffic loop according to the threshold required
        using Stochastic Gradient Descent (SGD) algorithm to train the model\n
        objectThreshold is the value we want to achieve for the objectsArray. It must a m X n array.
        where m is the number of training examples and n is the dimension of the array.\n
        timeArray contains the output value for the model. It must be a m X 1 array.\n
        """
        t = 0 # this is a pointer on where we are on the array

        if not self.isTraining:
            # if the number of training examples given to the light are too many 
            # it won't train to avoid overfitting
            print( 'training limit surpassed')
            return None
        
        # reshaping objectsArray and timeArray so that they don't cause us problems
        objectThreshold = np.array( objectThreshold)
        objectThreshold = np.reshape( objectThreshold, ( -1, 7))
        timeArray = np.array( timeArray)
        timeArray = np.reshape( timeArray, ( -1, 1))
        nExamples = len( timeArray)

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
                biasGradient += ( self.timeVal( objectThreshold[indx]) - timeArray[indx]) / batchSize
                weightGradient += (( self.timeVal( objectThreshold[indx]) - timeArray[indx]) * objectThreshold[indx].T) / batchSize
            
            t += batchSize  #increasing the pointer after calculating through 1 batch
            weightGradient = weightGradient.reshape( -1, 1)
            
            # updating weights
            self.weight -= self.lr_obj * weightGradient
            self.bias -= self.lr_obj * biasGradient
        
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
    

    
    


