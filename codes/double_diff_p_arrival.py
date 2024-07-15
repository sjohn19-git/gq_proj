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

time_diff=subset_KNK['artime'].values-subset_KLU['artime'].values

ortime=d2n(pd.to_datetime(subset_KNK['time']))

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(ortime,time_diff,s=4)
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
xlim_start = d2n(datetime.date(2005,1,1))
xlim_end = d2n(datetime.date(2025,1,1))
ax.set_xlim([xlim_start, xlim_end])
ax.set_ylim([-3,7])
ax.set_ylabel("p arrival at KNK - KLU")



##########


dt_object = datetime.datetime.utcfromtimestamp(subset_KNK['artime'].iloc[0])
dt_object = datetime.datetime.utcfromtimestamp(subset_KLU['ori_stamp'].iloc[0])
date_string = dt_object.strftime('%Y-%m-%d %H:%M:%S')


print("Formatted date string:", date_string)
subset_KNK['time'].iloc[0]
