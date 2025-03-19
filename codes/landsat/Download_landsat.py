#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 00:47:31 2024

@author: sebinjohn
"""




import os
from eodag import EODataAccessGateway, setup_logging
from datetime import datetime
import pandas as pd

csv=pd.read_csv("~/Downloads/landsat_ot_c2_l2_672e7653be119fdf.csv",encoding='ISO-8859-1')

setup_logging(0)

config_file = "config.yaml"
dag = EODataAccessGateway(config_file)

search_results, total_count = dag.search(
    productType='LANDSAT_C2L2',
    geom={'lonmin': 1.5, 'latmin': 43.5, 'lonmax': 2, 'latmax': 44},
    start='2023-01-01',
    end='2023-01-05',
)

search_results


for i in range(len(search_results)):
    product = search_results
    product_path = product.download()
    print(product_path)




