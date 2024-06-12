#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 13:22:18 2024
@author: sknoel
"""

import os
os.chdir("/home/sjohn/gq_proj/codes/Database2Python_Tools")
import numpy as np
import pandas as pd

# Created Modules
from database2python.Antelope2Python import event_dataframe



##-----INPUTS-----##
start_year = 1988
end_year = 2024

##----------------##




# Local path to AEC annual database foler
dbpath = '/aec/db/catalogs/final/yearly'

catalog_years = np.arange(start_year, (end_year+1), step=1)

annual_catalog = pd.DataFrame()
for year in catalog_years:
    catalog_df = event_dataframe(os.path.join(dbpath, ('catalog_' + str(year)) ))
    annual_catalog = pd.concat([annual_catalog, catalog_df])

os.chdir("/home/sjohn/gq_proj/data")
annual_catalog.to_csv('eq_catalog_1988-2024.csv', index=False) 

glacial_quakes = annual_catalog.loc[annual_catalog.etype == 'G']