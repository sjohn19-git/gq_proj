#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 18:44:48 2025

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


# Adjust year for December events to group them with the following year's "Dec-May" period
columbia_gq_dropped['adjusted_year'] = columbia_gq_dropped.apply(
    lambda row: row['year'] + 1 if row['time'].month == 12 else row['year'], axis=1
)

# Define periods
def determine_period(row):
    month = row['time'].month
    if month in [12, 1, 2, 3, 4, 5]:
        return "Dec-May"
    elif month in [6, 7, 8, 9, 10, 11]:
        return "Jun-Nov"
    else:
        return None

columbia_gq_dropped['period'] = columbia_gq_dropped.apply(determine_period, axis=1)

# Group by adjusted year and period
period_counts = (
    columbia_gq_dropped.groupby(['adjusted_year', 'period'])
    .size()
    .unstack(fill_value=0)
    .reset_index()
    .rename(columns={'adjusted_year': 'year'})
)

# Plotting
fig, ax = plt.subplots(figsize=(12, 6))

for period in ['Dec-May', 'Jun-Nov']:
    if period in period_counts.columns:
        ax.plot(
            period_counts['year'],
            period_counts[period],
            marker='o',
            label=f"{period}",
        )

# Customize the plot
ax.set_title("Number of Events (Dec-May vs. Jun-Nov)")
ax.set_xlabel("Year")
ax.set_ylabel("Number of Events")
ax.legend(title="Period")
ax.grid(axis='y')
plt.tight_layout()
plt.show()