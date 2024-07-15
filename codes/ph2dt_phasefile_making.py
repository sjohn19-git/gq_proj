#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 16:07:39 2024

@author: sebinjohn
"""


import pandas as pd
import os
from math import radians, sin, cos, sqrt, atan2
import matplotlib.pyplot as plt
import re
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime
from matplotlib.dates import date2num as d2n


os.chdir("/Users/sebinjohn/gq_proj")

#columbia
gq=pd.read_csv("/Users/sebinjohn/gq_proj/data/catalogs/columbia_gq_1988-2024.csv")
gq_p=gq[gq['phases']=='P']

gq_times=gq_p['time']

gq_datetime=[]

for ele in gq_times:
    cleaned_str = ele[:26]
    gq_datetime.append(datetime.strptime(cleaned_str, '%Y-%m-%d %H:%M:%S.%f'))

is_year_yr = [dt.year>2004 for dt in gq_datetime]  

gq_p_2005=gq_p[is_year_yr] 
gq_p_2005_ev=gq_p_2005["evid"].unique()    
    
os.chdir("/Users/sebinjohn/gq_proj/data/reloc")
with open("all.dat", "w") as file:
    for ele in gq_p_2005_ev:
        ele_df=gq_p_2005[gq_p_2005["evid"]==ele]
        elat=ele_df["lat"].iloc[0]
        elon=ele_df["lon"].iloc[0]
        edepth=ele_df["depth"].iloc[0]
        emag=ele_df["ml"].iloc[0]
        time_str=ele_df['time'].iloc[0]
        ele_date=datetime.strptime(time_str[:26], '%Y-%m-%d %H:%M:%S.%f')
        file.write( "# "+str(ele_date.year) + " "+str(ele_date.month)
                   +" "+str(ele_date.day)+" "+str(ele_date.hour)
                   +" "+str(ele_date.minute)+" "+str(ele_date.second)
                   +"."+str(ele_date.microsecond)[:2]+" "+str(elat)
                   +" "+str(elon)+" "+str(edepth)+" "+str(emag)+" 0"
                   +" 0"+" 0"+" "+str(ele)
                   +"\n")
        for i in range(len(ele_df)):
            artimes=pd.to_datetime(ele_df["artime"],unit="s")
            tt=str((artimes.iloc[i]-ele_date).total_seconds())[:4]
            sta=str(ele_df["sta"].iloc[i])
            file.write(sta+" "+tt+" -0.2 P"+"\n")
       
stas=gq_p_2005['sta'].unique()
stat_loc=pd.read_csv("./Alaska_network_station_location.csv")
lon_sta=np.array([])
lat_sta=np.array([])
for ele in stas:
    lon_sta=np.append(lon_sta,(stat_loc[stat_loc["Station Code"]==ele]["Longitude"].iloc[0]))
    lat_sta=np.append(lat_sta,(stat_loc[stat_loc["Station Code"]==ele]["Latitude"].iloc[0]))

with open("allsta.dat", "w") as file:
    for i in range(len(stas)):
        file.write(str(stas[i])+" "+str(lat_sta[i])+" "+str(lon_sta[i])+"\n")
 




##year classific
is_year_yr = [dt.year == 2014 for dt in gq_datetime]  
    
gq_p_yr=gq_p[is_year_yr]

gq_p_yr_ev=gq_p_yr["evid"].unique()

os.chdir("/Users/sebinjohn/gq_proj/data/reloc")
with open("yr.dat", "w") as file:
    for ele in gq_p_yr_ev:
        ele_df=gq_p_yr[gq_p_yr["evid"]==ele]
        elat=ele_df["lat"].iloc[0]
        elon=ele_df["lon"].iloc[0]
        edepth=ele_df["depth"].iloc[0]
        emag=ele_df["ml"].iloc[0]
        time_str=ele_df['time'].iloc[0]
        ele_date=datetime.strptime(time_str[:26], '%Y-%m-%d %H:%M:%S.%f')
        file.write( "# "+str(ele_date.year) + " "+str(ele_date.month)
                   +" "+str(ele_date.day)+" "+str(ele_date.hour)
                   +" "+str(ele_date.minute)+" "+str(ele_date.second)
                   +"."+str(ele_date.microsecond)[:2]+" "+str(elat)
                   +" "+str(elon)+" "+str(edepth)+" "+str(emag)+" 0"
                   +" 0"+" 0"+" "+str(ele)
                   +"\n")
        for i in range(len(ele_df)):
            artimes=pd.to_datetime(ele_df["artime"],unit="s")
            tt=str((artimes.iloc[i]-ele_date).total_seconds())[:4]
            sta=str(ele_df["sta"].iloc[i])
            file.write(sta+" "+tt+" -0.2 P"+"\n")
       
#writing station.dat
stas=gq_p_yr['sta'].unique()
stat_loc=pd.read_csv("./Alaska_network_station_location.csv")
lon_sta=np.array([])
lat_sta=np.array([])
for ele in stas:
    lon_sta=np.append(lon_sta,(stat_loc[stat_loc["Station Code"]==ele]["Longitude"].iloc[0]))
    lat_sta=np.append(lat_sta,(stat_loc[stat_loc["Station Code"]==ele]["Latitude"].iloc[0]))

with open("station.dat", "w") as file:
    for i in range(len(stas)):
        file.write(str(stas[i])+" "+str(lat_sta[i])+" "+str(lon_sta[i])+"\n")
 





