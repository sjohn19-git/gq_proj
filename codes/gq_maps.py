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


gq=pd.read_csv("/Users/sebinjohn/gq_proj/data/catalogs/columbia_gq_1988-2024.csv")
gq_p=gq[gq['phases']=='P']
gq_times=gq_p['time']

gq_datetime=[]

for ele in gq_times:
    cleaned_str = ele[:26]
    gq_datetime.append(datetime.strptime(cleaned_str, '%Y-%m-%d %H:%M:%S.%f'))
  
    
def map_plo(gdf_transformed,lon_o,lat_o,yr):   
    fig=pygmt.Figure()
    proj="L-155/35/33/85/10c"
    reg="212/61/214/61.5r"
    bounding_box=[-148, -146, 61, 61.5]
    bbox_polygon = Polygon([
    (bounding_box[0], bounding_box[1]),
    (bounding_box[0], bounding_box[3]),
    (bounding_box[2], bounding_box[3]),
    (bounding_box[2], bounding_box[1])])
    #reg="200/60/230/65.5r"
    with pygmt.config(MAP_FRAME_TYPE="plain"):
        fig.basemap(region=reg, projection=proj,frame="lrtb")
    #fig.grdimage(grid='/Users/sebinjohn/gq_proj/data/grids/GMRTv4_2_1_20240709topo.grd')
    for c in tqdm(range(gdf_transformed.shape[0])):
        geom=gdf_transformed.geometry[c]
        if geom.within(bbox_polygon):
            if geom.geom_type == 'Polygon':
                x, y = geom.exterior.xy
                fig.plot(x=x, y=y, pen="0.5p,grey")
            elif geom.geom_type == 'MultiPolygon':
                for polygon in geom.geoms:
                    x, y = polygon.exterior.xy
                    fig.plot(x=x, y=y, pen="0.5p,grey")
    fig.plot(x=lon_o,y=lat_o,style="c0.05c", fill="black", pen="red")
    
    fig.plot(x=212.7929,y=61.15669,style="c0.08c", fill="blue", pen="blue")
    fig.plot(x=212.98213,y=61.164,style="c0.08c", fill="blue", pen="blue")
    fig.text(text=yr,x=213,y=61.4)
    fig.coast(region=reg, projection=proj,borders=["1/0.5p,black"],area_thresh='100',dcw=["US.AK","RU","CA"],shorelines="0.02p")
    fig.show()  
  
years=np.arange(2010,2021)

for yr in years:
    is_year = [dt.year == yr for dt in gq_datetime] 
    gq_p_yr=gq_p[is_year]
    events_yr = gq_p_yr.drop_duplicates(subset='evid', keep='first')
    lon_o=events_yr['lon']
    lat_o=events_yr['lat']
    shapefile_path = '/Users/sebinjohn/gq_proj/data/glacier_extent/AK_{}_overall_glacier_covered_area.shp'.format(yr)
    gdf = gpd.read_file(shapefile_path)
    target_crs = 'EPSG:4326'
    print("Original CRS:", gdf.crs)
    gdf_transformed = gdf.to_crs(target_crs)
    map_plo(gdf_transformed,lon_o,lat_o,yr)
    
    




map_plo(gdf_transformed,lon_o,lat_o)    
