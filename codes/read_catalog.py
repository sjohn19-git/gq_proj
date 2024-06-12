#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 20:47:04 2024

@author: sebinjohn
"""

import pandas as pd
import os
from math import radians, sin, cos, sqrt, atan2


os.chdir("/Users/sebinjohn/gq_proj")

catalog=pd.read_csv("/Users/sebinjohn/gq_proj/Data/eq_catalog_1988-2024.csv")


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return r * c

def within_radius(lat1, lon1, lat2, lon2):
    """
    Check if the point (lat2, lon2) is within the defined radius from (lat1, lon1)
    """
    distance = haversine(lat1, lon1, lat2, lon2)
    return distance

lat1=61.156
lon1=-147.038

gq_catalog = catalog[catalog['etype'] == 'G']
gq_lon=gq_catalog['lon']
gq_lat=gq_catalog['lat']

columbia_boole=[]
for i in range(len(gq_lon)):
    dis=within_radius(lat1, lon1, gq_lat.iloc[i], gq_lon.iloc[i])
    if dis<15:
        columbia_boole.append(True)
    else:
        columbia_boole.append(False)
        
columbia_gq=gq_catalog[columbia_boole]

columbia_gq['time'] = pd.to_datetime(columbia_gq['time'], unit='s')
columbia_gq['year'] = columbia_gq['time'].dt.year
quakes_per_year = columbia_gq.groupby('year').size()


event_subset=columbia_gq[(columbia_gq['ml'] > 1) & (columbia_gq['ml'] < 1.5)]
nass=event_subset['nass']
time=event_subset['time'] 
event_subset['year']=time.dt.year
mean_nass=event_subset.groupby('year')['nass'].mean().reset_index()


import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(quakes_per_year.index, quakes_per_year.values,color="grey",width=0.7)
ax.set_title('Number of Glacier Quakes Per Year')
ax.set_xlabel('Year')
ax.set_ylabel('Number of Quakes')
ax.grid(axis='y')
ax.set_xlim([2000,2025])
ax2=ax.twinx()
#ax.set_xticks(range(2000, 2024)) 
ax2.plot(mean_nass['year'],mean_nass['nass'],marker="*",c="red")
ax2.set_ylabel('Mean number of assosciations (1<ml<1.5)')
