import os
import sys
# Add arcpy and dependencies to system path
sys.path.insert(0, r'C:\Program Files (x86)\ArcGIS\Desktop10.3\arcpy')
sys.path.insert(0, r'C:\Program Files (x86)\ArcGIS\Desktop10.3\bin')
sys.path.insert(0, r'C:\Python27\ArcGIS10.3\Lib\site-packages')
import arcpy


class PathGetter(object):
    def __init__(self, root):
        # Root directory within which to perform all link fixing
        self.root = root
        # Container for map filepaths
        self.map_paths = []
        # Layers, map paths, and source paths
        self.source_paths = []
        # Total number of layers
        self.num_layers = 0

    def find_files(self, ftype):
        """Given a path to root directory, recursively finds all files of given extension
        within root
        :type root: str
        :type ftype: str
        :rtype: None
        """
        # Container for ftype files by full path
        f = []
        # Recursively search from root, grabbing all files of given ftype
        for dirpath, subdirs, files in os.walk(self.root):
            for file in files:
                if file.endswith(ftype):
                    f.append(os.path.join(dirpath, file))
        self.map_paths = f

    def get_link_status(self, f):
        """Checks list of mxds to see if layer source links are broken, writes results to file
        :type f: List[str]
        :rtype: None
        """
        # Get current data source and broken status for all layers
        with open("Broken_links.txt", "w") as outfile:
            for filepath in f:
                mxd = arcpy.mapping.MapDocument(filepath)
                for lyr in arcpy.mapping.ListLayers(mxd):
                    if lyr.supports("DATASOURCE"):
                        outfile.write("Layer: " + lyr.name + " -- Source: " + lyr.dataSource + "  ------  [ Broken?  " + str(lyr.isBroken) + " ]" + "\n")

    def get_source_paths(self, filepath):
        """Returns a dictionary. Key is current mxd filepath, vals are tuples of
        map object, layer objects and their source paths
        :type filepath: str
        :rtype: None
        """
        mxd = arcpy.mapping.MapDocument(filepath)
        lyr_sources = {}
        # For all layers in a given .mxd
        for lyr in arcpy.mapping.ListLayers(mxd):
            self.num_layers += 1
            # If the layer has a dataSource property and its datasource is a shapefile
            if lyr.supports("DATASOURCE"): #and lyr.dataSource.endswith('.shp'):
                # Store the map object, layer object, map filepath, and data source filepath
                lyr_sources.setdefault(filepath, []).append((mxd, lyr, lyr.dataSource))
            elif lyr.isGroupLayer:
                for member in lyr:
                    # If the layer has a dataSource property and its datasource is a shapefile
                    if member.supports("DATASOURCE"): #and member.dataSource.endswith('.shp'):
                        # Store the map object, layer object, map filepath, and data source filepath
                        lyr_sources.setdefault(filepath, []).append((mxd, member, member.dataSource))
            else:
                print lyr.name + 'doesn\'t support datasource'
        self.source_paths.append(lyr_sources)
