from osgeo import gdal
import os
import glob
from tqdm import tqdm

landsat_folder = "/Volumes/Sebins-HDD/Landsat8:9_c2l2"

folders = [folder for folder in os.listdir(landsat_folder) if os.path.isdir(os.path.join(landsat_folder, folder)) and not folder.startswith(".")]


for folder in folders:
    os.chdir(os.path.join(landsat_folder,folder))
    vrt_output = os.path.join(os.getcwd(),"landsat_selected_bands.vrt")
    
    vrt_ds = gdal.Open(vrt_output)
    vrt_layer = QgsRasterLayer(vrt_output, "Landsat VRT Layer")

    # Check if the layer is valid
    if vrt_layer.isValid():
        # Add the layer to the QGIS project
        QgsProject.instance().addMapLayer(vrt_layer)
        print("Layer loaded successfully!")
    else:
        print("Failed to load the layer.")
    
    layout_manager = QgsProject.instance().layoutManager()
    layout = layout_manager.layoutByName("gq_velocity")

    scene=folder.split("_")[2]
    time=folder.split("_")[3]
    if not os.path.exists("/Users/sebinjohn/gq_proj/Results/Landsat/{}".format(scene)):
        os.makedirs("/Users/sebinjohn/gq_proj/Results/Landsat/{}".format(scene))
    
    os.chdir("/Users/sebinjohn/gq_proj/Results/Landsat/{}".format(scene))
    
    label = QgsLayoutItemLabel(layout)
    label.setText("{}-{}-{}".format(time[:4],time[4:6],time[6:]))
    label.setFont(QFont("Arial", 25))
    label.setFontColor(QColor(255, 0, 0))
    layout.addLayoutItem(label)
    position = QgsLayoutPoint(125.387, 6)
    size=QgsLayoutSize(100,10)
    label.attemptMove(position)
    label.attemptResize(size)
    
    exporter = QgsLayoutExporter(layout)
    png_settings = QgsLayoutExporter.ImageExportSettings()
    png_settings.dpi = 300  # Set DPI for PNG export
    # Export the layout to PNG
    exporter.exportToImage(f"./{time}.png", png_settings)
    QgsProject.instance().removeMapLayer(vrt_layer.id())
    layout.removeLayoutItem(label)
