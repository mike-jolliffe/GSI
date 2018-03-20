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
    for mxd in mxds:
        # Split the filepath of the mxd into a list of directories and a filename
        split_target = split_path(mxd)
        # Get the source data paths for each mxd
        src_paths = get_source_paths(mxd)
        # Split the filepath into a list
        for path in src_paths:
            if path[1].endswith('.shp'):
                new_src = set_source_path(path)

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

def get_source_paths(filepath):
    """Returns a list of layer path and layer sources for a given MapDocument file
    :type filepath: str
    :rtype: List[tuple]
    """
    mxd = arcpy.mapping.MapDocument(filepath)
    lyr_sources = []
    for lyr in arcpy.mapping.ListLayers(mxd):
        if lyr.supports("DATASOURCE"):
            lyr_sources.append((lyr, lyr.dataSource))
    return lyr_sources

def split_path(fpath):
    """Splits filepath into list of directories and file name
    :type fpath: str
    :rtype List[str]
    """
    dirs_file = fpath.split('\\')
    return dirs_file

def set_source_path(path):
    """Given drive and paths, creates appropriate filepath for new location of
    source data
    :type path: tuple(string, string)
    :rtype: str
    """
    # Create list of folders and filename from source path
    split_src = split_path(path[1])
    # Get drive name from path
    drive = split_src[0]
    # Get shape name from path
    shape_name = split_src[-1]
    print (split_src, drive, shape_name)
    exit()

    # # If drive is Z:
    # if drive == 'Z':
    #     # Map to _Data_Library
    #     return 'PDX\GIS_Files\_Data_Library\\' + shape_name
    # else:
    #     # Determine number of folders between Source_Figures and .mxd
    #     try:
    #         depth = len(split_target[split_target.index('Source_Figures'):])
    #         lyr = arcpy.mapping.ListLayers(path[0])
    #         if depth == 4:
    #             pass
    #             # Get folder names
    #             # Build path PDX/GIS_Files/<project_name>/Spatial/<task_name>/<shp_name>
    #         elif depth == 3:
    #             pass
    #             # PDX/GIS_Files/Spatial/<task_name>/<shp_name>
    #     except:
    #         # Probably errored b/c .mxd not in Source_Figures, came from elsewhere
    #         print "File not in source Figures: " + mxd



if __name__ == '__main__':
    main(r'\\PDX\GIS_Files\0302_Baxter')
