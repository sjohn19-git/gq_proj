#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 21:56:54 2025

@author: sebinjohn
"""

import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import geopandas as gpd
from scipy.spatial import cKDTree
import os

bath=pd.read_csv("/Users/sebinjohn/gq_proj/data/centerline/bath_lines/sampled_bathy/bath_lines.csv")



files=['2010-03-15','2010-09-15','2018-04-15','2017-05-31','2016-05-27','2019-06-04']
zs=[-200,-100,-185,-185,-185,-174,-185]

def plot_geo(file):
    geojson_file=os.path.join('/Users/sebinjohn/gq_proj/data/terminus_columbia/',file+".geojson")
    gdf = gpd.read_file(geojson_file)
    gdf = gdf.to_crs(epsg=32606)
    line1 = gdf.geometry.iloc[0]  # Access the first geometry (LineString)
    line1_x, line1_y = line1.xy  
    label=file
    return line1_x, line1_y


x=bath['x']
y=bath['y']
z=bath['SAMPLE_1']


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Create a 3D scatter plot
ax.plot(x, y, z, c="k")

for i in range(len(files)):
    file=files[i]
    line1_x, line1_y=plot_geo(file)
    ax.plot(line1_x, line1_y, zs=zs[i] * np.ones(len(line1_x)), linewidth=2, label=file)  # zs=[0] keeps the line on the X-Y plane

# Labels
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
ax.set_zlim([-300,0])
plt.legend()
# Show plot
plt.show()


