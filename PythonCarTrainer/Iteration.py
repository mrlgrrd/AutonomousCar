# -*- coding: utf-8 -*-


import pygame
import math
import time
from CarImage import *
from CarObject import *
import time

class Iteration:
    
    def __init__(self):
    #Variables keeping the top two fitness scores of the car.
    #Calculation algorithm is detailed below.
        self.best = 0
        self.second = 0
        #Funtion calculating time. Used to bound duration of car simulation.
        self.currentTime = lambda: int(round(time.time() * 1000))
    
    #The loop that creates a car, and drives it in the simulation untill time ends,
    #or the car crashes.
    def run(self, count, generation):
        #Start time, and reset score.
        start = self.currentTime()
        score = 0
                        
        #Initiate pygame, and a screen for simulation.          
        pygame.init()
        screen = pygame.display.set_mode((scale*sizeX,scale*sizeY))
        
        #Create a CarImage, which contains all the car data, and draws it on the screen.
        #Also initialise it with a bunch of values.
        #The car is initially positioned in the middle of the screen, close to the bottom.
        car = CarImage(CarObject(300,250,0),screen)
        string = "weights" +str(count)+ ".dat"
        try:
            car.carObject.neuralnet.readWeights(string)
        except:
            pass
        car.carObject.v=40
        car.carObject.wheelAngle=0
        
        #alternate the initial orientation of the car with each generation.
        #This makes sure the car will learn to steer both left and right.
        
        genParity = generation%2
        
        if genParity == 0:
            car.carObject.angle = math.pi/2
        else:
            car.carObject.angle = -math.pi/2
        
        #The simulation has to end if the car only turns, so keep track of this.
        turnCount = 0
        maxTurns = 2*math.pi*car.carObject.length/dt/car.carObject.v/math.sin(math.pi/6)
        
        #Game loop.    
        done=False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done=True
            if not done:
                #Change the position of the car, based on the physics programmed in CarObject
                car.carObject.changePosition()
                #Redraw screen
                screen.fill((0,0,0))            
                car.show(-car.carObject.angle) #because the y-axis is flipped, angles are reversed.
                #Update distances for input in neural network.
                car.carObject.calcDistances()
                
                #End simulation if car crashes.
                if car.checkBounds():
                    done = True
                #The car has to decide what to do based on its location, which is obtained from calcDistances.    
                car.carObject.decide()
                
                #The car gets a point of fitness score for each timestep it drives straight
                #If it only drives in circles, simulation ends because it wont get points.
                if car.carObject.wheelAngle == 0:
                    score += 1
                    turnCount = 0
                else:
                    #score += 1
                    turnCount += 1
                    if genParity == 0 and car.carObject.wheelAngle < 0:
                        score -= 6
                    if genParity == 1 and car.carObject.wheelAngle > 0:
                        score -= 6
                if turnCount > maxTurns:
                    print("Car got stuck in a loop!")
                    done = True
                #Simulation ends after 10 seconds
                if self.currentTime() - start > 10000:
                    print("Car drove without crashing!")
                    done = True
                #Switch screen buffers, pygame technicality.
                pygame.display.flip()
                #time.sleep(dt)
        #After game loop, quit pygame
        pygame.display.quit()    
        pygame.quit()
        
        #Print current best score, second best score and score of last drive for debug purposes
        #print("Score is: {}".format(score))
        #print("Best is: {}".format(best)) 
        #print("Second is: {}".format(second)) 
        
        #Save network weights, so that current best is saved in weights1,
        #and second best in weights2.
        if score > self.best:
            self.second = self.best
            try:
                file = open("weights1.dat", "r")
                secondWeights = [float(line.rstrip('\n')) for line in file]
                file.close()
                file = open("weights2.dat", "w")
                for weight in secondWeights:
                    file.write("%s\n" % weight)
                file.close()
            except:
                pass
            self.best = score
            print("New best with score: {}".format(score))
            car.carObject.neuralnet.saveWeights("weights1.dat")
        elif score > self.second:
            self.second = score
            print("New second with score: {}".format(score))
            car.carObject.neuralnet.saveWeights("weights2.dat")
    
