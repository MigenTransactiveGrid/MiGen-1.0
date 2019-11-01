#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
from os import getcwd
from os.path import join as pjoin
import datetime, time
import struct
import requests
import xmltodict as x2d
def append_path(function):
    for r,d,f in os.walk(os.path.normpath(os.getcwd()+os.sep+os.pardir)):
        for files in f:
            if files == function+'.py' or files == function+'.pyc':
                url = os.path.join(r,files)
                url = url.rsplit(files)[0]
    return url
sys.path.append(append_path('SepFunc'))
import SepFunc as sf
sys.path.append(append_path('dnsdiscover'))
import dnsdiscover as dns
sys.path.append(append_path('ADE7753'))
import ADE7753 as meter
sys.path.append(append_path('ServerPath'))
import ServerPath as sp
sys.path.append(append_path('Config'))
import Config
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(os.path.normpath(os.getcwd()+os.sep+os.pardir)+'/logs.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

cwd = append_path('Server')

def certificate(function):
    for r,d,f in os.walk(os.path.normpath(os.getcwd()+os.sep+os.pardir)):
        for files in f:
            if files == function+'.pem':
                url = os.path.join(r,files)
    return url

def ClientCert(function):
    for r,d,f in os.walk(os.path.normpath(os.getcwd()+os.sep+os.pardir)):
        for files in f:
            if files == function+'.crt':
                Crturl = os.path.join(r,files)
            if files == function+'.key':
                Keyurl = os.path.join(r,files)
    return Crturl, Keyurl

def XML2EXI(JAVApath, Enginepathe, XMLpath, EXIpath, XSDpath):
    command = JAVApath + ' -jar '+ Enginepathe + ' -xml_in ' + XMLpath + ' -exi_out ' + EXIpath + ' -schema ' + XSDpath + ' -preserve_comments' + ' -preserve_pi' + ' -preserve_prefixes'
    os.system(command)

def int_to_bytes(value, length):
    result = []
    for i in range(0, length):
        result.append(value >> (i * 8) & 0xff)
    result.reverse()
    ByteArray = ''
    return result

def discovery(ip, port, path, sFDI):
    r = requests.get('https://' + ip + ':' + port + path , verify = certificate('TAserver'), \
                     cert = (ClientCert('CA')[0],ClientCert('CA')[1]), auth=('username', 'password'), timeout = 5)
    if r.status_code == 200 :
        try:
            EndDeviceList = r.text
            doc = x2d.parse(EndDeviceList)
            if int(doc['EndDeviceList']['@all'])==1:
                if int(doc['EndDeviceList']['EndDevice']['sFDI']) == str(sFDI):
                    RegistrationLink = doc['EndDeviceList']['EndDevice']['RegistrationLink']['@href']
                    FunctionSetAssignmentsListLink = doc['EndDeviceList']['EndDevice']['FunctionSetAssignmentsListLink']['@href']
                    LoadShedAvailabilityLink = doc['EndDeviceList']['EndDevice']['LoadShedAvailabilityLink']['@href']
                return RegistrationLink, FunctionSetAssignmentsListLink, LoadShedAvailabilityLink
            else:
                for i in range(int(doc['EndDeviceList']['@all'])):
                    if doc['EndDeviceList']['EndDevice'][i]['sFDI'] == str(sFDI):
                        RegistrationLink = doc['EndDeviceList']['EndDevice'][i]['RegistrationLink']['@href']
                        FunctionSetAssignmentsListLink = doc['EndDeviceList']['EndDevice'][i]['FunctionSetAssignmentsListLink']['@href']
                        LoadShedAvailabilityLink = doc['EndDeviceList']['EndDevice'][i]['LoadShedAvailabilityLink']['@href']
                return RegistrationLink, FunctionSetAssignmentsListLink, LoadShedAvailabilityLink
                
        except:
            raise
            " server is not reposnding with given URI or SFDI is not correct"

def registery(ip, port, path, sFDI, RegistrationLink):
    r = requests.get('https://' + ip + ':' + port + RegistrationLink, verify = certificate('TAserver'), \
                     cert = (ClientCert('CA')[0],ClientCert('CA')[1]), auth=('username', 'password'), timeout = 5)
    try:
        if r.status_code == 200 :
            Registration = r.text
            doc = x2d.parse(Registration)
            dateTimeRegistered = int(doc['Registration']['dateTimeRegistered'])
            pIN = int(doc['Registration']['pIN'])
    except:
        print " server is not responding! "
    return  pIN

def run(ID, mRID, LFDI):
    # ReadingType Function set#
    id1 = ID
    _href = None
    _Behaviour = 12 #0 = Not Applicable 3 = Cumulative. The sum of the previous billing period values. 4 = DeltaData (The difference between the value at the end of the prescribed interval and the beginning of the interval.)
    #6 = Indicating (As if a needle is swung out on the meter face to a value to indicate the current value)9 = Summation (A form of accumulation which is selective with respect to time. 
    #12 = Instantaneous (Typically measured over the fastest period of time allowed by the definition of the metric (usually milliseconds or tens of milliseconds.))
    #The amount of heat generated when a given mass of fuel is completely burned. 
    _calorificMltiplier = 0 #-9 = nano=x10^-9, -6 = micro=x10^-6, -3 = milli=x10^-3, 0 = none=x1 (default, if not specified), 1 = deca=x10, 2 = hecto=x100, 3 = kilo=x1000, 6 = Mega=x10^6, 9 = Giga=x10^9
    _calorificUnit = 38 #0 = Not Applicable (default, if not specified)5 = A (Current in Amperes (RMS)), 6 = Kelvin (Temperature), 23 = Degrees Celsius (Relative temperature), 29 = Voltage31 = J (Energy joule), 33 = Hz (Frequency)
    #38 =W (Real power in Watts), 42 = m3 (Cubic Meter), 61 = VA (Apparent power), 63 = var (Reactive power), 65 = CosTheta (Displacement Power Factor), 67 = V² (Volts squared), 69 = A² (Amp squared), 71 = VAh (Apparent energy)
    #72 = Wh (Real energy in Watt-hours), 73 = varh (Reactive energy), 106 = Ah (Ampere-hours / Available Charge), 119 = ft3 (Cubic Feet), 122 = ft3/h (Cubic Feet per Hour), 125 = m3/h (Cubic Meter per Hour), 128 = US gl (US Gallons)
    #129 = US gl/h (US Gallons per Hour), 130 = IMP gl (Imperial Gallons), 131 = IMP gl/h (Imperial Gallons per Hour), 132 = BTU, 133 = BTU/h, 134 = Liter, 137 = L/h (Liters per Hour), 140 = PA(gauge), 155 = PA(absolute), 169 = Therm
    _calorificValue = 0
    _commodity = 1 #0 = Not Applicable, 1 = Electricity secondary metered value (a premises meter is typically a secondary meter), 2 = Electricity primary metered value, 4 = Air, 7 = NaturalGas, 8 = Propane
    #9 = PotableWater,10 = Steam, 11 = WasteWater, 12 = HeatingFluid, 13 = CoolingFluid, 
    #Accounts for changes in the volume of gas based on temperature and pressure.
    _conversionMultiplier = 0 #-9 = nano=x10^-9, -6 = micro=x10^-6, -3 = milli=x10^-3, 0 = none=x1 (default, if not specified), 1 = deca=x10, 2 = hecto=x100, 3 = kilo=x1000, 6 = Mega=x10^6, 9 = Giga=x10^9
    _conversionUnit = 38 #0 = Not Applicable (default, if not specified)5 = A (Current in Amperes (RMS)), 6 = Kelvin (Temperature), 23 = Degrees Celsius (Relative temperature), 29 = Voltage31 = J (Energy joule), 33 = Hz (Frequency)
    #38 =W (Real power in Watts), 42 = m3 (Cubic Meter), 61 = VA (Apparent power), 63 = var (Reactive power), 65 = CosTheta (Displacement Power Factor), 67 = V² (Volts squared), 69 = A² (Amp squared), 71 = VAh (Apparent energy)
    #72 = Wh (Real energy in Watt-hours), 73 = varh (Reactive energy), 106 = Ah (Ampere-hours / Available Charge), 119 = ft3 (Cubic Feet), 122 = ft3/h (Cubic Feet per Hour), 125 = m3/h (Cubic Meter per Hour), 128 = US gl (US Gallons)
    #129 = US gl/h (US Gallons per Hour), 130 = IMP gl (Imperial Gallons), 131 = IMP gl/h (Imperial Gallons per Hour), 132 = BTU, 133 = BTU/h, 134 = Liter, 137 = L/h (Liters per Hour), 140 = PA(gauge), 155 = PA(absolute), 169 = Therm
    _conversionValue = 0
    _dataQualifier = 2 # 0 = Not Applicable, 2 = Average, 8 = Maximum, 9 = Minimum, 12 = Normal
    _flowDirection = 19 #0 = Not Applicable (default, if not specified), 1 = Forward (delivered to customer), 19 = Reverse (received from customer)
    _intervalLength = 60 # Default interval length specified in seconds.
    _kind = 37 # 0 = Not Applicable, 3 = Currency, 8 = Demand, 12 = Energy, 37 = Power
    _maxNumberOfIntervals = 1 #To be populated for mirrors of interval data to set the expected number of intervals per ReadingSet. Servers may discard intervals received that exceed this number.
    _Blocks = 0 #Number of consumption blocks. 0 means not applicable, and is the default if not specified. The value needs to be at least 1 if any actual prices are provided.
    _Tiers  = 1 #The number of TOU tiers that can be used by any resource configured by this ReadingType.
    _phase = 132 # 0 = Not Applicable (default, if not specified), 32 = Phase C (and S2), 33 = Phase CN (and S2N),40 = Phase CA, 64 = Phase B, 65 = Phase BN, 66 = Phase BC
    #128 = Phase A (and S1), 129 = Phase AN (and S1N), 132 = Phase AB, 224 = Phase ABC
    _Multiplier = 0 # -9 = nano=x10^-9, -6 = micro=x10^-6, ,3 = milli=x10^-3, 0 = none=x1 (default, if not specified), 1 = deca=x10, 2 = hecto=x100, 3 = kilo=x1000, 6 = Mega=x10^6, 9 = Giga=x10^9
    _IntervalLength = 1 # Default sub-interval length specified in seconds for Readings of ReadingType. Some demand calculations are done over a number of smaller intervals.
    _supplyLimit = 281474976710655 # Reflects the supply limit set in the meter. This value can be compared to the Reading value to understand if limits are being approached or exceeded. 
    _tiered = "false" #Specifies whether or not the consumption blocks are differentiated by TOUTier or not. Default is false, if not specified.
    _uom = 38 # 0 = Not Applicable (default, if not specified), 5 = A (Current in Amperes (RMS)), 6 = Kelvin (Temperature), 23 = Degrees Celsius (Relative temperature)
    #29 = Voltage, 31 = J (Energy joule), 33 = Hz (Frequency), 38 =W (Real power in Watts), 42 = m3 (Cubic Meter), 61 = VA (Apparent power), 63 = var (Reactive power), 65 = CosTheta (Displacement Power Factor)
    #67 = V² (Volts squared), 69 = A² (Amp squared), 71 = VAh (Apparent energy), 72 = Wh (Real energy in Watt-hours), 73 = varh (Reactive energy), 106 = Ah (Ampere-hours / Available Charge), 119 = ft3 (Cubic Feet)
    #122 = ft3/h (Cubic Feet per Hour), 125 = m3/h (Cubic Meter per Hour), 128 = US gl (US Gallons), 129 = US gl/h (US Gallons per Hour), 130 = IMP gl (Imperial Gallons), 131 = IMP gl/h (Imperial Gallons per Hour)
    #132 = BTU, 133 = BTU/h, 134 = Liter, 137 = L/h (Liters per Hour), 140 = PA(gauge), 155 = PA(absolute), 169 = Therm
    ReadingType = sf.ReadingType_FUNC(_href, _Behaviour, _calorificMltiplier, _calorificUnit, _calorificValue, _commodity, _conversionMultiplier, _conversionUnit, _conversionValue, _dataQualifier, _flowDirection, _intervalLength,\
                     _kind, _maxNumberOfIntervals, _Blocks, _Tiers, _phase, _Multiplier, _IntervalLength, _supplyLimit, _tiered, _uom)
    #print (ReadingType.toxml(element_name='ReadingType'))
    # End of ReadingType Function set

    # Reading Function set
    _href = None
    _subscribable = 0 #The subscribable values. 0 - Resource does not support subscriptions, 1 - Resource supports non-conditional subscriptions, 2 - Resource supports conditional subscriptions
    #3 - Resource supports both conditional and non-conditional subscriptions
    _localID = "\x00\x01" #A 16-bit field encoded as a hex string (4 hex characters max).
    _BlockType = 0 # 0 = Not Applicable (default, if not specified), 1 = Block 1, 2 = Block 2, 3 = Block 3, 4 = Block 4, 5 = Block 5, 6 = Block 6, 7 = Block 7, ..., 16 = Block 16
    _qualityFlags = "\x00\x00" #ist of codes indicating the quality of the reading, using specification:
    #Bit 0 - valid: data that has gone through all required validation checks and either passed them all or has been verified 
    #Bit 1 - manually edited: Replaced or approved by a human
    #Bit 2 - estimated using reference day: data value was replaced by a machine computed value based on analysis of historical data using the same type of measurement.
    #Bit 3 - estimated using linear interpolation: data value was computed using linear interpolation based on the readings before and after it
    #Bit 4 - questionable: data that has failed one or more checks
    #Bit 5 - derived: data that has been calculated (using logic or mathematical operations), not necessarily measured directly 
    #Bit 6 - projected (forecast): data that has been calculated as a projection or forecast of future readings
    _duration = 1 # Duration of the interval, in seconds.
    _start = int(time.mktime(datetime.datetime.now().timetuple())) # Date and time of the start of the interval.
    _TOUType = 0 # 0 = Not Applicable (default, if not specified), 1 = TOU A, 2 = TOU B, 3 = TOU C, 4 = TOU D, 5 = TOU E, 6 = TOU F, 7 = TOU G, 8 = TOU H, 9 = TOU I, 10 = TOU J, 11 = TOU K, 12 = TOU L, 13 = TOU M, 14 = TOU N, 15 = TOU O, 
    #meter.run()
    _value = meter.run()[0]
    Reading = sf.Reading_FUNC(_href, _subscribable, _localID, _BlockType, _qualityFlags, _duration, _start, _TOUType, _value)
    #print (Reading.toxml(element_name='Reading ', root_only=True))

    # End of Reading Function set

    # MirrorReadingSet Function set
    _href = None #'/mup/1' # IdentifiedObject -> Resource. This is a root class to provide common naming attributes for all classes needing naming attributes
    _mRID = mRID #A master resource identifier. The IANA PEN [PEN] provider ID SHALL be specified in bits 0-31, the least-significant bits, and objects created by that provider SHALL be assigned unique IDs with the remaining 96 bits. 
    #0xFFFFFFFFFFFFFFFFFFFFFFFF[XXXXXXXX], where [XXXXXXXX] is the PEN, is reserved for a object that is being created (e.g., a ReadingSet for the current time that is still accumulating). A 128-bit field encoded as a hex string (32 hex characters max). 
    _description = "Test for DemandResponseProgram" #The description is a human readable text describing or naming the object.
    _version = 0 #Version SHALL indicate a distinct identifier for each revision of an IdentifiedObject. If not specified, a default version of "0" (initial version) SHALL be assumed. 
    _duration = _duration # Duration of the interval, in seconds.
    _start = _start # Date and time of the start of the interval.
    _Reading = [Reading]
    MirrorReadingSet = sf.MirrorReadingSet_FUNC(_href, _mRID, _description, _version, _duration, _start, _Reading) #_Reading must be plural
    #print (MirrorReadingSet.toxml(element_name='MirrorReadingSet ', root_only=True))
    # End of MirrorReadingSet Function set

    # MirrorMeterReading Function set
    _href = None #'/mup/1' # IdentifiedObject -> Resource. This is a root class to provide common naming attributes for all classes needing naming attributes
    _mRID = mRID #A master resource identifier. The IANA PEN [PEN] provider ID SHALL be specified in bits 0-31, the least-significant bits, and objects created by that provider SHALL be assigned unique IDs with the remaining 96 bits. 
    #0xFFFFFFFFFFFFFFFFFFFFFFFF[XXXXXXXX], where [XXXXXXXX] is the PEN, is reserved for a object that is being created (e.g., a ReadingSet for the current time that is still accumulating). A 128-bit field encoded as a hex string (32 hex characters max). 
    _description = "Test for DemandResponseProgram" #The description is a human readable text describing or naming the object.
    _version = 0 #Version SHALL indicate a distinct identifier for each revision of an IdentifiedObject. If not specified, a default version of "0" (initial version) SHALL be assumed. 
    _duration = _duration # Duration of the interval, in seconds.
    _nextUpdateTime = 60000 # Time is a signed 64 bit value representing the number of seconds since 0 hours, 0 minutes, 0 seconds, on the 1st of January, 1970, in UTC, not counting leap seconds.
    _lastUpdateTime = _start # Time is a signed 64 bit value representing the number of seconds since 0 hours, 0 minutes, 0 seconds, on the 1st of January, 1970, in UTC, not counting leap seconds.
    _MirrorReadingSet = [MirrorReadingSet]
    _Reading = Reading
    _ReadingType = ReadingType
    MirrorMeterReading = sf.MirrorMeterReading_FUNC(_href, _mRID, _description, _version, _MirrorReadingSet, _nextUpdateTime, _lastUpdateTime, _Reading, _ReadingType)
    # End of MirrorMeterReading Function set

    # MirrorUsagePoint Function set
    _href = sp.Path2(cwd, "mup", id1)[1] #'/mup/1' # IdentifiedObject -> Resource. This is a root class to provide common naming attributes for all classes needing naming attributes
    _mRID = mRID #A master resource identifier. The IANA PEN [PEN] provider ID SHALL be specified in bits 0-31, the least-significant bits, and objects created by that provider SHALL be assigned unique IDs with the remaining 96 bits. 
    #0xFFFFFFFFFFFFFFFFFFFFFFFF[XXXXXXXX], where [XXXXXXXX] is the PEN, is reserved for a object that is being created (e.g., a ReadingSet for the current time that is still accumulating). A 128-bit field encoded as a hex string (32 hex characters max). 
    _description = "Test for DemandResponseProgram" #The description is a human readable text describing or naming the object.
    _version = 0 #Version SHALL indicate a distinct identifier for each revision of an IdentifiedObject. If not specified, a default version of "0" (initial version) SHALL be assumed. 
    _roleFlags = "\x00\x00" # Specifies the roles that apply to a usage point.
    #Bit 0 - isMirror - SHALL be set if the server is not the measurement device
    #Bit 1 - isPremisesAggregationPoint - SHALL be set if the UsagePoint is the point of delivery for a premises
    #Bit 2 - isPEV - SHALL be set if the usage applies to an electric vehicle
    #Bit 3 - isDER - SHALL be set if the usage applies to a distributed energy resource, capable of delivering power to the grid.
    #Bit 4 - isRevenueQuality - SHALL be set if usage was measured by a device certified as revenue quality
    #Bit 5 - isDC - SHALL be set if the usage point measures direct current 
    #Bit 6 - isSubmeter - SHALL be set if the usage point is not a premises aggregation point
    _ServiceKind = 0 # Service kind: 0 - electricity 1 - gas 2 - water 3 - time 4 - pressure 5 - heat 6 - cooling
    _status = 1 # Specifies the current status of the service at this usage point.0 = off 1 = on 
    _LFDI = LFDI #Contains the Long Form Device Identifier (LFDI) of the device providing the response.
    _MirrorMeterReading = [MirrorMeterReading]
    MirrorUsagePoint = sf.MirrorUsagePoint_FUNC(_href, _mRID, _description, _version, _roleFlags, _ServiceKind, _status, _LFDI, _MirrorMeterReading)
    print MirrorUsagePoint.toxml(element_name = "MirrorUsagePoint", root_only=True)

    with open(pjoin(sp.Path2(cwd, "mup", id1)[0], 'MirrorUsagePoint.xml'), 'w') as f:
        f.write(MirrorUsagePoint.toDOM(parent=None, element_name='MirrorUsagePoint').toprettyxml())

    #requests.put("https://" + ip + ":" + port + "/mup/"+ str(id1), verify = certificate("TAserver"), \
                  #cert = (ClientCert("CA")[0],ClientCert("CA")[1]), auth=("username", "password"), timeout = 5, data = MirrorUsagePoint)

if __name__ == "__main__":
    mRID = Config.MRID
    sFDI = Config.SFDI
    LFDI = Config.LFDI
    PIN = Config.PIN
    while True:
        try:
            run(1, mRID, LFDI)
            print 'New power metering is saved!'
            logger.info("New power metering is saved!")
            time.sleep((Config.METER)*60)
        except Exception as e:
            print "Error CHM01, Cannot post the metering values"
            logger.info("Error CHM01, Cannot save the metering values" + str(e))
            logging.error('Error CHM01, Cannot save the metering values: ' + str(e))
            time.sleep(5)
