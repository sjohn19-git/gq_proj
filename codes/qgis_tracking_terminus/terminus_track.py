import ee
import datetime
from qgis.core import QgsRasterLayer, QgsProject
import urllib.request
from qgis.core import QgsCoordinateReferenceSystem
import zipfile
import glob
import os
import shutil
from osgeo import gdal

# Authenticate and Initialize GEE
ee.Initialize()

target_date = datetime.datetime(2010, 3, 15)

#delete()


date_range = 30  # Search ±10 days around target date
start_date = target_date - datetime.timedelta(days=date_range)
end_date = target_date + datetime.timedelta(days=date_range)

# List of Image Collections
collections = {
    "Landsat 4": "LANDSAT/LT04/C02/T1_TOA",
    "Landsat 5": "LANDSAT/LT05/C02/T1_TOA",
    "Landsat 7": "LANDSAT/LE07/C02/T1_TOA",
    "Landsat 8": "LANDSAT/LC08/C02/T1_TOA",
    "Landsat 9": "LANDSAT/LC09/C02/T1_TOA",
    "Sentinel-1": "COPERNICUS/S1_GRD",
    "Sentinel-2": "COPERNICUS/S2"
}

# Define Area of Interest (AOI) - Columbia Glacier, Alaska
columbia_glacier_center = ee.Geometry.Point([-147.1, 61.1])
aoi = columbia_glacier_center.buffer(5000)  # 5 km buffer

# Define band combinations
band_map = {
    "ASTER": ['B3N', 'B02', 'B01'],  # ASTER RGB
    "Landsat 4": ['B4', 'B3', 'B2'],  # Landsat RGB
    "Landsat 5": ['B4', 'B3', 'B2'],
    "Landsat 7": ['B4', 'B3', 'B2'],
    "Landsat 8": ['B4', 'B3', 'B2'],
    "Landsat 9": ['B4', 'B3', 'B2'],
    "Sentinel-1": ['VV', 'VH'],  # Sentinel-1 SAR bands
    "Sentinel-2": ['B4', 'B3', 'B2'],  # Sentinel-2 RGB
}

# Function to get the closest image and display in QGIS
def get_closest_image(collection_id, start_date, end_date, aoi, band_list):
    collection = ee.ImageCollection(collection_id) \
        .filterBounds(aoi) \
        .filterDate(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')) \
        .sort('system:time_start', True)  # Sort by closest date

    first_image = collection.first()
    # Get the date associated with the first image
    if first_image.getInfo() is None:
        return None,None  # No image found, return None
    
    timestamp = first_image.get('system:time_start')
    timestamp_ms = timestamp.getInfo() 
    date = datetime.datetime.utcfromtimestamp(timestamp_ms/ 1000).strftime('%Y-%m-%d %H:%M:%S')
    #crs = first_image.projection().getInfo()
    # Handle Sentinel-1 separately (SAR visualization)
    if "Sentinel-1" in collection_id:
        return first_image.select(band_list).visualize(min=-25, max=0),date  # Adjust for SAR
    if "ASTER" in collection_id:
        return first_image.select(band_list).visualize(min=0, max=255),date
    # General visualization for optical images
    return first_image.visualize(bands=band_list),date

# Fetch closest image from each collection
dates=[]
selected_images = {}
for name, coll_id in collections.items():
    band_list = band_map.get(name, ['B4', 'B3', 'B2'])  # Default to Landsat bands
    image,date= get_closest_image(coll_id, start_date, end_date, aoi, band_list)
    if image:
        dates.append(date)
        selected_images[name] = image
        
dates_dt = [datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in dates]
date_differences = [abs(target_date - date) for date in dates_dt]
sorted_dates = [date for _, date in sorted(zip(date_differences, dates), key=lambda x: x[0])]
sorted_images = {key: selected_images[key] for key in sorted(selected_images, key=lambda k: date_differences[list(selected_images.keys()).index(k)])}


def dwnld(name,imge,dates_t):
    try:
        download_url = image.getDownloadURL({'scale': 90,'region': image.geometry()})
        file_path = '/Users/sebinjohn/Downloads/tmp/columbia_terminus_image.zip'  # Update with your desired local file path
        urllib.request.urlretrieve(download_url, file_path)
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall('/Users/sebinjohn/Downloads/tmp/')
            
        raster_files=glob.glob('/Users/sebinjohn/Downloads/tmp/*.tif')
        raster_files = sorted(raster_files, key=lambda x: (('red' not in x.lower(), 
                                                    'green' not in x.lower(), 
                                                    'blue' not in x.lower())))
        vrt_output = os.path.join('/Users/sebinjohn/Downloads/tmp/',"landsat_selected_bands.vrt")
        
        gdal.BuildVRT(vrt_output, raster_files,options=["-separate"])
        
        vrt_ds = gdal.Open(vrt_output)
        vrt_layer = QgsRasterLayer(vrt_output, name+" "+dates_t)
        
        QgsProject.instance().addMapLayer(vrt_layer)
            
        print(f"Loaded {name} image into QGIS.")
    except Exception as e:
        print(f"Failed to load {name}: {e}")
print(f"{len(sorted_images)} Images found")
c=0
name, image = list(sorted_images.items())[c]
dwnld(name,image,sorted_dates[c])




