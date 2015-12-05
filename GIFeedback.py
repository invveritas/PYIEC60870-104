# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 15:21:55 2015

GIFeedback

Class that generates a "heart beat" telegram that is used to keep the client
sending the response to the GI command until everything is received

@author: Martin Baldinger / martin.baldinger@gmail.com
"""

from CommandFactory import CommandFactory

class GIFeedback(CommandFactory):
    """
    Currently a stub. This is meant to provide feedback about the progress of receiving its answers to the GI command.
    """
    def __init__(self, nr):
        CommandFactory.__init__(self)
        
        self.command.append(0x04)
        self.command.append(0x01)
        self.command.append(self.ZERO_BYTE)
        self.command.append(nr)
        self.command.append(self.ZERO_BYTE)
