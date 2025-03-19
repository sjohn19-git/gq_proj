#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 19:57:26 2024

@author: sebinjohn
"""

import os
import rasterio
import geopandas as gpd
from rasterio.mask import mask
import numpy as np
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# Load the polygon shapefile
polygon_gdf = gpd.read_file("/Users/sebinjohn/gq_proj/data/glacier_termi_polygon/columb_pol.shp")
polygon_geometry = [polygon_gdf.unary_union]  # Combine all polygons into one

# Prepare output DataFrame
df = pd.DataFrame(columns=['time', 'ide', 'area'])

os.chdir("/Volumes/Sebins-HDD/Landsat8:9_c2l2/")
folders = [f for f in os.listdir() if os.path.isdir(f) and not f.startswith('.')]
paths = [os.path.join(os.getcwd(), folder) for folder in folders]

for i in tqdm(range(len(paths))):
    path = paths[i]
    folder = folders[i]
    ide = folder.split("_")[2]
    if ide in ['066017', '067017']:
        print(folder)
        os.chdir(path)
        ndsi_file = [f for f in os.listdir() if f.endswith('.TIF') and 'NDSI' in f]
        
        if ndsi_file:
            with rasterio.open(ndsi_file[0]) as src:
                # Mask the raster with the polygon
                ndsi_data, ndsi_transform = mask(src, polygon_geometry, crop=True)
                
                # Apply the NDSI > 0.4 threshold
                ndsi_mask = ndsi_data[0] > 0.5
                
                # Calculate the area of valid pixels
                pixel_area = src.res[0] * src.res[1]  # Resolution of a pixel
                total_area = np.sum(ndsi_mask) * pixel_area
                
                print(f"Total area with NDSI > 0.4: {total_area}")
                time = pd.to_datetime(folder.split("_")[3], format='%Y%m%d')
                
                # Append results to DataFrame
                df = pd.concat([df, pd.DataFrame({'time': [time], 'ide': [ide], 'area': [total_area]})], ignore_index=True)

# Save the DataFrame
df.to_csv("/Users/sebinjohn/gq_proj/data/glacier_terminus_df/col_area_ndsi.csv")

df=pd.read_csv("/Users/sebinjohn/gq_proj/data/glacier_terminus_df/col_area_ndsi.csv")

df['time']=pd.to_datetime(df['time'])

df=df.sort_values(by='time')


# Plot time vs area
plt.figure(figsize=(10, 6))
plt.scatter(df['time'], df['area'], color='b', label='Area Over Time')

# Formatting the x-axis to show every year
ax = plt.gca()  # Get the current axis
ax.xaxis.set_major_locator(mdates.YearLocator())  # Mark every year
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # Format labels as 'YYYY'

# Additional formatting
plt.xlabel('Time', fontsize=12)
plt.ylabel('Area', fontsize=12)
plt.title('Time vs Area', fontsize=14)
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()

# Show the plot
plt.show()
