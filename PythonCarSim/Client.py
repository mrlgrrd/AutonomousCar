# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 15:27:14 2018

@author: aquelle
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 09:27:56 2018

@author: aquelle
"""

import socket
import threading

#This class runs the neural network client. It inherits from Thread, so that
#the client can run in a separate thread, and not block the main thread.
class Client (threading.Thread):    
    def __init__(self, car):        
        threading.Thread.__init__(self)
        self.car = car
        self.us = ''
        self.them = open('ip.dat').readline().strip()
        self.port = 50007
        #Create a socket on port 50007
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.settimeout(10)
        self.s.bind((self.us,50006))
        #Set run flag, and execute run() in separate thread.
        self.runFlag = True
        self.start()        
    
    #The server loop
    def run(self):
        while self.runFlag:
            #Wait for datapacket, and save date+sender
            try:
                data, addr = self.s.recvfrom(1024) # buffer size is 1024 bytes
                #Decode data into text
                data = data.decode('utf-8').strip().split()
                #If data is missing, skip
                if len(data) != 2:
                    continue
                #Else, parse into numbers, and feed into neural network
                for x in range(len(data)):
                    self.car.output[x]=float(data[x])
                self.car.decide()
            except:
                pass
        
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