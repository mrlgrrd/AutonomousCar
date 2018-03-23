# -*- coding: utf-8 -*-


import pygame
import math
import time
from CarImage import CarImage
from CarObject import *
import time
import numpy
                
#Initiate pygame, and a screen for simulation.          
pygame.init()
screen = pygame.display.set_mode((CarImage.scale*sizeX,CarImage.scale*sizeY))

#Create a CarImage, which contains all the car data, and draws it on the screen.
#Also initialise it with a bunch of values.
#The car is initially positioned in the middle of the screen, close to the bottom.
car = CarImage(CarObject(500,300,0),screen)
car.carObject.v=40
car.carObject.wheelAngle=0

car.carObject.angle = numpy.random.uniform(0, 2*math.pi)

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
        car.carObject.client.send(str(car.carObject.input[0]) + " " + str(car.carObject.input[1]) + " " +str(car.carObject.input[2]))
        #End simulation if car crashes.
        if car.checkBounds():
            done = True
        #The car has to decide what to do based on its location, which is obtained from calcDistances.
        car.carObject.decide()
        
        #Switch screen buffers, pygame technicality.
        pygame.display.flip()
        #time.sleep(dt)
#After game loop, quit pygame
car.carObject.client.stop()
pygame.display.quit()    
pygame.quit()
exit()
    
