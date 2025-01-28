#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 12:19:51 2024

@author: sebinjohn
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
import matplotlib.dates as mdates
from matplotlib.dates import date2num as d2n
import matplotlib.ticker as ticker
import random
from obspy import Stream,Trace
from sklearn.preprocessing import minmax_scale




client = Client("IRIS") 


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points 
    on the Earth's surface given their latitude and longitude in decimal degrees.

    :param lat1: Latitude of the first point in decimal degrees
    :param lon1: Longitude of the first point in decimal degrees
    :param lat2: Latitude of the second point in decimal degrees
    :param lon2: Longitude of the second point in decimal degrees
    :return: Distance between the two points in kilometers
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1 
    dlon = lon2 - lon1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)) 
    r = 6371  # Radius of Earth in kilometers
    return c * r



###loading relocated events for columbia and post glacier
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

###plotting events

columbia_gq_dropped= columbia_gq.drop_duplicates(subset='evid', keep='first')
columbia_gq_dropped['time'] = pd.to_datetime(columbia_gq_dropped['time'])
columbia_gq_dropped['year'] = columbia_gq_dropped['time'].dt.year

stations=columbia_gq["sta"].unique()

def station_gather(sta,maxlen,time_fr,evids=None,xof=20):
    cn=0
    ev_sta=columbia_gq[columbia_gq['sta']==sta]
    ev_ids=ev_sta["evid"].unique()
    try:
        ids=list(set(evids) & set(ev_ids))
    except:
        print("no common events found")
        return None
    ordered_ids = [id if id in ids else np.nan for id in evids]
    for i in range(maxlen):
        try:
            ev=columbia_gq[columbia_gq['evid']==ordered_ids[i]]
            org_ti=UTCDateTime(ev["time"].iloc[0])
            st=org_ti-(time_fr-xof)
            et=org_ti+time_fr
            if cn==0:
                stream = client.get_waveforms("AK,AV,XE,YM,TA,AT", sta, "*", "BHZ", st, et)
                cn+=1
            else:
                stream += client.get_waveforms("AK,AV,XE,YM,TA,AT", sta, "*", "BHZ", st, et)
        except Exception as e:
            n_points = time_fr*50+(time_fr-xof)*50
            network = "NET"       # Example network name
            station = "STA"       # Example station name
            channel = "BHZ"       # Example channel name
            start_time = UTCDateTime(0)  # Starting time of the trace
            
            # Create the trace data (18,000 zeros)
            data = np.zeros(n_points)
            
            # Create a Trace object
            trace = Trace()
            trace.data = data
            trace.stats.network = network
            trace.stats.station = station
            trace.stats.channel = channel
            trace.stats.starttime = start_time
            trace.stats.sampling_rate = 50.0  # Example sampling rate (in Hz)
            # Create a Stream and add the trace to it
            stream += Stream(traces=[trace])
            print(e)
        print(stream)
    return stream,ordered_ids

def cus_ticker(x,pos):
    dt=mdates.num2date(x)
    if pos==0:
        string=dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        string=dt.strftime('%M:%S')
    return string

def plot_sta_gat(stream,time_fr,evids=None,maxlen=None,spacing=1):
    
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14,9))
    plt.subplots_adjust(wspace=0.1)
    for i, tr in enumerate(stream):
        if i<maxlen/2:
            c=0
            position = i
        else:
            c=1
            position = i - int(maxlen / 2)
        evid=evids[i]
        timesec = tr.times()
        starttime = tr.stats.starttime
        label = f"{tr.stats.network}.{tr.stats.station}..{tr.stats.channel}"
        normalized_data = minmax_scale(tr.data, feature_range=(0, 1))
        axes[c].plot(timesec,normalized_data+position*spacing, 'k', lw=0.5)
        axes[c].text(timesec[-10*50],spacing+position*spacing,str(evid))
        axes[c].xaxis.set_major_locator(ticker.LinearLocator(numticks=5))
        #axes[c].xaxis.set_major_formatter(ticker.FuncFormatter(cus_ticker))
        #axes[c].legend(loc="upper left")
        #axes[c].axvline(x=mark_time, color='black', linestyle='--', linewidth=1.5,)
        axes[c].set_xlim([0, timesec[-1]])
    axes[1].set_title("Post events")
    axes[0].set_title("Columbia events")
    plt.show()
        

def event_sel(ev_no,col_ids_re,pos_ids_re):
    col_ids,pos_ids=[],[]
    ev_sta=columbia_gq[columbia_gq['sta']==sta]
    ev_ids=ev_sta["evid"].unique()
    for i in range(ev_no):
        selected_col_id = random.sample(list(col_ids_re), 1)[0]
        while selected_col_id not in ev_ids and selected_col_id not in col_ids:
            selected_col_id = random.sample(list(col_ids_re), 1)[0]
        col_ids.append(selected_col_id)
    for i in range(ev_no):
        selected_pos_id = random.sample(list(pos_ids_re), 1)[0]
        while selected_pos_id not in ev_ids and selected_pos_id not in pos_ids:
            selected_pos_id = random.sample(list(pos_ids_re), 1)[0]
        pos_ids.append(selected_pos_id)
    ids_to_plo = col_ids + pos_ids
    return ids_to_plo
                
    

ev_no=17
sta="GLI"
ids_to_plo=event_sel(ev_no,col_ids_re,pos_ids_re)

# Combine the two lists

maxlen=len(ids_to_plo)


stream,avail_ids=station_gather(sta,maxlen,evids=ids_to_plo,time_fr=50,xof=30)


plot_sta_gat(stream,time_fr=50,evids=ids_to_plo,maxlen=maxlen,spacing=0.8)


#filtering

stream2 = stream.copy()

# Set bandstop filter parameters to remove frequencies between 5 and 10 Hz
  # Minimum cutoff frequency in Hz
freq = 1 # Maximum cutoff frequency in Hz
filter_type = 'highpass'  # Bandstop filter

# Apply bandstop filter to all traces in the stream
for trace in stream2:
    trace.filter(filter_type, freq=freq, corners=4, zerophase=True)
    trace.taper(max_percentage=0.0001, type='cosine')
    
plot_sta_gat(stream2,time_fr=50,evids=ids_to_plo,maxlen=maxlen,spacing=0.8)




fig1, ax1 = plt.subplots()

# Generate the spectrogram and plot it on ax1
stream[0].spectrogram(axes=ax1)
ax1.set_ylim([0,5])
# Display the plot
plt.show()

fig1, ax1 = plt.subplots()

# Generate the spectrogram and plot it on ax1
stream2[-14].spectrogram(axes=ax1)
ax1.set_ylim([0,5])

# Display the plot
plt.show()


fig, axes = plt.subplots(nrows=17, ncols=2, figsize=(15, 60))  # Adjust figsize for better visibility

# Flatten the axes array for easier indexing
axes = axes.T.flatten()

# Loop through each trace in stream2 and plot
for i in range(len(stream2)):
    # Get the corresponding subplot axis
    ax = axes[i]
    
    # Plot spectrogram on the current axis
    stream2[i].spectrogram(axes=ax)
    
    # Set the title for the current subplot
    ax.set_title(f"Trace {i+1}", fontsize=10)
    ax.set_ylim([0,5])
