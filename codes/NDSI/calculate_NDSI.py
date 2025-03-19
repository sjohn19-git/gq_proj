#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 12:13:45 2024

@author: sebinjohn
"""

import rasterio
import numpy as np
from rasterio.features import shapes
import geopandas as gpd
from shapely.geometry import shape
import os
from tqdm import tqdm



##landsat 8/9

os.chdir("/Volumes/Sebins-HDD/Landsat8:9_c2l2/")
folders=folders = [f for f in os.listdir() if os.path.isdir(f) and not f.startswith('.')]
paths=[]
for folder in tqdm(folders):
    paths.append(os.path.join(os.getcwd(),folder))
    

for i in tqdm(range(len(paths))):
    path=paths[i]
    folder=folders[i]
    # Paths to the Green and SWIR1 band files
    green_band_path = os.path.join(path,folder+'_SR_B3.TIF')
    swir1_band_path = os.path.join(path,folder+'_SR_B6.TIF')

    # Open the bands using rasterio
    with rasterio.open(green_band_path) as green_src, rasterio.open(swir1_band_path) as swir1_src:
        green_band = green_src.read(1).astype(float)  # Read the Green band
        swir1_band = swir1_src.read(1).astype(float)  # Read the SWIR1 band
        profile = green_src.profile
    # Avoid division by zero by adding a small constant to the denominator
    epsilon = 1e-10

    # Calculate NDSI
    ndsi = (green_band - swir1_band) / (green_band + swir1_band + epsilon)
    
    # Save NDSI to a new GeoTIFF file
    ndsi_output_path = os.path.join(path,folder+'_NDSI.TIF')
    ndsi_meta = green_src.meta.copy()
    ndsi_meta.update(dtype=rasterio.float32)
    
    with rasterio.open(ndsi_output_path, "w", **ndsi_meta) as dst:
        dst.write(ndsi.astype(rasterio.float32), 1)
    
    print(f"NDSI saved to {ndsi_output_path}")

    
    threshold = 0.4
    binary_mask = (ndsi > threshold).astype(np.uint8)
    
    
    shapes_generator = shapes(binary_mask, transform=profile['transform'])
    
    # Convert shapes to a list of geometries and values
    polygons = [
        {"geometry": shape(geom), "value": value}
        for geom, value in shapes_generator if value == 1
    ]
    
    gdf = gpd.GeoDataFrame.from_records(polygons)
    gdf = gdf.set_geometry("geometry")
    gdf.crs = profile['crs']  # Assign CRS from the raster
    
    # Save the glacier boundaries to a shapefile
    output_path =  os.path.join(path,folder+'_terminus.shp')
    gdf.to_file(output_path)
    
    print(f"Glacier outlines saved to {output_path}")
