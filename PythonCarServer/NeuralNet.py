# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 13:12:25 2018

@author: aquelle
"""

import numpy
import math

#This class represents the neural network making the decisions for the car.
class NeuralNet:
    def __init__(self, inputs, outputs, layers, neurons):
        #It contains a number of inputs, outputs, layers and neurons, each of which
        #are arguments of the constructor.
        self.numberOfInputs = inputs
        self.numberOfOutputs = outputs
        self.numberOfLayers = layers
        self.numberOfNeurons = neurons
        #It also contains an output layer, with one neuron for each output,
        #and one input for each neuron in the previous layer.
        self.outputLayer = NeuralLayer(neurons,outputs)
        #It contains layers of hidden layers that do the calculation of the network.
        self.layers = [0 for x in range(layers)]
        #The constructor calls this function to actually fill the layers.
        self.createLayers()
    
    #Generate a neural layer object in each hidden layer, and put it in the list.
    #Since the first layer has a different number of inputs that the rest, it is created
    #outside of the for loop.
    def createLayers(self):        
        self.layers[0] = NeuralLayer(self.numberOfInputs,self.numberOfNeurons)
        for i in range(1,self.numberOfLayers):
            self.layers[i] = NeuralLayer(self.numberOfNeurons, self.numberOfNeurons)
    
    #This function calculaties an output from the input passed as a parameter.
    #It does this by using the processInput function of each layer. Note that the
    #input of each layer has a 1 prepended to it, which has its corresponding weight
    #in each Neuron. This allows for the realisation of affine, rather than linear functions.
    def processInput(self, input):
        self.layers[0].inputVector = [1]
        self.layers[0].inputVector.extend(input)
        self.layers[0].processInput()
        
        for i in range(1,self.numberOfLayers):
            self.layers[i].inputVector = [1]
            self.layers[i].inputVector.extend(self.layers[i-1].outputVector)
            self.layers[i].processInput()
            
        self.outputLayer.inputVector = [1]
        self.outputLayer.inputVector.extend(self.layers[self.numberOfLayers-1].outputVector)
        self.outputLayer.processInput()
        return self.outputLayer.outputVector
    
    #Puts all weights from the neural network in a list, and write it to a file,
    #the name of which is passed as a parameter.
    def saveWeights(self,string):
        outputVector = []
        #Append all layer weights to the output
        for i in range(self.numberOfLayers):
            for j in range(self.layers[i].numberOfNeurons):
                for k in range(self.layers[i].numberOfInputs+1):
                    outputVector.append(self.layers[i].weightMatrix[j][k])
        #Append the weights from the output layer also
        for j in range(self.outputLayer.numberOfNeurons):
                for k in range(self.outputLayer.numberOfInputs+1):
                    outputVector.append(self.outputLayer.weightMatrix[j][k])
        #Write to file.
        file = open(string, "w")
        for weight in outputVector:
            file.write("%s\n" % weight)
        file.close()
    
    #Read in weights from the filename in the parameter. Opposite of the previous
    #function.
    def readWeights(self, string):
        file = open(string, "r")
        inputVector = [float(line.rstrip('\n')) for line in file]        
        for i in range(self.numberOfLayers):
            for j in range(self.layers[i].numberOfNeurons):
                for k in range(self.layers[i].numberOfInputs+1):
                    self.layers[i].weightMatrix[j][k] = inputVector[0]
                    del inputVector[0]
        for j in range(self.outputLayer.numberOfNeurons):
                for k in range(self.outputLayer.numberOfInputs+1):
                    self.outputLayer.weightMatrix[j][k] = inputVector[0]
                    del inputVector[0]
                
    #Takes all the network weights, and perturb them randomly.
    #This allows the network to learn, by making its behaviour variable.
    def perturbWeights(self):
        weightVector = []
        #Put all network weights in a list
        for i in range(self.numberOfLayers):
            for j in range(self.layers[i].numberOfNeurons):
                for k in range(self.layers[i].numberOfInputs+1):
                    weightVector.append(self.layers[i].weightMatrix[j][k])
        #Append the weights from the output layer also
        for j in range(self.outputLayer.numberOfNeurons):
                for k in range(self.outputLayer.numberOfInputs+1):
                    weightVector.append(self.outputLayer.weightMatrix[j][k])
        #Perturb all the weights. Currently, it perturbs them by a Gaussian random variable.
        #The difference of two uniform variables is commented out, the tails of the distribution
        #are too small, so the car gets stuck with weights that give locally optimal behaviour.
        for i in range(len(weightVector)):
            weightVector[i]+= numpy.random.normal(0.0, 0.025) #numpy.random.uniform(0.0,0.05)-numpy.random.uniform(0.0,0.05)
                
        #Set the new weights
        for i in range(self.numberOfLayers):
            for j in range(self.layers[i].numberOfNeurons):
                for k in range(self.layers[i].numberOfInputs+1):
                    self.layers[i].weightMatrix[j][k] = weightVector[0]
                    del weightVector[0]
        for j in range(self.outputLayer.numberOfNeurons):
                for k in range(self.outputLayer.numberOfInputs+1):
                    self.outputLayer.weightMatrix[j][k] = weightVector[0]
                    del weightVector[0]

#This class gives the neural layers that comprise the neural network.                           
class NeuralLayer:
        
    def __init__(self, inputs, neurons):
        #Each layer has a number of inputs, and a number of neurons.
        self.numberOfInputs = inputs
        self.numberOfNeurons = neurons
        #each layer also has a vector of inputs, and a vector of outputs.
        #These are used by the processInput of the NeuralNet class
        self.inputVector = []
        self.outputVector = [0 for i in range(neurons)]
        #The weights of the layer are represented as a matrix, where each row
        #represents a neuron. The rows have length inputs+1 to allow for affine relations.
        self.weightMatrix = [[0 for j in range(inputs+1)] for i in range(neurons)] 
        #Initially, the layer is initialised with random weights. The weights can be
        #overridden using the readWeights function from NeuralNet
        self.generateRandomWeights()
    
    #This function sets the outputVector from the inputVector by left multiplying it
    #with the weightMatrix
    def processInput(self):
        for i in range(self.numberOfNeurons):
            for j in range(self.numberOfInputs+1):
                self.outputVector[i] += self.weightMatrix[i][j] * self.inputVector[j]
            self.outputVector[i] = self.sigmoid(self.outputVector[i])
    
    #Logistic function that is used on the output to make it binary.
    def sigmoid(self, x):
        try:
            e = math.exp(-x)
        except OverflowError:
            e = float('inf')
        return (1 / (1 + e));
    
    #The generateRandomWeights funtion that initialises the layer with random weights.
    def generateRandomWeights(self):
        for i in range(0,self.numberOfNeurons):
            for j in range(0,self.numberOfInputs+1):
                self.weightMatrix[i][j] = numpy.random.uniform()-numpy.random.uniform()
    
        
    
    