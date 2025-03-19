#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 13:50:33 2025

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
dem_path = "/Users/sebinjohn/gq_proj/data/DEMs/2022-03-30.tiff"
bedmap_path = "/Users/sebinjohn/gq_proj/data/bed_map/bed_map_merged.tif"
terminus_path = "/Users/sebinjohn/gq_proj/data/terminus_columbia/2013-03-15.geojson"

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


######
vmin,vmax=0,400
extent=[485275.77, 503475.77, 6770460.1049, 6790460.1049]
date=dem_path.split('/')[-1]
ticns_belw=downsamp_dem-bedmap_data
grnc = np.where(np.isnan(ticns_belw) | np.isnan(bedmap_data), np.nan, ticns_belw > bedmap_data)
plot=1


###load terminus position
terminus_gdf = gpd.read_file(terminus_path)
terminus_line = terminus_gdf.geometry[0]  # Assuming only one LineString feature

# Convert LineString coordinates to UTM
terminus_x, terminus_y = zip(*terminus_line.coords)
terminus_x_utm, terminus_y_utm = transform('EPSG:4326', crs_bedmap, terminus_x, terminus_y)

###



if plot==1:

    fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={'projection': ccrs.UTM(6)})
    ax.coastlines()
    pcm = ax.pcolormesh(dem_x, dem_y, reprojected_dem, cmap='nipy_spectral', shading='auto', vmin=vmin, vmax=vmax, transform=ccrs.UTM(6))
    ax.set_extent(extent, crs=ccrs.UTM(6))
    plt.colorbar(pcm, ax=ax, label="DEM Elevation (m)")
    plt.title("Reprojected DEM {}".format(date))
    plt.show()
    
    fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={'projection': ccrs.UTM(6)})
    ax.coastlines()
    pcolor_bedmap = ax.pcolormesh(bed_x, bed_y, bedmap_data, cmap='Blues', shading='auto', alpha=0.5, transform=ccrs.UTM(6))
    pcolor_dem1 = ax.pcolormesh(bed_x, bed_y, downsamp_dem, cmap='nipy_spectral', shading='auto', vmin=vmin, vmax=vmax, transform=ccrs.UTM(6))
    ax.set_extent(extent, crs=ccrs.UTM(6))
    cbar1 = plt.colorbar(pcolor_bedmap, ax=ax, label="Bedmap Elevation/Bathymetry (m)", shrink=0.7)
    cbar2 = plt.colorbar(pcolor_dem1, ax=ax, label="Reprojected DEM (m)", shrink=0.7)
    plt.title("Reprojected DEM and Bedmap Overlay {}".format(date))
    plt.show()
    
    
    ########
    
    
    
    fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={'projection': ccrs.UTM(6)})
    ax.coastlines()
    extent_bedmap = [
        transform_bedmap[2], 
        transform_bedmap[2] + transform_bedmap[0] * bedmap_src.width, 
        transform_bedmap[5] + transform_bedmap[4] * bedmap_src.height, 
        transform_bedmap[5]]
    pcolor_tic = plt.pcolor(bed_x, bed_y,downsamp_dem, cmap='nipy_spectral',shading='auto',vmin=vmin,vmax=vmax)
    #im_bed=ax.imshow(bedmap_data, extent=extent_bedmap, transform=ccrs.UTM(6), cmap='nipy_spectral', alpha=0.5,vmin=vmin,vmax=vmax)
    #ax.plot(terminus_x_utm, terminus_y_utm, color='k', linewidth=1, marker='o', markersize=2, transform=ccrs.UTM(6), label="Terminus 2010-09-15")
    ax.set_extent(extent, crs=ccrs.UTM(6))
    plt.colorbar(pcolor_tic, ax=ax, label="downsampled dem (m)")
    plt.title("downsampled dem {}".format(date))
    plt.legend()
    plt.show()
    
    
    fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={'projection': ccrs.UTM(6)})
    ax.coastlines()
    extent_bedmap = [
        transform_bedmap[2], 
        transform_bedmap[2] + transform_bedmap[0] * bedmap_src.width, 
        transform_bedmap[5] + transform_bedmap[4] * bedmap_src.height, 
        transform_bedmap[5]]
    #pcolor_dem1 = plt.pcolor(bed_x, bed_y,ticns_belw, cmap='nipy_spectral',shading='auto',vmin=vmin,vmax=vmax)
    im_bed=plt.pcolor(bed_x, bed_y,bedmap_data, cmap='nipy_spectral',shading='auto',vmin=-vmax,vmax=0)
    #ax.plot(terminus_x_utm, terminus_y_utm, color='k', linewidth=1, marker='o', markersize=2, transform=ccrs.UTM(6), label="Terminus 2010-09-15")
    ax.set_extent(extent, crs=ccrs.UTM(6))
    plt.colorbar(im_bed, ax=ax, label="bedmap (m)")
    plt.title("bedmap")
    plt.legend()
    plt.show()
    
    #####
    
    
    vmin,vmax=0,2400
    
    fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={'projection': ccrs.UTM(6)})
    ax.coastlines()
    extent_bedmap = [
        transform_bedmap[2], 
        transform_bedmap[2] + transform_bedmap[0] * bedmap_src.width, 
        transform_bedmap[5] + transform_bedmap[4] * bedmap_src.height, 
        transform_bedmap[5]]
    pcolor_tic = plt.pcolor(bed_x, bed_y,ticns_belw, cmap='nipy_spectral',shading='auto',vmin=vmin,vmax=vmax)
    #im_bed=ax.imshow(bedmap_data, extent=extent_bedmap, transform=ccrs.UTM(6), cmap='nipy_spectral', alpha=0.5,vmin=vmin,vmax=vmax)
    #ax.plot(terminus_x_utm, terminus_y_utm, color='k', linewidth=1, marker='o', markersize=2, transform=ccrs.UTM(6), label="Terminus 2010-09-15")
    ax.set_extent(extent, crs=ccrs.UTM(6))
    plt.colorbar(pcolor_tic, ax=ax, label="thickness below water if isostatic (m)")
    plt.title("thickness below water {}".format(date))
    plt.show()
    
    
    colors = ["blue", "red"]
    cmap = ListedColormap(colors)
    
    fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={'projection': ccrs.UTM(6)})
    ax.coastlines()
    extent_bedmap = [
        transform_bedmap[2], 
        transform_bedmap[2] + transform_bedmap[0] * bedmap_src.width, 
        transform_bedmap[5] + transform_bedmap[4] * bedmap_src.height, 
        transform_bedmap[5]]
    pcolor_tic = plt.pcolor(bed_x, bed_y,grnc, cmap=cmap,shading='auto',vmin=0,vmax=1)
    #im_bed=ax.imshow(bedmap_data, extent=extent_bedmap, transform=ccrs.UTM(6), cmap='nipy_spectral', alpha=0.5,vmin=vmin,vmax=vmax)
    #ax.plot(terminus_x_utm, terminus_y_utm, color='k', linewidth=1, marker='o', markersize=2, transform=ccrs.UTM(6), label="Terminus 2010-09-15")
    ax.set_extent(extent, crs=ccrs.UTM(6))
    plt.colorbar(pcolor_tic, ax=ax, label="grounded or not")
    plt.title("grounded or not {}".format(date))
    plt.legend()
    plt.show()
else:
    
    vmin,vmax=0,400
    
    fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={'projection': ccrs.UTM(6)})
    ax.coastlines()
    extent_bedmap = [
        transform_bedmap[2], 
        transform_bedmap[2] + transform_bedmap[0] * bedmap_src.width, 
        transform_bedmap[5] + transform_bedmap[4] * bedmap_src.height, 
        transform_bedmap[5]]
    pcolor_tic = plt.pcolor(bed_x, bed_y,ticns_belw, cmap='nipy_spectral',shading='auto',vmin=vmin,vmax=vmax)
    #im_bed=ax.imshow(bedmap_data, extent=extent_bedmap, transform=ccrs.UTM(6), cmap='nipy_spectral', alpha=0.5,vmin=vmin,vmax=vmax)
    ax.plot(terminus_x_utm, terminus_y_utm, color='k', linewidth=1, marker='o', markersize=2, transform=ccrs.UTM(6), label="Terminus 2010-09-15")
    ax.set_extent(extent, crs=ccrs.UTM(6))
    plt.colorbar(pcolor_tic, ax=ax, label="thickness below water if isostatic (m)")
    plt.title("thickness below water {}".format(date))
    plt.show()
    fig.savefig("/Users/sebinjohn/gq_proj/Results/thickness_below_water/{}.png".format(date))
    
    



#########centerline
centerline_path = "/Users/sebinjohn/gq_proj/data/centerline/columbia-centerline.shp"
centerline_gdf = gpd.read_file(centerline_path)
centerline = centerline_gdf.geometry[0]
centerline_x, centerline_y = zip(*centerline.coords)
centerline_x_utm, centerline_y_utm = transform('EPSG:4326', crs_bedmap, centerline_x, centerline_y)



 

