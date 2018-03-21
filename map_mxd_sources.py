from path_getter import PathGetter

def main(root):
    # Instantiate new Getter object
    getter = PathGetter(root)
    # Get all mxds in root
    print 'finding all .mxd files...'
    getter.find_files('.mxd')
    mxds = getter.map_paths
    tot_mxds = len(mxds)
    print str(tot_mxds) + ' mxd files found.'
    print 'Getting current source paths...'
    mxd_num = 1
    for mxd in mxds:
        # Split the filepath of the mxd into a list of directories and a filename
        split_target = getter.split_path(mxd)
        # Get the source data paths for each mxd
        getter.get_source_paths(mxd)
        print 'finishing mxd # ' + str(mxd_num) + " of " + str(tot_mxds)
        mxd_num += 1
        #print getter.source_paths
    exit()

    # TODO create a PathBuilder class that does the following
        # - Gets the depth of the current .mxd from source_figures
        # - Migrates source data from Z: into the _Data_Library
        # - Parses current path into variables for use in building the new path
        # - Taking depth into account, creates new filepath for source data


# def set_source_path(path):
#     """Given drive and paths, creates appropriate filepath for new location of
#     source data
#     :type path: tuple(string, string)
#     :rtype: str
#     """
#     # Create list of folders and filename from source path
#     split_src = split_path(path[1])
#     # Get drive name from path
#     drive = split_src[0]
#     # Get shape name from path
#     shape_name = split_src[-1]
#     print (split_src, drive, shape_name)
#     exit()

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
