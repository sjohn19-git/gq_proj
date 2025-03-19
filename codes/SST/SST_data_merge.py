#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 00:00:53 2025

@author: sebinjohn
"""

import xarray as xr
import rasterio
from rasterio.transform import from_origin
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
import pygmt
import glob
import geopandas as gpd
import re
import pandas as pd

#loading polygon
shapefile_path = "/Users/sebinjohn/gq_proj/codes/SST/qgis_sst/polygon.shp"
gdf = gpd.read_file(shapefile_path)
print(gdf.head())
gdf.plot()

polygon_geom = gdf.geometry.iloc[0]  # Assuming a single polygon
polygon_bounds = polygon_geom.bounds  # Get bounds (minx, miny, maxx, maxy)


time_values = []
avg_sst_values = []

# Regular expression to extract date-time from filename
pattern = re.compile(r'(\d{4}-\d{2}-\d{2}T\d{4})')  


files=glob.glob("/Users/sebinjohn/gq_proj/data/SST/*.nc")
files.sort()

for file in files:
    print(file)
    match = pattern.search(file)
    timestamp = pd.to_datetime(match.group(1), format="%Y-%m-%dT%H%M")
    dataset = xr.open_dataset(file)
    # Access the specific variable (e.g., "analysed_sst")
    try:
        sst_data = dataset["analysed_sst"]
        lon = dataset["lon"]
        lat = dataset["lat"]
        lon2d, lat2d = np.meshgrid(lon, lat)
        # Convert lat/lon to a GeoDataFrame
        points = gpd.GeoDataFrame(
            {"sst": sst_data.values.flatten()},
            geometry=gpd.points_from_xy(lon2d.flatten(), lat2d.flatten()),
            crs="EPSG:4326"  # Ensure it matches the polygon's CRS
        )
    
        points_within = points[points.geometry.within(polygon_geom)]
    
        if not points_within.empty:
            avg_sst = points_within["sst"].mean()
            time_values.append(timestamp)
            avg_sst_values.append(avg_sst)
            print(f"Average SST inside polygon: {avg_sst:.2f} °C")
        else:
            print("No SST points found inside the polygon.")
        dataset.close()
    except:
        time_values.append(np.nan)
        avg_sst_values.append(np.nan)
        

df_sst = pd.DataFrame({"time": time_values, "avg_sst": avg_sst_values})

# Sort DataFrame by time (just to be sure)
df_sst = df_sst.sort_values(by="time").reset_index(drop=True)

df_sst.to_csv("/Users/sebinjohn/gq_proj/data/SST/avg_sst_timeseries.csv", index=False)

df_sst=pd.read_csv("/Users/sebinjohn/gq_proj/data/SST/avg_sst_timeseries.csv")

df_sst['time']=pd.to_datetime(df_sst['time'])
# Plot
plt.figure(figsize=(12, 6))
plt.plot(df_sst["time"], df_sst["avg_sst"], marker="o", linestyle="-", color="b", label="Avg SST")

# Formatting
plt.xlabel("Time")
plt.ylabel("Average SST (°C)")
plt.title("Time Series of Average SST Inside Polygon")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.show()

# Ensure 'time' is the index for resampling
df_sst["year"] = df_sst["time"].dt.year  # Extract year
df_yearly_avg = df_sst.groupby("year")["avg_sst"].mean().reset_index()  # Compute yearly mean

# Plot
plt.figure(figsize=(12, 6))
plt.plot(df_yearly_avg["year"], df_yearly_avg["avg_sst"], marker="o", linestyle="-", color="r", label="Yearly Avg SST")

# Formatting
plt.xlabel("Year")
plt.ylabel("Average SST (°K)")
plt.title("Yearly Average SST Inside Polygon")
plt.legend()
plt.grid(True)
plt.xticks(df_yearly_avg["year"], rotation=45)  # Rotate x-axis labels
plt.xlim(2005,2024)
plt.ylim(280,283)
plt.show()
#####

time_values = []
avg_sst_values = []

files = glob.glob("/Users/sebinjohn/gq_proj/data/SST/*.nc")
files.sort()

# Loop over all files
for file in files:
    print(file)
    match = pattern.search(file)
    timestamp = pd.to_datetime(match.group(1), format="%Y-%m-%dT%H%M")
    dataset = xr.open_dataset(file)
    try:
        sst_data = dataset["analysed_sst"]
        # Compute the mean SST over the entire grid
        avg_sst = sst_data.mean().values  # Mean over all lat/lon grid points
        
        time_values.append(timestamp)
        avg_sst_values.append(avg_sst)
        print(f"Average SST over entire grid: {avg_sst:.2f} °C")
        
        dataset.close()
    except Exception as e:
        print(f"Error processing {file}: {e}")
        time_values.append(np.nan)
        avg_sst_values.append(np.nan)

# Create DataFrame with time and average SST values
df_sst = pd.DataFrame({"time": time_values, "avg_sst": avg_sst_values})

# Sort DataFrame by time (just to be sure)
df_sst = df_sst.sort_values(by="time").reset_index(drop=True)

# Save to CSV (optional)
df_sst.to_csv("/Users/sebinjohn/gq_proj/data/SST/avg_sst_timeseries_full_grid.csv", index=False)

#df_sst=pd.read_csv("/Users/sebinjohn/gq_proj/data/SST/avg_sst_timeseries_full_grid.csv")

# Plotting Time Series for Average SST over the entire grid
plt.figure(figsize=(12, 6))
plt.plot(df_sst["time"], df_sst["avg_sst"], marker="o", linestyle="-", color="b", label="Avg SST over Entire Grid")

# Formatting
plt.xlabel("Time")
plt.ylabel("Average SST (°C)")
plt.title("Time Series of Average SST Over Entire Grid")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.show()

# Ensure 'time' is the index for resampling
df_sst["year"] = df_sst["time"].dt.year  # Extract year
df_yearly_avg = df_sst.groupby("year")["avg_sst"].mean().reset_index()  # Compute yearly mean

# Plotting Yearly Average SST over the entire grid
plt.figure(figsize=(12, 6))
plt.plot(df_yearly_avg["year"], df_yearly_avg["avg_sst"], marker="o", linestyle="-", color="r", label="Yearly Avg SST")

# Formatting
plt.xlabel("Year")
plt.ylabel("Average SST (°C)")
plt.title("Yearly Average SST Over Entire Grid")
plt.legend()
plt.grid(True)
plt.xticks(df_yearly_avg["year"], rotation=45)  # Rotate x-axis labels
plt.xlim(2005, 2024)
plt.ylim(280, 283)
plt.show()

#####

# Plotting with Cartopy (using the flipped data)
fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
sst_data.plot(ax=ax, cmap='viridis')

min_lon, max_lon = sst_data.lon.min().values, sst_data.lon.max().values
min_lat, max_lat = sst_data.lat.min().values, sst_data.lat.max().values

ax.set_extent([min_lon, max_lon, min_lat, max_lat], crs=ccrs.PlateCarree())
ax.set_xticks([min_lon, max_lon], crs=ccrs.PlateCarree())
ax.set_yticks([min_lat, max_lat], crs=ccrs.PlateCarree())
ax.plot(-147.08463, 61.09027, marker='o', color='red', markersize=5, transform=ccrs.PlateCarree())
# Plot points inside the polygon
if not points_within.empty:
    sc = ax.scatter(
    points_within.geometry.x, 
    points_within.geometry.y, 
    c=points_within["sst"],  # Color by SST values
    cmap='viridis',  # Choose a colormap
    s=10,  # Point size
    edgecolor='k',
    transform=ccrs.PlateCarree(),vmin=np.nanmin(sst_data.data),vmax=np.nanmax(sst_data.data)
    )
    plt.colorbar(sc, ax=ax, label="SST (°C)")  # Add colorbar for reference

plt.show()


flipped_data = sst_data.copy()
flipped_data.data[0,:,:]=np.flipud(sst_data.values[0,:,:])


region = [min_lon-2,max_lon+1, min_lat, max_lat+0.5]

fig = pygmt.Figure()

fig.basemap(region=region, projection="M6i", frame=["a", "WSne"])

fig.grdimage(grid=flipped_data , cmap="turbo")

fig.coast(shorelines=True, resolution="i")
fig.plot(
    x=-147.08463,projection="M6i",y=61.09027,style="c0.3c",region=region,pen="1p",fill="red")

fig.colorbar(frame="af+l'Sea Surface Temperature (°C)'")
fig.show()



# Writing the flipped data to a GeoTIFF file
lon = flipped_data.lon.values
lat = flipped_data.lat.values
transform = from_origin(lon.min(), lat.max(), abs(lon[1] - lon[0]), abs(lat[1] - lat[0]))

output_tif = "flipped_sst_data.tif"
with rasterio.open(output_tif, "w", driver="GTiff", height=flipped_data.shape[1], width=flipped_data.shape[2],
                   count=1, dtype=flipped_data.dtype, crs="EPSG:4326", transform=transform) as dst:
    dst.write(flipped_data.values[0, :, :], 1)

print(f"Flipped SST data saved as GeoTIFF: {output_tif}")

