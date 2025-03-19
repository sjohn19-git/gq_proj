import ee
import datetime
from qgis.core import QgsRasterLayer, QgsProject
from ee_plugin import Map  # GEE QGIS plugin

# Authenticate and Initialize GEE
ee.Initialize()

target_date = datetime.datetime(2009, 5, 15)
date_range = 20  # ±30 days around target date
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
    "Sentinel-2": "COPERNICUS/S2",
    "ASTER": "ASTER/AST_L1T_003"
}

# Define Area of Interest (AOI) - Columbia Glacier, Alaska
columbia_glacier_center = ee.Geometry.Point([-147.1, 61.1])
aoi = columbia_glacier_center.buffer(5000)  # 5 km buffer

# Define band combinations
band_map = {
    "Landsat 4": ['B4', 'B3', 'B2'],  # Landsat RGB
    "Landsat 5": ['B4', 'B3', 'B2'],
    "Landsat 7": ['B4', 'B3', 'B2'],
    "Landsat 8": ['B4', 'B3', 'B2'],
    "Landsat 9": ['B4', 'B3', 'B2'],
    "Sentinel-1": ['VV', 'VH'],  # Sentinel-1 SAR bands
    "Sentinel-2": ['B4', 'B3', 'B2'],  # Sentinel-2 RGB
    "ASTER": ['B3N', 'B02', 'B01']  # ASTER RGB (VNIR Bands)
}

def get_closest_images(collection_id, start_date, end_date, aoi, band_list):
    collection = ee.ImageCollection(collection_id) \
        .filterBounds(aoi) \
        .filterDate(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')) \
        .sort('system:time_start', True)  # Sort by date

    image_list = collection.toList(collection.size()) 

    if image_list.size().getInfo() == 0:
        print("No image found", collection_id)
        return None, None

    # Fetch the first image only
    try:
        image = ee.Image(image_list.get(0))
    except:
        return None, None
    timestamp = image.get('system:time_start')
    timestamp_ms = timestamp.getInfo()
    date = datetime.datetime.utcfromtimestamp(timestamp_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')

    vis_params = {
        'bands': band_list,
        'min': 0, 
        'max': 30000, 
        'gamma': 1.4
    }

    # Handle Sentinel-1 separately (SAR visualization)
    if "Sentinel-1" in collection_id:
        vis_params = {'bands': band_list, 'min': -25, 'max': 0}

    # Handle ASTER separately (scale correction)
    if "ASTER" in collection_id:
        vis_params = {'bands': band_list, 'min': 0, 'max': 255}

    return image, vis_params, date

# Fetch first image from each collection
for name, coll_id in collections.items():
    band_list = band_map.get(name, ['B4', 'B3', 'B2'])
    image, vis_params, date = get_closest_images(coll_id, start_date, end_date, aoi, band_list)

    if image:
        # Add the first image to QGIS
        map_id = image.getMapId(vis_params)
        tile_url = map_id['tile_fetcher'].url_format
        layer = QgsRasterLayer(f"type=xyz&url={tile_url}", f"{name} {date}", "wms")
        QgsProject.instance().addMapLayer(layer)
        print(f"Loaded {name} image into QGIS.")
