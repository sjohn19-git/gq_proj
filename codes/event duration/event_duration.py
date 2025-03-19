#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 17:20:19 2025

@author: sebinjohn
"""

import pandas as pd
import obspy
from scipy.signal import hilbert
import numpy as np
from obspy.signal.filter import envelope
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import random

col_data=pd.read_csv("/Users/sebinjohn/gq_proj/data/feature_extraction/col_data.csv")

col_data.shape

def calc_envelope(group):
    # Apply Hilbert transform to the 'value' column
    analytic_signal = hilbert(group['data'])
    group['analytic_signal'] = analytic_signal
    group['envelope'] = np.abs(analytic_signal)
    return group

def trim_data(group):
    if len(group) > 200:  # Ensure at least 200 points exist
        return group.iloc[100:-100]
    return group  # If less than 200 points remain, keep as is

#filter events with no gaps

ids_5k = col_data['ide'].value_counts()[col_data['ide'].value_counts() ==5000].index

col_data_fl = col_data[col_data['ide'].isin(ids_5k)]

processed_col = col_data_fl.groupby('ide').apply(trim_data)
processed_col.rename(columns={'ide': 'ide_col'}, inplace=True)
processed_col = processed_col.groupby('ide').apply(calc_envelope)
processed_col = processed_col.droplevel(0)










idi = 300110
data_300110 = processed_col.loc[idi]
time = data_300110['Row']
original_data = data_300110['data']
analytic_signal_real = data_300110['analytic_signal'].apply(lambda x: x.real)
analytic_signal_imag = data_300110['analytic_signal'].apply(lambda x: x.imag)
envelop = data_300110['envelope']
std=envelop.std()


mask = envelop > 1.5*std
st= time[mask].values[0]
en = time[mask].values[-1]

# Plot original data, Hilbert transform (analytic signal real part), and envelope
plt.figure(figsize=(12, 6))

plt.plot(time, original_data, label='Original Data', color='blue')
plt.plot(time, envelop, label='Envelope', color='red', linestyle='dashed')
plt.axhline(std)
plt.fill_between(time, max(envelop), min(envelop), where=mask, color='green', alpha=0.3, label='Above Std Dev')
plt.axvspan(st, en, color='green', alpha=0.3, label='Above Std Dev')
plt.title('Original Data, Hilbert Transform, and Envelope (ide: 300110)')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
#plt.xlim([100,4900])

random_idis = random.sample(processed_col.index.get_level_values('ide').unique().tolist(), 100)

# Loop over each random 'idi' and plot
for idi in random_idis:
    data = processed_col.loc[idi]
    time = data['Row']
    original_data = data['data']
    envelop = data['envelope']
    std = envelop.std()

    # Mask for the envelope greater than 1.5 times the standard deviation
    mask = envelop > 3 * std
    st = time[mask].values[0]  # Start time of mask
    en = time[mask].values[-1]  # End time of mask

    # Plotting the data for each 'idi'
    plt.figure(figsize=(12, 6))
    plt.plot(time, original_data, label='Original Data', color='blue')
    plt.plot(time, envelop, label='Envelope', color='red', linestyle='dashed')
    plt.axhline(3*std)
    plt.fill_between(time, max(envelop), min(envelop), where=mask, color='green', alpha=0.3, label='Above Std Dev')
    plt.axvspan(st, en, color='green', alpha=0.3, label='Above Std Dev')
    
    plt.title(f'Original Data, Hilbert Transform, and Envelope (ide: {idi})')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)
    # Optional xlim if needed
    # plt.xlim([100,4900])
    
    # Show the plot for each 'idi'
    plt.show()