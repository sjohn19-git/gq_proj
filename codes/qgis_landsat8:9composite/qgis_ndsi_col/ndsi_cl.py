from osgeo import gdal
import os
import glob
from tqdm import tqdm

# Define input and output directories
input_dir = "/Users/sebinjohn/gq_proj/data/clipped_NDSI/"
output_dir = "/Users/sebinjohn/gq_proj/Results/cl_ndsi/"
#layout="/Users/sebinjohn/gq_proj/codes/qqgis_landsat8/9composite/qgis_ndsi_col/ndsi_layout.qpt"
files=[f for f in os.listdir(input_dir) if f.endswith(".tif")]

for file in files:
    print(file)
    time=file.split('_')[0]
    ide=file.split('_')[1]
    inp=os.path.join(input_dir,file)
    vrt_layer = QgsRasterLayer(inp, "Landsat VRT Layer")
    QgsProject.instance().addMapLayer(vrt_layer)
    layout_manager = QgsProject.instance().layoutManager()
    layout = layout_manager.layoutByName('col_clip')
    
    label = QgsLayoutItemLabel(layout)
    label.setText("{}-{}-{}".format(time[:4],time[4:6],time[6:]))
    label.setFont(QFont("Arial", 25))
    label.setFontColor(QColor(0, 0, 0))
    layout.addLayoutItem(label)
    position = QgsLayoutPoint(125.387, 6)
    size=QgsLayoutSize(100,10)
    label.attemptMove(position)
    label.attemptResize(size)
    
    os.chdir(output_dir)
    exporter = QgsLayoutExporter(layout)
    png_settings = QgsLayoutExporter.ImageExportSettings()
    png_settings.dpi = 300  # Set DPI for PNG export
    # Export the layout to PNG
    exporter.exportToImage(f"./{time}_{ide}.png", png_settings)
    QgsProject.instance().removeMapLayer(vrt_layer.id())
    layout.removeLayoutItem(label)