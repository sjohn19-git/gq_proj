import pandas as pd
import os
from qgis.core import QgsVectorLayer, QgsFeature, QgsGeometry, QgsPointXY, QgsProject
from PyQt5.QtCore import QVariant



columbia_gq=pd.read_csv("/Users/sebinjohn/gq_proj/data/catalogs/columbia_gq_1988-2024.csv")

columbia_gq_dropped= columbia_gq.drop_duplicates(subset='evid', keep='first')
columbia_gq_dropped['time'] = pd.to_datetime(columbia_gq_dropped['time'])
columbia_gq_dropped['year'] = columbia_gq_dropped['time'].dt.year

columbia_gq_2014 = columbia_gq_dropped[columbia_gq_dropped['year'] == 2014]

latitudes = columbia_gq_2014['lat']
longitudes = columbia_gq_2014['lon']

# Reference to the existing project
project = QgsProject.instance()

# Create a memory layer for points
layer = QgsVectorLayer("Point?crs=EPSG:4326", "Columbia GQ 2014 Events", "memory")
provider = layer.dataProvider()

# Define attribute fields
layer.dataProvider().addAttributes([
    QgsField("evid", QVariant.Int),
    QgsField("time", QVariant.String)
])
layer.updateFields()

# Add points to the layer
features = []
for _, row in columbia_gq_2014.iterrows():
    point = QgsPointXY(row['lon'], row['lat'])  # Ensure lon/lat order
    feature = QgsFeature()
    feature.setGeometry(QgsGeometry.fromPointXY(point))
    feature.setAttributes([row['evid'], str(row['time'])])
    features.append(feature)

# Add features to the layer
provider.addFeatures(features)
layer.updateExtents()

# Add the layer to the open map
project.addMapLayer(layer)
