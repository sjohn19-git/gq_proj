#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 13:55:16 2024

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

# Extract hour of the day
columbia_gq_dropped['hour'] = columbia_gq_dropped['time'].dt.hour

hourly_counts = columbia_gq_dropped.groupby('hour').size()

# Plotting
plt.figure(figsize=(10, 6))
hourly_counts.plot(kind='bar', color='grey')
plt.title("Total Number of GQs for Each Hour of the Day (2005 and Onward)")
plt.xlabel("Hour of the Day")
plt.ylabel("Number of GQs")
plt.xticks(ticks=range(24), labels=[f"{hour}:00" for hour in range(24)])
plt.grid(axis='y')
plt.ylim([0, hourly_counts.max() + 10])  # Adjust y-axis limit for better visibility
plt.ylim([40,80])
plt.show()
