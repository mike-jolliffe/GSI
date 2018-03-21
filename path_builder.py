import os
import sys
# Add arcpy and dependencies to system path
sys.path.insert(0, r'C:\Program Files (x86)\ArcGIS\Desktop10.3\arcpy')
sys.path.insert(0, r'C:\Program Files (x86)\ArcGIS\Desktop10.3\bin')
sys.path.insert(0, r'C:\Python27\ArcGIS10.3\Lib\site-packages')
import arcpy


class PathBuilder(object):

    def split_path(self, fpath):
        """Splits filepath into list of directories and file name
        :type fpath: str
        :rtype List[str]
        """
        dirs_file = fpath.split('\\')
        return dirs_file

    def get_path_variables(self, split_fpath):
        """Returns the drive location of a source
        :type split_path: List[str]
        :type depth: int
        :rtype: dict
        """
        # Create dict structure for all source paths. All paths will fit in this
        dir_dict = {'Root': None, 'Project': None, 'fname': None}
        dir_dict['fname'] = split_fpath[-1]
        dir_dict['Root'] = split_fpath[0]
        dir_dict['Project'] = split_fpath[1]
        return dir_dict

    def match_new_src(self, project_name, source_fname):
        """Returns filepath of source file in new path that matches source_fname
        :type project_name: str
        :type source_fname: str
        :rtype: str
        """
        search_path = '\\\\PDX\GIS_Files' + '\\' + project_name + '\\Data'
        for dirpath, subdirs, files in os.walk(search_path):
            for file in files:
                if file == source_fname:
                    return os.path.join(dirpath, file)
        return 'Not found in current drive: ' + source_fname

    def build(self, path_dict, source_fname, source_task):
        """Builds filepath for the new source data location
        :type path_dict: dict
        :type source_fname: str
        :type source_task: str
        :rtype: str
        """




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
