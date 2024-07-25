#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 12:01:29 2024

@author: sebinjohn
"""

import pygmt 
import pandas as pd
from math import radians, sin, cos, sqrt, atan2
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime
from matplotlib.dates import date2num as d2n 
import geopandas as gpd
from pyproj import CRS
from tqdm import tqdm
from pyproj import Proj, transform
from shapely.geometry import Polygon
import requests
import os

###loading loc and reloc
file_loc = '/Users/sebinjohn/gq_proj/data/reloc/>2005/hypoDD.reloc'

mdat = pd.read_csv(file_loc, delim_whitespace=True, header=None)

lon_re = mdat.iloc[:, 2].values
lat_re = mdat.iloc[:, 1].values
yr_re=mdat.iloc[:, 10].values
ids_re=mdat.iloc[:, 0].values

file_loc = '/Users/sebinjohn/gq_proj/data/reloc/>2005/hypoDD.loc'
mdat = pd.read_csv(file_loc, delim_whitespace=True, header=None)
ids_o=mdat.iloc[:, 0].values
lon_o = mdat.iloc[:, 2].values
lat_o = mdat.iloc[:, 1].values
yr_o=mdat.iloc[:, 10].values


proj="L-155/35/33/85/14c"
fig=pygmt.Figure()
reg="212/61/214/61.3r"
with pygmt.config(MAP_FRAME_TYPE="plain"):
    fig.basemap(region=reg, projection=proj,frame="lrtb")
pygmt.makecpt(cmap="rainbow", series=[2008, 2025,1])
fig.plot(x=lon_o,y=lat_o,style="c0.06c",fill=yr_o,pen="1p,+cl",cmap=True)
fig.text(text="original location",x=213,y=61.35)
fig.coast(region=reg, projection=proj,borders=["1/0.5p,black"],area_thresh='600',dcw=["US.AK","RU","CA"],shorelines="0.02p")
fig.colorbar(frame="x1+lyear",projection=proj,position="n0.05/-0.08+w13c/0.25c+h")
fig.basemap(map_scale="jBC+w10k+f")
fig.show()

proj="L-155/35/33/85/14c"
fig=pygmt.Figure()
reg="212/61/214/61.3r"
with pygmt.config(MAP_FRAME_TYPE="plain"):
    fig.basemap(region=reg, projection=proj,frame="lrtb")
pygmt.makecpt(cmap="rainbow", series=[2008, 2025,1])
fig.plot(x=lon,y=lat,style="c0.06c",fill=yr,pen="1p,+cl",cmap=True)
fig.text(text="relocated location",x=213,y=61.35)
fig.coast(region=reg, projection=proj,borders=["1/0.5p,black"],area_thresh='600',dcw=["US.AK","RU","CA"],shorelines="0.02p")
fig.colorbar(frame="x1+lyear",projection=proj,position="n0.05/-0.08+w13c/0.25c+h")
fig.basemap(map_scale="jBC+w10k+f")
fig.show()

#####################


def map_plo(lon,lat,yr,glacier_xs,glacier_ys,reloc=1):   
    glce_lat=61.134
    glce_lon=-147.1078
    fig=pygmt.Figure()
    proj="L-155/35/33/85/10c"
    reg="212/61/214/61.5r"
    with pygmt.config(MAP_FRAME_TYPE="plain"):
        fig.basemap(region=reg, projection=proj,frame="lrtb")
    for i in tqdm(range(len(glacier_xs))):
        x = glacier_xs[i]
        y = glacier_ys[i]
        fig.plot(x=x, y=y, pen="0.5p,grey")
    pygmt.makecpt(cmap="rainbow", series=[2010, 2025,1])
    fig.plot(x=lon,y=lat,style="c0.08c",fill=yr,pen="1p,+cl",cmap=True)
    fig.plot(x=[glce_lon, glce_lon], y=[60,62], pen="1p,red")
    if reloc==1:
        fig.text(text="relocated location {}".format(yr[0]),x=213,y=61.45)
    else:
        fig.text(text="original location {}".format(yr[0]),x=213,y=61.45)
    fig.coast(region=reg, projection=proj,borders=["1/0.5p,black"],area_thresh='100',dcw=["US.AK","RU","CA"],shorelines="0.02p")
    fig.colorbar(frame="x2+lyear",projection=proj,position="n0.05/-0.08+w9c/0.25c+h")
    fig.basemap(map_scale="jBC+w10k+f")
    fig.show()  
  
years=np.arange(2010,2020,2)

for yr in years:
    cl_yr_o=yr_o[yr_o==yr]
    cl_lon_o=lon_o[yr_o==yr]
    cl_lat_o=lat_o[yr_o==yr]
    cl_ids_o=ids_o[yr_o==yr]
    
    cl_yr_re=yr_re[yr_re==yr]
    cl_lon_re=lon_re[yr_re==yr]
    cl_lat_re=lat_re[yr_re==yr]
    cl_ids_re=ids_re[yr_re==yr]
    
    try:
        shapefile_path = '/Users/sebinjohn/gq_proj/data/glacier_extent/AK_{}_overall_glacier_covered_area.shp'.format(yr)
        gdf = gpd.read_file(shapefile_path)
    except Exception as e:
        print(e)
        try:
            print("trying download AK_{}_overall_glacier_covered_area.shp".format(yr))
            file_urls=["https://noaadata.apps.nsidc.org/NOAA/G10040/overall_area/AK_{}_overall_glacier_covered_area.prj".format(yr),
                      "https://noaadata.apps.nsidc.org/NOAA/G10040/overall_area/AK_{}_overall_glacier_covered_area.shp".format(yr),
                      "https://noaadata.apps.nsidc.org/NOAA/G10040/overall_area/AK_{}_overall_glacier_covered_area.shx".format(yr)]
            os.chdir("/Users/sebinjohn/gq_proj/data/glacier_extent")
            for url in file_urls:
                local_filename = os.path.basename(url)
                r = requests.get(url)
                r.raise_for_status()  
                with open(local_filename, 'wb') as f:
                    f.write(r.content)
                print(f"File successfully downloaded and saved as {local_filename}")
            gdf = gpd.read_file(shapefile_path)
        except:
            print("download failed AK_{}_overall_glacier_covered_area.shp".format(yr))
    target_crs = 'EPSG:4326'
    print("Original CRS:", gdf.crs)
    gdf_transformed = gdf.to_crs(target_crs)
    bounding_box=[-148, -146, 61, 61.5]
    bbox_polygon = Polygon([
    (bounding_box[0], bounding_box[1]),
    (bounding_box[0], bounding_box[3]),
    (bounding_box[2], bounding_box[3]),
    (bounding_box[2], bounding_box[1])])
    glacier_xs,glacier_ys=[],[]
    for c in tqdm(range(gdf_transformed.shape[0])):
        geom=gdf_transformed.geometry[c]
        if geom.within(bbox_polygon):
            if geom.geom_type == 'Polygon':
                x, y = geom.exterior.xy
                glacier_xs.append(x)
                glacier_ys.append(y)
            elif geom.geom_type == 'MultiPolygon':
                for polygon in geom.geoms:
                    x, y = polygon.exterior.xy
                    fig.plot(x=x, y=y, pen="0.5p,grey")
                    glacier_xs.append(x)
                    glacier_ys.append(y)
    map_plo(cl_lon_o,cl_lat_o,cl_yr_o,glacier_xs,glacier_ys,0)
    map_plo(cl_lon_re,cl_lat_re,cl_yr_re,glacier_xs,glacier_ys,1)
    
    
    




