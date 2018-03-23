import os
from path_getter import PathGetter
from path_builder import PathBuilder


def main(root):
    # Get all current map and data source paths, number of layers requiring mods
    # Instantiate new Getter object
    getter = PathGetter(root)
    # Get all mxds in root directory
    print 'finding all .mxd files...'
    getter.find_files('.mxd')
    # Store the total count of maps
    tot_mxds = len(getter.mxd_paths)
    print str(tot_mxds) + ' mxd files found.'
    print 'Getting current source paths...'
    mxd_num = 0
    # For a given map filepath
    for mxd in getter.mxd_paths:
        mxd_num += 1
        # Get the source data paths for map
        getter.get_source_paths(mxd)
        print '--------------------------------------------------\n'
        print 'FIXING PATHS FOR FOR MXD # ' + str(mxd_num) + " OF " + str(tot_mxds)
        print '\n'
        print 'Repairing ' + str(getter.num_layers) + ' layers...'
        print '\n--------------------------------------------------\n'
        build_new_paths(getter.source_paths, str(getter.num_layers))

def build_new_paths(map_dict, num_layers):
    """Given current source paths, builds new source paths to reflect modified
    directory structure
    :type map_dict: Dict
    :type num_layers: str
    :rtype: None
    """
    # Instantiate new PathBuilder object that will consume getter.source_paths list
    builder = PathBuilder()
    # For each map
    for mxd_path, lyr_sources_list in map_dict.items():
        # Grab the map object to be modified
        mxd = lyr_sources_list[0][0]
        # Split the map filepath into list of directories and filename
        split_target = builder.split_path(mxd_path)
        # for each (map object, layer object, old layer source filepath) tuple
        for lyr in lyr_sources_list:
            # Grab the filename
            source_fname = builder.split_path(lyr[2])[-1]
            # Drop the .shp, .tif extenson
            source_fname_wo_ext = str(source_fname.split('.')[0])
            # Get old workspace path
            old_workspace = lyr[1].workspacePath
            # Create dict for building new path
            path_dict = builder.get_path_variables(split_target[split_target.index('W:'): ])
            # Move shared data sources from Z: into special Data Library folder
            if old_workspace.startswith('Z') or old_workspace.startswith('W:\_Data_Library'):
                source_path = builder.split_path(old_workspace)[2:]
                source_path = '\\'.join(source_path)
                new_workspace = 'W:\_Data_Library' + '\\' + source_path
            else:
                # All other sources go into their respective project folders
                new_workspace = builder.match_new_src(path_dict['Project'], source_fname)
            builder.build(lyr[1], old_workspace, new_workspace)
        print 'Saving the mxd...'
        # If you get an error, make sure all other instances of mxd are closed
        print '-------------------------------------------------------'
        mxd.save()
        del mxd

"""TODO I'm getting runtime errors for large directories, most likely because
I gather all the map objects and layer objects in memory, then iterate on them,
fixing each. Definitely should have thought of this during design. I need to fix
the getter class so it only stores one map object and its layers at a time. Then
fix builder so it runs for a single map object, rather than a dictionary of all
the map and layer objects at once."""

if __name__ == '__main__':
    main(r'W:\0302_Baxter_DUPLICATE\Source_Figures')
    # main(r'\\PDX\GIS_Files\0302_Baxter\Source_Figures\Ross_Tract')
    # main(r'\\PDX\GIS_Files\0302_Baxter\Source_Figures\Arlington_Landfills\2016_Annual_Report')
    # main(r'\\PDX\GIS_Files\0302_Baxter_DUPLICATE\Source_Figures\Ross_Tract')
    # main(r'W:\0730_PPS_DUPLICATE\Source_Figures')
