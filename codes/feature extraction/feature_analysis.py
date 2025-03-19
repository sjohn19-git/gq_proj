#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 13:46:21 2024

@author: sebinjohn
"""

import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
from tsfresh import select_features
from tsfresh.utilities.dataframe_functions import impute




col_data=pd.read_csv("/Users/sebinjohn/gq_proj/data/feature_extraction/col_data.csv")
col_features=pd.read_csv("/Users/sebinjohn/gq_proj/data/feature_extraction/col_features.csv")

pos_data=pd.read_csv("/Users/sebinjohn/gq_proj/data/feature_extraction/pos_data.csv")
pos_features=pd.read_csv("/Users/sebinjohn/gq_proj/data/feature_extraction/pos_features.csv")



col_features = col_features.rename(columns={'Unnamed: 0': 'ide'})
col_data['start_time'] = pd.to_datetime(col_data['start_time'])

col_data_drop = col_data.drop_duplicates(subset=['ide', 'start_time'])

col_fmer = pd.merge(
    col_features,
    col_data_drop,
    on='ide'
)



pos_features = pos_features.rename(columns={'Unnamed: 0': 'ide'})

pos_data['start_time'] = pd.to_datetime(pos_data['start_time'])
pos_data_drop = pos_data.drop_duplicates(subset=['ide', 'start_time'])


###merge_features and identify relavent fetures algrothimically

features=pd.concat([col_features,pos_features], axis=0, ignore_index=True)
feature_ide=pd.concat([col_features,pos_features], axis=0, ignore_index=False)['ide']

y =np.hstack([np.ones(len(col_features)), np.zeros(len(pos_features))])

impute(features)

features_filtered = select_features(features, y)

feature_ide = feature_ide.reset_index(drop=True)

features_filtered['ide']=feature_ide

merged_col = pd.merge(features_filtered, col_data_drop[['ide', 'start_time']], on='ide', how='left')

# Merge features_filtered with pos_data_drop based on 'ide'
merged_pos = pd.merge(features_filtered, pos_data_drop[['ide', 'start_time']], on='ide', how='left')

features_filtered['start_time'] = merged_col['start_time'].combine_first(merged_pos['start_time'])



###plotting
columns_to_plot = [col for col in features_filtered.columns if col not in ['start_time', 'ide']][:]
#columns_to_plot=["data__spkt_welch_density__coeff_5"]

# Use tqdm to add a progress bar
for column in tqdm(columns_to_plot, desc="Plotting first 10 columns"):
    plt.figure(figsize=(10, 5))

    mask = y == 0# Create a new figure
    plt.scatter(features_filtered['start_time'][~mask], features_filtered[column][~mask], label=f"{column}", alpha=0.7)
    plt.scatter(features_filtered['start_time'][mask], features_filtered[column][mask], label=f"{column}", color='orange', alpha=0.7)
    plt.title(f"{column} vs Time")
    plt.xlabel("Time")
    plt.ylabel(column)
    plt.legend()
    plt.grid(True)
    plt.show()
        