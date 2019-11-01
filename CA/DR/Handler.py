from time import sleep
import os
import requests
import xmltodict as x2d
from datetime import datetime
import time
import sys
from os.path import join as pjoin

itt = 1

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

def certificate(function):
    for r,d,f in os.walk(os.path.normpath(os.getcwd()+os.sep+os.pardir)):
        for files in f:
            if files == function+'.pem':
                url = os.path.join(r,files)
    return url

def DRresponse_path(function):
    for r,d,f in os.walk(os.path.normpath(os.getcwd()+os.sep+os.pardir)):
        for files in f:
            if files == function+'.xml' or files == function+'.exi':
                url = os.path.join(r,files)
                url = url.rsplit(function)[0]
    return url

def ClientCert(function):
    for r,d,f in os.walk(os.path.normpath(os.getcwd()+os.sep+os.pardir)):
        for files in f:
            if files == function+'.crt':
                Crturl = os.path.join(r,files)
            if files == function+'.key':
                Keyurl = os.path.join(r,files)
    return Crturl, Keyurl

def discovery(ip, port, path, sFDI):
    print 'https://' + ip + ':' + port + path
    r = requests.get('https://' + ip + ':' + port + path, verify = certificate('TAserver'), cert = (ClientCert('CA')[0],ClientCert('CA')[1]), auth=('username', 'password'), timeout=3)
    sleep(3)
    if r.status_code == 200 :
        try:
            EndDeviceList = r.text
            doc = x2d.parse(EndDeviceList)
            if int(doc['EndDeviceList']['@all'])==1:
                if doc['EndDeviceList']['EndDevice']['sFDI'] == str(sFDI):
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
            print " server is not reposnding with given URI or SFDI is not correct"

def registery(ip, port, path, sFDI, RegistrationLink):
    r = requests.get('https://' + ip + ':' + port + RegistrationLink,  verify = certificate('TAserver'),\
                     cert = (ClientCert('CA')[0],ClientCert('CA')[1]), auth=('username', 'password'), timeout = 3)
    sleep(3)
    try:
        if r.status_code == 200 :
            Registration = r.text
            doc = x2d.parse(Registration)
            dateTimeRegistered = int(doc['Registration']['dateTimeRegistered'])
            pIN = int(doc['Registration']['pIN'])
    except:
        print " server is not responding! "
    return  pIN

def AssignmentLink(mRID, FunctionSetAssignmentsListLink):
    mRID = mRID.encode('hex')
    mRID = mRID.upper()
    try:
        r = requests.get('https://' + ip + ':' + port + FunctionSetAssignmentsListLink,  verify = certificate('TAserver'), \
                     cert = (ClientCert('CA')[0],ClientCert('CA')[1]), auth=('username', 'password'), timeout = 3)
        sleep(3)
        FSAL = r.text
        doc = x2d.parse(FSAL)
        if int(doc['FunctionSetAssignmentsList']['@all'])==1:
            if doc['FunctionSetAssignmentsList']['FunctionSetAssignments']['mRID'] == mRID:
                url = doc['FunctionSetAssignmentsList']['FunctionSetAssignments']['@href']
                r = requests.get('https://' + ip + ':' + port + url,  verify = certificate('TAserver'), \
                     cert = (ClientCert('CA')[0],ClientCert('CA')[1]), auth=('username', 'password'), timeout = 3)
                sleep(3)
                FSA = r.text
                dox = x2d.parse(FSA)
                DemandResponseProgramListLink = dox['FunctionSetAssignments']['DemandResponseProgramListLink']['@href']
                DERProgramListLink = dox['FunctionSetAssignments']['DERProgramListLink']['@href']
                ResponseSetListLink = dox['FunctionSetAssignments']['ResponseSetListLink']['@href']
                UsagePointListLink = dox['FunctionSetAssignments']['UsagePointListLink']['@href']
        else:
            for i in range(int(doc['FunctionSetAssignmentsList']['@all'])):
                if doc['FunctionSetAssignmentsList']['FunctionSetAssignments'][i]['mRID'] == mRID:
                    url = doc['FunctionSetAssignmentsList']['FunctionSetAssignments'][i]['@href']
                    r = requests.get('https://' + ip + ':' + port + url,  verify = certificate('TAserver'), \
                     cert = (ClientCert('CA')[0],ClientCert('CA')[1]), auth=('username', 'password'), timeout = 3)
                    sleep(3)
                    FSA = r.text
                    dox = x2d.parse(FSA)
                    DemandResponseProgramListLink = dox['FunctionSetAssignments']['DemandResponseProgramListLink']['@href']
                    DERProgramListLink = dox['FunctionSetAssignments']['DERProgramListLink']['@href']
                    ResponseSetListLink = dox['FunctionSetAssignments']['ResponseSetListLink']['@href']
                    UsagePointListLink = dox['FunctionSetAssignments']['UsagePointListLink']['@href']
        return url, DemandResponseProgramListLink, DERProgramListLink, ResponseSetListLink, UsagePointListLink
    except:
        print " Server is not running or mRID is wrong! "
        pass

def ActiveEndDeviceLink(id1, id2):
    _href = sp.Path3(append_path('Server'), 'dr', id1, 'actedc')[1]
    _all = 1
    ActiveEndDeviceControlListLink = sf.ActiveEndDeviceControlListLink_FUNC(_href, _all)
    return ActiveEndDeviceControlListLink

def EndDeviceControlLL(id1, id2):
    _href = sp.Path3(append_path('Server'), 'dr', id1, 'edc')[1]
    _all = 1 
    EndDeviceControlListLink = sf.EndDeviceControlListLink_FUNC(_href, _all)
    return EndDeviceControlListLink

def DemandResponseP(doc, mRID, id1, id2, i):
    _href_Dr = sp.Path2(append_path('Server'), 'dr', id1)[1]
    _mRID = mRID
    _description =  'GREAT-DR round# ' + str(i)
    _version = int(doc['DemandResponseProgram']['version'])
    _ActiveEndDeviceControlListLink = ActiveEndDeviceLink(id1, id2)
    _availabilityUpdatePercentChangeThreshold = int(doc['DemandResponseProgram']['availabilityUpdatePercentChangeThreshold'])
    _multiplier = int(doc['DemandResponseProgram']['availabilityUpdatePowerChangeThreshold']['multiplier'])
    _value = int(doc['DemandResponseProgram']['availabilityUpdatePowerChangeThreshold']['value'])
    _availabilityUpdatePowerChangeThreshold = 1 # TODO: wipe
    _EndDeviceControlListLink = EndDeviceControlLL(id1, id2)
    _primacy = int(doc['DemandResponseProgram']['primacy'])
    DemandResponseProgram = sf.DemandResponseProgram_FUNC(_href_Dr, _mRID, _description, _version, _ActiveEndDeviceControlListLink, _availabilityUpdatePercentChangeThreshold, _multiplier, _value, _availabilityUpdatePowerChangeThreshold, _EndDeviceControlListLink, _primacy)
    #print (DemandResponseProgram.toxml(element_name='DemandResponseProgram'))
    with open(pjoin(sp.Path2(append_path('Server'), 'dr', id1)[0], 'DemandResponseProgram.xml'), 'w') as f:
        f.write(DemandResponseProgram.toDOM().toprettyxml())

    JAVApath = 'java' #'/usr/java/jdk1.8.0_171/bin/java'
    Enginepathe = pjoin(append_path('Server'), 'ExiProcessor\ExiProcessor.jar')
    XMLpath = pjoin(sp.Path2(append_path('Server'), 'dr', id1)[0], 'DemandResponseProgram.xml')
    EXIpath = pjoin(sp.Path2(append_path('Server'), 'dr', id1)[0], 'DemandResponseProgram.exi')
    XSDpath = pjoin(append_path('Server'), 'sep.xsd')
    #XML2EXI(JAVApath, Enginepathe, XMLpath, EXIpath, XSDpath)
    return DemandResponseProgram

def EndDeviceC(doc, mRID, id1, id2, i):
    _href = sp.Path4(append_path('Server'), 'dr', id1, 'edc', id2)[1]
    _replyTo = sp.Path4(append_path('Server'), 'rsps', id1, 'rsp', id2)[1]
    ReplyTo = doc['EndDeviceControl']['@replyTo']
    _responseRequired = doc['EndDeviceControl']['@responseRequired']
    _mRID = mRID
    _description =  'GREAT-DR round# ' + str(i)
    _version = 0
    _subscribable = int(doc['EndDeviceControl']['@subscribable'])
    _currentStatus = int(doc['EndDeviceControl']['EventStatus']['currentStatus']) # 0 = Scheduled, 1 = Active, 2 = Cancelled, 3 = Cancelled with Randomization, 4 = Superseded
    _dateTime = int(time.mktime(datetime.now().timetuple()))
    if doc['EndDeviceControl']['EventStatus']['potentiallySuperseded'] == 'false':
        _potentiallySuperseded = 0
    else:
        _potentiallySuperseded = 1
    _potentiallySupersededTime = int(doc['EndDeviceControl']['EventStatus']['potentiallySupersededTime'])
    _reason = doc['EndDeviceControl']['EventStatus']['reason']
    _creationTime = int(doc['EndDeviceControl']['creationTime'])
    _duration =  int(doc['EndDeviceControl']['interval']['duration'])
    _start = int(doc['EndDeviceControl']['interval']['start'])
    _randomizeDuration = int(doc['EndDeviceControl']['randomizeDuration'])
    _randomizeStart =  int(doc['EndDeviceControl']['randomizeStart'])
    _ApplianceLoadReductionType =  int(doc['EndDeviceControl']['ApplianceLoadReduction']['type'])
    _DeviceCategoryType = '\x00\x00\x00\x00'
    if doc['EndDeviceControl']['drProgramMandatory'] == 'false':
        _drProgramMandatory = 0
    else:
        _drProgramMandatory = 1
    _DutyCycleValue = int(doc['EndDeviceControl']['DutyCycle']['normalValue'])
    if doc['EndDeviceControl']['loadShiftForward']== 'false':
        _loadShiftForward = 0
    else:
        _loadShiftForward = 1
    _coolingOffset = int(doc['EndDeviceControl']['Offset']['coolingOffset'])
    _heatingOffset = int(doc['EndDeviceControl']['Offset']['heatingOffset'])
    _loadAdjustmentPercentageOffset = int(doc['EndDeviceControl']['Offset']['loadAdjustmentPercentageOffset'])
    _overrideDuration = int(doc['EndDeviceControl']['overrideDuration'])
    _coolingSetpoint = int(doc['EndDeviceControl']['SetPoint']['coolingSetpoint'])
    _heatingSetpoint = int(doc['EndDeviceControl']['SetPoint']['heatingSetpoint'])
    _ReductionType = int(doc['EndDeviceControl']['TargetReduction']['type'])
    _ReductionValue = int(doc['EndDeviceControl']['TargetReduction']['value'])

    EndDeviceControl = sf.EndDeviceControl_FUNC(_href, _replyTo, _responseRequired, _mRID, _description, _version, _subscribable, _currentStatus, _dateTime, _potentiallySuperseded, _potentiallySupersededTime,\
                                             _reason, _creationTime, _duration, _start, _randomizeDuration, _randomizeStart, _ApplianceLoadReductionType, _DeviceCategoryType, _drProgramMandatory, _DutyCycleValue, _loadShiftForward,\
                                             _coolingOffset, _heatingOffset, _loadAdjustmentPercentageOffset, _overrideDuration, _coolingSetpoint, _heatingSetpoint, _ReductionType, _ReductionValue)
    #print (EndDeviceControl.toxml(element_name='EndDeviceControl'))
    with open(pjoin(sp.Path4(append_path('Server'), 'dr', id1, 'edc', id2)[0], 'EndDeviceControl.xml'), 'w') as f:
        f.write(EndDeviceControl.toDOM(parent=None, element_name='EndDeviceControl').toprettyxml())

    JAVApath = 'java' #'/usr/java/jdk1.8.0_171/bin/java'
    Enginepathe = pjoin(append_path('Server'),'ExiProcessor\ExiProcessor.jar')
    XMLpath = pjoin(sp.Path4(append_path('Server'), 'dr', id1, 'edc', id2)[0], 'EndDeviceControl.xml')
    EXIpath = pjoin(sp.Path4(append_path('Server'), 'dr', id1, 'edc', id2)[0], 'EndDeviceControl.exi')
    XSDpath = pjoin(append_path('Server'), 'sep.xsd')
    #XML2EXI(JAVApath, Enginepathe, XMLpath, EXIpath, XSDpath)
    return _href, _replyTo, ReplyTo

def GetDR(ip, port, DemandResponseProgramListLink, mRID, id1, id2, EDCtlTimeStamp, HEMSCmRID, DrNum, EdevNum, itt):
    mRIDX = mRID.encode('hex')
    mRIDX = mRIDX.upper()
    r = requests.get('https://' + ip + ':' + port + DemandResponseProgramListLink,  verify = certificate('TAserver'), \
                     cert = (ClientCert('CA')[0],ClientCert('CA')[1]), auth=('username', 'password'), timeout = 3)
    sleep(3)
    DemandResponseProgramList = r.text
    doc = x2d.parse(DemandResponseProgramList)
    DemandResponseLinks = []
    if int(doc['DemandResponseProgramList']['@all']) == 1:
        for item in doc['DemandResponseProgramList']['DemandResponseProgram']:
            mrid = doc['DemandResponseProgramList']['DemandResponseProgram']['mRID']
            if mrid == mRIDX:
               url = ((doc['DemandResponseProgramList']['DemandResponseProgram'])['@href']).replace('\\','/') 
               r = requests.get('https://' + ip + ':' + port + url, verify = certificate('TAserver'), \
                                cert = (ClientCert('CA')[0],ClientCert('CA')[1]), auth=('username', 'password'), timeout = 3)
               sleep(3)
               DemandResponseProgram = r.text
               DRP = x2d.parse(DemandResponseProgram)
               DemandResponseProgram = DemandResponseP(DRP, HEMSCmRID, DrNum, EdevNum, itt)
               url = ((doc['DemandResponseProgramList']['DemandResponseProgram'])['EndDeviceControlListLink']['@href']).replace('\\','/')
               r = requests.get('https://' + ip + ':' + port + url, verify = certificate('TAserver'), \
                                cert = (ClientCert('CA')[0],ClientCert('CA')[1]), auth=('username', 'password'), timeout = 3)
               sleep(3)
               EndDeviceControlList = r.text
               EndDeviceCtlList = x2d.parse(EndDeviceControlList)
               if int(EndDeviceCtlList['EndDeviceControlList']['@all']) == 1:
                   url = (EndDeviceCtlList['EndDeviceControlList']['EndDeviceControl']['@href']).replace('\\','/')
                   r = requests.get('https://' + ip + ':' + port + url , verify = certificate('TAserver'), \
                                cert = (ClientCert('CA')[0],ClientCert('CA')[1]), auth=('username', 'password'), timeout = 3)
                   sleep(3)
                   EndDeviceCtl = r.text
                   EndDeviceCtl = x2d.parse(EndDeviceCtl)
                   creationTime = int(EndDeviceCtl['EndDeviceControl']['creationTime'])
                   if creationTime != EDCtlTimeStamp:
                       _href, _replyTo, ReplyTo = EndDeviceC(EndDeviceCtl, HEMSCmRID, DrNum, EdevNum, itt)
                       logger.info("New EndDevice is created at " + _href )
                       print "New EndDevice is created at " , _href
                       DemandResponseLinks.append((_href, _replyTo, ReplyTo))
                   else:
                       print "No new EndDeviceControl! "
                   EDCtlTimeStamp = creationTime
               else:
                   for j in range(int(EndDeviceCtlList['EndDeviceControlList']['@all'])):
                      url = ((EndDeviceCtlList['EndDeviceControlList']['EndDeviceControl'])[j]['@href']).replace('\\','/')
                      r = requests.get('https://' + ip + ':' + port + url, verify = certificate('TAserver'), \
                                cert = (ClientCert('CA')[0],ClientCert('CA')[1]), auth=('username', 'password'), timeout = 3)
                      sleep(3)
                      EndDeviceCtl = r.text
                      EndDeviceCtl = x2d.parse(EndDeviceCtl)
                      creationTime = int(EndDeviceCtl['EndDeviceControl']['creationTime'])
                      if creationTime != EDCtlTimeStamp:
                          _href, _replyTo, ReplyTo = EndDeviceC(EndDeviceCtl, HEMSCmRID, DrNum, EdevNum, itt)
                          logger.info("New EndDevice is created at " + _href )
                          print "New EndDevice is created at " , _href
                          DemandResponseLinks.append((_href, _replyTo, ReplyTo))
                      else:
                          print "No new EndDeviceControl! "
                      EDCtlTimeStamp = creationTime

    else:
        for j in range(int(doc['DemandResponseProgramList']['@all'])):
            mrid = (doc['DemandResponseProgramList']['DemandResponseProgram'])[j]['mRID']
            if mrid == mRIDX:
               url = ((doc['DemandResponseProgramList']['DemandResponseProgram'])[j]['@href']).replace('\\','/')
               r = requests.get('https://' + ip + ':' + port + url, verify = certificate('TAserver'), \
                                cert = (ClientCert('CA')[0],ClientCert('CA')[1]), auth=('username', 'password'), timeout = 3)
               sleep(3)
               DemandResponseProgram = r.text
               DRP = x2d.parse(DemandResponseProgram)
               DemandResponseProgram = DemandResponseP(DRP, HEMSCmRID, DrNum, EdevNum, itt)
               url = ((doc['DemandResponseProgramList']['DemandResponseProgram'])[j]['EndDeviceControlListLink']['@href']).replace('\\','/')
               r = requests.get('https://' + ip + ':' + port + url, verify = certificate('TAserver'), \
                                cert = (ClientCert('CA')[0],ClientCert('CA')[1]), auth=('username', 'password'), timeout = 3)
               sleep(3)
               EndDeviceControlList = r.text
               EndDeviceCtlList = x2d.parse(EndDeviceControlList)
               if int(EndDeviceCtlList['EndDeviceControlList']['@all']) == 1:
                   url = (EndDeviceCtlList['EndDeviceControlList']['EndDeviceControl']['@href']).replace('\\','/')
                   r = requests.get('https://' + ip + ':' + port +url, verify = certificate('TAserver'), \
                                cert = (ClientCert('CA')[0],ClientCert('CA')[1]), auth=('username', 'password'), timeout = 3)
                   sleep(3)
                   EndDeviceCtl = r.text
                   EndDeviceCtl = x2d.parse(EndDeviceCtl)
                   creationTime = int(EndDeviceCtl['EndDeviceControl']['creationTime'])
                   if creationTime != EDCtlTimeStamp:
                       _href, _replyTo, ReplyTo = EndDeviceC(EndDeviceCtl, HEMSCmRID, DrNum, EdevNum, itt)
                       logger.info("New EndDevice is created at " + _href )
                       print "New EndDevice is created at " , _href
                       DemandResponseLinks.append((_href, _replyTo, ReplyTo))
                   else:
                       print "No new EndDeviceControl! ", creationTime
                   EDCtlTimeStamp = creationTime 
               else:
                   for j in range(int(EndDeviceCtlList['EndDeviceControlList']['@all'])):
                      url = ((EndDeviceCtlList['EndDeviceControlList']['EndDeviceControl'])[j]['@href']).replace('\\','/')
                      r = requests.get('https://' + ip + ':' + port + url, verify = certificate('TAserver'), \
                                cert = (ClientCert('CA')[0],ClientCert('CA')[1]), auth=('username', 'password'), timeout = 3)
                      sleep(3)
                      EndDeviceCtl = r.text
                      EndDeviceCtl = x2d.parse(EndDeviceCtl)
                      creationTime = int(EndDeviceCtl['EndDeviceControl']['creationTime'])
                      if int(EndDeviceCtl['EndDeviceControl']['creationTime']) != EDCtlTimeStamp:
                          _href, _replyTo, ReplyTo = EndDeviceC(EndDeviceCtl, HEMSCmRID, DrNum, EdevNum, itt)
                          logger.info("New EndDevice is created at " + _href )
                          print "New EndDevice is created at " , _href
                          DemandResponseLinks.append((_href, _replyTo, ReplyTo))
                      else:
                          print "No new EndDeviceControl! "
                      EDCtlTimeStamp = creationTime                         
    return DemandResponseLinks, EDCtlTimeStamp    


def DrRes(ApplianceLoadReductionType, CreatTime, Power, CoolingOffset, HeatingOffset, CoolingSetpoint, HeatingSetpoint, id1, id2):
    _href_EndDev = ('/' + 'rsps' + '/' + str(id1) + '/' + 'rsp' + '/' + str(id2))
    _createdDateTime = CreatTime
    _endDeviceLFDI = Config.LFDI
    _status = 0
    _subject = Config.MRID
    _ApplianceLoadReductionType = ApplianceLoadReductionType
    _type = 0
    _value = Power
    _DutyCycleValue = 0
    _coolingOffset = CoolingOffset
    _heatingOffset = HeatingOffset
    _loadAdjustmentPercentageOffset = 0
    _overrideDuration = 0
    _coolingSetpoint = CoolingSetpoint
    _heatingSetpoint = HeatingSetpoint
    [DrResponse,  Response] = sf.DrResponse_FUNC(_href_EndDev, _createdDateTime, _endDeviceLFDI, _status, _subject, _ApplianceLoadReductionType, _type, _value, \
                                                _DutyCycleValue, _coolingOffset, _heatingOffset, _loadAdjustmentPercentageOffset, _overrideDuration, _coolingSetpoint, _heatingSetpoint)
    DrResponse = DrResponse.toDOM().toprettyxml()
    return DrResponse

def DRResponse(ip, port, DemandResponseLinks, mRID, TimeStamp):
    mRIDX = mRID.encode('hex')
    mRIDX = mRIDX.upper()
    Directories = list()
    xml_dir = list()
    for root, dirs, files in os.walk(os.path.normpath(os.getcwd()+os.sep+os.pardir)):
        for file in files:
            if file.endswith("DrResponse" + ".xml"):
                xml_dir.append(os.path.join(root, file))
    for Dir in xml_dir:
        for item in DemandResponseLinks:
            if item[1] in Dir.replace('\\','/'):
                Directories.append((Dir, item[1], item[2]))

    ResDirectories = list()
    for i in Directories:
      if i not in ResDirectories:
        ResDirectories.append(i)

    for Res in ResDirectories:
        print Res
        with open(Res[0]) as fd:
            doc = x2d.parse(fd.read())

        if doc['DrResponse']['subject'] == mRIDX:
            print mRIDX
            Time = doc['DrResponse']['createdDateTime']
            print Time
            if Time != TimeStamp:
                TimeStamp = Time
		ApplianceLoadReductionType = doc['DrResponse']['ApplianceLoadReduction']['type']
                print ApplianceLoadReductionType 
		CreatTime = doc['DrResponse']['createdDateTime']
                print CreatTime 
		Power = doc['DrResponse']['AppliedTargetReduction']['value']
                print Power 
		CoolingOffset = doc['DrResponse']['Offset']['coolingOffset']
		HeatingOffset = doc['DrResponse']['Offset']['heatingOffset']
		CoolingSetpoint = doc['DrResponse']['SetPoint']['coolingSetpoint']
		HeatingSetpoint = doc['DrResponse']['SetPoint']['heatingSetpoint']
		id1 = 1
		id2 = 1
                payload =  DrRes(ApplianceLoadReductionType, CreatTime, Power, CoolingOffset, HeatingOffset, CoolingSetpoint, HeatingSetpoint, id1, id2)
                #print payload 
                url = Res[2]
                #print url
                while True:
                    r = requests.put('https://' + ip + ':' + port + url, verify = certificate('TAserver'), cert = (ClientCert('CA')[0],ClientCert('CA')[1]), auth=('username', 'password'), timeout = 5, data = payload)
                    if r.status_code == 201:
                        print "Response is sent..."
                        break
            else:
                print "No new response"
        else:
            print "No response from mRID# :", mRIDX

    return TimeStamp
    
if __name__ == "__main__":
    mRID = Config.MRID
    HEMSCmRID = Config.HEMSC_MRID
    sFDI = Config.SFDI
    PIN = Config.PIN
    TimeStamp = 1
    EDCTimeStamp = 1
    itt = 1
    DrNum = 1
    EdevNum = 1
    while True:
        try:
            ip, port, path, dcap = dns.SepServerFinder(Config.DNS_ADDRESS)
            break
        except:
            print 'Error H01, DNS cannot find the requested type'
            logger.info("Error H01, DNS cannot find the requested type")
            sleep(5)
    if ip != None:
        while True:
            try:
                RegistrationLink, FunctionSetAssignmentsListLink, LoadShedAvailabilityLink = discovery(ip, port, path, sFDI)
                break
            except:
                print "Error H02, Cannot discover the SEP server"
                logger.info("Error H02, Cannot discover the SEP server")
                sleep(5)
        id1 = int((FunctionSetAssignmentsListLink.split(path+'/')[-1]).split('/fsa')[0])
        while True:
            try:
                pIN = registery(ip, port, path, sFDI, RegistrationLink)
                break
            except:
                print "Error H03, Cannot retrieve the PIN"
                logger.info("Error H03, Cannot retrieve the PIN")
                sleep(5)
    if pIN == PIN:
        while True:
            try:
                while True:
                    try:
                        FALink, DemandResponseProgramListLink, DERProgramListLink, ResponseSetListLink, UsagePointListLink = AssignmentLink(mRID, FunctionSetAssignmentsListLink)
                        id2 =  int(((FALink).split(FunctionSetAssignmentsListLink+'/')[-1]))
                        break
                    except:
                        print "Error H04, Cannot retrieve the DR program link"
                        logger.info("Error H04, Cannot retrieve the DR program link")
                        sleep(5)
                while True:
                    try:
                        DemandResponseLinks, EDCtlTimeStamp = GetDR(ip, port, DemandResponseProgramListLink, mRID, id1, id2, EDCTimeStamp,HEMSCmRID, DrNum, EdevNum, itt)
                        EDCTimeStamp = EDCtlTimeStamp
                        break
                    except:
                        print "Error H05, Cannot get End Device funcion sets"
                        logger.info("Error H05, Cannot get End Device funcion sets")
                        sleep(5)
                print "Waiting for Response..."
                logger.info("Waiting for Response...")
                time.sleep((Config.RESPONSE)*60)
                while True:
                    try:
                        Time = DRResponse(ip, port, DemandResponseLinks, HEMSCmRID, TimeStamp)
                        TimeStamp = Time
                        break
                    except:
                        raise
                        print "Error H06, Cannot send the HEMSC response to TA"
                        logger.info("Error H06, Cannot send the HEMSC response to TA")
                        sleep(5)
                time.sleep((Config.EVENT)*60)
                itt = itt + 1
            except Exception as e:
                print "Error H07, An Error occurred during negotiation, will resume in 5 Sec!"
                logging.error('Error H07, An Error occurred during negotiation, will resume in 5 Sec! ' + str(e))
                logger.info("Error H07, An Error occurred during negotiation, will resume in 5 Sec! " + str(e))
                pass
                sleep(5)
