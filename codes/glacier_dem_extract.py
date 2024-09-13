#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 18:07:20 2024

@author: sebinjohn
"""

import geopandas as gpd
import rasterio
import numpy as np
from rasterio.features import geometry_mask, geometry_window
from tqdm import tqdm
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

# Paths to your files
shapefile_path = '/Users/sebinjohn/gq_proj/data/glacier_extent/AK_2018_overall_glacier_covered_area.shp'
dem_path = '/Users/sebinjohn/Downloads/tiffs/merged.tif'
output_tif_path = '/Users/sebinjohn/Downloads/extracted_dem.tif'

# Load shapefile
gdf = gpd.read_file(shapefile_path)

bounding_box=[-148, -146, 61, 61.5]
bbox_polygon = Polygon([
(bounding_box[0], bounding_box[1]),
(bounding_box[0], bounding_box[3]),
(bounding_box[2], bounding_box[3]),
(bounding_box[2], bounding_box[1])])

target_crs = 'EPSG:4326'
print("Original CRS:", gdf.crs)
gdf_transformed = gdf.to_crs(target_crs)

# Open the DEM file
with rasterio.open(dem_path) as src:
    # Read metadata
    meta = src.meta.copy()
    meta.update(dtype=rasterio.float32, count=1, nodata=src.nodata)

    # Create an empty array for the new raster
    new_data = np.zeros((src.height, src.width), dtype=np.float32)
        # Read the data from the DEM
    dem_data = src.read(1)  # Read the first band
    # Process each polygon
    for i in tqdm(range(gdf.geometry.shape[0])):
        # Create a mask for the current polygon
        if gdf_transformed.geometry[i].within(bbox_polygon):
            geom=gdf.geometry[i]
            mask = geometry_mask([geom], transform=src.transform, invert=True, out_shape=(src.height, src.width))
            # Apply the mask and update new_data
            new_data[mask] = dem_data[mask]

    # Write the new raster to a file
    with rasterio.open(output_tif_path, 'w', **meta) as dest:
        dest.write(new_data, 1)

print(f'Extracted DEM saved to {output_tif_path}')
