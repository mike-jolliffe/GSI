import os
from path_getter import PathGetter
from path_builder import PathBuilder


def main(root=None):
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
        print 'FILE NAME ' + mxd
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
    # Grab stored dict of filepaths
    builder.get_mapped_sources()
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
            try:
                old_workspace = lyr[1].workspacePath
            # Create dict for building new path
            except:
                print ("Layer doesn't have workspace path", lyr, type(lyr))
                print ("Service layer?", lyr[1].isServiceLayer)
                print ("Group layer?", lyr[1].isGroupLayer)
                print("Supports DataSource?", lyr[1].supports("DATASOURCE"))
                print lyr[1].longName
                break
            path_dict = builder.get_path_variables(split_target[split_target.index('Y:'): ])
            # Move shared data sources from Z: into special Data Library folder
            if old_workspace.startswith('Z') or old_workspace.startswith('Y:\_Data_Library'):
                source_path = builder.split_path(old_workspace)[2:]
                source_path = '\\'.join(source_path)
                new_workspace = 'Y:\_DataLibrary' + '\\' + source_path
            else:
                # All other sources go into their respective project folders
                new_workspace = builder.match_new_src(path_dict['Project'], source_fname)
            if not new_workspace:
                print "Couldn't make source match: " + source_fname
            else:
                builder.build(lyr[1], old_workspace, new_workspace)
        print 'Saving the mxd...'
        # If you get an error, make sure all other instances of mxd are closed
        print '-------------------------------------------------------'
        try:
            mxd.save()
            del mxd
        except (IOError, AttributeError), e:
            log_error(mxd.filePath)
            print "Unable to save mxd " + mxd.title

def log_error(filepath):
    with open ('unsaved_maps', 'a+') as error_log:
        error_log.write(filepath)


if __name__ == '__main__':
    # main(r'Y:\0149_Jordan_Valley')
    # main(r'Y:\0150_Keizer_City')
    # DIDN"T WORK main(r'Y:\0152_Gresham')
    # main(r'Y:\0188_Warren_Water_Association')
    # main(r'Y:\0189_Clean_Water_Services')
    # main(r'Y:\0190_City_of_Columbia')
    # main(r'Y:\0192_Great_Western_Malting')
    # main(r'Y:\0193_ClarkCo_Corrections')
    # main(r'Y:\0195_Nike')
    # main(r'Y:\0196_Wallowa')
    # main(r'Y:\0197_DeschutesCo')
    # main(r'Y:\0199_DavisWright_Tremaine')
    main(r'Y:\0200_SmallProjects')
    main(r'Y:\0201_Premier_Pacific_Vineyards')
    main(r'Y:\0202_City_Redmond')
    main(r'Y:\0203_City_Independence')
