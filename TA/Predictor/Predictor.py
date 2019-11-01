#!/usr/bin/python
# -*- coding: utf-8 -*-
from sklearn.svm import SVR
import numpy as np
import sqlite3
import os
import sys
from datetime import datetime, timedelta
import pandas as pd
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

def db_path(function):
    for r,d,f in os.walk(os.path.normpath(os.getcwd()+os.sep+os.pardir)):
        for files in f:
            if files == function+'.db':
                url = os.path.join(r,files)
                url = url.rsplit(files)[0]
    return url

def to_matrix(l, n):
    return [l[i:i+n] for i in xrange(0, len(l), n)]

def GroupPowerDay(power):
    df = pd.DataFrame(power)
    df['Datetime'] = pd.to_datetime(df[0])
    df = df.set_index(['Datetime'])
    del df[0]
    df = df.resample('H').mean()
    cons = df[1].values.tolist()
    cons = [0 if x != x else x for x in cons]
    return cons

_ToDate = datetime.now()
def dataGen(mRID, ToDate, Days):
    FromDate = ToDate - timedelta(days = Days) # 
    ToDate = ToDate - timedelta(days = Days-1)
    FromDate = str(FromDate)
    ToDate = str(ToDate)
    mRID = mRID.encode('hex')
    mRID = mRID.upper()
    query = 'SELECT * FROM power WHERE mRID = "' + mRID + '" AND Date BETWEEN "' + FromDate + '" AND "' + ToDate + '" ;'
    try:
        #connection = sqlite3.connect(os.path.normpath(os.path.normpath(os.getcwd() + os.sep + os.pardir) + os.sep + 'database' + os.sep + 'TAdb.db'),isolation_level = None)
        connection = sqlite3.connect(db_path(Config.DB_NAME)+Config.DB_NAME+'.db',isolation_level = None)
        cursor = connection.cursor()
        cursor.execute(query)
        Power_dbout = cursor.fetchall()
        connection.close()
    except:
        pass
    
    data = list()
    power = list()
    if Power_dbout != None:
        for d in Power_dbout:
            power.append([d[2],d[3]])
        power = GroupPowerDay(power)
    else:
        print "Warning PR01, Cannot fetch out data from DB to predict the consumption, a flat estiation is replaced!"
        logger.info("Warning PR01, Cannot fetch out data from DB to predict the consumption, a flat estiation is replaced!")
        power = 25 * [1000]
    return power


def predict(mRID, ToDate, DayNumber):
    data = list()
    for i in range (DayNumber):
        try:
            data.append(dataGen(mRID, ToDate, i+1))
            break
        except:
            print 'Error PR01, Cannot generate the historical list'
            logger.info('Error PR01, Cannot generate the historical list')
            pass
    try:
        Prediction = list()
        scoreList = list()
        testY = data[len(data)-1]
        for d in data:
            y = d
            x = range(1,(len(y)+1))
            ave = reduce(lambda x, y: x + y, y) / len(y)
            x = to_matrix(x,1)
            x = np.asarray(x)
            trainX = x #x[:-20]
            trainY = np.asarray(y) #y[:-20]
            clf = SVR(kernel = 'rbf', degree = 5, gamma='auto', C = ave, epsilon = 0.02)
            clf.fit(trainX, y) 
            predY = clf.predict(x)
            scoreList.append(clf.score(x, testY))
            Prediction.append(predY.tolist())
        Ytrained = [sum(e)/len(e) for e in zip(*Prediction)]
        score = sum(scoreList)/len(scoreList)
        return Ytrained
    except:
        print 'Error PR02, Cannot predict the consumption, a flat estimate is replaced'
        logger.info('Error PR02, Cannot predict the consumption, a flat estimate is replaced')
        

##mRID = '\x10\x00\x00\x00\x00\x00\x00\x34\x10\x00\x00\x00\x00\x00\x00\x01'
##ToDate = datetime.now()
##DayNumber = 1
##predict(mRID, ToDate, DayNumber)
