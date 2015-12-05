# -*- coding: utf-8 -*-
"""
Created on Mon Jun 08 12:10:28 2015

DTCommandFactory

Class that generates "start datatransfer" and "stop datatransfer" telegrams

@author: Martin Baldinger / martin.baldinger@gmail.com
"""

from CommandFactory import CommandFactory

class DTCommandFactory(CommandFactory):
    """
    Extends the clsCommandFactory class. It is used to build telegrams to send
    start and stop data transfer messages.
    """
    def __init__(self, DT_ACTION):
        """
        Builds the telegram as a list of bytes. DT_ACTION is used to specify whether
        data transfer should be started (\"START\") or terminated (\"STOP\").
        """
        CommandFactory.__init__(self)
        # 1) Apdu length
        self.command.append(self.SHORT_APDU_LENGTH)
        
        # 2-4) Control Fields
        if DT_ACTION == "START":            
            self.command.append(self.STARTDT_BYTE)
        elif DT_ACTION == "STOP":
            self.command.append(self.STOPDT_BYTE)
            
        self.command.append(self.ZERO_BYTE)
        self.command.append(self.ZERO_BYTE)
        self.command.append(self.ZERO_BYTE)
