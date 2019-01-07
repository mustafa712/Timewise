# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 00:09:48 2019

@author: Akul Bansal
"""
import xml.etree.ElementTree as ET
import pandas as pd


file = pd.read_csv("Test_datasets\lums-sum17.csv")
for i in range(len(file)):
    out = '\t <class id="'+str(file.iloc[i]["Class Id"]) +'" '
    out += 'days="'+str(file.iloc[i]["Days"])+'" '
    out += 'start="'+str(file.iloc[i]["Start"])+'" '
    out += 'weeks="'+str(file.iloc[i]["Weeks"])+'" '
    out += 'room="'+str(file.iloc[i]["Room Id"])+'"/>'
    print(out)  

    
