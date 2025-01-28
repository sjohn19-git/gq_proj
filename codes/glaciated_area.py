#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 21:48:44 2024

@author: sebinjohn
"""

import geopandas as gpd
from shapely.geometry import Polygon
import os
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

polygon_gdf = gpd.read_file("/Users/sebinjohn/gq_proj/data/glacier_termi_polygon/columb_pol.shp")


os.chdir("/Volumes/Sebins-HDD/Landsat8:9_c2l2/")
folders = [f for f in os.listdir() if os.path.isdir(f) and not f.startswith('.')]
paths=[]
for folder in tqdm(folders):
    paths.append(os.path.join(os.getcwd(),folder))

df=pd.DataFrame(columns=['time', 'ide', 'area'])
for i in tqdm(range(len(paths))):
    path=paths[i]
    folder=folders[i]
    ide=folder.split("_")[2]
    if ide=='066017' or ide=='067017':
        print(folder)
        os.chdir(path)
        file=[f for f in os.listdir() if f.endswith('shp')]
        shapefile_gdf = gpd.read_file(file[0])
        # Calculate the intersection
        intersection = gpd.overlay(shapefile_gdf, polygon_gdf, how='intersection')
        # Calculate the total area of the intersection
        intersection['area'] = intersection.geometry.area
        total_area = intersection['area'].sum()
        print(f"Total area of the intersection: {total_area}")
        time=pd.to_datetime(folder.split("_")[3], format='%Y%m%d')
        df=pd.concat([df, pd.DataFrame({'time': [time], 'ide': [ide], 'area': [total_area]})], ignore_index=True)

df.to_csv("/Users/sebinjohn/gq_proj/data/glacier_terminus_df/col_area.csv")        

df=pd.read_csv("/Users/sebinjohn/gq_proj/data/glacier_terminus_df/col_area.csv")

df['time']=pd.to_datetime(df['time'])

df.sort_values(by='time')


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
