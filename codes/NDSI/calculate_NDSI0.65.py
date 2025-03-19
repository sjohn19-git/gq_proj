#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 15:49:30 2024

@author: sebinjohn
"""

import rasterio
import numpy as np
from rasterio.features import shapes
import geopandas as gpd
from shapely.geometry import shape
import os
from tqdm import tqdm
from shapely.ops import unary_union



os.chdir("/Volumes/Sebins-HDD/Landsat8:9_c2l2/")
folders=folders = [f for f in os.listdir() if os.path.isdir(f) and not f.startswith('.')]
paths=[]
for folder in tqdm(folders):
    paths.append(os.path.join(os.getcwd(),folder))
    
    
for i in tqdm(range(len(paths))):
    path=paths[i]
    folder=folders[i]
    ndsi_output_path = os.path.join(path,folder+'_NDSI.TIF')
    with rasterio.open(ndsi_output_path) as src:
        ndsi = src.read(1)
        profile = src.profile
    threshold = 0.65
    binary_mask = (ndsi > threshold).astype(np.uint8)

    # Extract shapes from the binary mask
    shapes_generator = shapes(binary_mask, transform=profile['transform'])
    polygons = [
        shape(geom)
        for geom, value in shapes_generator if value == 1
    ]

    # Save individual polygons to a shapefile
    gdf_polygons = gpd.GeoDataFrame(geometry=polygons, crs=profile['crs'])
    polygons_output_path = os.path.join(path, folder + '_terminus0.65.shp')
    gdf_polygons.to_file(polygons_output_path)
    print(f"Individual glacier polygons saved to {polygons_output_path}")

    # Merge all polygons into a single outline
    outline_polygon = unary_union(polygons)

    # Save merged outline to a separate shapefile
    gdf_outline = gpd.GeoDataFrame({"geometry": [outline_polygon]}, crs=profile['crs'])
    outline_output_path = os.path.join(path, folder + '_outline_0.65.shp')
    gdf_outline.to_file(outline_output_path)
    print(f"Glacier outline polygon saved to {outline_output_path}")