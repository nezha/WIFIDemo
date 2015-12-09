#coding=utf-8
import numpy as np
import json   #the type database will be write into database as the format of json
import math
import re
#import matplotlib.pyplot as plt
'''
this code is to create fingerprint database 

'''
'''
@author nezha 2015/08/04
'''
DB_FN = "log.txt"  #原始数据源
DB_LandMark="LMDB_std" #目标数据库

#open the file of wifi info
f_db = open(DB_FN)
f_lmdb = open(DB_LandMark,'w')
#当是1 0的时候可以读取位置信息
#当是1 1的时候读取WiFi信息
StrStart = 'statusId | label';
StrEnd = 'statusId|sensorName|value|timestamp';
FlagStart = 0 
FlagEnd = 0
dictRF = {}
dictWiFi = {} #the item of string which will write into file
FlagLoc = '0' #init the flag of Loc position
#print 'start';
while True:
    #逐行读取
    line = f_db.readline()
    #去除空格或者换行符
    line = line.strip()
    if not line or len(line) < 5: 
        dictLoc = {};
        for key in dictWiFi.keys():
            if len(dictWiFi[key]) > 5:
                dictWiFi[key] = [np.mean(dictWiFi[key]),np.std(dictWiFi[key])];
            else:
                del(dictWiFi[key]);
        dictLoc['loc'] = dictRF[FlagLoc]; #get last loc
        #print FlagLoc;
        dictLoc['wifi'] = dictWiFi;
        outLine = str(dictLoc);
        f_lmdb.write(outLine)
        f_lmdb.flush()
        break
    
    if line == StrStart:
        FlagStart = 1
    if line == StrEnd:
        FlagEnd = 1   
    
    if FlagStart is 1 and FlagEnd is 0 and line !=  StrStart and line != StrEnd:
        #start read the location and label
        listTemp = line.split('|');
        dictRF[listTemp[0]] = listTemp[1];
    elif FlagStart is 1 and FlagEnd is 1 and line !=  StrStart and line != StrEnd:
        #start read the wifi info
        listTemp = line.split('|');
        dictLine = eval(listTemp[2]);   #get wifi info 
        if FlagLoc == '0':              #if is the init Flag ,init data
            FlagLoc = listTemp[0];
        
        #if FlagLoc ==  listTemp[0] and (dictLine['SSID'] is 'AirJ' or dictLine['SSID'] is 'AirJa'):    #the same as upper,so just add the 
        if FlagLoc ==  listTemp[0]:
            if dictLine['BSSID'] not in dictWiFi.keys():
                dictWiFi[dictLine['BSSID']] = [int(dictLine['level'])];
            else:
                dictWiFi[dictLine['BSSID']].append(int(dictLine['level']));         
        #elif dictLine['SSID'] is 'AirJ' or dictLine['SSID'] is 'AirJa':                          #if is is a new loc ,start write and reinit the data
        else:
            dictLoc = {};
            for key in dictWiFi.keys():
                #print('*****'+str(len(dictWiFi[key]))+'*****\n');
                if len(dictWiFi[key]) > 60:
                    dictWiFi[key] = [np.mean(dictWiFi[key]),np.std(dictWiFi[key])];
                else:
                    del(dictWiFi[key]);
            dictLoc['loc'] = dictRF[FlagLoc]; #get last loc
            dictLoc['wifi'] = dictWiFi;
            dictLoc['MeanStd'] = [0,0];  #用于确定定位精度的均值和方差
            outLine = str(dictLoc);
            outLine = outLine + '\n'
            f_lmdb.write(outLine)
            f_lmdb.flush()
            dictWiFi = {};
            dictLoc = {};
            FlagLoc = listTemp[0];      #new Flag
            if dictLine['BSSID'] not in dictWiFi.keys():
                dictWiFi[dictLine['BSSID']] = [int(dictLine['level'])];
            else:
                dictWiFi[dictLine['BSSID']].append(int(dictLine['level']));       

f_db.close()
f_lmdb.close()



        




