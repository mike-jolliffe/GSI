from path_getter import PathGetter
from path_builder import PathBuilder


def main(root):
    current_paths = map_current_paths(root)
    num_layers = str(len(current_paths))
    build_new_paths(current_paths, num_layers)

def map_current_paths(root):
    """Maps all current map paths, layer paths, and data source paths
    :type root: str
    :rtype: List[tuple(<map layer>, str, str)]
    """
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
        # Get the source data paths for each mxd
        getter.get_source_paths(mxd)
        print 'finishing mxd # ' + str(mxd_num) + " of " + str(tot_mxds)
        mxd_num += 1
        #print getter.source_paths
    return getter.source_paths

def build_new_paths(current_paths, num_layers):
    """Given current paths, builds new paths to reflect modified directory structure
    :type current_paths: List[tuple(<map layer>, str, str)]
    :type num_layers: str
    :rtype: None
    """
    # Instantiate new PathBuilder object that will consume getter.source_paths list
    print 'Repairing links for ' + num_layers + ' layers...'
    builder = PathBuilder()
    for fpath_tuple in current_paths:
        # Split the filepath of the map into a list of directories and a filename
        split_target = builder.split_path(fpath_tuple[1])
        source_fname = builder.split_path(fpath_tuple[2])[-1]

        # Create dict for building new path
        path_dict = builder.get_path_variables(split_target[split_target.index('GIS_Files'): ])
        if fpath_tuple[2].startswith('Z'):
            new_path = '\\\\PDX\GIS_Files\_Data_Library' + '\\' + source_fname
        else:
            new_path = builder.match_new_src(path_dict['Project'], source_fname)
        print new_path



#TODO fix 'vector' being treated as a 'Task' (e.g., in Ross Tract)
#TODO replace paths on a dummy area of the drive
#TODO keep track of all layers/mxds/source filepaths where links were not successfully repaired
#TODO keep track of total number of layers repaired / not repaired
#TODO test that links are repaired using get_link_status in path_getter module

if __name__ == '__main__':
    # main(r'\\PDX\GIS_Files\0302_Baxter')
    main(r'\\PDX\GIS_Files\0302_Baxter\Source_Figures\Ross_Tract')
    # main(r'\\PDX\GIS_Files\0302_Baxter\Source_Figures\Arlington_Landfills\2016_Annual_Report')
    # main(r'\\PDX\GIS_Files\0730_PPS\Source_Figures')
