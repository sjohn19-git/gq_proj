#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 16:51:58 2024

@author: sebinjohn
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pygmt
import geopandas as gpd
from shapely.geometry import Polygon


file_loc = '/Users/sebinjohn/gq_proj/data/reloc/>2005/hypoDD.reloc'

mdat = pd.read_csv(file_loc, delim_whitespace=True, header=None)

lon = mdat.iloc[:, 2].values
lat = mdat.iloc[:, 1].values
yr=mdat.iloc[:, 10].values
ids=mdat.iloc[:, 0].values

file_loc = '/Users/sebinjohn/gq_proj/data/reloc/>2005/hypoDD.loc'
mdat = pd.read_csv(file_loc, delim_whitespace=True, header=None)
ids_o=mdat.iloc[:, 0].values
lon_o = mdat.iloc[:, 2].values
lat_o = mdat.iloc[:, 1].values
yr_o=mdat.iloc[:, 10].values
#gdf = gpd.read_file("/Users/sebinjohn/gq_proj/data/Alaska_Glacier_Inventory__RGI_.kml",driver='KML')


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


def maps(lon_o,lat_o,yr_o,lon_cl,lat_cl,yr_cl,lon,lat,yr):
    glce_lat=61.134
    glce_lon=-147.1078
    
    try:
        proj="L-155/35/33/85/14c"
        fig=pygmt.Figure()
        reg="212/61/214/61.3r"
        with pygmt.config(MAP_FRAME_TYPE="plain"):
            fig.basemap(region=reg, projection=proj,frame="lrtb")
        pygmt.makecpt(cmap="rainbow", series=[2010, 2025,1])
        fig.plot(x=lon_o,y=lat_o,style="c0.08c",fill=yr_o,pen="1p,+cl",cmap=True)
        fig.text(text="original location {}".format(yr_o[0]),x=213,y=61.35)
        fig.plot(x=[glce_lon, glce_lon], y=[60,62], pen="2p,red")
        fig.coast(region=reg, projection=proj,borders=["1/0.5p,black"],area_thresh='600',dcw=["US.AK","RU","CA"],shorelines="0.02p")
        fig.colorbar(frame="x1+lyear",projection=proj,position="n0.05/-0.08+w13c/0.25c+h")
        fig.basemap(map_scale="jBC+w10k+f")
        fig.show()
        
        # proj="L-155/35/33/85/14c"
        # fig=pygmt.Figure()
        # reg="212/61/214/61.3r"
        # with pygmt.config(MAP_FRAME_TYPE="plain"):
        #     fig.basemap(region=reg, projection=proj,frame="lrtb")
        # pygmt.makecpt(cmap="rainbow", series=[2008, 2025,1])
        # #fig.plot(x=lon_o,y=lat_o,style="c0.02c",fill=yr_o,pen="1p,+cl",cmap=True)
        # fig.plot(x=lon_cl,y=lat_cl,style="c0.02c",fill=yr_cl,pen="1p,+cl",cmap=True)
        # fig.text(text="selected events",x=213,y=61.35)
        # fig.coast(region=reg, projection=proj,borders=["1/0.5p,black"],area_thresh='600',dcw=["US.AK","RU","CA"],shorelines="0.02p")
        # fig.colorbar(frame="x1+lyear",projection=proj,position="n0.05/-0.08+w13c/0.25c+h")
        # fig.show()
        
        proj="L-155/35/33/85/14c"
        fig=pygmt.Figure()
        reg="212/61/214/61.3r"
        with pygmt.config(MAP_FRAME_TYPE="plain"):
            fig.basemap(region=reg, projection=proj,frame="lrtb")
        pygmt.makecpt(cmap="rainbow", series=[2010, 2025,1])
        fig.plot(x=lon,y=lat,style="c0.08c",fill=yr,pen="1p,+cl",cmap=True)
        fig.plot(x=[glce_lon, glce_lon], y=[60,62], pen="2p,red")
        fig.text(text="relocated location {}".format(yr_o[0]),x=213,y=61.35)
        fig.coast(region=reg, projection=proj,borders=["1/0.5p,black"],area_thresh='600',dcw=["US.AK","RU","CA"],shorelines="0.02p")
        fig.colorbar(frame="x1+lyear",projection=proj,position="n0.05/-0.08+w13c/0.25c+h")
        fig.basemap(map_scale="jBC+w10k+f")
        fig.show()
    except:
        pass

un_years=np.arange(2010,2025,1)

for i in range(len(un_years)):
    cyr=un_years[i]
    print(cyr)
    bool_o=yr_o==cyr
    cyr_o=yr_o[bool_o]
    clon_o=lon_o[bool_o]
    clat_o=lat_o[bool_o]
    cids_o=ids_o[bool_o]
    boole=yr==cyr
    cids=ids[boole]
    boolec=np.isin(cids_o, cids)
    clon_cl=clon_o[boolec]
    clat_cl=clat_o[boolec]
    cyr_cl=cyr_o[boolec]
    clon=lon[boole]
    clat=lat[boole]
    cyr=yr[boole]
    maps(clon_o,clat_o,cyr_o,clon_cl,clat_cl,cyr_cl,clon,clat,cyr)    








