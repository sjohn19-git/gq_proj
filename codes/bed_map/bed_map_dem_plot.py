#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 00:24:24 2025

@author: sebinjohn
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import LineString
from pyproj import Transformer
import numpy as np
from scipy.spatial import cKDTree
import glob
from datetime import datetime

bathy=pd.read_csv("/Users/sebinjohn/gq_proj/data/centerline/bath_lines/sampled_bathy/bath_lines.csv")
dem=pd.read_csv("/Users/sebinjohn/gq_proj/data/centerline/bath_lines/sampled_dems/2010-09-06.csv")


termnses=glob.glob("/Users/sebinjohn/gq_proj/data/terminus_columbia/*.geojson")
dems=glob.glob("/Users/sebinjohn/gq_proj/data/centerline/bath_lines/sampled_dems/*.csv")

termnses.sort()

cpb_list = []
cpd_list = []


for termi in termnses:
    terminus=gpd.read_file(termi)
    
    date_s=termi.split('/')[-1].split('.')[0]
    date = datetime.strptime(date_s, '%Y-%m-%d').date()
    
    geometry = terminus['geometry'][0]
    coords = list(geometry.coords)
    line = LineString(coords)

    num_points = 100 
    densified_points = [line.interpolate(i / (num_points - 1), normalized=True) for i in range(num_points)]

    # Extract latitudes and longitudes of the densified points
    den_lats = [point.y for point in densified_points]
    den_lons = [point.x for point in densified_points]
    
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:32606", always_xy=True)

    # Convert latitudes and longitudes to EPSG:32606 (UTM Zone 6N)
    utm_x, utm_y = transformer.transform(den_lons, den_lats)
    utm_x, utm_y =np.array(utm_x),np.array(utm_y)
    
    bathy_points = bathy[['x', 'y']].values  
    utm_points = np.vstack((utm_x, utm_y)).T
    
    tree = cKDTree(utm_points)
    distances, indices = tree.query(bathy_points)
    
    bathy['nearest_utm_x'] = utm_x[indices]
    bathy['nearest_utm_y'] = utm_y[indices]
    bathy['distance'] = distances 
    min_indices = bathy.groupby('id')['distance'].idxmin()
    cpb = bathy.loc[min_indices]
    cpb['date'] = date
    cpb_list.append(cpb)

date_files = []
for file in dems:
    try:
        filename = file.split("/")[-1].replace(".csv", "")  # Extract the date part from the filename
        file_date = datetime.strptime(filename, "%Y-%m-%d").date()  # Convert to date
        date_files.append((file_date, file))
    except ValueError:
        continue  # Skip files that don't match the date format

for file in date_files:
    dem = pd.read_csv(file[1])
    dem_points = dem[['x', 'y']].values  
    distances, indices = tree.query(dem_points)
    dem['nearest_utm_x'] = utm_x[indices]
    dem['nearest_utm_y'] = utm_y[indices]
    dem['distance'] = distances 
    min_indices = dem.groupby('id')['distance'].idxmin()
    cpd = dem.loc[min_indices]
    cpd['date'] = file[0]
    cpd_list.append(cpd)  

#fig,ax=plt.subplots()
#ax.scatter(utm_x,utm_y)
#ax.scatter(dem['x'],dem['y'])
#ax.scatter(cpd['x'],cpd['y'])

cpb_merged = pd.concat(cpb_list, ignore_index=True)
cpd_merged = pd.concat(cpd_list, ignore_index=True)
cpd_merged = cpd_merged.sort_values(by="date", ascending=True)
cpd_merged['elevation']

fig,axes=plt.subplots(nrows=3,ncols=1,sharex=True,figsize=(8,8),dpi=300)
for i in range(1,4):
    cpb_id =cpb_merged[cpb_merged['id'] == i]
    cpd_id= cpd_merged[cpd_merged['id'] == i]
    axes[i-1].plot(cpb_id['date'],cpb_id['SAMPLE_1'],label="bathymetry",marker="*")
    axes[i-1].plot(cpd_id['date'],cpd_id['elevation'],label="dem",marker="*")
    thick=cpd_id['elevation']/0.104
    blw=-0.896*thick
    #axes[i-1].scatter(cpd_id['date'],blw,label="gl",marker="*",color="grey")
    axes[i-1].set_ylim([-400,290])
    axes[i-1].axhline(0, linestyle='--', color='grey',alpha=0.3)
    axes[i-1].grid(True, linestyle='--', color='lightgrey', alpha=0.5)
axes[i-1].legend()
axes[0].set_title("North to south profiles")
fig.savefig("/Users/sebinjohn/Downloads/dem_bath.png")

fig,axes=plt.subplots(nrows=3,ncols=1,sharex=True)
for i in range(1,4):
    cpb_id =cpb_merged[cpb_merged['id'] == i]
    cpd_id= cpd_merged[cpd_merged['id'] == i]
    axes[i-1].plot(cpb_id['date'],cpb_id['SAMPLE_1'],label="bathymetry",marker="*")
    axes[i-1].plot(cpd_id['date'],cpd_id['elevation'],label="dem",marker="*")
    thick=cpd_id['elevation']/0.104
    blw=-0.896*thick
    #axes[i-1].plot(cpd_id['date'],blw,label="gl",marker="*",color="grey")
    axes[i-1].set_ylim([-230,140])
axes[i-1].legend()




fig,ax=plt.subplots()
ax.scatter(utm_x,utm_y)
ax.scatter(cpd_merged['x'],cpd_merged['y'])
ax.scatter(cpd_id['x'],cpd_id['y'])