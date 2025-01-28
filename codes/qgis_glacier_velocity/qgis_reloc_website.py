from qgis.core import QgsSymbol, QgsVectorLayer, QgsProject, QgsSingleSymbolRenderer,QgsCoordinateReferenceSystem
from PyQt5.QtGui import QColor 
from qgis.core import QgsProject
import os
from qgis.core import QgsLayoutItemLabel
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

shapefiles.sort()
layout_manager = QgsProject.instance().layoutManager()
# Find the layout by name
layout = layout_manager.layoutByName("website")


del shapefiles[0]

for i in range(len(shapefiles)):
    sf=shapefiles[i]
    print(sf)
    layer = QgsVectorLayer(sf, os.path.basename(sf), "ogr")
    set_layer_style(layer)
    QgsProject.instance().addMapLayer(layer)
    try:
        yr=os.path.basename(sf)[3:7]
        for item in layout.items():
            if isinstance(item, QgsLayoutItemLabel):
                item.setText("{}".format(yr))  # Change to the new title
                break
        layout.refresh()
        os.chdir("/Users/sebinjohn/gq_proj/data/relocation_csvs_qgis/"+yr)
        uri = "file://{}/{}?delimiter={}&xField={}&yField={}".format(os.getcwd(),yr+'.csv', ",", "Longitude", "Latitude")
        layer1=QgsVectorLayer(uri, yr+"_reloc", "delimitedtext")
        QgsProject.instance().addMapLayer(layer1)
        crs = QgsCoordinateReferenceSystem("EPSG:4326")
        layer1.setCrs(crs)
        layer1.loadNamedStyle("/Users/sebinjohn/gq_proj/codes/qgis_alaska/web_style.qml")
        layer1.triggerRepaint()
        if not os.path.exists("/Users/sebinjohn/gq_proj/results/before and after relocation/"+yr):
            os.makedirs("/Users/sebinjohn/gq_proj/results/before and after relocation/"+yr)
        os.chdir("/Users/sebinjohn/gq_proj/results/before and after relocation/"+yr)
        exporter = QgsLayoutExporter(layout)
        image_settings = QgsLayoutExporter.ImageExportSettings()
        image_settings.dpi = 600 
        exporter.exportToImage("./{}.png".format(yr), image_settings)
        QgsProject.instance().removeMapLayer(layer.id())
        QgsProject.instance().removeMapLayer(layer1.id())
    except Exception as e:
        print(f"An error occurred: {e}")
    #iface.openLayoutDesigner(layout)



# sf=shapefiles[-1]
# print(sf)
# layer = QgsVectorLayer(sf, os.path.basename(sf), "ogr")
# set_layer_style(layer)
# QgsProject.instance().addMapLayer(layer)
# yr=os.path.basename(sf)[3:7]
# os.chdir("/Users/sebinjohn/gq_proj/data/relocation_csvs_qgis/"+yr)
# uri = "file://{}/{}?delimiter={}&xField={}&yField={}".format(os.getcwd(),yr+'.csv', ",", "Longitude", "Latitude")
# layer1=QgsVectorLayer(uri, yr+"_reloc", "delimitedtext")
# QgsProject.instance().addMapLayer(layer1)
# crs = QgsCoordinateReferenceSystem("EPSG:4326")
# layer1.setCrs(crs)
# layer1.loadNamedStyle("/Users/sebinjohn/gq_proj/codes/qgis_alaska/style_gq.qml")
# layer1.triggerRepaint()
# iface.openLayoutDesigner(layout)
    
    