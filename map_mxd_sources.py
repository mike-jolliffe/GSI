import os
import sys
# Add arcpy and dependencies to system path
sys.path.insert(0, r'C:\Program Files (x86)\ArcGIS\Desktop10.3\arcpy')
sys.path.insert(0, r'C:\Program Files (x86)\ArcGIS\Desktop10.3\bin')
sys.path.insert(0, r'C:\Python27\ArcGIS10.3\Lib\site-packages')
import arcpy


def main(root):
    # Get all mxds in root
    mxds = find_files(root, '.mxd')
    # Split the filepath into a list
    for file in mxds:
        print '----------------'
        print split_path(file)
        # Create project name variable
        # Create task name variable

        # Get the source data paths for those mxds
        src_paths = get_source_paths(file)
        # Split the filepath into a list
        for path in src_paths:
            if path.endswith('.shp'):
                split = split_path(path)
                drive = split[0]
                shape_name = split[-1]

        # TODO 
        # Rebuild the source path for each layer in each mxd
            # if source path starts with Z:, move to _Data_Library
            # otherwise, move to PDX/GIS_Files/<project_name>/Spatial/<task_name>/<shp_name> or
            # PDX/GIS_Files/Spatial/<task_name>/<shp_name>

def find_files(root, ftype):
    """Given a path to root directory, recursively finds all files of given extension
       within root
    :type root: str
    :type ftype: str
    :rtype: List[str]
    """
    # Container for ftype files by full path
    f = []
    # Recursively search from root, grabbing all files of given ftype
    for dirpath, subdirs, files in os.walk(root):
        for file in files:
            if file.endswith(ftype):
                f.append(os.path.join(dirpath, file))
    return f

def get_source_paths(filepath):
    """Returns a list of layer sources for a given MapDocument file
    :type filepath: str
    :rtype: List[str]
    """
    mxd = arcpy.mapping.MapDocument(filepath)
    lyr_sources = []
    for lyr in arcpy.mapping.ListLayers(mxd):
        if lyr.supports("DATASOURCE"):
            lyr_sources.append(lyr.dataSource)
    return lyr_sources

def get_link_status(f):
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

def split_path(fpath):
    """Splits filepath into list of directories and file name
    :type fpath: str
    :rtype List[str]
    """
    dirs_file = fpath.split('\\')
    return dirs_file


if __name__ == '__main__':
    main(r'\\PDX\GIS_Files\0302_Baxter')
