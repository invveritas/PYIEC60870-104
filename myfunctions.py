# -*- coding: utf-8 -*-
"""
Created on Mon May 04 14:19:31 2015

@author: Martin Baldinger
"""

import datetime as dt
import math as math

def mattime_to_datetime(mattime):
    """
    takes MATLAB time mattime (float) and returns a python datetime object
    """
    datetime = dt.datetime.fromordinal(int(mattime))+\
    dt.timedelta(days=mattime%1)-dt.timedelta(days = 366)
    
    return datetime
    
def time_to_discretetime(time):
    """
    takes a time object and returns the corresponding 15 Minute time step
    of the day
    """

    # EXPRESSION WON'T WORK IN PYTHON 3
    dtime = int(time.hour)*4 + int(time.minute)/15
    
    return dtime
    
def decwords_to_float(high_word, low_word):
    """
    Converts the decimal word representation of a floating point number to the
    floating point number.
    """
    # convert to hexadecimal numbers
    hex_high = hex(high_word)
    hex_low = hex(low_word)
    
    # split hexadecimal strings 
    hexs = []
    hexs.append(hex_high[2:4])
    hexs.append(hex_high[-2:])
    hexs.append(hex_low[2:4])
    hexs.append(hex_low[-2:])
    
    # convert to binaries
    binaries = []
    for i in range(0, len(hexs)):
        binaries.append(str(bin(int(hexs[i], 16))[2:].zfill(8)))

    # create binary string
    binary = str(binaries[0])
    
    for i in range(1, len(binaries)):
        binary += str(binaries[i])
        
    # first bit represents the sign
    sign = 0
    if int(binary[0], 2) == 0:
        sign = 1
    else:
        sign = -1

    # subsequent 8 bits represent the exponent
    exponent = binary[1:9]
    exponent = int(exponent, 2) - 127
    
    # subsequent 23 bits give the mantissa
    mantissa = binary[-23:]

    if exponent != -127:
        mantissa = 1.0 + float(int(mantissa, 2)) / int("800000", 16)
    else:
        mantissa = float(int(mantissa, 2)) / int("400000", 16)
        
    # calculate float
    return sign * mantissa * math.pow(2, exponent)
    
def int_to_hex_bytes(number):
    """
    Converts an integer into its hexadecimal byte representation.
    """
    hex_number = str(hex(number))[2:]
    
    while len(hex_number)<4:
        hex_number = "".join(["0", hex_number])
          
    return [int(hex_number[:2], 16), int(hex_number[2:], 16)]
    
def hex_to_int(hexstring):
    """
    Converts a hexadecimal string into its integer equivalent.
    """
    int_number = 0
    
    for i in range(0, len(hexstring)):
        int_number += int(hexstring[i], 16) * pow(16,(len(hexstring)-1-i))
        
    return int_number
    
  
    
    
    


