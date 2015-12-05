# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 15:33:00 2015

GIFactory

Class used to build a GI command telegram

@author: Martin Baldinger / martin.baldinger@gmail.com
"""

from CommandFactory import CommandFactory
from myfunctions import int_to_hex_bytes

class GIFactory(CommandFactory):
    """
    Extends CommandFactory class. It is used to send general interrogations.
    """
    def __init__(self, ASDU):
        """
        Builds the general interrogation command as a list of bytes.
        """
        CommandFactory.__init__(self)
        # 1) length of APDU
        self.command.append(14)
        
        # 2-5) Control Fields
        # leave them all zero for the moment
        # we need to care about them later, when trying to check whether 
        # telegrams arrived and were processed or not
        self.command.append(self.ZERO_BYTE)
        self.command.append(self.ZERO_BYTE)
        self.command.append(self.ZERO_BYTE)
        self.command.append(self.ZERO_BYTE)
        
        # 6) Type Identification
        self.command.append(self.TYPE_C_IC_NA_1)
        
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
        
        # 12-n) IOA is always zero for general interrogation command
        # IOA - low octet
        self.command.append(self.ZERO_BYTE)
        # IOA - high octet
        self.command.append(self.ZERO_BYTE)
        # IOA - special - always 0 in our case
        self.command.append(self.ZERO_BYTE)
        # Object Information - always one byte in our case
        self.command.append(self.GENERAL_INTERROGATION)
