from qgis.core import QgsSymbol, QgsVectorLayer, QgsSingleSymbolRenderer, QgsCoordinateReferenceSystem
from PyQt5.QtGui import QColor 
from qgis.core import QgsProject, QgsRasterLayer, QgsLayoutItemLabel, QgsLayoutItemLegend, QgsLayoutPoint
from qgis.utils import iface
from qgis.PyQt.QtCore import QFileInfo
import os


# Set working directory and get all .nc files
os.chdir("/Users/sebinjohn/gq_proj/data/glacier_velocity")
current_dir = os.getcwd()
shapefiles = [os.path.join(current_dir, f) for f in os.listdir(current_dir) if f.endswith('.nc')]

# Sort and remove the first file
sorted_files = sorted(shapefiles, key=lambda x: int(x.split('_')[-2]))
del sorted_files[0]

# Define variables
variable_name = 'v'
style_path = '/Users/sebinjohn/gq_proj/codes/qgis_glacier_velocity/velocity.qml'

# Set up layout manager and get layout
layout_manager = QgsProject.instance().layoutManager()
layout = layout_manager.layoutByName("gq_velocity")

# Change directory to save results
os.chdir("/Users/sebinjohn/gq_proj/Results/glacier_velocity")


# Loop through each file, add it to QGIS, apply style, and export to PDF
for path in sorted_files:
    year = path.split('_')[-2]
    uri = f'NETCDF:"{path}":{variable_name}'
    layer = QgsRasterLayer(uri, f"{variable_name} Layer", "gdal")
    QgsProject.instance().addMapLayer(layer)
    layer.loadNamedStyle(style_path)
    layer.triggerRepaint()
    
    
    color_ramp_settings = QgsColorRampLegendNodeSettings()
    color_ramp_settings.setSuffix(" m/yr")
    layer_tree = QgsProject.instance().layerTreeRoot()
    layer_tree_node = layer_tree.findLayer(layer.id())
    QgsMapLayerLegendUtils.setLegendNodeColorRampSettings(layer_tree_node, 1, color_ramp_settings)
    
    
    #legending
    lyrsToRemove = [l for l in QgsProject.instance().mapLayers().values() if l.name() != 'v Layer']
    print(lyrsToRemove)
    legend = QgsLayoutItemLegend(layout)
    legend.setAutoUpdateModel(False)
    layout.addLayoutItem(legend)
    root = legend.model().rootGroup()
    for ele in lyrsToRemove:
        root.removeLayer(ele)
        print("removed legend",ele)


    # Open the layout in QGIS interface
    corners = [QgsPointXY(0, 0), QgsPointXY(5, 0), QgsPointXY(5, 5), QgsPointXY(0, 5)]
    title = QgsLayoutItemLabel(layout)
    title.setText(year)
    title.setFont(QFont("Arial", 16))  # Set font and size for the title
    title.adjustSizeToText()
    

    # Add the title to the layout
    layout.addItem(title)
    
    
    #iface.openLayoutDesigner(layout)


    exporter = QgsLayoutExporter(layout)
    pdf_settings = QgsLayoutExporter.PdfExportSettings()
    pdf_settings.dpi = 100
    exporter.exportToPdf(f"./{year}.pdf", pdf_settings)
    
    # Remove layer after export
    print(f"Removing layer with ID: {layer.id()}")
    QgsProject.instance().removeMapLayer(layer.id())
    layout.removeLayoutItem(legend)
    layout.removeLayoutItem(title)
