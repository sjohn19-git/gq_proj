#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 22:42:39 2024

@author: sebinjohn
"""

import numpy as np
import requests
import os
import pandas as pd
import glob


years=np.arange(2005,2023,1)

output_folder = "/Users/sebinjohn/gq_proj/data/water_level"
os.makedirs(output_folder, exist_ok=True) 

for year in years:
    api="https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?"
    dat="product=hourly_height&application=NOS.COOPS.TAC.WL&begin_date="
    metdat="{0}0101&end_date={0}1231&datum=MLLW&station=9454240".format(year)
    tail="&time_zone=GMT&units=english&format=csv"
    
    url=api+dat+metdat+tail
    response = requests.get(url)
    
    if response.status_code == 200:
        file_path = os.path.join(output_folder, f"wl_{year}.csv")
        with open(file_path, "wb") as file:
            file.write(response.content)
            print(f"Data for {year} saved to {file_path}")
    else:
        print(f"Failed to retrieve data for {year}")
        
        
input_folder="/Users/sebinjohn/gq_proj/data/water_level"  
output_file="/Users/sebinjohn/gq_proj/data/water_level/merged_level.csv" 
        
all_files = glob.glob(os.path.join(input_folder, "*.csv"))

all_files.sort()


df_list = []
# Loop through the files and append them to the list
for filename in all_files:
    df = pd.read_csv(filename)  # Read each file as a DataFrame
    df_list.append(df) 

merged_df = pd.concat(df_list, ignore_index=True)

merged_df.to_csv(output_file, index=False)       
        