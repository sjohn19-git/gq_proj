#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 12:00:35 2024

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


os.chdir("/Users/sebinjohn/gq_proj")

#catalog=pd.read_csv("/Users/sebinjohn/gq_proj/data/catalog_1988-2024.csv")

gq_catalog=pd.read_csv("/Users/sebinjohn/gq_proj/data/catalogs/gq_catalog_1988-2024.csv")
gq_lon=gq_catalog['lon']
gq_lat=gq_catalog['lat']

##columbia
columbia_gq=pd.read_csv("/Users/sebinjohn/gq_proj/data/catalogs/columbia_gq_1988-2024.csv")
columbia_eq=pd.read_csv("/Users/sebinjohn/gq_proj/data/catalogs/columbia_eq_1988-2024.csv")

columbia_gq_dropped= columbia_gq.drop_duplicates(subset='evid', keep='first')
columbia_gq_dropped['time'] = pd.to_datetime(columbia_gq_dropped['time'])
columbia_gq_dropped['year'] = columbia_gq_dropped['time'].dt.year
columbia_gq_dropped = columbia_gq_dropped[columbia_gq_dropped['time'].dt.year >= 2005]

columbia_gq_dropped['month'] = columbia_gq_dropped['time'].dt.month

monthly_counts = columbia_gq_dropped.groupby('month').size()

columbia_gq_dropped['decimal_time'] = (
    columbia_gq_dropped['time'].dt.hour +
    columbia_gq_dropped['time'].dt.minute / 60 +
    columbia_gq_dropped['time'].dt.second / 3600
)

time_of_quakes=mdates.date2num(columbia_gq_dropped['time'])

fig,ax=plt.subplots(nrows=1,ncols=1,figsize=(12,6))
sc=ax.scatter(time_of_quakes,columbia_gq_dropped['decimal_time'],s=6,c=columbia_gq_dropped['ml'],cmap='viridis', )
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%B'))
cbar = plt.colorbar(sc, ax=ax)
cbar.set_label('Magnitude')  # Label for color bar
ax.set_title('Glacial quakes time of the day')
ax.set_ylabel('Time of the day (hr)')


plt.figure(figsize=(10, 6))
monthly_counts.plot(kind='bar', color='grey')
plt.title("Total Number of GQs for Each Month (2005 and Onward)")
plt.xlabel("Month")
plt.ylabel("Number of GQs")
#plt.ylim([90,240])
plt.xticks(ticks=range(12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.grid(axis='y')
plt.show()


monthly_counts_yr = columbia_gq_dropped.groupby(['year', 'month']).size().unstack(fill_value=0)

plt.figure(figsize=(12, 8))

# Plot each year's data as a separate line
for year in monthly_counts_yr.index:
    plt.plot(monthly_counts_yr.columns, monthly_counts_yr.loc[year], label=str(year), marker='o')

# Add labels, title, and legend
plt.title("Monthly GQ Counts by Year (2005 and Onward)")
plt.xlabel("Month")
plt.ylabel("Number of GQs")
plt.xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.legend(title="Year", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='y')
plt.tight_layout()
plt.ylim([-5,80])
plt.show()


# Exclude data from 2014
columbia_gq_dropped = columbia_gq_dropped[columbia_gq_dropped['time'].dt.year != 2014]

# Extract year and month for grouping
columbia_gq_dropped['year'] = columbia_gq_dropped['time'].dt.year
columbia_gq_dropped['month'] = columbia_gq_dropped['time'].dt.month

# Group by month and count occurrences
monthly_counts = columbia_gq_dropped.groupby('month').size()

# Plotting
plt.figure(figsize=(10, 6))
monthly_counts.plot(kind='bar', color='grey')
plt.title("Total Number of GQs for Each Month (2005 and Onward, Excluding 2014)")
plt.xlabel("Month")
plt.ylabel("Number of GQs")
plt.xticks(ticks=range(12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.grid(axis='y')
plt.show()
