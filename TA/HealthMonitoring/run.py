import numpy as np
import os
import HPredictor
from datetime import datetime
import time
import sys
import json
def append_path(function):
    for r,d,f in os.walk(os.path.normpath(os.getcwd()+os.sep+os.pardir)):
        for files in f:
            if files == function+'.py' or files == function+'.pyc':
                url = os.path.join(r,files)
                url = url.rsplit(files)[0]
    return url
sys.path.append(append_path('Config'))
import Config

def json_path(function):
    for r,d,f in os.walk(os.path.normpath(os.getcwd()+os.sep+os.pardir)):
        for files in f:
            if files == function+'.json':
                url = os.path.join(r,files)
                url = url.rsplit(files)[0]
    return url
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(os.path.normpath(os.getcwd()+os.sep+os.pardir)+'/logs.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def run(t, TOT_rated, TOT_fl, Tau, R, n, Tau_Rated, P_rated, PF, V, I_Rated, P_t, temprature):
    I = P_t / V
    K_t = I / I_Rated
    #K=P_t/P_rated
    # Calculating initial TOT
    c = len(K_t)
    TOT_initial_t = np.zeros(c)
    TOT_initial_t_new = np.zeros(c)

    for i in range(c):
        TOT_initial_t[i] = (TOT_rated * ((K_t[i] ** 2 * R + 1) / (R + 1)) ** n)

    for i in range(c):
        if i == 0:
            TOT_initial_t_new[0] = TOT_initial_t[0]
        else:
            TOT_initial_t_new[i] = TOT_initial_t[i - 1]

    # Calculating ultimate TOT
    TOT_ult_t = TOT_rated * np.power(((np.power(K_t, 2) * R + 1) / (R + 1)), n)
    # Calculating Top Oil Transformer Temp

    Delta_TOT = np.zeros(c)
    for i in range(c):
        Delta_TOT[i] = ((TOT_ult_t[i]) - (TOT_initial_t_new[i])) * (1 - np.exp(-(Tau / Tau_Rated))) + TOT_initial_t_new[i]

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # HST_Int=60; % Intial HS Temp
    HST_Rated = 23.5        # Rated-load HST Temp
    # HST_Int=55; % Intial HS Temp
    # HST_Rated=59; % Rated-load HST Temp
    T_HST = 7        # HST Time Constant
    m = 0.8        # Forced Cooling
    Tau_H = 2.75 * ((HST_Rated) / (1 + 10960) * 2.5 ** 2)        # Rated Time Constant
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Calculating initial HST
    HST_initial_t = np.zeros(c)
    HST_initial_t_new = np.zeros(c)
    for i in range(c):
        HST_initial_t[i] = HST_Rated * ((K_t[i] ** 2 * R + 1) / (R + 1)) ** n


    for i in range(c):
        if i == 0:
            HST_initial_t_new[0] = HST_initial_t[0]
        else:
            HST_initial_t_new[i] = HST_initial_t[i-1]

    # Calculating ultimate HST
    HST_ult_t = HST_Rated * np.power(K_t, (2 * m))

    # Calculating Hot Spot Temp Transformer Temp
    Delta_HST = (HST_ult_t - HST_initial_t_new) * (1 - np.exp(-(Tau / Tau_H))) + HST_initial_t_new

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # The Cumulative Thermal Model
    Cumulative_Temp = Ambient_Temp + Delta_HST + Delta_TOT

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    c = len(Cumulative_Temp)
    Faa = np.zeros(c)
    FAA_Cum = np.zeros(c)
    Feqa = np.zeros(c)
    LOL = np.zeros(c)
    PUL = np.zeros(c)
    # Calculating the Aging Acceleration Factor
    for i in range(c):
        Faa[i] = (np.exp((15000.0 / 383.0) - (15000.0 / (Cumulative_Temp[i] + 273.0))))

    CT_sort = np.sort(Cumulative_Temp)
    Id = np.argsort(Cumulative_Temp)

    # Sort eigenvector accordingly
    Faa_new = Faa[Id]

    # Calculating Cumulatiave Aging Hours
    for i in range(c):
        if i == 0:
            FAA_Cum[0] = Faa[0]
        else:
            FAA_Cum[i] = FAA_Cum[i - 1] + Faa[i]

    # Calculating the Equivalent Aging Factor
    for i in range(c):
        Feqa[i] = FAA_Cum[i] / 24

    # Calculating the Percent Loss of Life
    for i in range(c):
        LOL[i] = ((Feqa[i] * (i+1) * 100.0) / 180000.0)

    # Calculating Tranformer's Isolation Loss of Life
    for i in range(c):
        PUL[i] = (9.80 * (10 ** -18)) * (np.exp((15000 / (273 + Cumulative_Temp[i]))))

    CT_sort = np.sort(Cumulative_Temp)
    Id = np.argsort(Cumulative_Temp)
    # Sort eigenvector accordingly
    PUL_new = PUL[Id]

    return Delta_TOT, Delta_HST, Cumulative_Temp

while True:
    mRID = Config.TA_MRID
    ToDate = datetime.now()
    DayNumber = 1
    try:
        power, temprature = HPredictor.P_T(mRID, ToDate, DayNumber)
    except:
        print 'Error HM01, Cannot predict the power and temprature'
        logger.info('Error HM01, Cannot predict the power and temprature')
        power = Config.POWER
        temprature = Config.INITIAL_TEMP
    # Identifying the constants of the model
    t = np.arange(1,25)
    TOT_rated = Config.INITIAL_TEMP
    TOT_fl = Config.FULL_LOAD_TEMP
    Tau = Config.TAU
    R = Config.LOAD_LOSS_RASTIO
    n = Config.COOLING
    Tau_Rated = Config.RATED_TAU
    P_rated = Config.POWER
    PF = Config.POWER_FACTOR
    V = Config.VOLTAGE
    I_Rated = Config.CURRENT
    P_t = np.array(power) # instantenious Load Power
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Ambient Temp
    Ambient_Temp = np.array(temprature)
    try:
        Delta_TOT, Delta_HST, Cumulative_Temp = run(t, TOT_rated, TOT_fl, Tau, R, n, Tau_Rated, P_rated, PF, V, I_Rated, P_t, temprature)
    except:
        print 'Error HM02, Health monitoring algorithm is not functional for given inputs!'
        logger.info('Error HM02, Health monitoring algorithm is not functional for given inputs!')
        Cumulative_Temp = [Config.MAX_TEMP - 10]
    #print Cumulative_Temp
    TimeList = list()
    d = datetime.now()
    H = d.hour
    for i in Cumulative_Temp:
        if i > Config.MAX_TEMP:
            if np.where(Cumulative_Temp==i)[0][0]> H-1:
                TimeList.append(np.where(Cumulative_Temp==i)[0][0])
    if TimeList != []:
        Time = TimeList[0]
        data = {"DateTime": str(d.strftime("%Y-%m-%d %H:%M:%S")), "Power": 0.1*P_t[Time]*1000, "DRtime": str(datetime(d.year, d.month, d.day, Time, 0)), "duration": 3600}
        with open(json_path('DRes')+'DRes.json', 'w') as outfile:
            json.dump(data, outfile)
        print 'Alarm! Abnormal transformer temperature! a DR event is expected at: ', str(datetime(d.year, d.month, d.day, Time, 0))
        logger.info('Alarm! Abnormal transformer temperature! a DR event is expected at: ' + str(datetime(d.year, d.month, d.day, Time, 0)))
    else:
        print ' Transformer Temperature is normal '
        logger.info(' Transformer Temperature is normal ')
    time.sleep(60)
