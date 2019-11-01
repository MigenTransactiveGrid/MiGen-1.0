# -*- coding: utf-8 -*-
from scipy.optimize import linprog
import json
import xmltodict
import os
import datetime
import time
from random import randint
from os.path import join as pjoin
import json
import sqlite3
import sys
def append_path(function):
    for r,d,f in os.walk(os.path.normpath(os.getcwd()+os.sep+os.pardir)):
        for files in f:
            if files == function+'.py' or files == function+'.pyc':
                url = os.path.join(r,files)
                url = url.rsplit(files)[0]
    return url
sys.path.append(append_path('Reward'))
from Reward import Reward
sys.path.append(append_path('Predictor'))
from Predictor.Predictor import predict
sys.path.append(append_path('SepFunc'))
import SepFunc as sf
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

def Optimization(Xay, Credit, RemainedDR, i, itr, CuResp):
    n=0
    CreditBar = i*[0]
    for row in range(i):
        C = float(Credit[row])
        CreditBar[row] = (C/float(max(Credit)))
        if Xay[row] == 0:
            n = n+1
    N = i-n
    A = [N*[0]]
    b = 0
    X = [N*[0],N*[0]]
    lb = N*[0]
    ub = N*[0]
    f = (i-n)*[0]
    k = 0    
    b = -1 * RemainedDR
    Aeq = None
    Beq = None

    for row in range(i):
        if Xay[row] != 0:
            A[0][k] = -1*Xay[row]
            f[k] = -1*CreditBar[row] * Xay[row]
            X[0][k] = row
            lb[k] = 0.8 * (CuResp[row])
            ub[k] = 1.11 * (CuResp[row])
            k = k + 1
    S = linprog(f,A,b,Aeq,Beq,bounds=list(zip(lb,ub)),options={'disp': False, 'tol': 1e-08, })
    if S.success != False:
        x = (S.x).tolist()
    else:
        print 'Error OP01, Cannot find the optimal solution for given data! check inputs'
        logger.info('Error OP01, Cannot find the optimal solution for given data! check inputs')
    return x

def Credit_Insert(DateTime, mrid, CuResp):
    try:
        con = sqlite3.connect(os.path.normpath(os.getcwd() + os.sep + 'database' + os.sep + 'TAdb.db'))
        cur = con.cursor()
        mrid = mrid.encode('hex')
        mrid = mrid.upper()
        to_db_credit = [DateTime, mrid, CuResp]
        cur.execute("INSERT INTO credit (Date, mRID, credit) VALUES (?, ?, ?);", to_db_credit)
        con.commit()    
        con.close()
    except:
        pass
                          
def EndDeviceControl_Func(dr, edr, mRID, StartTime, DRduration, ReductionValue, _Mandatory, itr):
    try:
        id1 = dr
        id2 = edr
        _href = sp.Path4(cwd, 'dr', id1, 'edc', id2)[1] 
        _replyTo = sp.Path4(cwd, 'rsps', id1, 'rsp', id2)[1] 
        _responseRequired = '01' 
        _mRID = mRID
        _description =  'Great-DR'
        _version = itr
        _subscribable = 0
        _currentStatus = 1
        _dateTime = int(time.mktime(datetime.datetime.now().timetuple())) 
        _potentiallySuperseded = 0 
        _potentiallySupersededTime = 0 
        _reason = 'This is a test for EndDeviceControl' 
        _creationTime = int(time.mktime(datetime.datetime.now().timetuple())) 
        _duration = DRduration
        _start =  StartTime
        _randomizeDuration = randint(0, 100)
        _randomizeStart =  randint(0, 60)
        _ApplianceLoadReductionType = 1 
        _DeviceCategoryType = '\x00\x04\x00\x00' # bit 19 - Energy Management
        _drProgramMandatory = _Mandatory #boolean
        _DutyCycleValue = 50 
        _loadShiftForward = 1 # Boolean.
        _coolingOffset = 2 
        _heatingOffset = 2
        _loadAdjustmentPercentageOffset = 1 #UInt8; Unsigned integer, max inclusive 255 (2^8-1)
        _overrideDuration = 60 
        _coolingSetpoint = 22 
        _heatingSetpoint = 20 
        _ReductionType = 1
        _ReductionValue = int(ReductionValue) 
        EndDeviceControl = sf.EndDeviceControl_FUNC(_href, _replyTo, _responseRequired, _mRID, _description, _version, _subscribable, _currentStatus, _dateTime, _potentiallySuperseded, _potentiallySupersededTime,\
                                                 _reason, _creationTime, _duration, _start, _randomizeDuration, _randomizeStart, _ApplianceLoadReductionType, _DeviceCategoryType, _drProgramMandatory, _DutyCycleValue, _loadShiftForward,\
                                                 _coolingOffset, _heatingOffset, _loadAdjustmentPercentageOffset, _overrideDuration, _coolingSetpoint, _heatingSetpoint, _ReductionType, _ReductionValue)
        with open(pjoin(sp.Path4(cwd, 'dr', id1, 'edc', id2)[0], 'EndDeviceControl.xml'), 'w') as f:
            f.write(EndDeviceControl.toDOM(parent=None, element_name='EndDeviceControl').toprettyxml())
            logger.info('New EndDeviceControl is generated for ' + encode('hex'))
        return EndDeviceControl
    except:
        pass
        return None
        
def EndDeviceControlList(dr, EndDeviceControl):
    try:
        id1 = dr
        _href = sp.Path3(cwd, 'dr', id1, 'edc')[1]
        _subscribable = 0 #The subscribable values. 0 - Resource does not support subscriptions, 1 - Resource supports non-conditional subscriptions, 2 - Resource supports conditional subscriptions
        _all = len(EndDeviceControl) #The number specifying "all" of the items in the list. Required on GET, ignored otherwise.
        _results = len(EndDeviceControl) #Indicates the number of items in this page of results.
        _EndDeviceControl = EndDeviceControl
        EndDeviceControlList = sf.EndDeviceControlList_FUNC( _href, _subscribable, _all, _results, _EndDeviceControl)
        with open(pjoin(Path(cwd, 'dr', id1, 'edc')[0], 'EndDeviceControlList.xml'), 'w') as f:
            f.write(EndDeviceControlList.toDOM().toprettyxml())
    except:
        pass
        return None

def ActiveEndDeviceControlList(dr, EndDeviceControl):
    try:
        id1 = dr
        _href = sp.Path3(cwd, 'dr', id1, 'actedc')[1]
        _subscribable = 0 #The subscribable values. 0 - Resource does not support subscriptions, 1 - Resource supports non-conditional subscriptions, 2 - Resource supports conditional subscriptions
        _all = len(EndDeviceControl) #The number specifying "all" of the items in the list. Required on GET, ignored otherwise.
        _results = len(EndDeviceControl) #Indicates the number of items in this page of results.
        _EndDeviceControl = EndDeviceControl
        ActiveEndDeviceControlList = sf.EndDeviceControlList_FUNC( _href, _subscribable, _all, _results, _EndDeviceControl)
        with open(pjoin(sp.Path3(cwd, 'dr', id1, 'actedc')[0], 'ActiveEndDeviceControlList.xml'), 'w') as f:
            f.write(ActiveEndDeviceControlList.toDOM().toprettyxml())
    except:
        return None

def DrRes(ReplyTo, ApplianceLoadReductionType, CreatTime, Power, CoolingOffset, HeatingOffset, CoolingSetpoint, HeatingSetpoint, id1, id2):
    _href_EndDev = ReplyTo
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
    [DrResponse,  Response]= sf.DrResponse_Func(_href_EndDev, _createdDateTime, _endDeviceLFDI, _status, _subject, _ApplianceLoadReductionType, _type, _value, \
                                                _DutyCycleValue, _coolingOffset, _heatingOffset, _loadAdjustmentPercentageOffset, _overrideDuration, _coolingSetpoint, _heatingSetpoint)
    DrResponse = DrResponse.toDOM().toprettyxml()
    return DrResponse


def find(key, dictionary):
    for k, v in dictionary.iteritems():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find(key, d):
                    yield result

def initiat(ActiveEndDevice, TargetReduction, DRTime, itr, Results):
    mRIDList = Config.MRIDLIST
    Credit = []; CuResp = []
    for mRID in mRIDList:
        try:
            Re = Reward(mRID, datetime.datetime.now())
        except:
            Re = 1
            print "Error R02, reward is not calculated for ", mRID.encode('hex')
            logger.info("Error R02, reward is not calculated for "+ str(mRID.encode('hex')))
            pass
        Credit.append(Re)
        try:
            #Pr = predict(mRID, datetime.datetime.now(), Config.PREDICTION_PERIOD) #[DRTime] # TODO: you may change 1 to 14 to have a better prediction
            if TargetReduction <= Config.CUSTOMER_CAPACITY:
                Pr = TargetReduction
            else:
                Pr = Config.CUSTOMER_CAPACITY
        except:
            print "Error R03, Power prediction is not calculated for ", mRID.encode('hex')
            logger.info("Error R03, Power prediction is not calculated for "+ str(mRID.encode('hex')))
            if TargetReduction <= Config.CUSTOMER_CAPACITY:
                Pr = TargetReduction
            else:
                Pr = Config.CUSTOMER_CAPACITY
            pass
        CuResp.append(Pr) 
    Xay = ActiveEndDevice*[1]
    CuResp = [Config.CUSTOMER_CAPACITY_RATE*x for x in CuResp]
    while TargetReduction > sum(CuResp):
        TargetReduction = TargetReduction * 0.9
        print "Target Reduction is reduced to ", TargetReduction, "because the network has not enough capacity"
        logger.info("Warning R01, Power prediction is not calculated for "+ str(TargetReduction) + "because the network has not enough capacity")
    else:
        RemainedDR = TargetReduction
    CA_DictList = {}
    for k in range(ActiveEndDevice):
        CA_DictList.setdefault('mRID',[]).append(mRIDList[k])
        mRIDX = mRIDList[k].encode('hex')
        CA_DictList.setdefault('mRIDhex',[]).append(mRIDX.upper())
        CA_DictList.setdefault('Xay',[]).append(Xay[k])
        CA_DictList.setdefault('Credit',[]).append(Credit[k])
        CA_DictList.setdefault('CuResp',[]).append(CuResp[k])
        CA_DictList.setdefault('Mandatory',[]).append(0)
        CA_DictList.setdefault('Compliance',[]).append(0)

    try:
        OPT = Optimization(Xay, Credit, RemainedDR, ActiveEndDevice, itr, CuResp)
        OPT = map(int, list(OPT))
    except:
        OPT = ActiveEndDevice * [float(RemainedDR) / ActiveEndDevice]
        print " Error R04, Cannot optimize the DR allocation, and replaced by equal DR for all Active EndDevices"
        logger.info("Error R04, Cannot optimize the DR allocation, and replaced by equal DR for all Active EndDevices")

    for k in range(ActiveEndDevice): # Add optimizeddata into Dict
        CA_DictList.setdefault('Optimization',[]).append(round((list(OPT)[k]), 2))
    Results['result'+str(itr)] = CA_DictList
    return CA_DictList, Results, TargetReduction

def run(mRIDList, TargetReduction, DRTime, DR_Start, DRduration, OldResDateTime):
    print 'New DR event is recieved'
    logger.info("New DR event is recieved")
    Flag = False
    customer={}
    Xai=[]
    itr = 1
    ActiveEndDevice = len(mRIDList)
    Results = {}

    while True:
        try:
            CA_DictList, Results, TargetReduction = initiat(ActiveEndDevice, TargetReduction, DRTime, itr, Results)
            break
        except:
            pass
            print " Error R01, Cannot optimize the DR allocation, and replaced by equal DR for all Active EndDevices"
            logger.info("Error R01, Cannot optimize the DR allocation, and replaced by equal DR for all Active EndDevices")
            time.sleep(5)
    while True:
        try:
            for k in range(ActiveEndDevice):
                mRID = CA_DictList['mRID'][k]
                StartTime = DR_Start
                ReductionValue = CA_DictList['Optimization'][k]
                Mandatory = CA_DictList['Mandatory'][k]
                EndDeviceControl = EndDeviceControl_Func(k+1, 1, mRID, StartTime, DRduration, ReductionValue, Mandatory, itr)
                EndDeviceControlList(k+1, [EndDeviceControl])
                ActiveEndDeviceControlList(k+1, [EndDeviceControl])
            break
        except:
            pass
            print 'Error R05, the DR function sets have not generated correctly! No DR event can be set!'
            logger.info('Error R05, the DR function sets have not generated correctly! No DR event can be set!')
            time.sleep(10)

    time.sleep((Config.RESPONSE)*60)

    Xai = ActiveEndDevice * [0]
    mRIDListhex = []
    for mRID in mRIDList:
        mRID = mRID.encode('hex')
        mRIDListhex.append(mRID.upper())

    while itr < Config.Max_ITR:
        print 'itteration: ', itr
        data_list = []
        customer={}

        for row in range(ActiveEndDevice):
            with open(os.path.normpath(cwd + os.sep + 'rsps' + os.sep + str(row+1) + os.sep + 'rsp/1' + os.sep +'DrResponse.xml')) as fd:
                xml = xmltodict.parse(fd.read())
            customer["xml{0}".format(row)] = xml

        for i in range(ActiveEndDevice):
            CreationTime = int(customer["xml{0}".format(i)]['DrResponse']['createdDateTime'].encode("utf-8"))
            LFDI = customer["xml{0}".format(i)]['DrResponse']['endDeviceLFDI'].encode("utf-8")
            mRID = customer["xml{0}".format(i)]['DrResponse']['subject'].encode("utf-8")
            LoadReductionType = customer["xml{0}".format(i)]['DrResponse']['ApplianceLoadReduction']['type'].encode("utf-8")
            ReductionType = customer["xml{0}".format(i)]['DrResponse']['AppliedTargetReduction']['type'].encode("utf-8")
            ReductionValue = customer["xml{0}".format(i)]['DrResponse']['AppliedTargetReduction']['value'].encode("utf-8")
            single = {"CreationTime": CreationTime, "LFDI":LFDI, "mRID": mRID, "LoadReductionType": LoadReductionType, "ReductionType": ReductionType, "ReductionValue": ReductionValue}
            data_list.append(single)

        diff = lambda l1,l2: [x for x in l1 if x not in l2]
        TimeList = []
        for i in range(ActiveEndDevice):
            TimeList.append(data_list[i]['CreationTime'])

        DiffTime = diff(TimeList, OldResDateTime) or diff(OldResDateTime, TimeList)
        if DiffTime:
            Residue = [] 
            Res_Flag = True
            for m in range(ActiveEndDevice):
                if (list(find('mRID', data_list[m])))[0] in CA_DictList['mRIDhex']:
                    Xai[m] = 1
                    if data_list[m]['CreationTime'] != OldResDateTime[m]:
                        OldResDateTime[m] = data_list[m]['CreationTime']
                        Index = CA_DictList['mRIDhex'].index((list(find('mRID', data_list[m])))[0])
                        if int(data_list[m]['ReductionType']) == 0: #TODO
                           # Index = CA_DictList['mRIDhex'].index((list(find('mRID', data_list[m])))[0])
                            if CA_DictList['Optimization'][Index] <= int(data_list[m]['ReductionValue']): # <= 1.05 * (int(data_list[m]['ReductionValue']))
                                Xai[m] = 0
                                CA_DictList['CuResp'][Index] = int(data_list[m]['ReductionValue'])
                                CA_DictList['Xay'][Index] = Xai[m]
                                CA_DictList['Mandatory'][Index] = 1
                                CA_DictList['Compliance'][Index] = 1
                            elif CA_DictList['Optimization'][Index] > int(data_list[m]['ReductionValue']):
                                Xai[m] = 1
                                CA_DictList['CuResp'][Index] = int(data_list[m]['ReductionValue'])
                                CA_DictList['Xay'][Index] = Xai[m]
                                CA_DictList['Mandatory'][Index] = 0
                                CA_DictList['Compliance'][Index] = 1
                            else:
                                pass
                        else:
                            print 'ReductionValue is not a correct UNIT'
                            Res_Flag = False
                    else:
                        print "No new response is recieved from ", (list(find('mRID', data_list[m])))[0]
                        Xai[m] = 1
                        CA_DictList['Xay'][m] = Xai[m]
                        CA_DictList['Mandatory'][m] = 0
                else:
                    Index = 0
                    print 'Error R06 ', (list(find('mRID', data_list[m])))[0], ' is avilable but not listed!'
                    logger.info('Error R06 '+ str((list(find('mRID', data_list[m])))[0]) + ' is avilable but not listed!')
                    Xai[m] = 0
                    CA_DictList['Xay'][Index] = Xai[m]
                    Residue.append(0)

            for item in CA_DictList['CuResp']:
                Residue.append(item)

            if TargetReduction <= sum(Residue):
                Xai = ActiveEndDevice * [0]
                CA_DictList['Mandatory'] = ActiveEndDevice * [1]
                Res_Flag == True

            if (Res_Flag == True) and (sum(Xai) != 0 and TargetReduction - sum(Residue) > 0):
                Credit = []
                for mRID in mRIDList:
                    try:
                        Re = Reward(mRID, datetime.datetime.now())
                    except:
                        Re = 1
                        print "Error R07, reward is not calculated for ", mRID.encode('hex')
                        logger.info("Error R07, reward is not calculated for "+ str(mRID.encode('hex')))
                        pass
                    Credit.append(Re)
                RemainedDR = TargetReduction - sum(Residue)
                CuResp = CA_DictList['CuResp']
                while RemainedDR > sum(CuResp):
                    RemainedDR = RemainedDR * 0.5
                try:
                    OPT = Optimization(Xai, Credit, RemainedDR, ActiveEndDevice, itr, CuResp)
                    OPT = map(int, list(OPT))
                except:
                    AveRemainedDR = ActiveEndDevice * [float(RemainedDR) / ActiveEndDevice]
                    OPT = [a+b for a,b in zip(CA_DictList['CuResp'], AveRemainedDR)]
                    OPT = map(int, list(OPT))
                    print " Error R08, Cannot optimize the DR allocation, and replaced by equal DR for all Active EndDevices"
                    logger.info("Error R08, Cannot optimize the DR allocation, and replaced by equal DR for all Active EndDevices")
                CA_DictList['Optimization'] = []
                for i in range(ActiveEndDevice): # Add optimizeddata into Dict
                    CA_DictList.setdefault('Optimization',[]).append(round((list(OPT)[i]), 2))
                while True:
                    try:
                        for k in range(ActiveEndDevice):
                            mRID = CA_DictList['mRID'][k]
                            StartTime = DR_Start
                            ReductionValue = CA_DictList['Optimization'][k]
                            if itr == Config.Max_ITR-1:
                                Mandatory = 1
                            else:
                                Mandatory = CA_DictList['Mandatory'][k]
                            EndDeviceControl = EndDeviceControl_Func(k+1, 1, mRID, StartTime, DRduration, ReductionValue, Mandatory, itr)
                            ActiveEndDeviceControlList(k+1, [EndDeviceControl])
                        break
                    except:
                        print 'Error R09, the DR function sets have not generated correctly! No DR event can be set!'
                        logger.info('Error R09, the DR function sets have not generated correctly! No DR event can be set!')
                        time.sleep(10)
                            
            elif (Res_Flag == True) and (sum(Xai) == 0 or TargetReduction - sum(Residue) <= 0):
                itr = Config.Max_ITR
                while True:
                    try:
                        for k in range(ActiveEndDevice):
                            mRID = CA_DictList['mRID'][k]
                            StartTime = DR_Start
                            CA_DictList['CuResp'][k] = CA_DictList['CuResp'][k] * CA_DictList['Compliance'][k]
                            ReductionValue = CA_DictList['CuResp'][k]
                            Mandatory = CA_DictList['Mandatory'][k]            
                            EndDeviceControl = EndDeviceControl_Func(k+1, 1, mRID, StartTime, DRduration, ReductionValue, Mandatory, itr)
                            ActiveEndDeviceControlList(k+1, [EndDeviceControl])
                        break
                    except:
                        print 'Error R10, the DR function sets have not generated correctly! No DR event can be set!'
                        logger.info('Error R10, the DR function sets have not generated correctly! No DR event can be set!')
                        time.sleep(10)
                try:
                    Credit_Insert(datetime.datetime.now(), CA_DictList['mRID'][k], CA_DictList['CuResp'][k])
                except:
                    print 'Error R11, Cannot insert the new reward record to DB'
                    logger.info('Error R11, Cannot insert the new reward record to DB')
                    pass
            else:
                print 'Error R12, DR event is sent but no responses are recieved from clients in itteration# ', itr
                logger.info('Error R12, DR event is sent but no responses are recieved from clients in itteration# '+ str(itr))
            time.sleep((Config.RESPONSE)*60)
        else:
            print 'No response is recieved from clients'
            logger.info('No New response is recieved from clients')
            time.sleep((Config.RESPONSE)*60)
        itr = itr +1
    else:
        for k in range(ActiveEndDevice):
            CA_DictList['CuResp'][k] = CA_DictList['CuResp'][k] * CA_DictList['Compliance'][k]
        print 'Allocation proccess is done with !', CA_DictList['CuResp']
        logger.info('Allocation proccess is done with !' + str(CA_DictList['CuResp']) + 'in' + str(itr) + "iteration")
    return OldResDateTime
    
if __name__ == "__main__":
    mRIDList = Config.MRIDLIST
    OldDateTime = 1
    OldResDateTime = len(mRIDList) * [1]
    while True:
        try:
            with open('DRes.json') as data:
                d = json.load(data)
            utc_time = datetime.datetime.strptime(d['DateTime'], "%Y-%m-%d %H:%M:%S") #"%Y-%m-%d %H:%M:%S.%f"
            NewDateTime = (utc_time - datetime.datetime(1970, 1, 1)).total_seconds()
            DRTime = datetime.datetime.strptime(d['DRtime'], "%Y-%m-%d %H:%M:%S").hour
            DR_Start = int(time.mktime((datetime.datetime.strptime(d['DRtime'], "%Y-%m-%d %H:%M:%S")).timetuple()))
            DRduration = int(d['duration'])
            if OldDateTime != NewDateTime:
                TargetReduction = int(d['Power'])
                NewResDateTime = run(mRIDList, TargetReduction, DRTime, DR_Start, DRduration,OldResDateTime)
                #DrResponse = DrRes(ReplyTo, ApplianceLoadReductionType, CreatTime, Power, CoolingOffset, HeatingOffset, CoolingSetpoint, HeatingSetpoint, id1, id2)
                #requests.put('https://' + ip + ':' + port + replyTo, verify = False, cert = (ClientCert('postman')[0],ClientCert('postman')[1]), data = DrRespXML)
                OldResDateTime = NewResDateTime
                OldDateTime = NewDateTime
            else:
                print 'No new DR event is recieved!'
            time.sleep((Config.EVENT)*60)
        except ValueError as e:
            logger.info(str(e))
            pass
