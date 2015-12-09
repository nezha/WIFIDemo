#coding=utf-8
from LMDB import LMDB
import matplotlib.pyplot as plt
import numpy as np 

'''
功能：绘制真实效果

'''
#read the sample data
Train_loc1 = open('loc1.txt');

#读取指纹数据库
lmdb = LMDB('LMDB_std')

walk = []

while True:
    #逐行读取
    wifiEntry = Train_loc1.readline()
    #去除空格或者换行符
    wifiEntry = wifiEntry.strip()
    if not wifiEntry or len(wifiEntry) < 10: 
        break;
    location = lmdb.nn_location(wifiEntry)
    walk.append(location)
Train_loc1.close()  
print(walk)   


