from pyModbusTCP.client import ModbusClient
import ctypes
#import win_inet_pton
import os
import sys
def append_path(function):
    for r,d,f in os.walk(os.path.normpath(os.getcwd()+os.sep+os.pardir)):
        for files in f:
            if files == function+'.py' or files == function+'.pyc':
                url = os.path.join(r,files)
                url = url.rsplit(files)[0]
    return url
sys.path.append(append_path('Config'))
import Config

# MODBUS DETAILS
INVERTER_IP = Config.INVERTER_IP
MODBUS_PORT = Config.MODBUS_PORT
UNIT_ID = Config.UNIT_ID
METER_ADDR = Config.METER_ADDR
MODBUS_TIMEOUT = Config.MODBUS_TIMEOUT #seconds to wait before failure

'''
 These classes/structures/unions, allow easy conversion between
 modbus 16bit registers and ctypes (a useful format)
'''

# Single register (16 bit) based types
class convert1(ctypes.Union):
    _fields_ = [("u16", ctypes.c_uint16),
                ("s16", ctypes.c_int16)]
    
# Two register (32 bit) based types
class x2u16Struct(ctypes.Structure):
    _fields_ = [("h", ctypes.c_uint16),
                ("l", ctypes.c_uint16)]
class convert2(ctypes.Union):
    _fields_ = [("float", ctypes.c_float),
                ("u16", x2u16Struct),
                ("sint32", ctypes.c_int32),
                ("uint32", ctypes.c_uint32)]
    
# Four register (64 bit) based types
class x4u16Struct(ctypes.Structure):
    _fields_ = [("hh", ctypes.c_uint16),
                ("hl", ctypes.c_uint16),
                ("lh", ctypes.c_uint16),
                ("ll", ctypes.c_uint16)]
class convert4(ctypes.Union):
    _fields_ = [("u16", x4u16Struct),
                ("sint64", ctypes.c_int64),
                ("uint64", ctypes.c_uint64)]

class convert16(ctypes.Union):
    _fields_ = [("sint256", ctypes.c_int64),
                ("uint256", ctypes.c_uint64)]

# Modbus instances
mb_inverter = ModbusClient(host=INVERTER_IP, port=MODBUS_PORT, auto_open=True, auto_close=True, timeout=MODBUS_TIMEOUT, unit_id=UNIT_ID)

def TX_Volt_AB():
    mb_inverter.open()
    if mb_inverter.is_open():
        Translate=convert1()
        TranslateScale=convert1()
        regs = mb_inverter.read_holding_registers(50081, 1)  # 77
        scale = mb_inverter.read_holding_registers(50084, 1) # Sunssf Scale factor
        mb_inverter.close()
    TranslateScale.u16 = scale[0]
    Translate.u16=regs[0]
    #print TranslateScale.u16
    Volt_AB = Translate.s16*(10**(-1))
    return Volt_AB
	
def TX_Volt_AN():
    mb_inverter.open()
    if mb_inverter.is_open():
        Translate=convert1()
        TranslateScale=convert1()
        regs = mb_inverter.read_holding_registers(50077, 1)  
        scale = mb_inverter.read_holding_registers(50084, 1) # Sunssf Scale factor
        mb_inverter.close()
    TranslateScale.u16 = scale[0]
    Translate.u16=regs[0]
    #print TranslateScale.u16
    Volt_AN = Translate.s16*(10**(-1))
    return Volt_AN

def TX_Volt_BN():
    mb_inverter.open()
    if mb_inverter.is_open():
        Translate=convert1()
        TranslateScale=convert1()
        regs = mb_inverter.read_holding_registers(50078, 1)  
        scale = mb_inverter.read_holding_registers(50084, 1) # Sunssf Scale factor
        mb_inverter.close()
    TranslateScale.u16 = scale[0]
    Translate.u16=regs[0]
    #print TranslateScale.u16
    Volt_BN = Translate.s16*(10**(-1))
    return Volt_BN

def TX_Volt_CN():
    mb_inverter.open()
    if mb_inverter.is_open():
        Translate=convert1()
        TranslateScale=convert1()
        regs = mb_inverter.read_holding_registers(50079, 1)  
        scale = mb_inverter.read_holding_registers(50084, 1) # Sunssf Scale factor
        mb_inverter.close()
    TranslateScale.u16 = scale[0]
    Translate.u16=regs[0]
    #print TranslateScale.u16
    Volt_CN = Translate.s16*(10**(-1))
    return Volt_CN

def TX_Freq():
    mb_inverter.open()
    if mb_inverter.is_open():
        Translate=convert1()
        TranslateScale=convert1()
        regs = mb_inverter.read_holding_registers(50085, 1)
        scale = mb_inverter.read_holding_registers(50086, 1) # Sunssf Scale factor
        mb_inverter.close()
    TranslateScale.u16 = scale[0]
    Translate.u16=regs[0]
    Freq = Translate.s16*(10**(TranslateScale.s16))
    return Freq

def TX_I_A():
    mb_inverter.open()
    if mb_inverter.is_open():
        Translate=convert1()
        TranslateScale=convert1()
        regs = mb_inverter.read_holding_registers(50072, 1)
        scale = mb_inverter.read_holding_registers(50075, 1) # Sunssf Scale factor
        mb_inverter.close()
    TranslateScale.u16 = scale[0]
    Translate.u16=regs[0]
    Currnet_A = Translate.s16*(10**(-1))
    return Currnet_A

def TX_I_B():
    mb_inverter.open()
    if mb_inverter.is_open():
        Translate=convert1()
        TranslateScale=convert1()
        regs = mb_inverter.read_holding_registers(50073, 1)
        scale = mb_inverter.read_holding_registers(50075, 1) # Sunssf Scale factor
        mb_inverter.close()
    TranslateScale.u16 = scale[0]
    Translate.u16=regs[0]
    Currnet_B = Translate.s16*(10**(-1))
    return Currnet_B

def TX_P_A():
    mb_inverter.open()
    if mb_inverter.is_open():
        Translate=convert1()
        TranslateScale=convert1()
        regs = mb_inverter.read_holding_registers(50088, 1)
        scale = mb_inverter.read_holding_registers(50091, 1) # Sunssf Scale factor
        mb_inverter.close()
    TranslateScale.u16 = scale[0]
    #print TranslateScale.s16
    Translate.u16=regs[0]
    Power_A = Translate.s16*(10**(TranslateScale.s16))
    return Power_A

def TX_P_B():
    mb_inverter.open()
    if mb_inverter.is_open():
        Translate=convert1()
        TranslateScale=convert1()
        regs = mb_inverter.read_holding_registers(50089, 1)
        scale = mb_inverter.read_holding_registers(50091, 1) # Sunssf Scale factor
        mb_inverter.close()
    TranslateScale.u16 = scale[0]
    #print TranslateScale.s16
    Translate.u16=regs[0]
    Power_B = Translate.s16*(10**(TranslateScale.s16))
    return Power_B

def TX_pf_A():
    mb_inverter.open()
    if mb_inverter.is_open():
        Translate=convert1()
        TranslateScale=convert1()
        regs = mb_inverter.read_holding_registers(50103, 1)
        scale = mb_inverter.read_holding_registers(50106, 1) # Sunssf Scale factor
        mb_inverter.close()
    TranslateScale.u16 = scale[0]
    #print TranslateScale.s16
    Translate.u16=regs[0]
    pf_A = Translate.s16*(10**(TranslateScale.s16))
    return pf_A

def TX_pf_B():
    mb_inverter.open()
    if mb_inverter.is_open():
        Translate=convert1()
        TranslateScale=convert1()
        regs = mb_inverter.read_holding_registers(50104, 1)
        scale = mb_inverter.read_holding_registers(50106, 1) # Sunssf Scale factor
        mb_inverter.close()
    TranslateScale.u16 = scale[0]
    #print TranslateScale.s16
    Translate.u16=regs[0]
    pf_B = Translate.s16*(10**(TranslateScale.s16))
    return pf_B

def run():
    return [TX_Volt_AN()+TX_Volt_BN(), TX_I_A(), TX_I_B(), TX_P_A(), TX_P_B(), TX_Freq(), TX_pf_A(), TX_pf_B()]

if __name__ == "__main__":
    data = run()



