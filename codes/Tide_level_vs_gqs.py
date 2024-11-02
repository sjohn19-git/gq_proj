#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 19:52:28 2024

@author: sebinjohn
"""

import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
import matplotlib.dates as mdates
import datetime
from matplotlib.dates import date2num as d2n
from scipy.optimize import curve_fit


columbia_gq=pd.read_csv("/Users/sebinjohn/gq_proj/data/catalogs/columbia_gq_1988-2024.csv")
columbia_eq=pd.read_csv("/Users/sebinjohn/gq_proj/data/catalogs/columbia_eq_1988-2024.csv")

columbia_gq_dropped= columbia_gq.drop_duplicates(subset='evid', keep='first')
columbia_gq_dropped['time'] = pd.to_datetime(columbia_gq_dropped['time'])
columbia_gq_dropped['year'] = columbia_gq_dropped['time'].dt.year
columbia_gq_dropped = columbia_gq_dropped[columbia_gq_dropped['time'].dt.year >= 2005]
columbia_gq_dropped['hour'] = columbia_gq_dropped['time'].dt.hour
columbia_gq_dropped['posix']=columbia_gq_dropped['time'].astype('int64')


# Load the merged data file
merged_file_path = "/Users/sebinjohn/gq_proj/data/tide_predictions/merged_tide_predictions.csv"
tide_data = pd.read_csv(merged_file_path)

# Convert date/time column to datetime object, assuming a column 'DateTime' exists
# Adjust the column name if necessary
tide_data['Date Time'] = pd.to_datetime(tide_data['Date Time'])  
tide_data['posix']=tide_data['Date Time'].astype('int64')


start_date = tide_data['Date Time'].min()
end_date = start_date + pd.Timedelta(days=1)

# Plotting with matplotlib
fig, ax = plt.subplots(figsize=(14, 7))

# Plot the tide level data
ax.plot(tide_data['Date Time'], tide_data[' Prediction'], label='Tide Level', color='b',marker="*")

# Labeling the plot
ax.set_title('Tide Level Over Time')
ax.set_xlabel('Date')
ax.set_ylabel('Tide Level (meters)')
ax.legend()
ax.set_xlim([start_date, end_date])
# Improve formatting and display plot
fig.autofmt_xdate()
plt.tight_layout()
plt.show()

closest_tide_levels = []
quake_times = []
mls=[]


for i in range(len(columbia_gq_dropped['posix'])):
    gq_time=columbia_gq_dropped['posix'].iloc[i]
    idx = (np.abs(tide_data['posix']-gq_time)).argmin()
    time_difference = np.abs(tide_data['posix'].iloc[idx] - gq_time)// 1_000_000_000
    # Check if the time difference is less than 2 hours (7200 seconds)
    if time_difference < 7200:  # 2 hours in seconds
        print(columbia_gq_dropped['time'].iloc[i],tide_data['Date Time'].iloc[idx])
        closest_tide_levels.append(tide_data[' Prediction'].iloc[idx])
        quake_times.append(columbia_gq_dropped['time'].iloc[i])
        mls.append(columbia_gq_dropped['ml'].iloc[i])
        
fig, ax = plt.subplots(figsize=(14, 7))
sc=ax.scatter(closest_tide_levels,quake_times,c=mls)
ax.set_title("tide level vs glacial quakes")
ax.set_ylabel('year')
cbar = fig.colorbar(sc, ax=ax)
cbar.set_label('ml')