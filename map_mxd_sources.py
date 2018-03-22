import os
from path_getter import PathGetter
from path_builder import PathBuilder


def main(root):
    current_paths, num_layers = map_current_paths(root)
    print (current_paths, num_layers)
    for map_dict in current_paths:
        build_new_paths(map_dict, num_layers)

def map_current_paths(root):
    """Generates dictionary of all current map paths, layer paths, and data
    source paths, and also returns total number of layers to be modified
    :type root: str
    :rtype: Dict, str
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
        print 'current paths found for mxd # ' + str(mxd_num) + " of " + str(tot_mxds)
        mxd_num += 1
        #print getter.source_paths
    return getter.source_paths, str(getter.num_layers)

def build_new_paths(map_dict, num_layers):
    """Given current paths, builds new paths to reflect modified directory structure
    :type map_dict: Dict
    :type num_layers: str
    :rtype: None
    """
    # Instantiate new PathBuilder object that will consume getter.source_paths list
    print 'Repairing links for ' + num_layers + ' layers...'
    builder = PathBuilder()
    # For each mxd dictionary
    for mxd_path, lyr_sources_list in map_dict.items():
        print "rebuilding links for " + mxd_path
        mxd = arcpy.mapping.MapDocument(mxd_path)
        # Split the filepath of the map into a list of directories and a filename
        split_target = builder.split_path(mxd_path)
        for lyr in lyr_sources_list:
            source_fname = builder.split_path(lyr[1])[-1]
            # Drop the .shp extenson
            source_fname_wo_ext = str(source_fname.split('.')[0])
            # Get name of featureclass and workspace path
            featureclass = lyr[0].name
            old_workspace = lyr[0].workspacePath
            # Create dict for building new path
            path_dict = builder.get_path_variables(split_target[split_target.index('GIS_Files'): ])
            if lyr[1].startswith('Z'):
                new_workspace = '\\\\PDX\GIS_Files\_Data_Library'
            else:
                new_workspace = builder.match_new_src(path_dict['Project'], source_fname)
                #new_path = new_path.replace('.shp', '')
            builder.build(lyr[0], old_workspace, new_workspace)
            print 'Old file location: ' + old_workspace
            print 'New file location: ' + new_workspace
            # make a temporary copy so you can save it. Otherwise, IO error if attempt
            # to save current mxd
            print 'Saving the mxd...'
            print '-------------------------------'
        tmp_mxd_copy = mxd_path.replace('.mxd', '_NEW6.mxd')
        print 'New map path: ' + tmp_mxd_copy
        print 'current map path: ' + mxd.filePath
        mxd.saveACopy(tmp_mxd_copy)
        print 'copy saved as ' + tmp_mxd_copy
        # Delete the original mxd, and rename the copy to original name
        del mxd

    # os.remove(mxd_path)
    # os.rename(tmp_mxd_copy, mxd_path)


#TODO GAAAAH why isn't the workspacepath being replaced?
    # https://support.esri.com/en/bugs/nimbus/QlVHLTAwMDA5Njc3OQ==

#TODO keep track of all layers/mxds/source filepaths where links were not successfully repaired
#TODO keep track of total number of layers repaired / not repaired
#TODO test that links are repaired using get_link_status in path_getter module

if __name__ == '__main__':
    # main(r'\\PDX\GIS_Files\0302_Baxter')
    # main(r'\\PDX\GIS_Files\0302_Baxter\Source_Figures\Ross_Tract')
    # main(r'\\PDX\GIS_Files\0302_Baxter\Source_Figures\Arlington_Landfills\2016_Annual_Report')
    #main(r'\\PDX\GIS_Files\0302_Baxter_DUPLICATE\Source_Figures\Ross_Tract')
    main(r'\\PDX\GIS_Files\0730_PPS_DUPLICATE\Source_Figures')
