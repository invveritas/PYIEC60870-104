# -*- coding: utf-8 -*-
"""
Created on Mon Jun 08 11:10:28 2015

CommandFactory

Parent class for command factory classes

@author: Martin Baldinger - martin.baldinger@gmail.com
"""

class CommandFactory(object):
    """
    Parent class to all IEC command factories. It holds the definitions of some individual bytes.
    If additional bytes are needed while extending the protocol, it is recommended to add their
    definitions here.

    Currently, the following bytes are available:

        START_BYTE = 0x68
        
        ZERO_BYTE = 0x00
        
        SHORT_APDU_LENGTH = 0x04
        
        STARTDT_BYTE = 0x07
        STOPDT_BYTE = 0x13
        
        TYPE_C_DC_NA_1 = 0x2E
        
        TYPE_C_IC_NA_1 = 0x64
        
        COT_ACTIVATION = 0x06
        
        COT_DEACTIVATION = 0x08
        
        EXECUTE_UNSPECIFIED_OFF = 0x01
        
        EXECUTE_UNSPECIFIED_ON = 0x02
        
        GENERAL_INTERROGATION = 0x14
    """
    
    START_BYTE = 0x68
    ZERO_BYTE = 0x00
    SHORT_APDU_LENGTH = 0x04
    STARTDT_BYTE = 0x07
    STOPDT_BYTE = 0x13
    TYPE_C_DC_NA_1 = 0x2E # double command
    TYPE_C_IC_NA_1 = 0x64 # general interrogation
    COT_ACTIVATION = 0x06
    COT_DEACTIVATION = 0x08
    EXECUTE_UNSPECIFIED_OFF = 0x01
    EXECUTE_UNSPECIFIED_ON = 0x02
    GENERAL_INTERROGATION = 0x14
    
    def __init__(self):
        """
        Initializes the command sequence list and adds the START_BYTE as the first element.
        """
        self.command = []
        
        # 0) start byte is the same for all commands
        self.command.append(self.START_BYTE)
        
    def commandstring(self):
        """
        Converts the command sequence list of bytes into the command string.
        """
        return "".join(map(chr, self.command))
    
