from path_getter import PathGetter
from path_builder import PathBuilder


def main(root):
    current_paths = map_current_paths(root)
    build_new_paths(current_paths)

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

def build_new_paths(current_paths):
    """Given current paths, builds new paths to reflect modified directory structure
    :type current_paths: List[tuple(<map layer>, str, str)]
    :rtype: None
    """
    # Instantiate new PathBuilder object that will consume getter.source_paths list
    builder = PathBuilder()
    for fpath_tuple in current_paths:
        # Split the filepath of the source into a list of directories and a filename
        split_target = builder.split_path(fpath_tuple[1])
        target_depth = builder.get_depth(split_target)
        print target_depth
        path_dict = builder.get_path_variables(split_target[split_target.index('Source_Figures'): ], target_depth)
        print path_dict
    exit()




if __name__ == '__main__':
    # main(r'\\PDX\GIS_Files\0302_Baxter')
    #main(r'\\PDX\GIS_Files\0302_Baxter\Source_Figures\Arlington_Landfills\2016_Annual_Report')
    main(r'\\PDX\GIS_Files\0730_PPS\Source_Figures\001_GW_Protectiveness')
