#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 23:17:15 2024

@author: sebinjohn
"""

import netCDF4 as net
import matplotlib.pyplot as plt
import pygmt
import numpy as np
from pyproj import Transformer

file_path="/Users/sebinjohn/gq_proj/data/Glacier_velocity/ITS_LIVE_velocity_120m_RGI01A_2022_v02.nc"
transformer = Transformer.from_crs("EPSG:3413", "EPSG:4326")


gl_velocity=net.Dataset(file_path, mode='r') 


print(gl_velocity)

# Access specific variables or metadata
print(gl_velocity.variables.keys())  # List all variables in the file
print(gl_velocity.dimensions.keys()) # List all dimensions in the file
velocity=gl_velocity.variables['v'][:].data


plt.figure(figsize=(10, 6))
plt.hist(velocity.flatten(), bins=50, color='skyblue', edgecolor='black')
plt.xlabel("Velocity (m/year)")
plt.ylabel("Frequency")
plt.title("Distribution of Glacier Velocity")
plt.yscale("log")  # Log scale for better visibility if there are large differences in frequencies
plt.show()


x=gl_velocity.variables['x'][:].data
y=gl_velocity.variables['y'][:].data

x_grid, y_grid = np.meshgrid(x, y)

# Flatten the meshgrid to perform transformation
x_flat = x_grid.ravel()
y_flat = y_grid.ravel()

lon, lat = transformer.transform(x_flat, y_flat)



velocity[velocity==-32767]=np.nan



proj="L-155/35/33/85/14c"
fig=pygmt.Figure()
reg="212/61/214/61.3r"
with pygmt.config(MAP_FRAME_TYPE="plain"):
    fig.basemap(region=reg, projection=proj,frame="lrtb")
fig.coast(region=reg, projection=proj,borders=["1/0.5p,black"],area_thresh='600',dcw=["US.AK","RU","CA"],shorelines="0.02p")
fig.basemap(map_scale="jBC+w10k+f")
fig.show()
