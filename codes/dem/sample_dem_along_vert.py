#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 23:15:48 2025

@author: sebinjohn
"""

import rasterio
import pandas as pd
import numpy as np
from rasterio.transform import xy
from pyproj import Transformer
from scipy.interpolate import griddata 
import matplotlib.pyplot as plt
import glob

# Input files
csv_file = "/Users/sebinjohn/gq_proj/data/centerline/bath_lines/vertices_bathlines.csv"  # CSV with 'x' and 'y' columns
df = pd.read_csv(csv_file)
x_samp=df['x']
y_samp=df['y']
ide=df['id']
sample_points = np.vstack((x_samp, y_samp)).T
    
dem_files = glob.glob("/Users/sebinjohn/gq_proj/data/DEMs/*.tiff") # DEM raster file

for dem_file in dem_files:
    with rasterio.open(dem_file) as src1:
        dem_data = src1.read(1)
        dem_nodata = src1.nodata
        dem_transform = src1.transform
        dem_crs = src1.crs
        dem_shape = src1.shape
        dem_prof = src1.profile
    
    rows, cols = dem_shape
    row_indices, col_indices = np.meshgrid(np.arange(rows), np.arange(cols), indexing="ij")
    n_x, n_y = xy(dem_transform, row_indices, col_indices)
    n_x,n_y=np.array(n_x),np.array(n_y)
    transformer = Transformer.from_crs("EPSG:3413","EPSG:32606", always_xy=True)
    
    utm_x,utm_y=transformer.transform(n_x, n_y)
    
    
    valid_mask = dem_data != dem_nodata  # Mask valid points
    points = np.vstack((utm_x[valid_mask], utm_y[valid_mask])).T  # Grid points
    values = dem_data[valid_mask] 
    
    
    elevation_values = griddata(points, values, sample_points, method="nearest")
    
    
    df1 = pd.DataFrame({
        'id': ide,
        'x': x_samp,  # Easting values (transformed)
        'y': y_samp,  # Northing values (transformed)
        'elevation': elevation_values  # Corresponding elevation values
    })
    name=dem_file.split("/")[-1].split(".")[0]
    csv_output_file = "/Users/sebinjohn/gq_proj/data/centerline/bath_lines/sampled_dems/{}.csv".format(name)
    df1.to_csv(csv_output_file, index=False)

#####
dem_pl=dem_data.copy()
dem_pl[dem_pl==dem_nodata]=np.nan

fig, ax = plt.subplots(figsize=(10, 8))

# Plot the reprojected DEM
dem_img = ax.scatter(utm_x,utm_y,c=dem_pl, cmap="turbo",s=0.9,marker='o', edgecolor='none',vmin=0,vmax=400)

# Overlay the scatter plot for the sampled points with interpolated elevation values
im = ax.scatter(x_samp, y_samp, c=elevation_values, cmap="turbo", s=0.5, marker='o', edgecolor='none',vmin=0,vmax=400)

# Add color bar for the scatter plot (interpolated elevation values)
fig.colorbar(im, ax=ax, label="Elevation (m)")

# Add color bar for the DEM (you can adjust limits if necessary)
fig.colorbar(dem_img, ax=ax, label="DEM Elevation (m)")

# Labels and title
ax.set_title("Reprojected DEM and Sampled Points with Interpolated Elevations")
ax.set_xlabel("Easting (m)")
ax.set_ylabel("Northing (m)")

plt.show()