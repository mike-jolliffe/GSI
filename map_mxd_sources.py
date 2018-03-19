import os
from socket import *
import sys

# Add arcpy and dependencies to system path
sys.path.insert(0, r'C:\Program Files (x86)\ArcGIS\Desktop10.3\arcpy')
sys.path.insert(0, r'C:\Program Files (x86)\ArcGIS\Desktop10.3\bin')
sys.path.insert(0, r'C:\Python27\ArcGIS10.3\Lib\site-packages')

import arcpy

# Grab all mxds and put in list by full path
f = []
path = r'\\PDX\GIS_Files'
for dirpath, subdirs, files in os.walk(path):
    for file in files:
        if file.endswith('.mxd'):
            f.append(os.path.join(dirpath, file))

# List all broken maps that need link to source fixed
for filepath in f:
    mxd = arcpy.mapping.MapDocument(filepath)
    brknList = arcpy.mapping.ListBrokenDataSources(mxd)
    print(brknList)




# TODO Get the root dir from the user

# TODO Get the current data source path for the mxd to the shp

# TODO Create new path based on conventions for project type

# TODO Replace old path with new path as mxd's data source

# TODO Test filepath for existence of a file (assert exists)
