#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 19:19:55 2024

@author: sebinjohn
"""

import pandas as pd
import obspy
from scipy.signal import hilbert
import numpy as np
from obspy.signal.filter import envelope
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

col_data=pd.read_csv("/Users/sebinjohn/gq_proj/data/feature_extraction/col_data.csv")
pos_data=pd.read_csv("/Users/sebinjohn/gq_proj/data/feature_extraction/pos_data.csv")


col_data.shape

def calc_envelope(group):
    # Apply Hilbert transform to the 'value' column
    analytic_signal = hilbert(group['data'])
    group['analytic_signal'] = analytic_signal
    group['envelope'] = np.abs(analytic_signal)
    return group
    

ids_5k = col_data['ide'].value_counts()[col_data['ide'].value_counts() ==5000].index

col_data_fl = col_data[col_data['ide'].isin(ids_5k)]

processed_col = col_data_fl.groupby('ide').apply(calc_envelope)
processed_col.rename(columns={'ide': 'ide_col'}, inplace=True)

max_idx = processed_col.loc[(processed_col['Row'] >= 100) & (processed_col['Row'] <= 4900)].groupby('ide')['envelope'].idxmax()
# Extract 'ide', 'envelope', and 'start_time' for the max values
max_envelope_per_ide_col = processed_col.loc[max_idx, ['ide_col', 'envelope', 'time']].reset_index(drop=True)

max_envelope_per_ide_col['time'] = pd.to_datetime(max_envelope_per_ide_col['time'])


max_envelope_per_ide_col['year'] = max_envelope_per_ide_col['time'].dt.year
mean_envelope_per_year = max_envelope_per_ide_col.groupby('year')['envelope'].mean()

plt.figure(figsize=(10, 6))
mean_envelope_per_year.plot(kind='bar', color='skyblue')
plt.title('Mean Envelope Amplitude per Year')
plt.xlabel('Year')
plt.ylabel('Mean Envelope Amplitude')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



max_envelope_per_ide_col['month'] = max_envelope_per_ide_col['time'].dt.month
mean_envelope_per_mon = max_envelope_per_ide_col.groupby('month')['envelope'].mean()

plt.figure(figsize=(10, 6))
mean_envelope_per_mon.plot(kind='bar', color='skyblue')
plt.title('Mean Envelope Amplitude per Year')
plt.xlabel('Year')
plt.ylabel('Mean Envelope Amplitude')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


### calculate sum of envelop

sum_env_col=processed_col.loc[(processed_col['Row'] >= 100) & (processed_col['Row'] <= 4900)].groupby('ide')['envelope'].sum()
org_times = processed_col.groupby('ide')['org_time'].first()

sum_env_col_df = sum_env_col.reset_index(name='sum_envelope')
sum_env_col_df=sum_env_col_df.merge(org_times.reset_index(), on='ide')

sum_env_col_df["org_time"]=pd.to_datetime(sum_env_col_df["org_time"])

plt_time=mdates.date2num(sum_env_col_df["org_time"])

sum_env_col_df["plt_time"]=plt_time

sum_env_col_df['year'] = sum_env_col_df['org_time'].dt.year
sum_env_col_df['month'] = sum_env_col_df['org_time'].dt.month

monthly_avg = (
    sum_env_col_df.groupby(['year', 'month'])['sum_envelope']
    .mean()
    .reset_index()
)

monthly_avg['date'] = pd.to_datetime(monthly_avg[['year', 'month']].assign(day=1))


plt.figure(figsize=(12, 6))

# Plot the data
plt.plot(monthly_avg['date'], monthly_avg['sum_envelope'], marker='o', color='blue')

# Formatting
plt.grid(True)
plt.xlabel('Date')
plt.ylabel('Average Sum Envelope')
plt.title('Monthly Averages of Sum Envelope')
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # Label every month
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))  # Format date as Month Year
plt.xticks(rotation=45)
plt.grid(True)
# Display plot
plt.tight_layout()
plt.show()



ids=sum_env_col_df["ide"]

for idi in ids:

    # Filter data for ide == 300110
    data_300110 = processed_col.loc[idi]
    
    # Extract columns
    time = data_300110['Row']
    original_data = data_300110['data']
    analytic_signal_real = data_300110['analytic_signal'].apply(lambda x: x.real)
    analytic_signal_imag = data_300110['analytic_signal'].apply(lambda x: x.imag)
    envelop = data_300110['envelope']
    
    # Plot original data, Hilbert transform (analytic signal real part), and envelope
    plt.figure(figsize=(12, 6))
    
    # Plot original data
    plt.plot(time, original_data, label='Original Data', color='blue')
    
    # Plot real part of analytic signal (Hilbert transform)
    #plt.plot(time, analytic_signal_real, label='Hilbert Transform (Real)', color='orange', linestyle='dotted')
    #plt.plot(time, analytic_signal_imag, label='Hilbert Transform (Imaginary)', color='green', linestyle='dotted')
    
    #plt.plot(time, envelop, label='Envelope', color='red', linestyle='dashed')
    
    
    plt.plot(time, envelop, label='Envelope', color='red', linestyle='dashed')
    
    # Add labels, legend, and title
    plt.title('Original Data, Hilbert Transform, and Envelope (ide: 300110)')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)
    plt.xlim([100,4900])
    
    # Show the plot
    plt.show()


