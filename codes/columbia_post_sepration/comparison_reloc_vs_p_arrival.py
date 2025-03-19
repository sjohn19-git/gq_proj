#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 14:17:36 2024

@author: sebinjohn
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pygmt
import geopandas as gpd


file_loc = '/Users/sebinjohn/gq_proj/data/reloc/>2005/hypoDD.reloc'
columbia_gq=pd.read_csv("/Users/sebinjohn/gq_proj/data/catalogs/columbia_gq_1988-2024.csv")

mdat = pd.read_csv(file_loc, delim_whitespace=True, header=None)

lon_re = mdat.iloc[:, 2].values
lat_re = mdat.iloc[:, 1].values
yr_re=mdat.iloc[:, 10].values
ids_reloc=mdat.iloc[:, 0].values
glce_lat=61.134
glce_lon=-147.1078


proj="L-155/35/33/85/14c"
fig=pygmt.Figure()
reg="212/61/214/61.3r"
with pygmt.config(MAP_FRAME_TYPE="plain"):
    fig.basemap(region=reg, projection=proj,frame="lrtb")
pygmt.makecpt(cmap="rainbow", series=[2008, 2025,1])
fig.plot(x=lon_re,y=lat_re,style="c0.08c",fill=yr_re,pen="1p,+cl",cmap=True)
fig.text(text="relocated location",x=213,y=61.35)
fig.coast(region=reg, projection=proj,borders=["1/0.5p,black"],area_thresh='600',dcw=["US.AK","RU","CA"],shorelines="0.02p")
fig.colorbar(frame="x1+lyear",projection=proj,position="n0.05/-0.08+w13c/0.25c+h")
fig.plot(x=[glce_lon, glce_lon], y=[60,62], pen="1p,red")
fig.basemap(map_scale="jBC+w10k+f")
fig.show()





#################p_arrival
 
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
######################################

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

time_diff=subset_KNK['artime'].values-subset_KLU['artime'].values

sd[sd>0.7]=np.nan
time_diff[sd>0.7]=np.nan


KNK_lat=61.4131
KNK_lon=-148.4585
KLU_lat=61.4924
KLU_lon=-145.9227

ce_KNK=haversine(glce_lat, glce_lon, KNK_lat, KNK_lon)
ce_KLU=haversine(glce_lat, glce_lon, KLU_lat, KLU_lon)
p_vel=3

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
 
###################### comparison

sd_KNK=subset_KNK['deltim'].apply(lambda x: float(x.strip('(),')))
sd_KLU=subset_KLU['deltim'].apply(lambda x: float(x.strip('(),')))
sd2=(sd_KNK.values)**2+(sd_KLU.values)**2
sd=np.sqrt(sd2)

time_diff_sd=time_diff[sd<0.7]
p_arr_evid= common_evid[sd<0.7]
col_p_id=p_arr_evid[time_diff_sd>ttdiff]
pos_p_id=p_arr_evid[time_diff_sd<ttdiff]

gq_p_years=np.array([pd.to_datetime(ele).year for ele in col_gq_p['time'].unique()])
col_gq_events=col_gq_p.drop_duplicates(subset='evid', keep='first')
col_gq_events['year']=gq_p_years

af_bool=[]
for ele in col_p_id:
    sub_df=col_gq_events[col_gq_events['evid']==ele]
    if sub_df['year'].iloc[0]>=2015:
        af_bool.append(True)
    else:
        af_bool.append(False)

col_p_id_afyr=col_p_id[af_bool]

af_bool=[]
for ele in pos_p_id:
    sub_df=col_gq_events[col_gq_events['evid']==ele]
    if sub_df['year'].iloc[0]>=2015:
        af_bool.append(True)
    else:
        af_bool.append(False)
        

pos_p_id_afyr=pos_p_id[af_bool]

####reloc

col_bool_re=np.array([True if ele>glce_lon else False for ele in lon_re])
yr_bool_re=np.array([True if ele>=2015 else False for ele in yr_re])

col_bool_re_fi=np.logical_and(col_bool_re,yr_bool_re)
pos_bool_re_fi=np.logical_and(~col_bool_re,yr_bool_re)

col_ids_re=ids_reloc[col_bool_re_fi]
pos_ids_re=ids_reloc[pos_bool_re_fi]

#####compre

cmon_col = np.intersect1d(col_ids_re, col_p_id_afyr)


# Find elements in b not in a
p_col_not_reloc = np.array(list(set(col_p_id_afyr) - set(col_ids_re)))

reloc_not_pcol = np.array(list(set(col_ids_re)-set(col_p_id_afyr)))



proj="L-155/35/33/85/14c"
fig=pygmt.Figure()
reg="212/61/214/61.3r"
with pygmt.config(MAP_FRAME_TYPE="plain"):
    fig.basemap(region=reg, projection=proj,frame="lrtb")
pygmt.makecpt(cmap="rainbow", series=[2015, 2025,1])
for ele in p_col_not_reloc:
    sub_set=col_gq_events[col_gq_events['evid']==ele] 
    fig.plot(x=sub_set.lon,y=sub_set.lat,style="c0.08c",fill=sub_set.year,pen="1p,+cl",cmap=True)
fig.text(text="Columbia gq in parrival method but not in relocation",x=213,y=61.3)
fig.plot(x=[glce_lon, glce_lon], y=[60,62], pen="1p,red")
fig.colorbar(frame="x1+lyear",projection=proj,position="n0.05/-0.08+w13c/0.25c+h")
fig.coast(region=reg, projection=proj,borders=["1/0.5p,black"],area_thresh='600',dcw=["US.AK","RU","CA"],shorelines="0.02p")
fig.basemap(map_scale="jBC+w10k+f")
fig.show()


proj="L-155/35/33/85/14c"
fig=pygmt.Figure()
reg="212/61/214/61.3r"
with pygmt.config(MAP_FRAME_TYPE="plain"):
    fig.basemap(region=reg, projection=proj,frame="lrtb")
pygmt.makecpt(cmap="rainbow", series=[2015, 2025,1])
for ele in cmon_col:
    sub_set=col_gq_events[col_gq_events['evid']==ele] 
    fig.plot(x=sub_set.lon,y=sub_set.lat,style="c0.08c",fill=sub_set.year,pen="1p,+cl",cmap=True)
    if sub_set.lon.values[0]<glce_lon:
        print(lon_re[ids_reloc==sub_set.evid.iloc[0]],glce_lon)
fig.text(text="Columbia gq in both method",x=213,y=61.3)
fig.plot(x=[glce_lon, glce_lon], y=[60,62], pen="1p,red")
fig.colorbar(frame="x1+lyear",projection=proj,position="n0.05/-0.08+w13c/0.25c+h")
fig.coast(region=reg, projection=proj,borders=["1/0.5p,black"],area_thresh='600',dcw=["US.AK","RU","CA"],shorelines="0.02p")
fig.basemap(map_scale="jBC+w10k+f")
fig.show()


proj="L-155/35/33/85/14c"
fig=pygmt.Figure()
reg="212/61/214/61.3r"
with pygmt.config(MAP_FRAME_TYPE="plain"):
    fig.basemap(region=reg, projection=proj,frame="lrtb")
pygmt.makecpt(cmap="rainbow", series=[2015, 2025,1])
for ele in reloc_not_pcol:
    sub_set=col_gq_events[col_gq_events['evid']==ele] 
    fig.plot(x=sub_set.lon,y=sub_set.lat,style="c0.08c",fill=sub_set.year,pen="1p,+cl",cmap=True)
fig.text(text="Columbia gq in relocation method but not in p arrival",x=213,y=61.3)
fig.plot(x=[glce_lon, glce_lon], y=[60,62], pen="1p,red")
fig.colorbar(frame="x1+lyear",projection=proj,position="n0.05/-0.08+w13c/0.25c+h")
fig.coast(region=reg, projection=proj,borders=["1/0.5p,black"],area_thresh='600',dcw=["US.AK","RU","CA"],shorelines="0.02p")
fig.basemap(map_scale="jBC+w10k+f")
fig.show()
