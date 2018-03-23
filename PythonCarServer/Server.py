# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 09:27:56 2018

@author: aquelle
"""

import socket
from NeuralNet import NeuralNet
import threading

#This class runs the neural network server. It inherits from Thread, so that
#the server can run in a separate thread, and not block the main thread. The
#server reads in UDP data on port 50007, and feeds it to the Neural Network
#It then sends back the output to the sender.
class Server (threading.Thread):    
    def __init__(self):        
        threading.Thread.__init__(self)
        self.us = ''
        #Sender ip is changed after every recieved data packet
        self.them = ''
        self.port = 50006
        #Create a socket on port 50007
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.us,50007))
        #Create a neural net, with weights from data file.
        self.net = NeuralNet(3,2,1,8)
        self.net.readWeights("weights.dat")
        #Set run flag, and execute run() in separate thread.
        self.runFlag = True
        self.start()        
    
    #The server loop
    def run(self):
        while self.runFlag:
            #Wait for datapacket, and save date+sender
            data, addr = self.s.recvfrom(1024) # buffer size is 1024 bytes            
            self.them = addr[0]
            #Allow for remote server stop
            stop = (data.decode('utf-8')=="Stop!")
            if stop:
                self.stop()
            #Decode datapacket into string
            data = data.decode('utf-8').strip().split()
            #If data is missing, skip
            if len(data) != 3:
                continue
            #Else, parse into numbers, and feed into neural network
            inp = []
            for x in data:
                inp.append(float(x))
            otp = self.net.processInput(inp)
            #Send back the output.
            returnString = str(otp[0])+" "+str(otp[1])
            self.send(returnString)
        
    #Function that sends back message to self.them, which is last sender of
    #a datapacket      
    def send(self, message):
        self.s.sendto(message.encode('utf-8'), (self.them, self.port))
    
    #Sets flag to exit server loop, and closes socket. Causes exception
    #if currently in recvfrom().
    def stop(self):
        self.runFlag = False
        self.s.close()
        print("Server thread ending, socket closed.")

#Create a Server objecy.        
server = Server()
        