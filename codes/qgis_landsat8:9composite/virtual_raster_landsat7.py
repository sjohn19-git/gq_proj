#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 15:05:54 2024

@author: sebinjohn
"""

from osgeo import gdal
import os
import glob
from tqdm import tqdm
gdal.UseExceptions() 

landsat_folder = "/Volumes/Sebins-HDD/Landsat7_c2l2"  # Change this to your Landsat 7 folder

# List all subdirectories in the Landsat folder (each folder represents a Landsat scene)
folders = [folder for folder in os.listdir(landsat_folder) if os.path.isdir(os.path.join(landsat_folder, folder)) and not folder.startswith(".")]

bands_of_interest = ['B3', 'B2', 'B1']



for folder in tqdm(folders):
    print(folder)
    os.chdir(os.path.join(landsat_folder, folder))
    raster_files = [os.path.join(os.getcwd(), f) for f in os.listdir(os.getcwd())
                    if any(band in f for band in bands_of_interest) and f.endswith('.TIF')
                    and not f.startswith(".")]
    raster_files.sort(key=lambda x: bands_of_interest.index(next(band for band in bands_of_interest if band in x)))
    
    vrt_output = os.path.join(os.getcwd(),folder+".vrt")
    vrt_dataset = gdal.BuildVRT(vrt_output, raster_files,options=["-separate"])
