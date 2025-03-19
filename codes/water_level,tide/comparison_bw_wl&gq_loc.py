#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 23:24:27 2024

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

columbia_gq=pd.read_csv("/Users/sebinjohn/gq_proj/data/catalogs/columbia_gq_1988-2024.csv")
columbia_eq=pd.read_csv("/Users/sebinjohn/gq_proj/data/catalogs/columbia_eq_1988-2024.csv")

columbia_gq_dropped= columbia_gq.drop_duplicates(subset='evid', keep='first')
columbia_gq_dropped['time'] = pd.to_datetime(columbia_gq_dropped['time'])
columbia_gq_dropped['year'] = columbia_gq_dropped['time'].dt.year
columbia_gq_dropped = columbia_gq_dropped[columbia_gq_dropped['time'].dt.year >= 2005]
columbia_gq_dropped['hour'] = columbia_gq_dropped['time'].dt.hour

gq_counts = columbia_gq_dropped.resample('w',on='time').size()


wl=pd.read_csv("/Users/sebinjohn/gq_proj/data/water_level/merged_level.csv")
wl['time'] = pd.to_datetime(wl['Date Time'])

wl_avg=wl.resample('w',on='time').agg({' Water Level':'mean'})

gq_mag=columbia_gq_dropped.resample('w',on='time').agg({'ml':'mean'})


%matplotlib qt
# Create a figure and axis
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot the GQ counts on the primary y-axis
gq_counts.plot(ax=ax1, color='steelblue', linewidth=1.5, label='Number of GQs')
ax1.set_xlabel("Time")
ax1.set_ylabel("Number of GQs")
ax1.set_title("Number of GQs and Average Water Levels")
ax1.grid(axis='y', linestyle='--', alpha=0.7)
ax1.set_xlim(pd.Timestamp('2010-01-01'), pd.Timestamp('2014-12-31'))
ax1.set_ylim([-1,30])
# Create a secondary y-axis for the average water levels
ax2 = ax1.twinx()
wl_avg.plot(ax=ax2, color='orange', linewidth=1.5, label='Average Water Level')
ax2.set_ylabel("Average Water Level")
ax2.set_ylim([4,8])
# Add legends
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
ax2.set_xlim(pd.Timestamp('2010-01-01'), pd.Timestamp('2014-12-31'))
# Adjust layout
plt.tight_layout()
plt.show()


%matplotlib qt

fig, ax1 = plt.subplots(figsize=(12, 6))

# Line plot for average magnitude on the primary y-axis with * marker
ax1.plot(gq_mag.index, gq_mag.values, color='blue', label='Average Magnitude', linestyle='-', marker='*', markersize=1,lw=0.5)
ax1.set_xlabel("Time")
ax1.set_ylabel("Average Magnitude")
ax1.set_title("Average Magnitude and Average Water Levels")
ax1.grid(axis='y', linestyle='--', alpha=0.7)
ax1.set_xlim(pd.Timestamp('2010-01-01'), pd.Timestamp('2015-12-31'))
ax1.set_ylim([1, 2])  # Adjust as necessary for your data

# Create a secondary y-axis for the average water levels
ax2 = ax1.twinx()
ax2.plot(wl_avg.index, wl_avg.values, color='orange', label='Average Water Level', linewidth=1.5, marker='*', markersize=1)  # Line plot for water levels
ax2.set_ylabel("Average Water Level")
ax2.set_ylim([4, 8])  # Adjust as necessary for your data
ax2.set_xlim(pd.Timestamp('2010-01-01'), pd.Timestamp('2015-12-31'))

# Add legends
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# Adjust layout
plt.tight_layout()
plt.show()
