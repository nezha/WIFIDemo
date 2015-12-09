#coding=utf-8
import string
from scipy import stats
import math

class DBEntry:
    location = ''
    def __init__(self):
        self.location = ''
        self.ap_rss_dict = {} #need init or all object will use the same apRssiList to append
class LMDB(list):             #extend the list
    def __init__(self,path):#read the file and add DBEntry to self
        f = open(path);
        while True:
            line = f.readline();
            line = line.strip();
            if not line:break;
            line = eval(line);   #set the str to dict
            db_entry = DBEntry();
            db_entry.location = line['loc'];
            db_entry.ap_rss_dict = line['wifi'];
            self.append(db_entry);
        f.close();
        
    
    def __calDiatance(self,query_entry, db_entry):
        query_aps = set(query_entry.keys());
        db_aps = set(db_entry.keys());
        all_aps = query_aps & db_aps;
        distance = 0.0;
        sum = 0.0
        for singleAp in all_aps:
            sum = sum + (query_entry[singleAp]-db_entry[singleAp][0])**2;
        distance = sum;
        return distance/len(all_aps);
    #use knn lm_str format as {'mac1':level,'mac2':level2}
    def nn_location(self,lm_str):
        client_entry = eval(lm_str);
        distance_list = [];
        for db_entry in self:
            distance = self.__calDiatance(client_entry,db_entry.ap_rss_dict);
            distance_list.append(distance);
        nn_index = distance_list.index(min(distance_list));
        return self[nn_index].location;     