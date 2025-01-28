#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 14:01:53 2024

@author: sebinjohn
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ast


col_power=pd.read_csv("/Users/sebinjohn/gq_proj/data/PSDs/col_power.csv")
pos_power=pd.read_csv("/Users/sebinjohn/gq_proj/data/PSDs/pos_power.csv")


# Convert 'org_time' to datetime
col_power['org_time'] = pd.to_datetime(col_power['org_time'])
pos_power['org_time'] = pd.to_datetime(pos_power['org_time'])

def extract_band_power(power_freq_df):
    # Extract the power in the bands 1-2 Hz, 2-3 Hz, 3-4 Hz
    power_band = []
    for _, row in power_freq_df.iterrows():
        freq_s = row['frequency']
        power_s = row['power']
        freq_l = ast.literal_eval(freq_s)
        power_l = ast.literal_eval(power_s)

        freq= np.array(freq_l)
        power = np.array(power_l)
        
        # Find indices for frequency bands
        band_1_2 = (freq >= 1) & (freq < 2)
        band_2_3 = (freq >= 2) & (freq < 3)
        band_3_4 = (freq >= 3) & (freq < 4)
        band_1_4 = (freq >= 1) & (freq < 4)
        
        # Calculate the average power in each band
        avg_power_1_2 = power[band_1_2].mean() if band_1_2.any() else 0
        avg_power_2_3 = power[band_2_3].mean() if band_2_3.any() else 0
        avg_power_3_4 = power[band_3_4].mean() if band_3_4.any() else 0
        avg_power_1_4 = power[band_1_4].mean() if band_1_4.any() else 0
        
        
        power_band.append([avg_power_1_2, avg_power_2_3, avg_power_3_4,avg_power_1_4])
    
    return power_band

col_band_powers = extract_band_power(col_power)
pos_band_powers = extract_band_power(pos_power)

# Add the band powers to the original DataFrame
col_power[['1-2 Hz', '2-3 Hz', '3-4 Hz','1-4 Hz']] = pd.DataFrame(col_band_powers, index=col_power.index)
pos_power[['1-2 Hz', '2-3 Hz', '3-4 Hz','1-4 Hz']] = pd.DataFrame(pos_band_powers, index=pos_power.index)

col_power['year'] = col_power['org_time'].dt.year
pos_power['year'] = pos_power['org_time'].dt.year




col_power_all_ev=col_power['1-4 Hz']
col_power_all_tim=col_power['org_time']

fig,ax=plt.subplots()
ax.scatter(col_power_all_tim,col_power_all_ev)







############
col_avg_power = col_power.groupby('year')[['1-2 Hz', '2-3 Hz', '3-4 Hz','1-4 Hz']].mean()
pos_avg_power = pos_power.groupby('year')[['1-2 Hz', '2-3 Hz', '3-4 Hz','1-4 Hz']].mean()




# Create a figure with subplots for each frequency band
fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)


axs[0].plot(col_avg_power.index, col_avg_power['1-4 Hz'], label='Columbia Glacier', marker='o')
axs[0].set_title('Average Power in 1-4 Hz Frequency Band')
axs[0].set_ylabel('Average Power (dB)')
axs[0].legend()

# Adjust layout for better spacing between subplots
axs[1].plot(pos_avg_power.index, pos_avg_power['1-4 Hz'], label='Post Glacier', marker='o')
axs[1].set_title('Average Power in 1-4 Hz Frequency Band')
axs[1].set_ylabel('Average Power (dB)')
axs[1].legend()

# Adjust layout for better spacing between subplots
plt.tight_layout()
axs[0].grid()
axs[1].grid()
axs[1].set_xticks(col_avg_power.index)
plt.show()


col_power['month'] = col_power['org_time'].dt.month
pos_power['month'] = pos_power['org_time'].dt.month

col_avg_monthly_power = col_power.groupby(['year', 'month'])[['1-2 Hz', '2-3 Hz', '3-4 Hz', '1-4 Hz']].mean()
pos_avg_monthly_power = pos_power.groupby(['year', 'month'])[['1-2 Hz', '2-3 Hz', '3-4 Hz', '1-4 Hz']].mean()

col_avg_monthly_power['year_month'] = col_avg_monthly_power.index.map(lambda x: f"{x[0]}-{x[1]:02d}")
pos_avg_monthly_power['year_month'] = pos_avg_monthly_power.index.map(lambda x: f"{x[0]}-{x[1]:02d}")



fig, axs = plt.subplots(2, 1, figsize=(10, 8))

# Plot for the Columbia Glacier data
axs[0].plot(col_avg_monthly_power['year_month'], col_avg_monthly_power['1-4 Hz'], label='Columbia Glacier', marker='o')
axs[0].set_title('Average Power in 1-4 Hz Frequency Band (Monthly)')
axs[0].set_ylabel('Average Power (dB)')
axs[0].legend()

# Plot for the Post Glacier data
axs[1].plot(pos_avg_monthly_power['year_month'], pos_avg_monthly_power['1-4 Hz'], label='Post Glacier', marker='o')
axs[1].set_title('Average Power in 1-4 Hz Frequency Band (Monthly)')
axs[1].set_xlabel('Year-Month')
axs[1].set_ylabel('Average Power (dB)')
axs[1].legend()

# Adjust layout for better spacing between subplots
plt.tight_layout()

# Add grid lines
axs[0].grid()
axs[1].grid()

# Set x-axis ticks every 6 months for both subplots
tick_indices = range(0, len(col_avg_monthly_power['year_month']),1 )  # Get indices every 6 months
axs[0].set_xticks([col_avg_monthly_power['year_month'].iloc[i] for i in tick_indices])
#axs[1].set_xticks([pos_avg_monthly_power['year_month'].iloc[i] for i in tick_indices])

# Rotate x-axis labels for readability
axs[1].tick_params(axis='x', rotation=45)
axs[0].tick_params(axis='x', rotation=45)

plt.show()

# Rotate x-axis labels for readability
#axs[1].tick_params(axis='x', rotation=45)
#axs[0].tick_params(axis='x', rotation=45)
