# -*- coding: utf-8 -*-
"""
@ author:    Javad Fattahi
@ detail:    Configuration file for Customer Agent (The Great-DR project)
"""
# UNIT DETAILS
MRIDLIST = ['\x0a\xaf\x72\x05\x44\x04\xff\xa0\xed\x54\xc1\xab\x00\x00\x87\xb4', '\x29\x25\x00\x2e\x58\x6c\xf4\x62\x11\xba\x3d\xbb\x00\x00\x87\xb4', \
'\xcf\x36\x3b\x08\x5a\x91\xb7\xcd\xf1\x33\x02\x85\x00\x00\x87\xb4', '\xff\xb9\x04\x40\x8f\x24\xa5\x18\xa0\x72\x1e\x12\x00\x00\x87\xb4']
    
SFDI = 900000021002
PIN = 123456

#INTERVALS
RESPONSE = 4.1/6 # Hz
EVENT = 1.0/6 # Hz
Max_ITR = 5

# SYSTEM
TA_MRID = '\x7e\x60\xc7\x48\xe9\x95\xa4\xcc\xfb\xae\x23\x02\x00\x00\x87\xb4'
CUSTOMER_CAPACITY_RATE = 1.0 # TODO 1.0 is the capacity reduction and can be changed to other values like .2 or .25
CUSTOMER_CAPACITY = 1000
DB_NAME = 'TAdb'
PREDICTION_PERIOD = 1 # day

# MODBUS DETAILS
INVERTER_IP = "10.132.193.190"
MODBUS_PORT = 502
UNIT_ID = 100
METER_ADDR = 240
MODBUS_TIMEOUT = 30 #seconds to wait before failure

# TRANSFORMER
INITIAL_TEMP = 38.3 # Initial Temp Rise
FULL_LOAD_TEMP = 85 # Full-load Temp Rise
TAU = 24 # Time Constant
LOAD_LOSS_RASTIO = 5 # Ratio of load losses at rated load to no load loss.
COOLING = 0.9 # Forced Cooling or self cooled (n = 0.8)
RATED_TAU = ((5184 * 38.3) / 107633)# Rated Time Constant
POWER = 167e3 # Rated Power in MW %that is based on the assumption that
POWER_FACTOR = 1; 
VOLTAGE = 8.320e3 # 11.86 KV
CURRENT = 20.0 # Amp
MAX_TEMP = 185
