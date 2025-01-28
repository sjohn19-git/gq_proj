#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 13:27:09 2024

@author: sebinjohn
"""

import pandas as pd
import numpy as np
from tqdm import tqdm
from obspy import UTCDateTime
from obspy.clients.fdsn import Client

client = Client("IRIS") 


file_loc = '/Users/sebinjohn/gq_proj/data/reloc/>2005/hypoDD.reloc'
columbia_gq=pd.read_csv("/Users/sebinjohn/gq_proj/data/catalogs/columbia_gq_1988-2024.csv")

mdat = pd.read_csv(file_loc, delim_whitespace=True, header=None)

lon_re = mdat.iloc[:, 2].values
lat_re = mdat.iloc[:, 1].values
yr_re=mdat.iloc[:, 10].values
ids_reloc=mdat.iloc[:, 0].values
glce_lat=61.134
glce_lon=-147.1078

col_bool_re=np.array([True if ele>glce_lon else False for ele in lon_re])
yr_bool_re=np.array([True if ele>=2005 else False for ele in yr_re])
col_bool_re_fi=np.logical_and(col_bool_re,yr_bool_re)
pos_bool_re_fi=np.logical_and(~col_bool_re,yr_bool_re)

col_ids_re=ids_reloc[col_bool_re_fi]
pos_ids_re=ids_reloc[pos_bool_re_fi]

###########################################

columbia_gq_dropped= columbia_gq.drop_duplicates(subset='evid', keep='first')
columbia_gq_dropped['time'] = pd.to_datetime(columbia_gq_dropped['time'])
columbia_gq_dropped['year'] = columbia_gq_dropped['time'].dt.year

sta="GLI"
col_df=[]

for ide in tqdm(col_ids_re, desc="Processing Events"):
    ev_sta=columbia_gq[columbia_gq['sta']==sta]
    ev_ids=ev_sta["evid"].unique()
    if ide in ev_ids:
        ev=columbia_gq[columbia_gq['evid']==ide]
        org_ti=UTCDateTime(ev["time"].iloc[0])
        st=org_ti-30
        et=org_ti+40+30
        try:
            stream = client.get_waveforms("AK,AV,XE,YM,TA,AT", sta, "*", "BHZ", st, et)
            freq = 1 # Maximum cutoff frequency in Hz
            filter_type = 'highpass'  # Bandstop filter
            print(len(stream))
            for trace in stream:
                trace.filter(filter_type, freq=freq, corners=4, zerophase=True)
                trace.taper(max_percentage=0.0001, type='cosine')
        except:
            pass
        data = stream[0].data  # Get the data array
        start_time = stream[0].stats.starttime  # Extract the start time from the stream metadata
        sampling_rate = 50  # 50 samples per second
        n = len(data)
        time_step = 1 / sampling_rate
        time_array = np.array([start_time + i * time_step for i in range(n)])
        
        df=pd.DataFrame({'Row': range(len(data)),'ide': ide,           
                         'data': data,'time': time_array,'org_time':[org_ti]*len(data)})
        col_df.append(df)
        
col_df = pd.concat(col_df, ignore_index=True)
col_df.to_csv("/Users/sebinjohn/gq_proj/data/feature_extraction/col_data.csv", index=False)


sta="GLI"
pos_df=[]

for ide in tqdm(pos_ids_re, desc="Processing Events"):
    ev_sta=columbia_gq[columbia_gq['sta']==sta]
    ev_ids=ev_sta["evid"].unique()
    if ide in ev_ids:
        ev=columbia_gq[columbia_gq['evid']==ide]
        org_ti=UTCDateTime(ev["time"].iloc[0])
        st=org_ti-30
        et=org_ti+40+30
        try:
            stream = client.get_waveforms("AK,AV,XE,YM,TA,AT", sta, "*", "BHZ", st, et)
            freq = 1 # Maximum cutoff frequency in Hz
            filter_type = 'highpass'  # Bandstop filter
            print(len(stream))
            for trace in stream:
                trace.filter(filter_type, freq=freq, corners=4, zerophase=True)
                trace.taper(max_percentage=0.0001, type='cosine')
        except:
            pass
        data = stream[0].data  # Get the data array
        start_time = stream[0].stats.starttime  # Extract the start time from the stream metadata
        sampling_rate = 50  # 50 samples per second
        n = len(data)
        time_step = 1 / sampling_rate
        time_array = np.array([start_time + i * time_step for i in range(n)])
        
        df=pd.DataFrame({'Row': range(len(data)),'ide': ide,           
                         'data': data,'time': time_array,'org_time':[org_ti]*len(data)})
        pos_df.append(df)
        
pos_df = pd.concat(pos_df, ignore_index=True)
pos_df.to_csv("/Users/sebinjohn/gq_proj/data/feature_extraction/pos_data.csv", index=False)

