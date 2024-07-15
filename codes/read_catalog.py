#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 20:47:04 2024

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


os.chdir("/Users/sebinjohn/gq_proj")

catalog=pd.read_csv("/Users/sebinjohn/gq_proj/data/catalog_1988-2024.csv")


gq_catalog = catalog[catalog['etype'] == 'G']
gq_lon=gq_catalog['lon']
gq_lat=gq_catalog['lat']

gq_catalog.to_csv("/Users/sebinjohn/gq_proj/data/gq_catalog_1988-2024.csv")

#############
gq_catalog=pd.read_csv("/Users/sebinjohn/gq_proj/data/gq_catalog_1988-2024.csv")
gq_lon=gq_catalog['lon']
gq_lat=gq_catalog['lat']

lat1=61.156
lon1=-147.038

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


######
columbia_boole=[]
for i in tqdm(range(len(gq_lon))):
    dis=within_radius(lat1, lon1, gq_lat.iloc[i], gq_lon.iloc[i])
    if dis<15:
        columbia_boole.append(True)
    else:
        columbia_boole.append(False)
        
columbia_gq=gq_catalog[columbia_boole]
columbia_gq['time'] = pd.to_datetime(columbia_gq['time'], unit='s')



columbia_gq.to_csv("/Users/sebinjohn/gq_proj/data/columbia_gq_1988-2024.csv")
##############columbia_eq#####


eq_catalog = catalog[catalog['etype'] == '-']
eq_lon=eq_catalog['lon']
eq_lat=eq_catalog['lat']

columbia_boole=[]
for i in tqdm(range(len(eq_lon))):
    dis=within_radius(lat1, lon1, eq_lat.iloc[i], eq_lon.iloc[i])
    if dis<15:
        columbia_boole.append(True)
    else:
        columbia_boole.append(False)
        
columbia_eq=eq_catalog[columbia_boole]

columbia_eq['time'] = pd.to_datetime(columbia_eq['time'], unit='s')

columbia_eq.to_csv("/Users/sebinjohn/gq_proj/data/columbia_eq_1988-2024.csv")
##############

hubval_lat1=59.994
hubval_lon1=-139.511
  
hubval_boole=[]
for i in tqdm(range(len(gq_lon))):
    dis=within_radius(hubval_lat1, hubval_lon1, gq_lat.iloc[i], gq_lon.iloc[i])
    if dis<15:
        hubval_boole.append(True)
    else:
        hubval_boole.append(False)

hubval_gq=gq_catalog[hubval_boole]
hubval_gq['time'] = pd.to_datetime(hubval_gq['time'], unit='s')

hubval_gq.to_csv("/Users/sebinjohn/gq_proj/data/hubval_gq_1988-2024.csv")

##################

eq_catalog = catalog[catalog['etype'] == '-']
eq_lon=eq_catalog['lon']
eq_lat=eq_catalog['lat']

hubval_boole=[]
for i in tqdm(range(len(eq_lon))):
    dis=within_radius(hubval_lat1, hubval_lon1, eq_lat.iloc[i], eq_lon.iloc[i])
    if dis<15:
        hubval_boole.append(True)
    else:
        hubval_boole.append(False)
        
hubval_eq=eq_catalog[hubval_boole]

hubval_eq['time'] = pd.to_datetime(hubval_eq['time'], unit='s')

hubval_eq.to_csv("/Users/sebinjohn/gq_proj/data/hubval_eq_1988-2024.csv")

##############

la_lat1=58.462
la_lon1=-137.292

la_boole=[]
for i in tqdm(range(len(gq_lon))):
    dis=within_radius(la_lat1, la_lon1, gq_lat.iloc[i], gq_lon.iloc[i])
    if dis<15:
        la_boole.append(True)
    else:
        la_boole.append(False)

la_gq=gq_catalog[la_boole]
la_gq['time'] = pd.to_datetime(la_gq['time'], unit='s')

la_gq.to_csv("/Users/sebinjohn/gq_proj/data/la_gq_1988-2024.csv")

######################

la_boole=[]
for i in tqdm(range(len(eq_lon))):
    dis=within_radius(la_lat1, la_lon1, eq_lat.iloc[i], eq_lon.iloc[i])
    if dis<15:
        la_boole.append(True)
    else:
        la_boole.append(False)
        
la_eq=eq_catalog[la_boole]

la_eq['time'] = pd.to_datetime(la_eq['time'], unit='s')

la_eq.to_csv("/Users/sebinjohn/gq_proj/data/la_eq_1988-2024.csv")

##yahtse
ya_lat1=60.15
ya_lon1=-141.389

ya_boole=[]
for i in tqdm(range(len(gq_lon))):
    dis=within_radius(ya_lat1, ya_lon1, gq_lat.iloc[i], gq_lon.iloc[i])
    if dis<15:
        ya_boole.append(True)
    else:
        ya_boole.append(False)

ya_gq=gq_catalog[ya_boole]
ya_gq['time'] = pd.to_datetime(ya_gq['time'], unit='s')

ya_gq.to_csv("/Users/sebinjohn/gq_proj/data/ya_gq_1988-2024.csv")

###ya eq

ya_boole=[]
for i in tqdm(range(len(eq_lon))):
    dis=within_radius(ya_lat1, ya_lon1, eq_lat.iloc[i], eq_lon.iloc[i])
    if dis<15:
        ya_boole.append(True)
    else:
        ya_boole.append(False)
        
ya_eq=eq_catalog[ya_boole]

ya_eq['time'] = pd.to_datetime(ya_eq['time'], unit='s')

ya_eq.to_csv("/Users/sebinjohn/gq_proj/data/ya_eq_1988-2024.csv")


######map
import pygmt

proj="L-155/35/33/85/10c"
fig=pygmt.Figure()
reg="180/50/230/65r"
with pygmt.config(MAP_FRAME_TYPE="plain"):
    fig.basemap(region=reg, projection=proj,frame="lrtb")
fig.plot(x=gq_lon.values,y=gq_lat.values,style="c0.02c", color="red", pen="black")
fig.coast(region=reg, projection=proj,borders=["1/0.5p,black"],area_thresh='600',dcw=["US.AK","RU","CA"],shorelines="0.02p")
fig.show()

###
gq_dropped= gq_catalog.drop_duplicates(subset='evid', keep='first')

gq_dropped['time'] = pd.to_datetime(gq_dropped['time'], unit='s')
gq_dropped['year'] = gq_dropped['time'].dt.year







######misc

columbia_gq=pd.read_csv('/Users/sebinjohn/gq_proj/data/columbia_gq_1988-2024.csv')
columbia_gq['time'] = pd.to_datetime(columbia_gq['time'], unit='s')

columbia_gq_dropped= columbia_gq.drop_duplicates(subset='evid', keep='first')


columbia_gq_dropped['time'] = pd.to_datetime(columbia_gq_dropped['time'], unit='s')
columbia_gq_dropped['year'] = columbia_gq_dropped['time'].dt.year

quakes_per_year = columbia_gq_dropped.groupby('year').size()

event_subset=columbia_gq_dropped[(columbia_gq_dropped['ml'] > 1) & (columbia_gq_dropped['ml'] < 1.5)]

nass=event_subset['nass']
time=event_subset['time'] 
event_subset['year']=time.dt.year
mean_nass=event_subset.groupby('year')['nass'].mean().reset_index()


fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(quakes_per_year.index, quakes_per_year.values,color="grey",width=0.7)
ax.set_title('Number of Glacier Quakes Per Year')
ax.set_xlabel('Year')
ax.set_ylabel('Number of Quakes')
ax.grid(axis='y')
ax2=ax.twinx()
ax.set_xticks(range(2005, 2024,2)) 
ax.set_xlim([2005,2025])
ax2.plot(mean_nass['year'],mean_nass['nass'],marker="*",c="red")
ax2.set_ylabel('Mean number of assosciations (1<ml<1.5)')

# Drop duplicates to keep only unique combinations of event_id and sta
unique_event_sta = columbia_gq.drop_duplicates(subset=['evid', 'sta'])

value_counts = unique_event_sta['sta'].value_counts()
print(f'Occurrences of each element in "sta" column:\n{value_counts}')

top= value_counts.head(30)

# Plotting the bar graph
plt.figure()
top.plot(kind='bar')
plt.xlabel('Elements')
plt.ylabel('Count')
plt.title('Top 30 Elements in "sta" Column')
plt.show()




event_ids_with_scm = columbia_gq[columbia_gq['sta'] == 'SCM']['evid'].unique()
scm_events = columbia_gq[columbia_gq['evid'].isin(event_ids_with_scm)]

scm_events_dropped=scm_events.drop_duplicates(subset='evid', keep='first')
scm_events_dropped['time'] = pd.to_datetime(scm_events_dropped['time'], unit='s')
scm_events_dropped['year'] = scm_events_dropped['time'].dt.year
quakes_per_year_scm = scm_events_dropped.groupby('year').size()

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(quakes_per_year_scm.index, quakes_per_year_scm.values,color="grey",width=0.7)
ax.set_title('Number of Glacier Quakes Per Year recorded in SCM')
ax.set_xlabel('Year')
ax.set_ylabel('Number of Quakes')
ax.grid(axis='y')
#ax2=ax.twinx()
ax.set_xticks(range(2005, 2024,2)) 
ax.set_xlim([2005,2025])
#ax2.plot(mean_nass['year'],mean_nass['nass'],marker="*",c="red")
#ax2.set_ylabel('Mean number of assosciations (1<ml<1.5)')

columbia_gq['time'] = pd.to_datetime(columbia_gq['time'], unit='s')
columbia_gq['year'] = columbia_gq['time'].dt.year

p_occurrences = columbia_gq[columbia_gq['phases'] == 'P']
grouped_p= p_occurrences.groupby('year')['evid'].nunique()
count_p = p_occurrences.groupby('year').size()
result_p = count_p / grouped_p

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(result_p.index, result_p.values,color="grey",width=0.7)
ax.set_title('Average Number of Occurrences of Phase P per Unique Evid for Each Year')
ax.set_xlabel('Year')
ax.set_ylabel('average')
ax.grid(axis='y')
#ax2=ax.twinx()
ax.set_xticks(range(2005, 2024,2)) 
ax.set_xlim([2005,2025])


s_occurrences = columbia_gq[columbia_gq['phases'] == 'S']
grouped = s_occurrences.groupby('year')['evid'].nunique()
count_s = s_occurrences.groupby('year').size()
result_s = count_s / grouped

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(result_s.index, result_s.values,color="grey",width=0.7)
ax.set_title('Average Number of Occurrences of Phase S per Unique Evid for Each Year')
ax.set_xlabel('Year')
ax.set_ylabel('average')
ax.grid(axis='y')
#ax2=ax.twinx()
ax.set_xticks(range(2005, 2024,2)) 
ax.set_xlim([2005,2025])

columbia_gq_high = columbia_gq_dropped[columbia_gq['ml'] > 1.5]
# Step 2: Group the filtered DataFrame by 'year' and count the number of events in each group
events_above_high = columbia_gq_high.groupby('year').size()


fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(events_above_high.index, events_above_high.values,color="grey",width=0.7)
ax.set_title('Number of Glacier Quakes Per Year above 1.5 ml')
ax.set_xlabel('Year')
ax.set_ylabel('Number of Quakes')
ax.grid(axis='y')
#ax2=ax.twinx()
ax.set_xticks(range(2005, 2024,2)) 
ax.set_xlim([2005,2025])

nass=columbia_gq_dropped['nass']

plt.figure(figsize=(10, 6))
plt.hist(nass, bins=40, color='skyblue', edgecolor='black')  # Adjust the number of bins as needed
plt.xlabel('Number of association')
plt.ylabel('Number of gquakes')
plt.title('Distribution of association')

plt.grid(True)

# Calculate bin centers
bin_centers = 0.5 * (np.histogram(nass, bins=40)[1][1:] + np.histogram(nass, bins=40)[1][:-1])

# Plot sticks at bin centers
#plt.vlines(bin_centers, ymin=0, ymax=plt.hist(nass, bins=40)[0], color='red', linewidth=2)

# Set xticks at bin centers
#plt.xticks(bin_centers)
plt.xlim([0, 50])
plt.tight_layout()
plt.show()



yearlyzz=columbia_gq_dropped[columbia_gq_dropped['nass']>15].groupby('year').size()
plt.figure()
plt.plot(yearlyzz.index,yearlyzz.values,marker="*")
plt.xlim([2005,2025])

####


# Group by 'sta' and get the first occurrence in each group
min_times = columbia_gq.groupby('sta')['time'].min().reset_index()
stas=min_times['sta']
min_deltas = columbia_gq.groupby('sta')['delta'].min().reset_index()

min_deltas=min_deltas.sort_values(by='delta')

filt_deltas=min_deltas[min_deltas['delta']<0.35]


plt.figure(figsize=(20, 6))
plt.bar(filt_deltas['sta'], filt_deltas['delta'], color='blue')
plt.xlabel('STA')
plt.ylabel('Delta')
plt.title('Delta values for different STA')
plt.xticks(rotation=45) # Rotate the x labels for better readability
plt.show()

#####
from matplotlib.dates import date2num as d2n

event_subset1=columbia_gq[(columbia_gq['ml'] > 1) & (columbia_gq['ml'] < 1.5)]

deltas=event_subset1['delta']
#deltas_km=deltas*111
times=event_subset1['time']
times =d2n(times)



fig, axes = plt.subplots()
axes.scatter(times, deltas, s=0.2,c="green",zorder=2)
axes.set_ylabel("epicentral distance (degrees)")
xlim_start = d2n(datetime.date(2005,1,1))
xlim_end = d2n(datetime.date(2025,1,1))
# for i in range(len(stas)):
#     smi=mdates.date2num(min_times['time'][i])
#     smin=(smi-xlim_start)/(xlim_end-xlim_start)
#     axes.axhline(min_deltas['delta'][i],xmin=smin,ls="--",zorder=1,alpha=0.1)
# # Define the x-axis limits as datetime objects
# Set the x-axis limits
axes.set_xlim([xlim_start, xlim_end])
# Format the x-axis to show dates nicely
axes.xaxis.set_major_locator(mdates.YearLocator())
axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
axes.set_ylim([0,2])
# Rotate date labels for better readability
plt.xticks(rotation=45)

plt.show()



event_subset2=columbia_eq[(columbia_eq['ml'] > 1) & (columbia_eq['ml'] < 1.5)]

deltas2=event_subset2['delta']
#deltas_km=deltas*111
times2=event_subset2['time']
times2 =d2n(times2)

fig, axes = plt.subplots()
axes.scatter(times2, deltas2, s=0.2,c="green",zorder=2)
xlim_start = d2n(datetime.date(2005,1,1))
xlim_end = d2n(datetime.date(2025,1,1))
axes.set_ylabel("epicentral distance (degrees)")
# for i in range(len(stas)):
#     smi=mdates.date2num(min_times['time'][i])
#     smin=(smi-xlim_start)/(xlim_end-xlim_start)
#     axes.axhline(min_deltas['delta'][i],xmin=smin,ls="--",zorder=1,alpha=0.1)
# Define the x-axis limits as datetime objects
# Set the x-axis limits
axes.set_xlim([xlim_start, xlim_end])
# Format the x-axis to show dates nicely
axes.xaxis.set_major_locator(mdates.YearLocator())
axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
axes.set_ylim([0,2])
# Rotate date labels for better readability
plt.xticks(rotation=45)

plt.show()



fig, axes = plt.subplots()
axes.scatter(times, deltas, s=0.2,c="green",zorder=2)
xlim_start = d2n(datetime.date(2005,1,1))
xlim_end = d2n(datetime.date(2025,1,1))
# for i in range(len(stas)):
#     smi=mdates.date2num(min_times['time'][i])
#     smin=(smi-xlim_start)/(xlim_end-xlim_start)
#     axes.axhline(min_deltas['delta'][i],xmin=smin,ls="--",zorder=1,alpha=0.1)
# # Define the x-axis limits as datetime objects
# Set the x-axis limits
axes.set_xlim([xlim_start, xlim_end])
# Format the x-axis to show dates nicely
axes.xaxis.set_major_locator(mdates.YearLocator())
axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
axes.set_ylim([0,0.35])
# Rotate date labels for better readability
plt.xticks(rotation=45)

plt.show()



filt_gq_with_delta_less=event_subset1[event_subset1['delta']<0.35]

filt_gq_with_delta_less['sta'].nunique()

deltas_fgq_del_l=filt_gq_with_delta_less['delta']
#deltas_km=deltas*111
times_fgq_del_l=filt_gq_with_delta_less['time']
times_fgq_del_l =d2n(times_fgq_del_l)

unique_stations = filt_gq_with_delta_less['sta'].unique()
colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_stations)))

fig, axes = plt.subplots()
for station, color in zip(unique_stations, colors):
    station_data = filt_gq_with_delta_less[filt_gq_with_delta_less['sta'] == station]
    axes.scatter(d2n(station_data['time']), station_data['delta'], s=2, c=[color], label=station, zorder=2)

# Define the x-axis limits as datetime objects
xlim_start = d2n(datetime.date(2005, 1, 1))
xlim_end = d2n(datetime.date(2025, 1, 1))

# Set the x-axis limits
axes.set_xlim([xlim_start, xlim_end])
# Format the x-axis to show dates nicely
axes.xaxis.set_major_locator(mdates.YearLocator())
axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
axes.set_ylim([0, 0.35])
# Rotate date labels for better readability
plt.xticks(rotation=45)

# Add legend
axes.legend()

# Show the plot
plt.show()

####

mag=columbia_gq['ml']
times=columbia_gq['time']
times = pd.to_datetime(times)

fig, axes = plt.subplots()
axes.scatter(times, mag, s=0.2,c="red")

# Define the x-axis limits as datetime objects
xlim_start = pd.to_datetime('2009-01-01')
xlim_end = pd.to_datetime('2025-01-01')
# Set the x-axis limits
axes.set_xlim([xlim_start, xlim_end])
# Format the x-axis to show dates nicely
axes.xaxis.set_major_locator(mdates.YearLocator())
axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
axes.set_ylim([0.5,2.5])
# Rotate date labels for better readability
plt.xticks(rotation=45)

plt.show()

####

