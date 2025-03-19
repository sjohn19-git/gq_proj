#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 11:32:40 2025

@author: sebinjohn
"""

import rasterio
import numpy as np
import matplotlib.pyplot as plt
from rasterio.warp import reproject, calculate_default_transform, Resampling
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
from rasterio.warp import transform
from scipy.interpolate import griddata
from rasterio.transform import array_bounds
from matplotlib.colors import ListedColormap
from pyproj import CRS, Transformer

# Paths to your raster files
dem_path = "/Users/sebinjohn/gq_proj/data/DEMs/2019-04-14.tiff"
bedmap_path = "/Users/sebinjohn/gq_proj/data/bed_map/bed_map_merged.tif"
terminus_path = "/Users/sebinjohn/gq_proj/data/terminus_columbia/2019-06-04.geojson"

# Open Bedmap file (Target CRS)
with rasterio.open(bedmap_path) as bedmap_src:
    bedmap_data = bedmap_src.read(1)  # Read first band
    crs_bedmap = bedmap_src.crs  # Get Bedmap CRS
    transform_bedmap = bedmap_src.transform
    bedmap_data = np.where(bedmap_data == bedmap_src.nodata, np.nan, bedmap_data)  # Mask no-data values
    bedmap_shape = bedmap_src.shape
    
# Open DEM file (Source CRS)
with rasterio.open(dem_path) as dem_src:
    dem_data = dem_src.read(1)  # Read first band
    crs_dem = dem_src.crs  # Get DEM CRS
    transform_dem = dem_src.transform
    dem_data = np.where(dem_data == dem_src.nodata, np.nan, dem_data)  # Mask no-data values

    # Compute new transform and shape for reprojected DEM to match Bedmap CRS
    transform_new, width, height = calculate_default_transform(
        crs_dem, crs_bedmap, dem_src.width, dem_src.height, *dem_src.bounds
    )

    # Create empty array for reprojected DEM
    reprojected_dem = np.empty((height, width), dtype=dem_data.dtype)

    # Reproject DEM to match Bedmap CRS
    reproject(
        source=dem_data,
        destination=reprojected_dem,
        src_transform=transform_dem,
        src_crs=crs_dem,
        dst_transform=transform_new,
        dst_crs=crs_bedmap,
        resampling=Resampling.nearest  # Using nearest neighbor resampling
    )
    reprojected_dem[reprojected_dem==0]=np.nan
    
extent_reprojected_dem = array_bounds(height, width, transform_new)
extent_reprojected_dem = (extent_reprojected_dem[2], extent_reprojected_dem[3], extent_reprojected_dem[0], extent_reprojected_dem[1])


rows, cols = np.indices(reprojected_dem.shape)
x_coords, y_coords = cols, rows
dem_x, dem_y = rasterio.transform.xy(transform_new, y_coords, x_coords)
dem_x,dem_y=np.array(dem_x),np.array(dem_y)

rows, cols = np.indices(bedmap_shape)
x_coords, y_coords = cols, rows
bed_x,bed_y=rasterio.transform.xy(transform_bedmap, y_coords, x_coords)
bed_x,bed_y=np.array(bed_x),np.array(bed_y)

dem_coords = np.vstack((dem_x.flatten(), dem_y.flatten())).T
dem_values = reprojected_dem.flatten()

# Perform interpolation at the Bedmap coordinates (bed_x, bed_y)
bed_coords = np.vstack((bed_x.flatten(), bed_y.flatten())).T

# Interpolate reprojected DEM values at Bedmap coordinates using nearest neighbor
interpolated_values = griddata(dem_coords, dem_values, bed_coords, method='nearest')
downsamp_dem = interpolated_values.reshape(bed_x.shape)
downsamp_dem[np.isnan(bedmap_data)] = np.nan

terminus_gdf = gpd.read_file(terminus_path)
terminus_line = terminus_gdf.geometry[0]  # Assuming only one LineString feature
terminus_x, terminus_y = zip(*terminus_line.coords)
terminus_x_utm, terminus_y_utm = transform('EPSG:4326', crs_bedmap, terminus_x, terminus_y)

#########
gl_thickness=downsamp_dem-bedmap_data
stbl_crit=gl_thickness/-bedmap_data


#####plots
vmin,vmax=0,400
extent=[485275.77, 503475.77, 6770460.1049, 6790460.1049]
date=dem_path.split('/')[-1]
termi_date=terminus_path.split('/')[-1]
fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={'projection': ccrs.UTM(6)})
ax.coastlines()
pcm = ax.pcolormesh(bed_x, bed_y, gl_thickness, cmap='nipy_spectral', shading='auto', vmin=vmin, vmax=vmax, transform=ccrs.UTM(6))
ax.set_extent(extent, crs=ccrs.UTM(6))
ax.plot(terminus_x_utm, terminus_y_utm, color='k', linewidth=1, marker='o', markersize=2, 
        transform=ccrs.UTM(6), label="Terminus {}".format(termi_date))
plt.colorbar(pcm, ax=ax, label="glacier thickness (m)")
plt.title("glacier thickness DEM {}".format(date))
plt.show()





vmin,vmax=1,2
extent=[485275.77, 503475.77, 6770460.1049, 6790460.1049]
date=dem_path.split('/')[-1]
termi_date=terminus_path.split('/')[-1]
fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={'projection': ccrs.UTM(6)})
ax.coastlines()
pcm = ax.pcolormesh(bed_x, bed_y, stbl_crit, cmap='nipy_spectral', shading='auto', vmin=vmin, vmax=vmax, transform=ccrs.UTM(6))
ax.set_extent(extent, crs=ccrs.UTM(6))
ax.plot(terminus_x_utm, terminus_y_utm, color='k', linewidth=1, marker='o', markersize=2, 
        transform=ccrs.UTM(6), label="Terminus {}".format(termi_date))
plt.colorbar(pcm, ax=ax, label="glacier thickness (m)")
plt.title("Stability criterion {}".format(date))
plt.show()
fig.savefig("/Users/sebinjohn/gq_proj/Results/stabl_crt/{}.png".format(date))







