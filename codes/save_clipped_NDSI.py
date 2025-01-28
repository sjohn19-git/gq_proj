#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 08:24:55 2024

@author: sebinjohn
"""

import rasterio
import geopandas as gpd
import numpy as np
from rasterio.mask import mask
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
import re
from datetime import datetime
import pandas as pd

# Load the polygon shapefile
polygon_gdf = gpd.read_file("/Users/sebinjohn/gq_proj/data/glacier_termi_polygon/columb_pol.shp")
polygon_geometry = [polygon_gdf.unary_union]  # Combine all polygons into one

os.chdir("/Volumes/Sebins-HDD/Landsat8:9_c2l2/")
folders = [f for f in os.listdir() if os.path.isdir(f) and not f.startswith('.')]
paths = [os.path.join(os.getcwd(), folder) for folder in folders]


def calculate_edge_displacement(edge1, edge2):
    """Calculate the average displacement between two edges."""
    if edge1 is None or edge2 is None:
        return None

    # Calculate distance between edges: Use the Hausdorff distance or closest point distance
    displacement = edge1.distance(edge2)
    
    return displacement

def raster_to_shapely(edges, transform):
    # Convert the binary edge array to polygons using shapely
    contours = np.argwhere(edges)  # Find non-zero edge pixels
    if contours.size == 0:
        return None
    # Convert contours to polygons (this is a simple method, you may use more sophisticated ones)
    points = [tuple(transform * (c[1], c[0])) for c in contours]
    edge_line = LineString(points)
    return edge_line

def extract_date(file_path):
    # Extract the date (assumed to be in the format 'YYYYMMDD')
    match = re.search(r'_(\d{8})_', file_path)
    if match:
        return datetime.strptime(match.group(1), '%Y%m%d')
    return datetime.min  # Return a very early date if no match

paths = sorted(paths, key=extract_date)

output_dir = "/Users/sebinjohn/gq_proj/data/clipped_NDSI/" 

for i in tqdm(range(len(paths))):
    path = paths[i]
    folder = path.split('/')[-1]
    ide = folder.split("_")[2]
    if ide in ['066017', '067017','068017']:
        print(path)
        os.chdir(path)
        ndsi_file = [f for f in os.listdir() if f.endswith('.TIF') and 'NDSI' in f]
        if ndsi_file:
            ndsi_path = os.path.join(path, ndsi_file[0])
            with rasterio.open(ndsi_path) as src:
                # Clip the NDSI raster to the polygon
                clipped_ndsi, clipped_transform = mask(src, polygon_geometry, crop=True)
                transform=src.transform
                clipped_meta = src.meta.copy()
                clipped_meta.update({
                    "driver": "GTiff",
                    "height": clipped_ndsi.shape[1],
                    "width": clipped_ndsi.shape[2],
                    "transform": clipped_transform
                })
        
        time = pd.to_datetime(folder.split("_")[3], format='%Y%m%d')
        date_str = time.strftime('%Y%m%d')
        
        # Save the clipped raster
        output_file = f"{date_str}_{ide}_clipped_NDSI.tif"
        output_path = os.path.join(output_dir, output_file)
        
        with rasterio.open(output_path, "w", **clipped_meta) as dest:
            dest.write(clipped_ndsi)
        
        print(f"Saved clipped NDSI raster to {output_path}")
                