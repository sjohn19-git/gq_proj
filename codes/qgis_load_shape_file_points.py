from qgis.core import QgsSymbol, QgsVectorLayer, QgsProject, QgsSingleSymbolRenderer
from PyQt5.QtGui import QColor 
from qgis.core import QgsProject
import os
from qgis.utils import iface


os.chdir("/Users/sebinjohn/gq_proj/data/glacier_extent")
current_dir = os.getcwd()
# Find all .shp files and get their full paths
shapefiles = [os.path.join(current_dir, f) for f in os.listdir(current_dir) if f.endswith('.shp')]

def set_layer_style(layer):
    # Get the fill symbol for the layer's geometry type
    symbol = QgsFillSymbol.createSimple({'color': 'white', 'color_border': 'transparent', 'width_border': '0'})
    
    # Set the fill color with 90% opacity
    fill_color = QColor("white")
    fill_color.setAlphaF(0.9)  # Set fill opacity to 90%
    symbol.setColor(fill_color)
    
    # Apply the symbol to the layer with a single symbol renderer
    renderer = QgsSingleSymbolRenderer(symbol)
    layer.setRenderer(renderer)
    
    # Update the layer to reflect changes
    layer.triggerRepaint()

sf=shapefiles[0]
print(sf)
layer = QgsVectorLayer(sf, os.path.basename(sf), "ogr")
set_layer_style(layer)
QgsProject.instance().addMapLayer(layer)
layout_manager = QgsProject.instance().layoutManager()
# Find the layout by name
layout = layout_manager.layoutByName("gq_loca")
iface.openLayoutDesigner(layout)

#QgsProject.instance().removeMapLayer(layer.id())