import os
import sys
# Add arcpy and dependencies to system path
sys.path.insert(0, r'C:\Program Files (x86)\ArcGIS\Desktop10.3\arcpy')
sys.path.insert(0, r'C:\Program Files (x86)\ArcGIS\Desktop10.3\bin')
sys.path.insert(0, r'C:\Python27\ArcGIS10.3\Lib\site-packages')
import arcpy


class PathBuilder(object):

    def get_depth(self, split_fpath):
        """Returns the depth of the file below the Source_Figures directory
        :type split_fpath: List[str]
        :rtype: int
        """
        try:
            # Find depth of file below Source_Figures folder
            return len(split_fpath[split_fpath.index('Source_Figures'):])
        except:
            # If Source_Figures isn't in path
            return -1

    def split_path(self, fpath):
        """Splits filepath into list of directories and file name
        :type fpath: str
        :rtype List[str]
        """
        dirs_file = fpath.split('\\')
        return dirs_file

    def get_path_variables(self, split_fpath, depth):
        """Returns the drive location of a source
        :type split_path: List[str]
        :type depth: int
        :rtype: dict
        """
        # Create dict structure for all source paths
        dir_dict = {0: None, 1: None, 2: None, 'fname': None}
        dir_dict['fname'] = split_fpath[-1]
        for level in range(depth - 1):
            dir_dict[level] = split_fpath[level]
        return dir_dict




    # TODO create a PathBuilder class that does the following
        # - Store folders for current source in dictionary
        # - Build path for Z drive to _Data_Library

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
    #
    #
    #             # Get folder names
    #             # Build path PDX/GIS_Files/<project_name>/Spatial/<task_name>/<shp_name>
    #         elif depth == 3:
    #             pass
    #             # PDX/GIS_Files/Spatial/<task_name>/<shp_name>
    #     except:
    #         # Probably errored b/c .mxd not in Source_Figures, came from elsewhere
    #         print "File not in source Figures: " + mxd
