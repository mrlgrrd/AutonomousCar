# -*- coding: utf-8 -*-

import pygame
import math
from CarObject import *
scale = 1
#A class that has all the functionality to show a rectangle representing the car
#in the main window

class CarImage:
    def __init__(self, carObject, window):
        #The object knows in what window to draw, it has a CarObject which contains
        #the physical data about the Car, and it contains an image with a rectangle.
        self.window = window
        self.carObject = carObject
        self.surface = pygame.Surface((scale*self.carObject.width+2,scale*self.carObject.length+2))
        pygame.draw.rect(self.surface,(0,128,255),pygame.Rect(1,1,scale*self.carObject.width,scale*self.carObject.length))
    
    #The class has a show function which calculates where to draw the car in the window, based on the data in the carObject.
    #It then draws the rectangle representing the car in the correct position.
    def show(self, angle):
        surface = pygame.transform.rotate(self.surface, angle*360/(2*math.pi))
        xPos = scale*self.carObject.x-surface.get_rect().width/2
        yPos = scale*self.carObject.y-surface.get_rect().height/2
        self.window.blit(surface, (xPos, yPos))
    
    #The class has a function that checks whether the car is too close the edge of the arena.
    #If it is, the car has crashed.
    def checkBounds(self):
        rect = self.surface.get_rect()
        xPos = scale*self.carObject.x
        yPos = scale*self.carObject.y
        if xPos - rect.width < 0 or xPos + rect.width > scale*sizeX or yPos - rect.height < 0 or yPos + rect.height > scale*sizeY:
            print("The car has crashed!")
            crashed = True
        else:
            crashed = False
        return crashed

#This class is not actually used. It can be used to draw dots on the screen.
#Useful for making a grid, but it slows the simulation.        
class dot:
    def __init__(self, window, xPos,yPos):
        self.window = window
        self.surface = pygame.Surface((2,2))
        self.xPos = xPos
        self.yPos = yPos
        pygame.draw.rect(self.surface,(0,0,255),pygame.Rect(0,0,2,2))
        
    def show(self):
        xPos = scale*self.xPos-1
        yPos = scale*self.yPos-1
        self.window.blit(self.surface, (xPos,yPos))