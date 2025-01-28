#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 20:33:09 2024

@author: sebinjohn
"""

import rasterio
import geopandas as gpd
import numpy as np
from rasterio.mask import mask
from scipy.ndimage import sobel
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from shapely.geometry import Polygon, LineString
from shapely.geometry import Point
import re
from datetime import datetime

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


for i in tqdm(range(len(paths))):
    path = paths[i]
    folder = path.split('/')[-1]
    ide = folder.split("_")[2]
    if ide in ['066017', '067017']:
        print(path)
        os.chdir(path)
        ndsi_file = [f for f in os.listdir() if f.endswith('.TIF') and 'NDSI' in f]
        if ndsi_file:
            ndsi_path = os.path.join(path, ndsi_file[0])
            name=ndsi_path.split("_")[-5]
            with rasterio.open(ndsi_path) as src:
                # Clip the NDSI raster to the polygon
                clipped_ndsi, clipped_transform = mask(src, polygon_geometry, crop=True)
                transform=src.transform
                # Optional: Save the clipped raster or process further
                print(f"Clipped NDSI raster from {ndsi_file[0]} successfully.")

                glacier_mask = clipped_ndsi > 0.4
                
                
                # Edge detection using Sobel filters
                sobel_x = sobel(glacier_mask.astype(float), axis=0)  # Edge detection in x-direction
                sobel_y = sobel(glacier_mask.astype(float), axis=1)  # Edge detection in y-direction
                edges = np.hypot(sobel_x, sobel_y) > 0  # Combine Sobel outputs into a single edge map
                
                
                fig, axs = plt.subplots(1, 3, figsize=(15, 8))
                
                # Plot the clipped NDSI
                im=axs[0].imshow(clipped_ndsi[0,:,:], cmap="viridis")
                axs[0].set_title("Clipped NDSI")
                axs[0].axis('off')
                
                
                # Plot the glacier mask
                axs[1].imshow(glacier_mask[0,:,:], cmap="gray")
                axs[1].set_title("Glacier Mask (Thresholded)")
                axs[1].axis('off')
                
                # Plot the edges with the detected terminus line
                axs[2].imshow(edges[0,:,:], cmap="hot")
                axs[2].set_title("Glacier Terminus (Edges)")
                fig.suptitle(ide+" "+str(extract_date(path)), y=0.8)
                plt.tight_layout()
                plt.savefig(f"/Users/sebinjohn/gq_proj/Results/edge_detection/{name}.png")
