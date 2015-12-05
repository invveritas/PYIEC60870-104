# -*- coding: utf-8 -*-
"""
Created on Thu Jun 04 17:03:51 2015

PYIEC60870Handler

Class that handles IEC60870-104 protocol communication

@author: Martin Baldinger / martin.baldinger@gmail.com
"""

import socket
from DTCommandFactory import DTCommandFactory
from DoubleCommandFactory import DoubleCommandFactory
from GIFactory import GIFactory
from GIFeedback import GIFeedback
from myfunctions import hex_to_int

class PYIEC60870Handler(object):
    BUFFERSIZE = 128
    
    def __init__(self, ASDU, IP, PORT):
        self.ASDU = ASDU
        self.IP = IP
        self.PORT = PORT
        
    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(50)

        self.s.connect((self.IP,self.PORT))
        
    def receive(self):
        return self.s.recv(self.BUFFERSIZE)    
        
    def start_datatransfer(self):
        STARTCommandFactory = DTCommandFactory("START")
        
        self.s.send(STARTCommandFactory.commandstring())
        #print(STARTCommandFactory.commandstring())
    
    def stop_datatransfer(self):
        STOPCommandFactory = DTCommandFactory("STOP")
        
        self.s.send(STOPCommandFactory.commandstring())
        #print(STOPCommandFactory.commandstring())
        
    def disconnect(self):
        # self.s.close()

    def getobjstates(self):
        # returns a list of lists [ON, OFF, INDETERMINATE, NONEXISTANT],
        # that contains the IEC numbers of the objects that are in the
        # corresponding state
    
        InterrogationCommandFactory = GIFactory(self.ASDU)
        self.s.send(InterrogationCommandFactory.commandstring())
        
        # as a response to the general interrogation command, the slave will send
        # back the following three strings:
        # 1) confirmation 680e0000000064010700030000000014
        # 2) actual data
        # 3) end string 680401000200
        received = []              
        c = 0    
 
        # to make sure, that the information regarding IOA addresses 41xxx is 
        # received, we need to receive around 60 packets
        while c<60:
            c += 1
            received.append(self.receive())
            
            # the slave will stop to send information, when it does not get a
            # feedback from the receiver. Hence, we send a quick "confirmation"
            # message to it after each recv.             
            GIIntFeedback = GIFeedback(c)  
            self.s.send(GIIntFeedback.commandstring())
                    
        data = received[1:len(received)-2]
        
        string = ""
        
        for i in range(0, len(data)):
            string += data[i].encode("hex")
        
        # split into individual telegrams
        telegrams = string.split("68")
        del(telegrams[0])
               
        # find the telegrams that contain the information about the information
        # objects with IOA addresses 41xxx.
        # Note: Communication from the slave will address them with 11xxx
        # i.e. we have to find the telegram that contains 11001 as IOA address
        # and keep all subsequent telegrams until IOA >= 12000 or we reach
        # the end of the list of telegrams
        
        # 1) IOA address is located in bytes 12 and 13, hence we cut off the
        #   first 22 characters of each telegram (we already cut off the start
        #   byte when splitting)
        for i in range(0, len(telegrams)):
            temp = telegrams[i][22:]
            telegrams[i] = temp
            
        # 2) the IOA address is now in byte 0 and 1 of each string. We convert
        #   it back to decimal numbers (keep in mind that the low byte comes 
        #   before the high byte) and delete the telegram if the IOA address
        #   does not lie within 11001 to 11999
            
        significant_telegrams = []
        for i in range(0, len(telegrams)):
            temp = hex_to_int(telegrams[i][2:4]+telegrams[i][0:2])
            if temp > 11000 and temp < 12000 and len(telegrams[i]) > 30:
                significant_telegrams.append(telegrams[i])
            
        # 3) each of the remaining telegrams contains the status information of
        #   127 information objects. We will now group all IECs (NOT IOAS!!) 
        #   into 4 lists: (remember, if the IOA is 41xxx the IEC is xxx)
        #   - ON
        #   - OFF
        #   - Indeterminate
        #   - NONEXISTENT
        
        ON = []
        OFF = []
        IND = []
        NA = []
        
        for i in range(0, len(significant_telegrams)):
            # identify the IEC number of the first object
            first = hex_to_int(\
            significant_telegrams[i][2:4]+significant_telegrams[i][0:2])
            
            # cut-off the first 3 bytes, i.e. first 6 characters
            temp = significant_telegrams[i][6:]
            
            # split it into bytes (i.e. into strings of length 2)
            hex_bytes = [temp[i:i+2] for i in range(0, len(temp), 2)]
            
            # decode every byte and put the IEC number in the corresponding list
            for i in range(0, len(hex_bytes)):
                IEC = first + i
                if hex_bytes[i] == "01":
                    OFF.append(IEC)
                elif hex_bytes[i] == "02":
                    ON.append(IEC)
                elif hex_bytes[i] == "00":
                    IND.append(IEC)
                else:
                    NA.append(IEC)
        
        return [ON, OFF, IND, NA]
        
    def switch_ON(self, IOAs):
        for i in range(0, len(IOAs)):
            ONCommandFactory = DoubleCommandFactory(self.ASDU, IOAs[i], "ON")
            self.s.send(ONCommandFactory.commandstring())
        #print(ONCommandFactory.commandstring())
        
    def switch_OFF(self, IOAs):
        for i in range(0, len(IOAs)):
            OFFCommandFactory = DoubleCommandFactory(self.ASDU, IOAs[i], "OFF")
            self.s.send(OFFCommandFactory.commandstring())
        #print(OFFCommandFactory.commandstring())
        
        
