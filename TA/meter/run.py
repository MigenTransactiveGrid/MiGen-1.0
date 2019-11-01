import os
import sqlite3
import datetime
import Measurlogic
import Termometer
import time
import sys
import xmltodict
def append_path(function):
    for r,d,f in os.walk(os.path.normpath(os.getcwd()+os.sep+os.pardir)):
        for files in f:
            if files == function+'.py' or files == function+'.pyc':
                url = os.path.join(r,files)
                url = url.rsplit(files)[0]
    return url
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

def runRTU():
    try:
        RTU = Measurlogic.run()
    except:
        print 'Error M01, Cannot read the transofrmer data, check RTU'
        logger.info('Error M01, Cannot read the transofrmer data, check RTU')
    try:
        Termo = Termometer.run()
    except:
        print 'Error M02, Cannot read the transformer temperature'
        logger.info('Error M02, Cannot read the transformer temperature')

    try:
        mrid = Config.TA_MRID
        mrid = mrid.encode('hex')
        mrid = mrid.upper()
        Volt_AB = RTU[0]
        Currnet_A = RTU[1]
        Currnet_B = RTU[2]
        Power_A = RTU[3]
        Power_B = RTU[4]
        Freq = RTU[5]
        pf_A = RTU[6]
        pf_B = RTU[7]
        CaseTemp = Termo[0][0]
        EnvTemp = Termo[2][0]
    except:
        print 'Error M03, data is not in correct format'
        logger.info('Error M03, data is not in correct format')

    try:
        to_db = [(datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S'), mrid, Volt_AB, Currnet_A, Currnet_B, Power_A, Power_B, Freq, pf_A, pf_B, CaseTemp, EnvTemp]
        #connection = sqlite3.connect(os.path.normpath(os.getcwd() + os.sep + 'database' + os.sep + 'TAdb.db'),isolation_level = None)
        connection = sqlite3.connect(os.path.normpath(os.path.normpath(os.getcwd() + os.sep + os.pardir) + os.sep + 'database' + os.sep + 'TAdb.db'),isolation_level = None)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO XF (Date, mRID, Volt_AB, Currnet_A, Currnet_B, Power_A, Power_B, Freq, pf_A, pf_B, CaseTemp, EnvTemp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
        connection.commit()
        connection.close()
    except:
        print 'Error M04, Cannot insert RTU data to DB'
        logger.info('Error M04, Cannot insert RTU data to DB')

def runCAs(timestamp):
    cwd = append_path('Server')
    mRIDList = Config.MRIDLIST
    ActiveEndDevice = len(mRIDList)
    #ActiveEndDevice = 2
    meter = []
    try:
        for row in range(ActiveEndDevice):
            with open(os.path.normpath(cwd + os.sep + 'mup' + os.sep + str(row+1) + os.sep +'MirrorUsagePoint.xml')) as fd:
                dic = xmltodict.parse(fd.read())
                mrid = str(dic['MirrorUsagePoint']['mRID'])
                StrtTime = datetime.datetime.fromtimestamp(int(dic['MirrorUsagePoint']['MirrorMeterReading']['Reading']['timePeriod']['start'])).strftime('%Y-%m-%d %H:%M:%S')
                MeterValue = int(dic['MirrorUsagePoint']['MirrorMeterReading']['Reading']['value'])
                if MeterValue > 40000000:
                    MeterValue = 0
                meter.append([StrtTime, mrid, MeterValue])
    except:
        print 'Error M05, data is not in a correct format for CA metering '
        logger.info('Error M05, data is not in a correct format for CA metering ')
        pass
    try:    
        for i in range(len(meter)):
            if meter[i][0] != timestamp[i]:
                timestamp[i] = meter[i][0]
                to_db = [meter[i][0], meter[i][1], meter[i][2]]
                connection = sqlite3.connect(os.path.normpath(os.path.normpath(os.getcwd() + os.sep + os.pardir) + os.sep + 'database' + os.sep + 'TAdb.db'),isolation_level = None)
                cursor = connection.cursor()
                cursor.execute("INSERT INTO power (Date, mRID, Power) VALUES (?, ?, ?);", to_db)
                connection.commit()
                connection.close()
            else:
                print "No new metering data received for ", meter[i][1]
                logger.info('Error M06, No new CA metering data received for '+ meter[i][1])
    except:
        print 'Error M07, Cannot insert CA metering data to DB'
        logger.info('Error M07, Cannot insert CA metering data to DB')
        raise
    return timestamp
mRIDList = Config.MRIDLIST
ActiveEndDevice = len(mRIDList)
timestamp = ActiveEndDevice * [0]    
while True:
    runRTU()
    timestamp = runCAs(timestamp)
    time.sleep(60)
 
