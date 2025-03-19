#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 08:54:05 2024

@author: sebinjohn
"""

import os
from eodag import EODataAccessGateway, setup_logging
from datetime import datetime
import pandas as pd



setup_logging(0)

config_file = "/Volumes/Sebins-HDD/Landsat7_c2l2/eodag_landsat_config.yaml"
dag = EODataAccessGateway(config_file)


search_results= dag.search_all(
    productType='LANDSAT_C2L2',
    geom={'lonmin': -147.3239, 'latmin': 61.0795, 'lonmax': -146.8707, 'latmax': 61.2650},
    start='2010-01-01',
    end='2011-12-21',
    count=True
)


flt=search_results.filter_property(cloudCover=30, operator="lt")


for product in flt:
    print(product)