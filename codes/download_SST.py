#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 11:24:46 2025

@author: sebinjohn
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 11:24:46 2025

@author: sebinjohn
"""

import earthaccess
import xarray as xr
import os
from tqdm import tqdm
from datetime import datetime
from datatree import DataTree
import time

def download_and_process_sst_data():
    try:
        # Authenticate with Earthdata
        auth = earthaccess.login()
        if not auth.authenticated:
            auth = earthaccess.login(strategy="all")
        if auth.authenticated:
            print("Authentication successful!")
        else:
            print("Authentication unsuccessful")
            return

        # Search for the granule by the name and provider
        search_results = earthaccess.search_data(
            short_name="MUR-JPL-L4-GLOB-v4.1",
            provider="POCLOUD",
            temporal=("2005-01", "2024-12")
        )

        # Define region of interest
        min_lon = -147.66504
        min_lat = 60.2182
        max_lon = -146.38184
        max_lat = 61.32974

        for granule in tqdm(search_results):
            fname = str(granule).split("/")[-1]
            datet = fname.split("-")[0]
            dt_object = datetime.strptime(datet, '%Y%m%d%H%M%S')
            fn = dt_object.strftime('%Y-%m-%dT%H%M')
            output_file_path = f"/Users/sebinjohn/gq_proj/data/SST/{fn}.nc"

            if not os.path.exists(output_file_path):
                print(f"Processing: {output_file_path}")
                files_array = earthaccess.open([granule])
                file = files_array[0]  # Get the first file (granule)

                # Open the dataset and process it
                ds = xr.open_dataset(file)
                dt = DataTree(ds)
                dt = dt.sel(lat=slice(min_lat, max_lat), lon=slice(min_lon, max_lon))
                dataset = dt.to_dataset()

                for var in dataset.variables:
                    dataset[var].encoding = {'dtype': 'float64'}  # Ensure dtype is float64
                dataset.to_netcdf(output_file_path)
                print(f"Saved: {output_file_path}")
                
        print("Processing complete.")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        raise  # Re-raise the exception to be caught in the restart logic

if __name__ == "__main__":
    while True:
        try:
            download_and_process_sst_data()
            break  # Exit loop if the function completes successfully
        except Exception as e:
            print("Restarting script due to an error...")
            time.sleep(10) 






#########

# file_path="/Users/sebinjohn/gq_proj/data/SST/2025-01-01T0900.nc"
# dataset = xr.open_dataset(file_path)

# # Access the specific variable (e.g., "analysed_sst")
# sst_data = dataset["analysed_sst"]

# # Check the shape and size of the dataset
# print(f"Shape of the dataset: {sst_data.shape}")  # Get the shape of the variable
# print(f"Size of the dataset in bytes: {sst_data.nbytes}")  # Size in bytes

# # Create a plot with Cartopy (PlateCarree projection)
# fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})

# # Plot the data with a color map (e.g., 'viridis')
# sst_data.plot(ax=ax, cmap='viridis')

# # Set the spatial extent (modify based on your data)
# min_lon, max_lon = sst_data.lon.min().values, sst_data.lon.max().values
# min_lat, max_lat = sst_data.lat.min().values, sst_data.lat.max().values

# ax.set_extent([min_lon,max_lon, min_lat, max_lat], crs=ccrs.PlateCarree())

# # Add coastlines and other map features
# ax.coastlines()
# ax.set_xticks([min_lon, max_lon], crs=ccrs.PlateCarree())
# ax.set_yticks([min_lat, max_lat], crs=ccrs.PlateCarree())
# ax.plot(-147.08463, 61.09027, marker='o', color='red', markersize=5, transform=ccrs.PlateCarree())

# # Show the plot
# plt.show()




