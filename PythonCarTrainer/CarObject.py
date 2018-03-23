# -*- coding: utf-8 -*-

import math
from NeuralNet import *

#Timestep of the simulation in seconds
dt = 0.01
#Size of the field in the simulation
sizeX = 600
sizeY = 300
#The angle between the vertical line through the car center of mass and
#the line through the car center of mass and one of the corners of the field.
#There are four such angles, for the UpperLeft corner, the LowerLeft, LowerRight
#and UpperRight. These are used to calculate the distance from the car to the wall.
thUL = 0
thLL = 0
thLR = 0
thUR = 0

#The object that represents the physical car.

class CarObject:
    #Constructor, initiates a car, pointing at angle from north at coordinates (x,y), stationary.
    #Several other variables are hard-coded
    def __init__(self,x,y,angle):
        #dimensions of car
        self.length = 20
        self.width = 15
        #Angle between center of bumper, car center of mass and side of bumper.
        self.cornerAngle = math.atan(self.width/self.length)
        #position of car
        self.x = x
        self.y = y
        #speed of wheels, and angle away from forward
        self.v = 0
        self.wheelAngle = 0
        #angle car makes with north, counterclockwise
        self.angle = angle
        #The distance to an obstruction at left, right and front, frontLeft, and frontRight
        self.fDist = 0
        self.flDist = 0
        self.lDist = 0
        self.rDist = 0
        self.frDist = 0
        #The car is coupled to a Neural Net, it has 1 hidden layer, 5 inputs (the above 5 distances)
        #8 neurons in the hidden layer, and two outputs, which determine if the car steers left or right.
        self.neuralnet = NeuralNet(3,2,1,8)
            
    #Moves the car, by calculating its change in position from the wheel velocity and angle.
    #It uses the functions defined below.
    def changePosition(self):
        #Put object variables in the call stack.
        v = self.v
        th = self.angle
        phi = self.wheelAngle
        length = self.length
        
        #If phi==0, car drives forward
        if phi == 0:
            dth = 0
            dx = -v*math.sin(th)*dt
            dy = v*math.cos(th)*dt            
        else:
        #If not, it will drive in a large circle.
            dth = v*math.sin(phi)*dt/length
            dx = length*math.cos(th+v*dt*math.sin(phi)/length)/math.tan(phi)-length*math.sin(th+v*dt*math.sin(phi)/length)\
                -length*math.cos(th)/math.tan(phi)+length*math.sin(th)
            dy = length*math.sin(th+v*dt*math.sin(phi)/length)/math.tan(phi)+length*math.cos(th+v*dt*math.sin(phi)/length)\
                -length*math.sin(th)/math.tan(phi)-length*math.cos(th)
        #When the appropriate change in car orientation and position is calculated,
        #update these variables.
        self.angle += dth
        self.x += dx
        self.y += dy    
       
        
    #Calculate the five distances that are inputs for the Neural Network.   
    def calcDistances(self):
        #Put angle and position on call stack. Angle is in [0,2Pi)
        th = self.angle%(2*math.pi)
        x = self.x
        y = self.y
        #These are the internal dimensions of the car, put on the call stack.
        hLength = self.length/2
        hWidth = self.width/2
        diag= math.sqrt(hLength**2 + hWidth**2)
        #first calculate at what angles the edges of the screen are:
        thUL = math.atan((x)/(sizeY-y))
        thLL = math.pi/2+math.atan((y)/(x))
        thLR = math.pi + math.atan((sizeX-x)/(y))
        thUR = 3*math.pi/2 + math.atan((sizeY-y)/(sizeX-x))
        
        #Set fDist:
        if th <= thUL or th > thUR:
            fDist = (sizeY-y)/math.cos(th)-hLength
        if th > thUL and th <= thLL:
            fDist = x/math.sin(th)-hLength
        if th > thLL and th <= thLR:
            fDist = - y / math.cos(th)-hLength
        if th > thLR and th <= thUR:
            fDist = (x - sizeX) / math.sin(th)-hLength
        
        th = (th+self.cornerAngle)%(2*math.pi)
        
        #Set flDist:
        if th <= thUL or th > thUR:
            flDist = (sizeY-y)/math.cos(th)-diag
        if th > thUL and th <= thLL:
            flDist = x/math.sin(th)-diag
        if th > thLL and th <= thLR:
            flDist = - y / math.cos(th)-diag
        if th > thLR and th <= thUR:
            flDist = (x - sizeX) / math.sin(th)-diag
        
        #Set lDist
        th = (th+math.pi/2-self.cornerAngle)%(2*math.pi)
                
        if th <= thUL or th > thUR:
            lDist = (sizeY-y)/math.cos(th)-hWidth
        if th > thUL and th <= thLL:
            lDist = x/math.sin(th)-hWidth
        if th > thLL and th <= thLR:
            lDist = - y / math.cos(th)-hWidth
        if th > thLR and th <= thUR:
            lDist = (x - sizeX) / math.sin(th)-hWidth
            
        #Set rDist
        th = (th-math.pi)%(2*math.pi)                
        if th <= thUL or th > thUR:
            rDist = (sizeY-y)/math.cos(th)-hWidth
        if th > thUL and th <= thLL:
            rDist = x/math.sin(th)-hWidth
        if th > thLL and th <= thLR:
            rDist = - y / math.cos(th)-hWidth
        if th > thLR and th <= thUR:
            rDist = (x - sizeX) / math.sin(th)-hWidth
        
        #Set frDist
        th = (th+math.pi/2-self.cornerAngle)%(2*math.pi)
        if th <= thUL or th > thUR:
            frDist = (sizeY-y)/math.cos(th)-diag
        if th > thUL and th <= thLL:
            frDist = x/math.sin(th)-diag
        if th > thLL and th <= thLR:
            frDist = - y / math.cos(th)-diag
        if th > thLR and th <= thUR:
            frDist = (x - sizeX) / math.sin(th)-diag
        
        #Finally update these variables in the object
        self.fDist = fDist
        self.lDist = lDist
        self.rDist = rDist
        self.frDist = frDist
        self.flDist = flDist
        
    #The decision function that steers the car.
    #It feeds the distances into the neural network, and updates the wheel angle.       
       
    def decide(self):
        
        #Input into the neural network. Currently we only use three of the distances
        inputs = [self.lDist, self.fDist, self.rDist]                        
        #Generate an output from the Neural Net.
        output=self.neuralnet.processInput(inputs)
        
        #Assign these outputs, and scale.   
        self.leftForce = output[0]
        self.rightForce = output[1] 
        self.leftTheta = 10*self.leftForce
        self.rightTheta = 10*self.rightForce
        
        #Steer the car, based on this output. If either left of right dominates,
        #the car steers that way, otherwise, it goes straight ahead.
        if abs(self.leftTheta - self.rightTheta) < 1:
            self.wheelAngle=0
        elif self.leftForce > self.rightForce:
            self.wheelAngle=math.pi/6
        else:
            self.wheelAngle=-math.pi/6
         
        
        
        