import os
from path_getter import PathGetter
from path_builder import PathBuilder


def main(root):
    # Get all current map and data source paths, number of layers requiring mods
    current_paths, num_layers = map_current_paths(root)
    print 'Repairing links for ' + num_layers + ' layers...'
    # For each map
    for map_dict in current_paths:
        # Replace old datasource locations with new ones
        build_new_paths(map_dict, num_layers)
    # Check that replacement worked
    del current_paths
    del num_layers
    #current_paths, num_layers = map_current_paths(root)
    #print current_paths

def map_current_paths(root):
    """Generates dictionary of all current map paths, layer paths, and data
    source paths, and also returns total number of layers to be modified
    :type root: str
    :rtype: Dict, str
    """
    # Instantiate new Getter object
    getter = PathGetter(root)
    # Get all mxds in root directory
    print 'finding all .mxd files...'
    getter.find_files('.mxd')
    # Get list of all map filepaths
    mxds = getter.map_paths
    # Store the total count of maps
    tot_mxds = len(mxds)
    print str(tot_mxds) + ' mxd files found.'
    print 'Getting current source paths...'
    mxd_num = 1
    # For a given map filepath
    for mxd in mxds:
        # Get the source data paths for map
        getter.get_source_paths(mxd)
        print 'current paths found for mxd # ' + str(mxd_num) + " of " + str(tot_mxds)
        mxd_num += 1
    # Pass back filepaths for all data sources, total number of layers to be changed
    return getter.source_paths, str(getter.num_layers)

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
        print '........MXD........'
        print 'rebuilding links for ' + mxd_path
        print '...................'
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
            print lyr[1]
            old_workspace = lyr[1].workspacePath
            # Create dict for building new path
            path_dict = builder.get_path_variables(split_target[split_target.index('W:'): ])
            # Move shared data sources from Z: into special Data Library folder
            if old_workspace.startswith('Z') or old_workspace.startswith('W:\_Data_Library'):
                source_path = builder.split_path(old_workspace)[2:]
                print source_path
                source_path = '\\'.join(source_path)
                new_workspace = 'W:\_Data_Library' + '\\' + source_path
            else:
                # All other sources go into their respective project folders
                new_workspace = builder.match_new_src(path_dict['Project'], source_fname)
            builder.build(lyr[1], old_workspace, new_workspace)
        print 'Saving the mxd...'
        # If you get an error, make sure all other instances of mxd are closed
        mxd.save()
        print '-------------------------------'
        del mxd


#TODO GAAAAH why isn't the workspacepath being replaced?
    # https://support.esri.com/en/bugs/nimbus/QlVHLTAwMDA5Njc3OQ==

#TODO keep track of all layers/mxds/source filepaths where links were not successfully repaired
#TODO keep track of total number of layers repaired / not repaired
#TODO test that links are repaired using get_link_status in path_getter module

if __name__ == '__main__':
    main(r'W:\0302_Baxter_DUPLICATE\Source_Figures')
    # main(r'\\PDX\GIS_Files\0302_Baxter\Source_Figures\Ross_Tract')
    # main(r'\\PDX\GIS_Files\0302_Baxter\Source_Figures\Arlington_Landfills\2016_Annual_Report')
    # main(r'\\PDX\GIS_Files\0302_Baxter_DUPLICATE\Source_Figures\Ross_Tract')
    # main(r'W:\0730_PPS_DUPLICATE\Source_Figures')
