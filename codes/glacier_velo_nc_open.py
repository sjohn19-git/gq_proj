#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 11:03:19 2024

@author: sebinjohn
"""

import netCDF4 as nc



ds=nc.Dataset("/Users/sebinjohn/gq_proj/data/Glacier_velocity/ITS_LIVE_velocity_120m_RGI01A_0000_v02.nc")

# Access the variable 'v' and its attributes
if 'v' in ds.variables:
    v_var = ds.variables['v']
    print("Variable 'v' found:")
    print(f"Dimensions: {v_var.dimensions}")
    print(f"Shape: {v_var.shape}")
    print("Attributes:")
    for attr in v_var.ncattrs():
        print(f"  {attr}: {getattr(v_var, attr)}")
else:
    print("Variable 'v' not found.")


# Extract the variable 'v'
v_var_data = ds.variables['v'][:]

# Extract the coordinate variables 'x' and 'y'
x = ds.variables['x'][:] 
y = ds.variables['y'][:]  
#this is not a lat lon. 
#this is projection: 3413



ds.close()