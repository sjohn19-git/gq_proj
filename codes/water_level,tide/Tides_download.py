#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 13:04:19 2024

@author: sebinjohn
"""
import numpy as np
import requests
import os
import pandas as pd
import glob
from datetime import datetime

# Define the range of years and months for the data retrieval
years = np.arange(2005, 2023, 1)
months = np.arange(1, 13, 1)

# Create an output folder for saving the downloaded tide data
output_folder = "/Users/sebinjohn/gq_proj/data/tide_predictions"
os.makedirs(output_folder, exist_ok=True)

# Loop through each year and month to retrieve tide data
for year in years:
    for month in months:
        # Format month with leading zero if needed
        month_str = f"{month:02d}"
        
        # Define start date for each month
        begin_date = f"{year}{month_str}01"
        
        # Determine the last day of the month
        last_day = (datetime(year, month % 12 + 1, 1) - pd.Timedelta(days=1)).day
        end_date = f"{year}{month_str}{last_day:02d}"
        
        # Construct the API URL for tide predictions with updated parameters
        api = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?"
        params = (f"product=predictions&application=NOS.COOPS.TAC.WL&begin_date={begin_date}&"
                  f"end_date={end_date}&datum=MLLW&station=9454240&time_zone=GMT&"
                  f"units=metric&interval=h&format=csv")
        
        url = api + params
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            file_path = os.path.join(output_folder, f"tide_{year}_{month_str}.csv")
            with open(file_path, "wb") as file:
                file.write(response.content)
                print(f"Tide data for {year}-{month_str} saved to {file_path}")
        else:
            print(f"Failed to retrieve tide data for {year}-{month_str}")

# Merge the downloaded monthly tide data files into one file
input_folder = "/Users/sebinjohn/gq_proj/data/tide_predictions"  
output_file = "/Users/sebinjohn/gq_proj/data/tide_predictions/merged_tide_predictions.csv"

all_files = glob.glob(os.path.join(input_folder, "*.csv"))
all_files.sort()

df_list = []
# Loop through the files and append them to the list
for filename in all_files:
    df = pd.read_csv(filename)  # Read each file as a DataFrame
    df_list.append(df)

# Concatenate all DataFrames into a single DataFrame
merged_df = pd.concat(df_list, ignore_index=True)

# Save the merged DataFrame to a CSV file
merged_df.to_csv(output_file, index=False)
print(f"All tide predictions data merged into {output_file}")      
