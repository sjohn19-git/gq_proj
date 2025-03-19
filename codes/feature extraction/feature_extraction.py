#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 11:28:09 2024

@author: sebinjohn
"""
import matplotlib.pyplot as plt
from tsfresh import extract_features
from tsfresh import select_features
from tsfresh.utilities.dataframe_functions import impute  
import pandas as pd  
  

from tsfresh.examples.robot_execution_failures import download_robot_execution_failures, \
    load_robot_execution_failures
download_robot_execution_failures()
timeseries, y = load_robot_execution_failures()  

col_data=pd.read_csv("/Users/sebinjohn/gq_proj/data/feature_extraction/col_data.csv")

col_data_f=col_data[['ide','data']]

extracted_features = extract_features(col_data_f, column_id="ide")

extracted_features.to_csv("/Users/sebinjohn/gq_proj/data/feature_extraction/col_features.csv") 


pos_data=pd.read_csv("/Users/sebinjohn/gq_proj/data/feature_extraction/pos_data.csv")

pos_data_f=pos_data[['ide','data']]

extracted_features_pos = extract_features(pos_data_f, column_id="ide")

extracted_features_pos.to_csv("/Users/sebinjohn/gq_proj/data/feature_extraction/pos_features.csv") 
