# -*- coding: utf-8 -*-
"""
Created on Mon Jun 08 10:41:44 2015

clsIECDoubleCommandFactory

Class that creates double command telegrams (only On/Off)

@author: Martin Baldinger / martin.baldinger@gmail.com
"""

from CommandFactory import CommandFactory
from myfunctions import int_to_hex_bytes

class CDoubleCommandFactory(CommandFactory):
    """
    Extends the CommandFactory class. It generates the double command telegrams that
    are needed to switch objects in the FPS controller ON or OFF.
    """
    def __init__(self, ASDU, IOA, CONTROL_ACTION):
        """
        Builds the telegram as a list of bytes. CONTROL_ACTION specifies whether the target
        object given by the IOA should be switched \"ON\" or \"OFF\".
        """
        CommandFactory.__init__(self)
        # 1) length of APDU
        self.command.append(10 + 4)
        
        # 2-5) Control Fields
        # leave them all zero for the moment
        # we need to care about them later, when trying to check whether 
        # telegrams arrived and were processed or not
        self.command.append(self.ZERO_BYTE)
        self.command.append(self.ZERO_BYTE)
        self.command.append(self.ZERO_BYTE)
        self.command.append(self.ZERO_BYTE)
        
        # 6) Type Identification
        self.command.append(self.TYPE_C_DC_NA_1)
        
        # 7) SQ / Number of Objects  
        self.command.append(1)
        
        # 8) T / P/N / Cause of Transmission
        self.command.append(self.COT_ACTIVATION)
        # COT is always "activation", even if switching off!!!
            
        # 9) Originator Address
        # this is always zero in our case        
        self.command.append(self.ZERO_BYTE)
        
        # 10-11) ASDU address
        asdu_bytes = int_to_hex_bytes(ASDU)
        # - low octet
        self.command.append(asdu_bytes[1])
        # - high octet
        self.command.append(asdu_bytes[0])
        
        # 12-n) IOAs + respective Object informations
        ioa_bytes = int_to_hex_bytes(IOA)
        # IOA - low octet
        self.command.append(ioa_bytes[1])
        # IOA - high octet
        self.command.append(ioa_bytes[0])
        # IOA - special - always 0 in our case
        self.command.append(self.ZERO_BYTE)
        # Object Information - always one byte in our case
        if CONTROL_ACTION == "ON":
            self.command.append(self.EXECUTE_UNSPECIFIED_ON)
        else:
            self.command.append(self.EXECUTE_UNSPECIFIED_OFF)
            
    
