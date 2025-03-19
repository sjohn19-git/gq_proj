#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 00:40:50 2025

@author: sebinjohn
"""

import rasterio
import numpy as np
import os
from rasterio.warp import reproject, Resampling
from rasterio.enums import Resampling
from pyproj import Transformer
import matplotlib.pyplot as plt

os.chdir("/Users/sebinjohn/gq_proj/data/bed_map")
em="/Users/sebinjohn/gq_proj/data/bed_map/EM2016_with_errors.tif"
bathy="/Users/sebinjohn/gq_proj/data/Bathymetry/nos-item-559670/BAG/H13418_MB_VR_Ellipsoid_1of1.bag"

with rasterio.open(bathy) as src1:
    bathy_data = src1.read(1)
    bathy_nodata = src1.nodata
    bathy_transform = src1.transform
    bathy_crs = src1.crs
    bathy_shape = src1.shape
    profile = src1.profile
    
# Open EM2016 raster (EM)
with rasterio.open(em) as src2:
    em_data = src2.read(1)
    em_nodata = src2.nodata
    em_transform = src2.transform
    em_crs = src2.crs
    em_shape = src2.shape


    
bathy_xmin, bathy_ymax = bathy_transform * (0, 0)  # top-left corner (0,0)
bathy_xmax, bathy_ymin = bathy_transform * (bathy_shape[1], bathy_shape[0])  # bottom-right corner

# Get corner coordinates for EM2016 raster
em_xmin, em_ymax = em_transform * (0, 0)  # top-left corner (0,0)
em_xmax, em_ymin = em_transform * (em_shape[1], em_shape[0])  # bottom-right corner

xmin = min(bathy_xmin, em_xmin)
ymin = min(bathy_ymin, em_ymin)
xmax = max(bathy_xmax, em_xmax)
ymax = max(bathy_ymax, em_ymax)


pixel_size_x = bathy_transform[0]  # Pixel size in the x direction (width)
pixel_size_y = -bathy_transform[4] 

new_width = int((xmax - xmin) / pixel_size_x)
new_height = int((ymax - ymin) / pixel_size_y)

new_transform = rasterio.Affine(pixel_size_x, 0, xmin, 0, -pixel_size_y, ymax)


merged_data = np.full((new_height, new_width), np.nan, dtype=np.float32)  # Initialize with NaN
merged_error = np.full((new_height, new_width), np.nan, dtype=np.float32)  # Initialize with NaN


