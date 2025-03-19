#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 21:26:48 2024

@author: sebinjohn
"""

import pandas as pd
import os
from math import radians, sin, cos, sqrt, atan2
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
import matplotlib.dates as mdates
import datetime
from matplotlib.dates import date2num as d2n
import datetime
import math

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

# Example usage
lat1, lon1 = 61.134605, -147.107864  # Point 1: 61° 8'4.58"N, 147° 6'28.31"W
lat2, lon2 = 60.169856, 24.938379  # Point 2: Helsinki, Finland
distance = haversine(lat1, lon1, lat2, lon2)
print(f"Distance: {distance:.2f} km")



os.chdir("/Users/sebinjohn/gq_proj")

gq_catalog=pd.read_csv("/Users/sebinjohn/gq_proj/data/catalogs/gq_catalog_1988-2024.csv")
gq_lon=gq_catalog['lon']
gq_lat=gq_catalog['lat']

columbia_gq=pd.read_csv("/Users/sebinjohn/gq_proj/data/catalogs/columbia_gq_1988-2024.csv")

####
unq_ev_st_col = columbia_gq.drop_duplicates(subset=['evid', 'sta'])
sta_cnts = unq_ev_st_col['sta'].value_counts()

tp_stas= sta_cnts.head(30)

# Plotting the bar graph
plt.figure()
tp_stas.plot(kind='bar')
plt.xlabel('Elements')
plt.ylabel('Count')
plt.title('Top 30 Elements in "sta" Column')
plt.show()
###

col_gq_p=columbia_gq[columbia_gq['phases']=='P']

col_gq_p_KNK=col_gq_p[columbia_gq['sta']=='KNK']
col_gq_p_KLU=col_gq_p[columbia_gq['sta']=='KLU']
col_gq_p_KNK=col_gq_p_KNK.drop_duplicates('evid')
col_gq_p_KLU=col_gq_p_KLU.drop_duplicates('evid')


common_evid = pd.Series(list(set(col_gq_p_KNK['evid']) & set(col_gq_p_KLU['evid'])))

subset_KNK = col_gq_p_KNK[col_gq_p_KNK['evid'].isin(common_evid)]
subset_KLU = col_gq_p_KLU[col_gq_p_KLU['evid'].isin(common_evid)]

sd_KNK=subset_KNK['deltim'].apply(lambda x: float(x.strip('(),')))
sd_KLU=subset_KLU['deltim'].apply(lambda x: float(x.strip('(),')))
sd2=(sd_KNK.values)**2+(sd_KLU.values)**2
sd=np.sqrt(sd2)

plt.figure(figsize=(10, 6))
plt.hist(sd, bins=30, edgecolor='black', alpha=0.7)

# Adding titles and labels
plt.title('Distribution of Standard Deviations')
plt.xlabel('Standard Deviation')
plt.ylabel('Frequency')
plt.grid(True)
# Display the plot
plt.show()


time_diff=subset_KNK['artime'].values-subset_KLU['artime'].values

sd[sd>0.7]=np.nan
time_diff[sd>0.7]=np.nan

glce_lat=61.134
glce_lon=-147.1078
KNK_lat=61.4131
KNK_lon=-148.4585
KLU_lat=61.4924
KLU_lon=-145.9227

ce_KNK=haversine(glce_lat, glce_lon, KNK_lat, KNK_lon)
ce_KLU=haversine(glce_lat, glce_lon, KLU_lat, KLU_lon)
p_vel=3.0

ttKNK=ce_KNK/p_vel
ttKLU=ce_KLU/p_vel
ttdiff=ttKNK-ttKLU

ortime=d2n(pd.to_datetime(subset_KNK['time']))

ortime_yrs=np.array([ele.year for ele in pd.to_datetime(subset_KNK['time'])])

col_ortime=ortime[time_diff>ttdiff]
col_yerr=sd[time_diff>ttdiff]
col_time_diff=time_diff[time_diff>ttdiff]
col_ortime_yrs=ortime_yrs[time_diff>ttdiff]

pos_ortime=ortime[time_diff<ttdiff]
pos_yerr=sd[time_diff<ttdiff]
pos_time_diff=time_diff[time_diff<ttdiff]
pos_ortime_yrs=ortime_yrs[time_diff<ttdiff]


fig, ax = plt.subplots(figsize=(10, 6))
ax.errorbar(col_ortime,col_time_diff,yerr=col_yerr,fmt='o', ecolor='red', capsize=4,markersize=4,markerfacecolor='blue', markeredgecolor='blue')
ax.errorbar(pos_ortime,pos_time_diff,yerr=pos_yerr,fmt='o', ecolor='red', capsize=4,markersize=4,markerfacecolor='green', markeredgecolor='green')
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
xlim_start = d2n(datetime.date(2005,1,1))
xlim_end = d2n(datetime.date(2025,1,1))
ax.axhline(ttdiff,ls="--",c="red")
ax.set_xlim([xlim_start, xlim_end])
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.set_ylim([-3,7])
ax.set_ylabel("p arrival at KNK - KLU")

plt.hist(sd, bins=50, edgecolor='black')

pos_yr,pos_cnts=np.unique(pos_ortime_yrs, return_counts=True)
col_yr,col_cnts=np.unique(col_ortime_yrs, return_counts=True)

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(pos_yr, pos_cnts, color='grey')
# Set labels and title
ax.set_xlabel('Year')
ax.set_ylabel('Number of GQ')
ax.set_title('Number of GQ of Each Year post')
ax.set_xticks(range(2005, 2024,2))
ax.set_xlim([2005,2025])

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(col_yr, col_cnts, color='grey')
# Set labels and title
ax.set_xlabel('Year')
ax.set_ylabel('Number of GQ')
ax.set_title('Number of GQ of Each Year columbia')
ax.set_xticks(range(2005, 2025,2))
ax.set_xlim([2005,2024])

##########


dt_object = datetime.datetime.utcfromtimestamp(subset_KNK['artime'].iloc[0])
dt_object = datetime.datetime.utcfromtimestamp(subset_KLU['ori_stamp'].iloc[0])
date_string = dt_object.strftime('%Y-%m-%d %H:%M:%S')


print("Formatted date string:", date_string)
subset_KNK['time'].iloc[0]
