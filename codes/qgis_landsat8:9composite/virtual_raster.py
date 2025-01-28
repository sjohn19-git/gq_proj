from osgeo import gdal
import os
import glob
from tqdm import tqdm

landsat_folder = "/Volumes/Sebins-HDD/Landsat8:9_c2l2"

folders = [folder for folder in os.listdir(landsat_folder) if os.path.isdir(os.path.join(landsat_folder, folder)) and not folder.startswith(".")]


# List of bands of interest in the desired order
bands_of_interest = ['B4', 'B3', 'B2']

c=0
for folder in folders:
    c+=1
    print(c)
    os.chdir(os.path.join(landsat_folder,folder))

    # Create a list of raster files that match the bands of interest
    raster_files = [os.path.join(os.getcwd(), f) for f in os.listdir(os.getcwd())
                    if any(band in f for band in bands_of_interest) and f.endswith('.TIF')
                    and not f.startswith(".")]

    # Sort the raster files to ensure the correct order (B4, B3, B2)
    # This uses the band names to order the files: 'B4' first, 'B3' second, 'B2' last.
    raster_files.sort(key=lambda x: bands_of_interest.index(next(band for band in bands_of_interest if band in x)))

    # Print the selected and ordered raster files
    for file in raster_files:
        print(file)

    # Output VRT file path
    vrt_output = os.path.join(os.getcwd(),"landsat_selected_bands.vrt")

    # Build the VRT with the ordered raster files
    gdal.BuildVRT(vrt_output, raster_files,options=["-separate"])




# vrt_ds = gdal.Open(vrt_output)

# vrt_layer = QgsRasterLayer(vrt_output, "Landsat VRT Layer")

# # Check if the layer is valid
# if vrt_layer.isValid():
#     # Add the layer to the QGIS project
#     QgsProject.instance().addMapLayer(vrt_layer)
#     print("Layer loaded successfully!")
# else:
#     print("Failed to load the layer.")
    
    
# layout_manager = QgsProject.instance().layoutManager()
# layout = layout_manager.layoutByName("gq_velocity")

# iface.openLayoutDesigner(layout)

# exporter = QgsLayoutExporter(layout)
# pdf_settings = QgsLayoutExporter.PdfExportSettings()
# pdf_settings.dpi = 100
# exporter.exportToPdf(f"./{title}.pdf", pdf_settings)