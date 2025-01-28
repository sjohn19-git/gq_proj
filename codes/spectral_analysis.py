#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 11:41:24 2024

@author: sebinjohn
"""

import pandas as pd
from scipy.fft import fft, fftfreq
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

col_data=pd.read_csv("/Users/sebinjohn/gq_proj/data/feature_extraction/col_data.csv")

pos_data=pd.read_csv("/Users/sebinjohn/gq_proj/data/feature_extraction/pos_data.csv")



grouped_col = col_data.groupby('ide')

# Sample rate (Hz)
sample_rate = 50.0

spectra_df_col = pd.DataFrame()
for ide, group in grouped_col:
    # Extract the 'data' values
    data_values = group['data'].values[23*50:76*50]

    # Compute the FFT
    n = len(data_values)  # Number of samples
    fft_values = fft(data_values)
    fft_magnitudes = np.abs(fft_values[:n // 2])  # Keep positive frequencies

    # Compute the frequencies
    frequencies = fftfreq(n, d=1/sample_rate)[:n // 2]

    # Create a DataFrame for this ide's spectral features
    ide_spectra = pd.DataFrame({
        'frequency': frequencies,
        'magnitude': fft_magnitudes,
        'ide': ide
    })

    # Append to the main spectra DataFrame
    spectra_df_col = pd.concat([spectra_df_col, ide_spectra], ignore_index=True)

# Preview the resulting spectra DataFrame
print(spectra_df_col)


grouped_pos = pos_data.groupby('ide')

# Sample rate (Hz)
sample_rate = 50.0

spectra_df_pos = pd.DataFrame()
for ide, group in grouped_pos:
    # Extract the 'data' values
    data_values = group['data'].values[23*50:76*50]

    # Compute the FFT
    n = len(data_values)  # Number of samples
    fft_values = fft(data_values)
    fft_magnitudes = np.abs(fft_values[:n // 2])  # Keep positive frequencies

    # Compute the frequencies
    frequencies = fftfreq(n, d=1/sample_rate)[:n // 2]

    # Create a DataFrame for this ide's spectral features
    ide_spectra = pd.DataFrame({
        'frequency': frequencies,
        'magnitude': fft_magnitudes,
        'ide': ide
    })

    # Append to the main spectra DataFrame
    spectra_df_pos = pd.concat([spectra_df_pos, ide_spectra], ignore_index=True)

# Preview the resulting spectra DataFrame
print(spectra_df_pos)

def compute_average_power(spectra_df, original_data,freq_min,freq_max):
    # Filter for frequencies between 1 and 3 Hz
    spectra_filtered = spectra_df[
        (spectra_df['frequency'] >= freq_min) & (spectra_df['frequency'] <= freq_max)
    ]

    # Compute the average magnitude for each 'ide'
    avg_power = spectra_filtered.groupby('ide')['magnitude'].mean().reset_index()
    avg_power.rename(columns={'magnitude': 'avg_power'}, inplace=True)

    # Merge with the original data to get the start_time
    avg_power_with_time = pd.merge(
        avg_power,
        original_data[['ide', 'time']].drop_duplicates(),
        on='ide',
        how='left'
    )
    return avg_power_with_time

freq_min,freq_max=1,4
avg_power_col = compute_average_power(spectra_df_col, col_data,freq_min,freq_max)
avg_power_pos = compute_average_power(spectra_df_pos, pos_data,freq_min,freq_max)


avg_power_col['time'] = pd.to_datetime(avg_power_col['time'])
avg_power_pos['time'] = pd.to_datetime(avg_power_pos['time'])



############# Add year columns

avg_power_col['year'] = avg_power_col['time'].dt.year
avg_power_pos['year'] = avg_power_pos['time'].dt.year

# Group by year and calculate the mean
yearly_avg_col = avg_power_col.groupby('year')['avg_power'].mean().reset_index()
yearly_avg_pos = avg_power_pos.groupby('year')['avg_power'].mean().reset_index()

# Plot the results
plt.figure(figsize=(12, 6))

# Plot for Glacier 1 (col_data)
plt.plot(yearly_avg_col['year'], yearly_avg_col['avg_power'], label='Glacier 1', color='blue', marker='o')

# Plot for Glacier 2 (pos_data)
plt.plot(yearly_avg_pos['year'], yearly_avg_pos['avg_power'], label='Glacier 2', color='orange', marker='o')

# Plot settings
plt.title('Yearly Average Spectral Power ({}-{} Hz)'.format(freq_min, freq_max))
plt.xlabel('Year')
plt.ylabel('Average Spectral Power')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show plot
plt.show()

###################################Year###############

######################Month###############

# Resample data by month and calculate the monthly average


avg_power_col['month_year'] = avg_power_col['time'].dt.strftime('%b %Y')
avg_power_pos['month_year'] = avg_power_col['time'].dt.strftime('%b %Y')

# Group by year and calculate the mean
my_avg_col = avg_power_col.groupby('month_year')['avg_power'].mean().reset_index()
my_avg_pos = avg_power_pos.groupby('month_year')['avg_power'].mean().reset_index()

my_avg_col['month_year'] = pd.to_datetime(my_avg_col['month_year'], format='%b %Y')
my_avg_pos['month_year'] =pd.to_datetime(my_avg_pos['month_year'], format='%b %Y')

my_avg_col=my_avg_col.sort_values(by='month_year')
my_avg_pos=my_avg_pos.sort_values(by='month_year')

plt.figure(figsize=(12, 6))

# Plot for Glacier 1 (col_data)
plt.plot(my_avg_col['month_year'], my_avg_col['avg_power'], label='Columbia', color='blue', marker='o')

start_date = my_avg_col['month_year'].iloc[0]
end_date = my_avg_col['month_year'].iloc[-1]

plt.title('Monthly Average Spectral Power ({}-{} Hz) from {} to {}'.format(freq_min, freq_max, start_date, end_date))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # Label every month
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))  # Format date as Month Year

# Plot settings
plt.xlabel('Month')
plt.ylabel('Average Spectral Power')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Show plot
plt.show()

######################Month###############