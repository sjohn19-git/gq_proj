#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 22:14:30 2024

@author: sebinjohn
"""

import geopandas as gpd
import rasterio
from rasterio import features
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

# Path to your shapefile
shapefile_path = '/Users/sebinjohn/gq_proj/data/glacier_extent/AK_2020_overall_glacier_covered_area.shp'

# Load the shapefile using Geopandas
gdf = gpd.read_file(shapefile_path)

# Open the reference raster (e.g., DEM) to get the transform and shape
with rasterio.open('/Users/sebinjohn/gq_proj/data/qgis_data/tiffs/merged.tif') as src:
    transform = src.transform
    out_shape = (src.height, src.width)
    crs = src.crs

# Rasterize the shapefile polygons
rasterized = features.rasterize(
    [(geometry, 1) for geometry in tqdm(gdf.geometry)],
    out_shape=out_shape,
    transform=transform,
    fill=0,
    dtype=np.uint8
)

# Save the rasterized output as a new GeoTIFF
out_raster_path = '/Users/sebinjohn/gq_proj/data/qgis_data/rasterized_glacier_extent/gl_2020_extent.tif'
with rasterio.open(
    out_raster_path, 'w',
    driver='GTiff',
    height=rasterized.shape[0],
    width=rasterized.shape[1],
    count=1,
    dtype=rasterized.dtype,
    crs=crs,
    transform=transform
) as dst:
    dst.write(rasterized, 1)

print("Raster created successfully!")

plt.imshow(rasterized)
