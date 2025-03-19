#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 10:41:37 2024

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


###plot functions
def arriavls_plot(times, deltas,title):
    fig, axes = plt.subplots()
    axes.scatter(times, deltas, s=0.2,c="green",zorder=2)
    axes.set_ylabel("epicentral distance (degrees)")
    xlim_start = d2n(datetime.date(2005,1,1))
    xlim_end = d2n(datetime.date(2025,1,1))
    axes.set_xlim([xlim_start, xlim_end])
    axes.set_title(title)
    # Format the x-axis to show dates nicely
    #axes.xaxis.set_major_locator(mdates.YearLocator())
    #axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    axes.set_ylim([0,2])
    # Rotate date labels for better readability
    plt.xticks(rotation=45)
    plt.show()
    
def quakes_year(years,gqs,tit,typ,*argv):
    fig, ax = plt.subplots(figsize=(10, 6),dpi=300)
    ax.bar(years,gqs,color="grey",width=0.7)
    ax.set_title(tit)
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Quakes')
    ax.grid(axis='y')
    if not argv:
        ax.set_xticks(range(2005, 2024,2)) 
        ax.set_xlim([2005,2025])
    else:
        lim=argv[0]
        ax.set_xticks(range(lim[0], lim[1],2)) 
        ax.set_xlim(lim)
    if typ==1:
        fig.savefig("/Users/sebinjohn/gq_proj/Results/columbia_glacier/gq_per_yr.png")
    else:
        fig.savefig("/Users/sebinjohn/gq_proj/Results/columbia_glacier/eq_per_yr.png")
        

def gq_vs_eq(years,gqs,eq_yrs,eq,gl):
    fig, ax = plt.subplots(figsize=(10, 6),dpi=300)
    ax.bar(years,gqs,color="grey",width=0.7)
    ax2=ax.twinx()
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Quakes')
    ax.grid(axis='y')
    ax.set_title("Numbe of glacial and earth quakes in {0} glacier".format(gl))
    ax.set_xticks(range(2005, 2024,2)) 
    ax.set_xlim([2005,2025])
    ax2.plot(eq_yrs,eq,color='red',label=("number of earthquakes"),marker="*")
    ax2.legend()
    ax2.set_ylim([0,800])
    ax.set_ylim([0,800])
    fig.savefig("/Users/sebinjohn/gq_proj/Results/columbia_glacier/gq_vs_eq.png")



########total 

gq_dropped= gq_catalog.drop_duplicates(subset='evid', keep='first')

gq_dropped['time'] = pd.to_datetime(gq_dropped['time'], unit='s')
gq_dropped['year'] = gq_dropped['time'].dt.year

gq_per_year = gq_dropped.groupby('year').size()
quakes_year(gq_per_year.index,gq_per_year.values,"total Number of gq per year ",[1990,2024])

###map

import pygmt

proj="L-155/35/33/85/10c"
fig=pygmt.Figure()
reg="210/59/215/62r"
with pygmt.config(MAP_FRAME_TYPE="plain"):
    fig.basemap(region=reg, projection=proj,frame="lrtb")
fig.plot(x=gq_lon.values,y=gq_lat.values,style="c0.02c", fill="red", pen="black")
fig.coast(region=reg, projection=proj,borders=["1/0.5p,black"],area_thresh='600',dcw=["US.AK","RU","CA"],shorelines="0.02p")
fig.show()

##columbia
columbia_gq=pd.read_csv("/Users/sebinjohn/gq_proj/data/catalogs/columbia_gq_1988-2024.csv")
columbia_eq=pd.read_csv("/Users/sebinjohn/gq_proj/data/catalogs/columbia_eq_1988-2024.csv")

columbia_gq_dropped= columbia_gq.drop_duplicates(subset='evid', keep='first')
columbia_gq_dropped['time'] = pd.to_datetime(columbia_gq_dropped['time'])
columbia_gq_dropped['year'] = columbia_gq_dropped['time'].dt.year

gq_per_year = columbia_gq_dropped.groupby('year').size()
quakes_year(gq_per_year.index,gq_per_year.values,"Number of glacial quakes per year in Columbia glacier",typ=1)


columbia_eq_dropped= columbia_eq.drop_duplicates(subset='evid', keep='first')
columbia_eq_dropped['time'] = pd.to_datetime(columbia_eq_dropped['time'])
columbia_eq_dropped['year'] = columbia_eq_dropped['time'].dt.year

eq_per_year = columbia_eq_dropped.groupby('year').size()
quakes_year(eq_per_year.index,eq_per_year.values,"Number of earthquakes per year in Columbia glacier",typ=2)


columbia_gq['time']=pd.to_datetime(columbia_gq['time'])
columbia_gq_ml_sub=columbia_gq[(columbia_gq['ml'] > 1) & (columbia_gq['ml'] < 1.5)]
delt_gq_ml_sub_colu=columbia_gq_ml_sub['delta']
times_gq_ml_sub_colu=columbia_gq_ml_sub['time']

arriavls_plot(times_gq_ml_sub_colu, delt_gq_ml_sub_colu,"gq_arrivals columbia")

columbia_eq['time']=pd.to_datetime(columbia_eq['time'])
columbia_eq_ml_sub=columbia_eq[(columbia_eq['ml'] > 1) & (columbia_eq['ml'] < 1.5)]
delt_eq_ml_sub_colu=columbia_eq_ml_sub['delta']
times_eq_ml_sub_colu=columbia_eq_ml_sub['time']

arriavls_plot(times_eq_ml_sub_colu, delt_eq_ml_sub_colu,"eq_arrivals columbia")

gq_vs_eq(gq_per_year.index,gq_per_year.values,eq_per_year.index,eq_per_year.values,"Columbia")





##########hubval


hubval_gq=pd.read_csv("/Users/sebinjohn/gq_proj/data/catalogs/hubval_gq_1988-2024.csv")
hubval_eq=pd.read_csv("/Users/sebinjohn/gq_proj/data/catalogs/hubval_eq_1988-2024.csv")


hubval_gq_dropped= hubval_gq.drop_duplicates(subset='evid', keep='first')
hubval_gq_dropped['time'] = pd.to_datetime(hubval_gq_dropped['time'])
hubval_gq_dropped['year'] = hubval_gq_dropped['time'].dt.year

gq_per_year = hubval_gq_dropped.groupby('year').size()
quakes_year(gq_per_year.index,gq_per_year.values,"Number of glacial quakes per year hubbard&valerie glacier",typ=1)

hubval_eq_dropped= hubval_eq.drop_duplicates(subset='evid', keep='first')
hubval_eq_dropped['time'] = pd.to_datetime(hubval_eq_dropped['time'])
hubval_eq_dropped['year'] = hubval_eq_dropped['time'].dt.year

eq_per_year = hubval_eq_dropped.groupby('year').size()
quakes_year(eq_per_year.index,eq_per_year.values,"Number of earth quakes per year hubbard&valerie",typ=2)


hubval_gq['time']=pd.to_datetime(hubval_gq['time'])
hubval_gq_ml_sub=hubval_gq[(hubval_gq['ml'] > 1) & (hubval_gq['ml'] < 1.5)]
delt_gq_ml_sub_colu=hubval_gq_ml_sub['delta']
times_gq_ml_sub_colu=hubval_gq_ml_sub['time']

arriavls_plot(times_gq_ml_sub_colu, delt_gq_ml_sub_colu,"gq_arrivals hubbard&valerie")

hubval_eq['time']=pd.to_datetime(hubval_eq['time'])
hubval_eq_ml_sub=hubval_eq[(hubval_eq['ml'] > 1) & (hubval_eq['ml'] < 1.5)]
delt_eq_ml_sub_colu=hubval_eq_ml_sub['delta']
times_eq_ml_sub_colu=hubval_eq_ml_sub['time']

arriavls_plot(times_eq_ml_sub_colu, delt_eq_ml_sub_colu,"eq_arrivals hubbard&valerie")

gq_vs_eq(gq_per_year.index,gq_per_year.values,eq_per_year.index,eq_per_year.values,"Hubbard & Valerie")

#####

la_gq=pd.read_csv("/Users/sebinjohn/gq_proj/data/catalogs/la_gq_1988-2024.csv")
la_eq=pd.read_csv("/Users/sebinjohn/gq_proj/data/catalogs/la_eq_1988-2024.csv")


la_gq_dropped= la_gq.drop_duplicates(subset='evid', keep='first')
la_gq_dropped['time'] = pd.to_datetime(la_gq_dropped['time'])
la_gq_dropped['year'] = la_gq_dropped['time'].dt.year

gq_per_year = la_gq_dropped.groupby('year').size()
quakes_year(gq_per_year.index,gq_per_year.values,"Number of gq per year la",1)

la_eq_dropped= la_eq.drop_duplicates(subset='evid', keep='first')
la_eq_dropped['time'] = pd.to_datetime(la_eq_dropped['time'])
la_eq_dropped['year'] = la_eq_dropped['time'].dt.year

eq_per_year = la_eq_dropped.groupby('year').size()
quakes_year(eq_per_year.index,eq_per_year.values,"Number of eq per year la")


la_gq['time']=pd.to_datetime(la_gq['time'])
la_gq_ml_sub=la_gq[(la_gq['ml'] > 1.5) & (la_gq['ml'] < 2)]
delt_gq_ml_sub_colu=la_gq_ml_sub['delta']
times_gq_ml_sub_colu=la_gq_ml_sub['time']

arriavls_plot(times_gq_ml_sub_colu, delt_gq_ml_sub_colu,"gq_arrivals la")

la_eq['time']=pd.to_datetime(la_eq['time'])
la_eq_ml_sub=la_eq[(la_eq['ml'] > 1.5) & (la_eq['ml'] < 2)]
delt_eq_ml_sub_colu=la_eq_ml_sub['delta']
times_eq_ml_sub_colu=la_eq_ml_sub['time']

arriavls_plot(times_eq_ml_sub_colu, delt_eq_ml_sub_colu,"eq_arrivals la")


##Yahtse

ya_gq=pd.read_csv("/Users/sebinjohn/gq_proj/data/catalogs/ya_gq_1988-2024.csv")
ya_eq=pd.read_csv("/Users/sebinjohn/gq_proj/data/catalogs/ya_eq_1988-2024.csv")



ya_gq_dropped= ya_gq.drop_duplicates(subset='evid', keep='first')
ya_gq_dropped['time'] = pd.to_datetime(ya_gq_dropped['time'])
ya_gq_dropped['year'] = ya_gq_dropped['time'].dt.year

gq_per_year = ya_gq_dropped.groupby('year').size()
quakes_year(gq_per_year.index,gq_per_year.values,"Number of gq per year Yahtse",1)

ya_eq_dropped= ya_eq.drop_duplicates(subset='evid', keep='first')
ya_eq_dropped['time'] = pd.to_datetime(ya_eq_dropped['time'])
ya_eq_dropped['year'] = ya_eq_dropped['time'].dt.year

eq_per_year = ya_eq_dropped.groupby('year').size()
quakes_year(eq_per_year.index,eq_per_year.values,"Number of eq per year Yahtse",2)


ya_gq['time']=pd.to_datetime(ya_gq['time'])
ya_gq_ml_sub=ya_gq[(ya_gq['ml'] > 1) & (ya_gq['ml'] < 1.5)]
delt_gq_ml_sub_colu=ya_gq_ml_sub['delta']
fustimes_gq_ml_sub_colu=ya_gq_ml_sub['time']

arriavls_plot(times_gq_ml_sub_colu, delt_gq_ml_sub_colu,"gq_arrivals Yahtse")

ya_eq['time']=pd.to_datetime(ya_eq['time'])
ya_eq_ml_sub=ya_eq[(ya_eq['ml'] > 1) & (ya_eq['ml'] < 1.5)]
delt_eq_ml_sub_colu=ya_eq_ml_sub['delta']
times_eq_ml_sub_colu=ya_eq_ml_sub['time']

arriavls_plot(times_eq_ml_sub_colu, delt_eq_ml_sub_colu,"eq_arrivals Yahtse")

gq_vs_eq(gq_per_year.index,gq_per_year.values,eq_per_year.index,eq_per_year.values,"Yahtse")

