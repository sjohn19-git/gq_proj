#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 10:53:50 2025

@author: sebinjohn
"""

import h5py
import numpy as np
import rasterio
from rasterio.transform import from_origin
import matplotlib.pyplot as plt

# Load the HDF5 file and inspect its structure
with h5py.File('/Users/sebinjohn/gq_proj/data/bed_map/C_bedmap.mat', 'r') as f:
    def print_structure(name, obj):
        print(name, "->", obj)

    f.visititems(print_structure)

# Extract the necessary datasets from the HDF5 file
with h5py.File('/Users/sebinjohn/gq_proj/data/bed_map/C_bedmap.mat', 'r') as f:
    dz = f['B']['dz'][:]  # Extract 'dz' dataset
    x = f['B']['x'][:]    # Extract 'x' dataset
    y = f['B']['y'][:]    # Extract 'y' dataset
    err = f['B']['z']['err'][:]   # Extract 'err' dataset
    orig = f['B']['z']['orig'][:]  # Extract 'orig' dataset

orig = np.nan_to_num(orig, nan=1000000)
err = np.nan_to_num(err, nan=1000000)
# Ensure x and y are 1D arrays
x = x.reshape(-1)  # Convert (314,1) → (314,)
y = y.reshape(-1)  # Convert (326,1) → (326,)

# Create a 2D meshgrid using x and y
X, Y = np.meshgrid(x, y)  # Note: y comes first in np.meshgrid

# Get resolution (assuming uniform grid spacing)
x_res = (x.max() - x.min()) / (len(x) - 1)
y_res = (y.max() - y.min()) / (len(y) - 1)

# Define raster transformation (top-left corner, pixel size)
transform = from_origin(x.min(), y.max(), x_res, y_res)

# Define output file name for UTM projection (NAD83 / UTM Zone 6N)
output_tif_utm = "/Users/sebinjohn/gq_proj/data/bed_map/EM2016_with_errors.tif"

# Write both the original and error data as separate bands
with rasterio.open(
    output_tif_utm, "w",
    driver="GTiff",
    height=orig.shape[1],  # Ensure correct shape order
    width=orig.shape[0],
    count=2,  # Two bands, one for the original and one for the error
    dtype=orig.dtype,
    crs="EPSG:32606",
    transform=transform,
    nodata=1000000
) as dst:
    # Write the original data as the first band
    dst.write(np.flipud(orig.T), 1)  # Flip vertically and write to band 1
    
    # Write the error data as the second band
    dst.write(np.flipud(err.T), 2)  # Flip vertically and write to band 2

print(f"GeoTIFF file with original and error data saved to {output_tif_utm}")
