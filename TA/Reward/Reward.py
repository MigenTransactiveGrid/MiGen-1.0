import sqlite3
import os
from datetime import datetime, timedelta
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
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(os.path.normpath(os.getcwd()+os.sep+os.pardir)+'/logs.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
#------------------------------------------------------
def db_path(function):
    for r,d,f in os.walk(os.path.normpath(os.getcwd()+os.sep+os.pardir)):
        for files in f:
            if files == function+'.db':
                url = os.path.join(r,files)
                url = url.rsplit(files)[0]
    return url

def Reward(mRID, _ToDate):
    FromDate = _ToDate - timedelta(days = 1) # ToDate = datetime.now()
    FromDate = str(FromDate)
    ToDate = str(_ToDate)
    mRID = mRID.encode('hex')
    mRID = mRID.upper()
    query = 'SELECT * FROM power WHERE mRID = "' + mRID + '" AND Date BETWEEN "' + FromDate + '" AND "' + ToDate + '" ;'
    try:
        connection = sqlite3.connect(db_path(Config.DB_NAME)+Config.DB_NAME+'.db',isolation_level = None)
        cursor = connection.cursor()
        cursor.execute(query)
        Power_dbout = cursor.fetchall()
        connection.close()
    except:
        raise
    FromDate = _ToDate - timedelta(days = 30) # ToDate = datetime.now()
    FromDate = str(FromDate)
    query = 'SELECT * FROM credit WHERE mRID = "' + mRID + '" AND Date BETWEEN "' + FromDate + '" AND "' + ToDate + '" ;'
    try:
        connection = sqlite3.connect(db_path(Config.DB_NAME)+Config.DB_NAME+'.db',isolation_level=None)
        cursor = connection.cursor()
        cursor.execute(query)
        Credit_dbout = cursor.fetchall()
        connection.close()
    except:
        pass

    PowerList = []
    CreditList = []
    if Power_dbout:
        for i in range (len(Power_dbout)):
            PowerList.append(Power_dbout[i][3])
    #Power_dbout = [1000] # TO TEST
        PowerBar = float(sum(PowerList))/len(PowerList)
    else:
        PowerBar = 1000

    #Credit_dbout = [1000] # TO TEST
    if CreditList:
        for i in range (len(Credit_dbout)):
            CreditList.append(Credit_dbout[i][3])
        CreditBar = float(sum(CreditList))/len(CreditList)
    else:
        CreditBar = 1000

    query = 'SELECT * FROM power WHERE mRID = "' + mRID + '" ORDER BY ID DESC LIMIT 1;'
    try:
        connection = sqlite3.connect(db_path(Config.DB_NAME)+Config.DB_NAME+'.db',isolation_level = None)
        cursor = connection.cursor()
        cursor.execute(query)
        Power_now = cursor.fetchall()
        connection.close()
    except:
        logger.info("Error Re01, Cannot fetch out power data from DB")
        pass

    if Power_now != []:
        Power_now = Power_now[0][3]
    else:
        Power_now = 1000
        logger.info("Warning Re02, Cannot fetch out power data from DB to predict the consumption, a flat estiation is replaced!")
        
    #Power_now = float([900][0]) # TO TEST
    query = 'SELECT * FROM credit WHERE mRID = "' + mRID + '" ORDER BY ID DESC LIMIT 1;'
    try:
        connection = sqlite3.connect(db_path(Config.DB_NAME)+Config.DB_NAME+'.db',isolation_level = None)
        cursor = connection.cursor()
        cursor.execute(query)
        credit_now = cursor.fetchall()
        connection.close()
    except:
        logger.info("Error Re03, Cannot fetch out credit data from DB")
        pass

    if credit_now != []:
        credit_now = credit_now[0][3]
    else:
        credit_now = 1000
        logger.info("Warning Re04, Cannot fetch out credit data from DB to predict the consumption, a flat estiation is replaced!")
    #credit_now = float([900][0]) # TO TEST
    
    C0 = 1.2
    C1 = 0.5
    C2 = 0.5
    reward = C0 * ((C1 * (1+(PowerBar - Power_now)/PowerBar)) + (C2 * (1 + (credit_now - CreditBar)/CreditBar)))
    return reward







        
