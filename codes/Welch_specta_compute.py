#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Wed Dec 18 13:28:18 2024

@author: sebinjohn
"""

from obspy.clients.iris import Client
from obspy import UTCDateTime
import pandas as pd
from obspy.signal.invsim import evalresp
import scipy.signal as sig
import numpy as np
import matplotlib.pyplot as plt


client = Client()

starttime=UTCDateTime(2005,1,1)
endtime=UTCDateTime(2024,12,18)

reponse=client.resp("AK","GLI",location="*",channel="BHZ",starttime=starttime, endtime=endtime, filename="/Users/sebinjohn/gq_proj/data/RESP/GLI")
nfft=2**14


col_data=pd.read_csv("/Users/sebinjohn/gq_proj/data/feature_extraction/col_data.csv")
pos_data=pd.read_csv("/Users/sebinjohn/gq_proj/data/feature_extraction/pos_data.csv")

grouped_col = col_data.groupby('ide')

power_freq_df = pd.DataFrame(columns=["power", "frequency", "org_time"])
for ide, group in grouped_col:
    # Extract the 'data' values
    data_values = group['data'].values
    if len(data_values) == 5000:
        data_values = group['data'].values[23*50:76*50]
        plt.plot
        time=UTCDateTime(group['org_time'].iloc[0])
        org_time = group['org_time'].iloc[0]
        nfft=1024
        resp1 = evalresp(t_samp = 50, nfft=nfft, 
                      filename="/Users/sebinjohn/gq_proj/data/RESP/GLI", date = time,
                      station="GLI", channel="BHZ",
                      locid="*", network="AK",
                      units="ACC")
        windlap=0.5
        f,Pxx=sig.welch(data_values,fs=50,nperseg=nfft,noverlap=nfft*windlap)
        dbPxx=10.*np.log10(Pxx[1:]/(np.abs(resp1[1:])**2))
        power_freq_df.loc[ide] = [dbPxx.tolist(), f[1:].tolist(), org_time]
    else:
        print(ide)
power_freq_df.to_csv("/Users/sebinjohn/gq_proj/data/PSDs/col_power.csv")


grouped_pos = pos_data.groupby('ide')

power_freq_df = pd.DataFrame(columns=["power", "frequency", "org_time"])
for ide, group in grouped_pos:
    # Extract the 'data' values
    data_values = group['data'].values
    if len(data_values) == 5000:
        data_values = group['data'].values[23*50:76*50]
        time=UTCDateTime(group['org_time'].iloc[0])
        org_time = group['org_time'].iloc[0]
        nfft=1024
        resp1 = evalresp(t_samp = 50, nfft=nfft, 
                      filename="/Users/sebinjohn/gq_proj/data/RESP/GLI", date = time,
                      station="GLI", channel="BHZ",
                      locid="*", network="AK",
                      units="ACC")
        windlap=0.5
        f,Pxx=sig.welch(data_values,fs=50,nperseg=nfft,noverlap=nfft*windlap)
        dbPxx=10.*np.log10(Pxx[1:]/(np.abs(resp1[1:])**2))
        power_freq_df.loc[ide] = [dbPxx.tolist(), f[1:].tolist(), org_time]
    else:
        print(ide)
power_freq_df.to_csv("/Users/sebinjohn/gq_proj/data/PSDs/pos_power.csv")


for ide, group in grouped_pos:
    # Extract the 'data' values
    data_values = group['data'].values[23*50:76*50]
    plt.figure()
    plt.plot(data_values)