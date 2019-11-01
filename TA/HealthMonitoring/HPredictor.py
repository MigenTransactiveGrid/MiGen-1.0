#!/usr/bin/python
# -*- coding: utf-8 -*-
from sklearn.svm import SVR
import numpy as np
import sqlite3
import os
from datetime import datetime, timedelta
import pandas as pd
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(os.path.normpath(os.getcwd()+os.sep+os.pardir)+'/logs.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def to_matrix(l, n):
    return [l[i:i+n] for i in xrange(0, len(l), n)]

def GroupDay(power):
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
    query = 'SELECT * FROM XF WHERE mRID = "' + mRID + '" AND Date BETWEEN "' + FromDate + '" AND "' + ToDate + '" ;'
    try:
        connection = sqlite3.connect(os.path.normpath(os.path.normpath(os.getcwd() + os.sep + os.pardir) + os.sep + 'database' + os.sep + 'TAdb.db'),isolation_level = None)
        #connection = sqlite3.connect(os.path.normpath(os.getcwd() + os.sep + 'database' + os.sep + 'TAdb.db'),isolation_level = None)
        cursor = connection.cursor()
        cursor.execute(query)
        dbout = cursor.fetchall()
        connection.close()
    except:
        raise
    data = list()
    power = list()
    EnvTemp = list()
    if dbout != []:
        for d in dbout:
            power.append([d[2],float(d[6]+d[7])])
            EnvTemp.append([d[2],float(d[11]+d[12])])
        power = GroupDay(power)
        temperature = GroupDay(EnvTemp)
        return power, temperature
    else:
        print 'Error HP01, Cannot fetch the data out from DB'
        logger.info('Error HP01, Cannot fetch the data out from DB')


def prdedict(data):
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

def P_T(mRID, ToDate, DayNumber):
    datapower = list()
    datatemperature = list()
    for i in range (DayNumber):
        try:
            power, temperature = dataGen(mRID, ToDate, i+1)
            datapower.append(power)
            datatemperature.append(temperature)
        except:
            print 'Error HP02, Cannot generate the data for prediction'
            logger.info('Error HP02, Cannot generate the data for prediction')
    try:
        PredictedPower = prdedict(datapower)
        PredictedTemp = prdedict(datatemperature)
    except:
        print 'Error HP03, Cannot predict transformer power and temperature'
        logger.info('Error HP03, Cannot predict transformer power and temperature')
        PredictedPower = 24 * [24]
        PredictedTemp = 24 * [7.5]
    return PredictedPower, PredictedTemp
#if __name__ == "__main__":
    #mRID = '\x10\x00\x00\x00\x00\x00\x00\x44\x10\x00\x00\x00\x00\x00\x00\x0a'
    #ToDate = datetime.now()
    #DayNumber = 1
    #power, temprature = run(mRID, ToDate, DayNumber)
