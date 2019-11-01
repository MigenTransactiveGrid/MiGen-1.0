from time import sleep
import os
import requests
import xmltodict as x2d
from datetime import datetime
import time
import sys
from os.path import join as pjoin
import json

#from requests.packages.urllib3.exceptions import SubjectAltNameWarning
#requests.packages.urllib3.disable_warnings(SubjectAltNameWarning)
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
#sys.path.append(append_path('dnsdiscover'))
#import dnsdiscover as dns
sys.path.append(append_path('ServerPath'))
import ServerPath as sp
sys.path.append(append_path('Config'))
import Config

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

def json_path(function):
    for r,d,f in os.walk(os.path.normpath(os.getcwd()+os.sep+os.pardir)):
        for files in f:
            if files == function+'.json':
                url = os.path.join(r,files)
                url = url.rsplit(files)[0]
    return url

def discovery(ip, port, path, sFDI):
    try:
        r = requests.get('https://' + ip + ':' + port + path, cert = ('./postman.crt', './postman.key'), verify=False)
        LoadShedAvailabilityLink = None
        if r.status_code == 200 :
            EndDeviceList = r.text
            doc = x2d.parse(EndDeviceList)
            if int(doc['EndDeviceList']['@results'])==1:
                if doc['EndDeviceList']['EndDevice']['sFDI'] == str(sFDI):
                    RegistrationLink = doc['EndDeviceList']['EndDevice']['RegistrationLink']['@href']
                    FunctionSetAssignmentsListLink = doc['EndDeviceList']['EndDevice']['FunctionSetAssignmentsListLink']['@href']
                    #LoadShedAvailabilityLink = doc['EndDeviceList']['EndDevice']['LoadShedAvailabilityLink']['@href']
                return RegistrationLink, FunctionSetAssignmentsListLink, LoadShedAvailabilityLink
            else:
                for i in range(int(doc['EndDeviceList']['@results'])):
                    if doc['EndDeviceList']['EndDevice'][i]['sFDI'] == str(sFDI):
                        RegistrationLink = doc['EndDeviceList']['EndDevice'][i]['RegistrationLink']['@href']
                        FunctionSetAssignmentsListLink = doc['EndDeviceList']['EndDevice'][i]['FunctionSetAssignmentsListLink']['@href']
                        #LoadShedAvailabilityLink = doc['EndDeviceList']['EndDevice'][i]['LoadShedAvailabilityLink']['@href']
                return RegistrationLink, FunctionSetAssignmentsListLink, LoadShedAvailabilityLink
                
    except:
        pass
        " server is not reposnding with given URI or SFDI is not correct"

def registery(ip, port, path, sFDI, RegistrationLink):
    pIN = None
    try:
        r = requests.get('https://' + ip + ':' + port + RegistrationLink, cert = ('./postman.crt', './postman.key'), verify=False)
        if r.status_code == 200 :
            Registration = r.text
            doc = x2d.parse(Registration)
            dateTimeRegistered = int(doc['Registration']['dateTimeRegistered'])
            pIN = int(doc['Registration']['pIN'])
    except:
        print " server is not responding! "
        pass
    return  pIN

def AssignmentLink(mRID, FunctionSetAssignmentsListLink):
    mRID = mRID.encode('hex')
    mRID = mRID.upper()
    try:
        r = requests.get('https://' + ip + ':' + port + FunctionSetAssignmentsListLink, cert = ('./postman.crt', './postman.key'), verify=False)
        FSAL = r.text
        doc = x2d.parse(FSAL)
        if int(doc['FunctionSetAssignmentsList']['@all'])==1:
            if doc['FunctionSetAssignmentsList']['FunctionSetAssignments']['mRID'] != None:
                url = doc['FunctionSetAssignmentsList']['FunctionSetAssignments']['@href']
                r = requests.get('https://' + ip + ':' + port + url, cert = ('./postman.crt', './postman.key'), verify=False)
                FSA = r.text
                dox = x2d.parse(FSA)
                DemandResponseProgramListLink = dox['FunctionSetAssignments']['DemandResponseProgramListLink']['@href']
                #DERProgramListLink = dox['FunctionSetAssignments']['DERProgramListLink']['@href']
                #ResponseSetListLink = dox['FunctionSetAssignments']['ResponseSetListLink']['@href']
                #UsagePointListLink = dox['FunctionSetAssignments']['UsagePointListLink']['@href']
        else:
            for i in range(int(doc['FunctionSetAssignmentsList']['@all'])):
                if doc['FunctionSetAssignmentsList']['FunctionSetAssignments'][i]['mRID'] != None:
                    url = doc['FunctionSetAssignmentsList']['FunctionSetAssignments'][i]['@href']
                    r = requests.get('https://' + ip + ':' + port + url, cert = ('./postman.crt', './postman.key'), verify=False)
                    FSA = r.text
                    dox = x2d.parse(FSA)
                    DemandResponseProgramListLink = dox['FunctionSetAssignments']['DemandResponseProgramListLink']['@href']
                    #DERProgramListLink = dox['FunctionSetAssignments']['DERProgramListLink']['@href']
                    #ResponseSetListLink = dox['FunctionSetAssignments']['ResponseSetListLink']['@href']
                    #UsagePointListLink = dox['FunctionSetAssignments']['UsagePointListLink']['@href']
        return url, DemandResponseProgramListLink
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
##    DemandResponseProgram = sf.DemandResponseProgram_FUNC(_href_Dr, _mRID, _description, _version, _ActiveEndDeviceControlListLink,#
##    _availabilityUpdatePercentChangeThreshold, _multiplier, _value, _availabilityUpdatePowerChangeThreshold, _EndDeviceControlListLink, _primacy)
    #print (DemandResponseProgram.toxml(element_name='DemandResponseProgram'))
##    with open(pjoin(sp.Path2(append_path('Server'), 'dr', id1)[0], 'DemandResponseProgram.xml'), 'w') as f:
##        f.write(DemandResponseProgram.toDOM().toprettyxml())
##
##    JAVApath = 'java' #'/usr/java/jdk1.8.0_171/bin/java'
##    Enginepathe = pjoin(append_path('Server'), 'ExiProcessor\ExiProcessor.jar')
##    XMLpath = pjoin(sp.Path2(append_path('Server'), 'dr', id1)[0], 'DemandResponseProgram.xml')
##    EXIpath = pjoin(sp.Path2(append_path('Server'), 'dr', id1)[0], 'DemandResponseProgram.exi')
##    XSDpath = pjoin(append_path('Server'), 'sep.xsd')
    #XML2EXI(JAVApath, Enginepathe, XMLpath, EXIpath, XSDpath)
    return DemandResponseProgram

def EndDeviceC(doc, mRID, id1, id2, i):
    _href = "/dr" 
    _replyTo = sp.Path4(append_path('Server'), 'rsps', id1, 'rsp', id2)[1]
    _subscribable = 0
    _version = int(doc['EndDeviceControl']['version'])
    _currentStatus = int(doc['EndDeviceControl']['EventStatus']['currentStatus']) # 0 = Scheduled, 1 = Active, 2 = Cancelled, 3 = Cancelled with Randomization, 4 = Superseded
    _creationTime = int(doc['EndDeviceControl']['creationTime'])
    creationTime = datetime.fromtimestamp(_creationTime).strftime('%Y-%m-%d %H:%M:%S')
    _duration =  int(doc['EndDeviceControl']['interval']['duration'])
    _start = int(doc['EndDeviceControl']['interval']['start'])
    start = datetime.fromtimestamp(_start).strftime('%Y-%m-%d %H:%M:%S')
    _randomizeDuration = int(doc['EndDeviceControl']['randomizeDuration'])
    _randomizeStart =  int(doc['EndDeviceControl']['randomizeStart'])
    if doc['EndDeviceControl']['drProgramMandatory'] == 'false':
        _drProgramMandatory = 0
    else:
        _drProgramMandatory = 1
    _ReductionType = int(doc['EndDeviceControl']['TargetReduction']['type'])
    _ReductionValue = int(doc['EndDeviceControl']['TargetReduction']['value'])
    if _ReductionType == 0:
        Reduction = (_ReductionValue * 1000)/60.0
    elif _ReductionType == 0:
        Reduction = (_ReductionValue * 1000)
    elif _ReductionType == 3:
        Reduction = (_ReductionValue * 1.0)
    else:
        Reduction = (_ReductionValue * 1.0)
    payload = [_href, _replyTo, _subscribable, _currentStatus, creationTime,\
               _duration, start, _randomizeDuration,  _randomizeStart, Reduction]
    return payload

def GetDR(ip, port, DemandResponseProgramListLink, mRID, id1, id2, EDCtlTimeStamp, TAmRID, DrNum, EdevNum, itt, Oldversion):
    mRIDX = mRID.encode('hex')
    mRIDX = mRIDX.upper()
    r = requests.get('https://' + ip + ':' + port + DemandResponseProgramListLink, cert = ('./postman.crt', './postman.key'), verify=False)
    DemandResponseProgramList = r.text
    doc = x2d.parse(DemandResponseProgramList)
    print doc
    DemandResponseLinks = []
    payload = None
    if int(doc['DemandResponseProgramList']['@all']) == 1:
        for item in doc['DemandResponseProgramList']['DemandResponseProgram']:
            mrid = doc['DemandResponseProgramList']['DemandResponseProgram']['mRID']
            if mrid != None:
               url = ((doc['DemandResponseProgramList']['DemandResponseProgram'])['@href']).replace('\\','/') 
               r = requests.get('https://' + ip + ':' + port + url, cert = ('./postman.crt', './postman.key'), verify=False)
               DemandResponseProgram = r.text
               DRP = x2d.parse(DemandResponseProgram)
##               DemandResponseProgram = DemandResponseP(DRP, TAmRID, DrNum, EdevNum, itt)
               url = ((doc['DemandResponseProgramList']['DemandResponseProgram'])['EndDeviceControlListLink']['@href']).replace('\\','/')
               r = requests.get('https://' + ip + ':' + port + url, cert = ('./postman.crt', './postman.key'), verify=False)
               EndDeviceControlList = r.text
               EndDeviceCtlList = x2d.parse(EndDeviceControlList)
               if int(EndDeviceCtlList['EndDeviceControlList']['@all']) == 1:
                   url = (EndDeviceCtlList['EndDeviceControlList']['EndDeviceControl']['@href']).replace('\\','/')
                   r = requests.get('https://' + ip + ':' + port + url, cert = ('./postman.crt', './postman.key'), verify=False)
                   EndDeviceCtl = r.text
                   EndDeviceCtl = x2d.parse(EndDeviceCtl)
                   creationTime = int(EndDeviceCtl['EndDeviceControl']['creationTime'])
                   version = int(EndDeviceCtl['EndDeviceControl']['version'])
                   if creationTime != EDCtlTimeStamp or version != Oldversion:
                       payload = EndDeviceC(EndDeviceCtl, TAmRID, DrNum, EdevNum, itt)
                   else:
                       print "No new EndDeviceControl! "
                   EDCtlTimeStamp = creationTime
               else:
                   for j in range(int(EndDeviceCtlList['EndDeviceControlList']['@all'])):
                      url = ((EndDeviceCtlList['EndDeviceControlList']['EndDeviceControl'])[j]['@href']).replace('\\','/')
                      r = requests.get('https://' + ip + ':' + port + url, cert = ('./postman.crt', './postman.key'), verify=False)
                      EndDeviceCtl = r.text
                      EndDeviceCtl = x2d.parse(EndDeviceCtl)
                      creationTime = int(EndDeviceCtl['EndDeviceControl']['creationTime'])
                      version = int(EndDeviceCtl['EndDeviceControl']['version'])
                      if creationTime != EDCtlTimeStamp or version != Oldversion:
                          payload = EndDeviceC(EndDeviceCtl, TAmRID, DrNum, EdevNum, itt)
                      else:
                          print "No new EndDeviceControl! "
                      EDCtlTimeStamp = creationTime

    else:
        for j in range(int(doc['DemandResponseProgramList']['@all'])):
            mrid = (doc['DemandResponseProgramList']['DemandResponseProgram'])[j]['mRID']
            if mrid != None:
               url = ((doc['DemandResponseProgramList']['DemandResponseProgram'])[j]['@href']).replace('\\','/')
               r = requests.get('https://' + ip + ':' + port + url, cert = ('./postman.crt', './postman.key'), verify=False)
               DemandResponseProgram = r.text
               DRP = x2d.parse(DemandResponseProgram)
##               DemandResponseProgram = DemandResponseP(DRP, TAmRID, DrNum, EdevNum, itt)
               url = ((doc['DemandResponseProgramList']['DemandResponseProgram'])[j]['EndDeviceControlListLink']['@href']).replace('\\','/')
               r = requests.get('https://' + ip + ':' + port + url, cert = ('./postman.crt', './postman.key'), verify=False)
               EndDeviceControlList = r.text
               EndDeviceCtlList = x2d.parse(EndDeviceControlList)
               if int(EndDeviceCtlList['EndDeviceControlList']['@all']) == 1:
                   url = (EndDeviceCtlList['EndDeviceControlList']['EndDeviceControl']['@href']).replace('\\','/')
                   r = requests.get('https://' + ip + ':' + port +url, cert = ('./postman.crt', './postman.key'), verify=False)
                   EndDeviceCtl = r.text
                   EndDeviceCtl = x2d.parse(EndDeviceCtl)
                   creationTime = int(EndDeviceCtl['EndDeviceControl']['creationTime'])
                   version = int(EndDeviceCtl['EndDeviceControl']['version'])
                   if creationTime != EDCtlTimeStamp or version != Oldversion:
                       payload = EndDeviceC(EndDeviceCtl,TAmRID, DrNum, EdevNum, itt)
                   else:
                       print "No new EndDeviceControl! "
                   EDCtlTimeStamp = creationTime 
               else:
                   for j in range(int(EndDeviceCtlList['EndDeviceControlList']['@all'])):
                      url = ((EndDeviceCtlList['EndDeviceControlList']['EndDeviceControl'])[j]['@href']).replace('\\','/')
                      r = requests.get('https://' + ip + ':' + port + url, cert = ('./postman.crt', './postman.key'), verify=False)
                      EndDeviceCtl = r.text
                      EndDeviceCtl = x2d.parse(EndDeviceCtl)
                      creationTime = int(EndDeviceCtl['EndDeviceControl']['creationTime'])
                      version = int(EndDeviceCtl['EndDeviceControl']['version'])
                      if (int(EndDeviceCtl['EndDeviceControl']['creationTime']) != EDCtlTimeStamp) or version != Oldversion:
                          payload = EndDeviceC(EndDeviceCtl, TAmRID, DrNum, EdevNum, itt)
                      else:
                          print "No new EndDeviceControl! "
                      EDCtlTimeStamp = creationTime
                      
    return DemandResponseLinks, EDCtlTimeStamp, version ,payload    

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
                Directories.append((Dir, item[1]))
    ResDirectories = list()
    for i in Directories:
      if i not in ResDirectories:
        ResDirectories.append(i)
        
    for Res in ResDirectories:
        with open(Res[0]) as fd:
            doc = x2d.parse(fd.read())
        
        if doc['DrResponse']['subject'] == mRIDX:
            Time = doc['DrResponse']['createdDateTime']
            if Time != TimeStamp:
                TimeStamp = Time
                payload = open(Res[0], "r").read()
                url = Res[1]
                requests.put('https://' + ip + ':' + port + url, cert = ('./postman.crt', './postman.key'), verify=False, data = payload)
                print "Response is sent..."
            else:
                print "No new response"
        else:
            print "No response from mRID# :", mRIDX
    
    return TimeStamp
    
if __name__ == "__main__":
    mRID = '\x56\x88\x70\x69\x24\x41\x56\x88\x70\x00\x00\x00\x00\x00\x00\x00'
    sFDI = 568870692441
    TAmRID = mRID
    PIN = 123123
    TimeStamp = 1
    EDCTimeStamp = 1
    oldversion = 0
    itt = 1
    DrNum = 1
    EdevNum = 1
    ip = '10.8.0.16'
    port = '3030'
    path = '/sep2/edev'
    dcap = '/sep2/dcap'
    
    if ip != None:
        while True:
            try:
                RegistrationLink, FunctionSetAssignmentsListLink, LoadShedAvailabilityLink = discovery(ip, port, path, sFDI)
                id1 = (FunctionSetAssignmentsListLink.split(path+'/')[-1]).split('/fsa')[0]
                pIN = registery(ip, port, path, sFDI, RegistrationLink)
                break
            except:
                print "Check the server connection"
                time.sleep(10)
    while pIN == PIN:
        while True:
            try:
                FALink, DemandResponseProgramListLink = AssignmentLink(mRID, FunctionSetAssignmentsListLink)
                id2 =  ((FALink).split(FunctionSetAssignmentsListLink+'/')[-1])
                DemandResponseLinks, EDCtlTimeStamp, version, payload = GetDR(ip, port, DemandResponseProgramListLink, mRID, id1, id2, EDCTimeStamp,TAmRID, DrNum, EdevNum, itt, oldversion)
                break
            except:
                print "Check the server connection for payloads" 
                time.sleep(10)   
        EDCTimeStamp = EDCtlTimeStamp
        oldversion = version
        if payload != None:
            data = {"DateTime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "Power": payload[9], "DRtime": payload[6], "duration": payload[5]}
            with open(json_path('DRes')+'DRes.json', 'w') as outfile:
                json.dump(data, outfile)
            print "Waiting for Response..."
        time.sleep((Config.RESPONSE)*60)
        Time = DRResponse(ip, port, DemandResponseLinks, TAmRID, TimeStamp)
        TimeStamp = Time
        time.sleep(10)
        itt = itt + 1
