#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 19:05:52 2024

@author: sebinjohn
"""

import os
import glob
import shutil
from tqdm import tqdm
import tarfile


os.chdir("/Volumes/Sebins-HDD/Landsat8:9_c2l2/")
destination_path="/Volumes/Sebins-HDD/Landsat8:9_c2l2/"

files = [f for f in os.listdir() if os.path.isfile(f)]


def get_base_name(file):
    # Find the position of 'T1' and extract the base name up to that point
    return file.split('T1')[0] + 'T1'

for i in tqdm(range(len(files))): 
    file=files[i]
    dir_name = get_base_name(file)
    full_dir_path = os.path.join(destination_path, dir_name)
    if not os.path.exists(full_dir_path):
        os.makedirs(dir_name)
    try:
        shutil.move(os.path.join(destination_path, file), os.path.join(full_dir_path, file))
        print(f"Moved {file} to {full_dir_path}")
    except:
        pass


tars=glob.glob("/Volumes/Sebins-HDD/Landsat8:9_c2l2/*/*.tar")
for i in tqdm(range(len(tars))):
    tar_path=tars[i]
    extract_path = os.path.dirname(tar_path)
    
    extract_command = f"tar -xf '{tar_path}' -C '{extract_path}'"
    delete_command = f"rm '{tar_path}'"  # Command to delete the .tar file after extraction
    
    # Execute the extract command
    os.system(extract_command)
    print(f"Extracted {tar_path} to {extract_path}")
    
    # Execute the delete command
    os.system(delete_command)
    print(f"Deleted {tar_path}")
    
    
    
    
def rename_folders(directory):
    # Iterate through each folder in the directory
    for folder_name in os.listdir(directory):
        folder_path = os.path.join(directory, folder_name)
        
        # Ensure it is a directory
        if os.path.isdir(folder_path) and "T2" in folder_name:
            # Rename folder
            new_name = folder_name.split('T2')[0] + 'T2'
            new_path = os.path.join(directory, new_name)
            if os.path.exists(new_path):
                print(f'Skipping: "{folder_name}" -> "{new_name}" (Target name exists)')
                continue
            if new_name != folder_name:  # Avoid renaming to the same name
                os.rename(folder_path, new_path)
                print(f'Renamed: "{folder_name}" -> "{new_name}"')

rename_folders(destination_path)    


for folder_name in os.listdir(destination_path):
    folder_path = os.path.join(destination_path, folder_name)
    if os.path.isdir(folder_path) and "T2" in folder_name and not folder_name.endswith("T2") and not folder_name.startswith("."):
        print(folder_name)
        item_path=os.path.join(folder_path,os.path.basename(folder_path).split('T1')[0])
        dest_path=os.path.join(destination_path,folder_name.split('T2')[0] + 'T2')
        shutil.move(item_path, dest_path)
    
for folder_name in os.listdir(destination_path):
    folder_path = os.path.join(destination_path, folder_name)
    if os.path.isdir(folder_path) and "T2" in folder_name and not folder_name.endswith("T2") and not folder_name.startswith("."):
        dire=os.path.join(destination_path,folder_name)
        if not os.listdir(folder_path):  # Check if the directory is empty
            os.rmdir(folder_path)  # Delete the empty directory
            print(f'Deleted empty directory: {folder_path}')
        else:
            print(f'Not empty: {folder_path}')