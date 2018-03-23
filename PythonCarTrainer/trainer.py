# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 16:18:18 2018

@author: AQUELLE
"""

from Iteration import *
from NeuralNet import *

#Entry point for the training routine. This file calls the run function from
#Iteration, a bunch of times, and then generates perturbed copies of the winners.

iteration = Iteration()

#Run n generations of the algorithm.
for generation in range(100):
    #In each generation, run the simulation ten times. The simulation saves the two best performing
    #sets of weights into the files weights1 and weights2.
    for count in range(1,11):
        iteration.run(count, generation)
    #After this, make four copies of the best and second best set of weights,
    #and perturb the weights of these copies. This generates networks that are 
    #close to the winners, but not identical. This random variation allows the
    #network to learn through generations.
    updateNet = NeuralNet(3,2,1,8)
    
    for i in range(4):
        string = "weights" +str(i+3)+ ".dat"    
        updateNet.readWeights("weights1.dat")
        updateNet.perturbWeights()
        updateNet.saveWeights(string)
        string = "weights" + str(i+7) + ".dat"
        updateNet.readWeights("weights2.dat")
        updateNet.perturbWeights()
        updateNet.saveWeights(string)
    
    #Reset the highscores for the next generation
    iteration.best = 0
    iteration.second = 0