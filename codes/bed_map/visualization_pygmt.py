#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 08:29:41 2025

@author: sebinjohn
"""

import pygmt
import rasterio
import numpy as np
from rasterio.transform import xy
from pyproj import Transformer
import xarray as xr
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import os
 
os.chdir("/Users/sebinjohn/gq_proj/data/bed_map")

bathy="/Users/sebinjohn/gq_proj/data/bed_map/bed_map_merged.tif"

with rasterio.open(bathy) as src1:
    bathy_data = src1.read(1)
    bathy_nodata = src1.nodata
    bathy_transform = src1.transform
    bathy_crs = src1.crs
    bathy_shape = src1.shape
    profile = src1.profile

rows, cols = bathy_shape
row_indices, col_indices = np.meshgrid(np.arange(rows), np.arange(cols), indexing="ij")

# Convert indices to UTM coordinates (X, Y)
utm_x, utm_y = xy(bathy_transform, row_indices, col_indices)

# Convert to NumPy arrays
utm_x = np.array(utm_x)
utm_y = np.array(utm_y)

# Define the transformer from EPSG:32606 (UTM Zone 6N) to EPSG:4326 (WGS84 lat/lon)
transformer = Transformer.from_crs("EPSG:32606", "EPSG:4326", always_xy=True)

# Convert UTM (X, Y) to WGS84 (Longitude, Latitude)
lons, lats = transformer.transform(utm_x, utm_y)
bathy_data[bathy_data==bathy_nodata]=np.nan
bathy_data[bathy_data>100]=np.nan

latg = (lats[:, 0])
long = (lons[0, :])
bed_grd = xr.DataArray(
    bathy_data, dims=["lat", "lon"], coords={"lat": latg, "lon": long}
    )




demi="/Users/sebinjohn/gq_proj/data/DEMs/columbia_dem.tiff"

with rasterio.open(demi) as src1:
    dem_data = src1.read(1)
    dem_nodata = src1.nodata
    dem_transform = src1.transform
    dem_crs = src1.crs
    dem_shape = src1.shape
    dem_prof = src1.profile

rows, cols = dem_shape
row_indices, col_indices = np.meshgrid(np.arange(rows), np.arange(cols), indexing="ij")

# Convert indices to UTM coordinates (X, Y)
utm_x, utm_y = xy(dem_transform, row_indices, col_indices)

# Convert to NumPy arrays
utm_x = np.array(utm_x)
utm_y = np.array(utm_y)

# Define the transformer from EPSG:32606 (UTM Zone 6N) to EPSG:4326 (WGS84 lat/lon)
transformer = Transformer.from_crs("EPSG:3413", "EPSG:4326", always_xy=True)

# Convert UTM (X, Y) to WGS84 (Longitude, Latitude)
lons_dem, lats_dem = transformer.transform(utm_x, utm_y)
dem_data[dem_data==dem_nodata]=np.nan

res=0.0001
g_lats=np.arange(61.1,61.25,res)
g_lons=np.arange(-147.3,-146.8,res)

grid_lat,grid_lon=np.meshgrid(g_lats,g_lons)
points = np.column_stack((lons_dem.ravel(), lats_dem.ravel()))
values = dem_data.ravel()


grid_dem = griddata(points, values, (grid_lon,grid_lat), method="linear")


latd = (grid_lat[0,:])
lond = (grid_lon[:,0])

dem_grd = xr.DataArray(
    grid_dem.T, dims=["lat", "lon"], coords={"lat": latd, "lon": lond}
    )


extent = [lond.min(), lond.max(), latd.min(), latd.max()]

# Plot the DEM using imshow
plt.figure(figsize=(8, 6))
plt.imshow(grid_dem.T, extent=extent, origin="upper", cmap="terrain")
plt.colorbar(label="Elevation (m)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Columbia Glacier DEM")
plt.show()




maxdep=400
# Create color palette for topography
pygmt.makecpt(
    cmap="turbo",
    series=f"-{maxdep}/20/10",  # Adjusted elevation range
    continuous=True,output="./gl.cpt")




 
 
region = [-147.25, -146.85, 61.1, 61.230, -maxdep, 100]# Columbia Glacier region
projection = "M15c"  # Set projection globally
#dem= pygmt.datasets.load_earth_relief(resolution="15s", region=[-148.3, -146.8, 61.1, 61.25, -maxdep, 100])

frame = ["xa0.5f0.1", "ya0.5f0.1", "wsen"]
proj="M10c"
per=[180,75]

# Create the figure
fig = pygmt.Figure()
pygmt.config(MAP_FRAME_TYPE="plain",MAP_FRAME_WIDTH="0.5p",MAP_FRAME_PEN="1p")

pygmt.makecpt(cmap="bath1.cpt",series=[-8000,0])

# fig.grdimage(
#     grid=dem_grd,
#     cmap=True,
#     shading='+a300+nt1',
#     region=region,
#     projection=proj)
fig.grdimage(
    grid=dem_grd,
    cmap=True,
    shading='+a300+nt1',
    region=region,
    projection=proj)



# fig.grdview(
#     grid=bed_grd,
#     region=[-147.25, -146.85, 61.1, 61.235, -maxdep, 100],  # Adjusted vertical range
#     perspective=per,  # Viewing angle
#     frame=frame,
    
#     projection=proj,
#     shading='+a300+nt1',
#     cmap="./gl.cpt",
#     surftype="c",
#     zsize="0.1c"
# )


fig.colorbar(frame=["x100+lElevation (m)"],position="JBC+w5c/0.3c+o0c/0.2c",projection=proj)
# Show the figure
fig.show()


#####################################misc

# Create a PyGMT figure
fig = pygmt.Figure()
fig.coast(
    shorelines=True,
    region=region,
    resolution="h",
    water="skyblue",
    land="gray",
    frame=["xa0.5f0.1", "ya0.5f0.1", "z1000+lmeters", "wSEnZ"],
    projection=projection,  # Apply projection
)

fig.grdimage(
    grid=bed_grd,
    cmap="./gl.cpt",
    region=region,
    projection=projection,  # Apply projection
    nan_transparent=True,
)

# Plot a red point
fig.plot(
    x=-147.08463,
    y=61.09027,
    style="c0.3c",
    region=region,
    projection=projection,  # Apply projection
    pen="1p",
    fill="red",
)

fig.show()

