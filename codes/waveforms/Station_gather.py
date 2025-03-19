#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 18:13:19 2024

@author: sebinjohn
"""

from obspy.clients.fdsn import client
import pandas as pd
from obspy import UTCDateTime
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from matplotlib.dates import date2num as d2n
import matplotlib.ticker as ticker


client=client.Client("IRIS")

############
columbia_gq=pd.read_csv("/Users/sebinjohn/gq_proj/data/catalogs/columbia_gq_1988-2024.csv")
columbia_eq=pd.read_csv("/Users/sebinjohn/gq_proj/data/catalogs/columbia_eq_1988-2024.csv")

columbia_gq_dropped= columbia_gq.drop_duplicates(subset='evid', keep='first')
columbia_gq_dropped['time'] = pd.to_datetime(columbia_gq_dropped['time'])
columbia_gq_dropped['year'] = columbia_gq_dropped['time'].dt.year

stations=columbia_gq["sta"].unique()




def event_gather(evid,maxlen):
    cn=0
    ev=columbia_gq[columbia_gq['evid']==evid]
    ev_stas=ev["sta"].unique()
    org_ti=UTCDateTime(ev["time"].iloc[0])
    st=org_ti-180
    et=org_ti+420
    if len(ev_stas)>maxlen:
        stc=maxlen
    else:
        stc=len(ev_stas)
    for i in range(stc):
        try:
            sta=ev_stas[i]
            if cn==0:
                stream = client.get_waveforms("AK,AV,XE,YM,TA,AT", sta, "*", "BHZ", st, et)
                cn+=1
            else:
                stream+=client.get_waveforms("AK,AV,XE,YM,TA,AT", sta, "*", "BHZ", st, et)
        except Exception as e:
            cn=0
            print(e)
    print(stream)
    return stream

def station_gather(sta,maxlen,evids=None):
    cn=0
    ev_sta=columbia_gq[columbia_gq['sta']==sta]
    ev_ids=ev_sta["evid"].unique()
    if evids==None:
        ids=ev_ids[-10:]
    else:
        try:
            ids=list(set(evids) & set(ev_ids))
        except:
            print("no common events found")
            return None
    if len(ids)>maxlen:
        stc=maxlen
    else:
        stc=len(ids)
    for i in range(stc):
        ev=columbia_gq[columbia_gq['evid']==ids[i]]
        org_ti=UTCDateTime(ev["time"].iloc[0])
        st=org_ti-180
        et=org_ti+420
        try:
            if cn==0:
                stream = client.get_waveforms("AK,AV,XE,YM,TA,AT", sta, "*", "BHZ", st, et)
                cn+=1
            else:
                stream += client.get_waveforms("AK,AV,XE,YM,TA,AT", sta, "*", "BHZ", st, et)
        except Exception as e:
            cn=0
            print(e)
        print(stream)
    return stream



def plot(stream):
    stream.plot()
    return

def cus_ticker(x,pos):
    dt=mdates.num2date(x)
    if pos==0:
        string=dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        string=dt.strftime('%H:%M:%S')
    return string

def plot_sta_gat(stream):
    nrows=len(stream)
    fig,axes=plt.subplots(nrows=nrows,ncols=1,figsize=(10,3.3*nrows))
    plt.subplots_adjust(hspace=0.3)
    for i in range(nrows):
        tr=stream[i]
        timesec=tr.times()
        starttime=tr.stats.starttime
        obspy_times=[starttime+ele for ele in timesec]
        plt_times=[d2n(ele) for ele in obspy_times]
        label=tr.stats.network+"."+tr.stats.station+".."+tr.stats.channel
        axes[i].plot(plt_times, tr.data, 'k',lw=0.5,label=label)
        axes[i].xaxis.set_major_locator(ticker.LinearLocator(numticks=5)) 
        axes[i].xaxis.set_major_formatter(ticker.FuncFormatter(cus_ticker))
        axes[i].legend(loc="upper left")
        axes[i].set_xlim([plt_times[0],plt_times[-1]])
        axes[i].set_title(cus_ticker(plt_times[0],0)+" - "+cus_ticker(plt_times[-1],0))
        

    
stream=event_gather(885906,6)
plot(stream)

sta="GLI"
stream=station_gather(sta,6)
plot_sta_gat(stream)
    
    


