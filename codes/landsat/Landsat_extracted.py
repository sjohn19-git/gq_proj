#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 14:33:45 2024

@author: sebinjohn
"""

import os
from tqdm import tqdm

# Define the directory containing .tar files
folder_path = "/Volumes/Sebins-HDD/Landsat7_c2l2"
os.chdir(folder_path)

files = [f for f in os.listdir(folder_path) if f.endswith('.tar') and not f.startswith('.')]

#os.makedirs(os.path.join(folder_path,"extracted"))


for file in tqdm(files):
    file_path=os.path.join(folder_path,file)
    ex_path=os.path.join(folder_path,"extracted")
    base_name = os.path.splitext(os.path.basename(file))[0]
    # Create the extraction folder
    extraction_folder = os.path.join(folder_path, base_name)
    os.makedirs(extraction_folder, exist_ok=True)
    os.system(f"tar -xf '{file_path}' -C '{extraction_folder}'")
    os.system(f"mv '{file_path}' '{ex_path}'")
