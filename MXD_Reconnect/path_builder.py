import os
import pickle
import sys
# Add arcpy and dependencies to system path
sys.path.insert(0, r'C:\Program Files (x86)\ArcGIS\Desktop10.3\arcpy')
sys.path.insert(0, r'C:\Program Files (x86)\ArcGIS\Desktop10.3\bin')
sys.path.insert(0, r'C:\Python27\ArcGIS10.3\Lib\site-packages')
import arcpy


class PathBuilder(object):

    def __init__(self):
        self.missing_sources = {}
        self.all_source_paths = {}

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

    def get_mapped_sources(self):
        """Unpickles dictionary of the form {project: {filename: path to file}}
        for quickly getting matching source filepaths instead of os.walk each time
        :return: Modifies the instance variable
        :rtype: dict
        """
        try:
            with open(r'C:\Users\MJolliffe\Documents\GitHub\GSI\MXD_Reconnect\all_source_paths_pickle', 'rb') as fp:
                self.all_source_paths = pickle.load(fp)
        except:
            raise 'Something went wrong loading the filepaths from Pickle'

    def match_new_src(self, project_name, source_fname):
        """Returns new filepath for location where filename matches source
        :type project_name: str
        :type source_fname: str
        :rtype: str or None
        """

        try:
            dirpath = self.all_source_paths[project_name][source_fname]
            if dirpath:
                return dirpath
            else:
                return None
        except KeyError:
            return None

    def build(self, map_layer, old_workspace, new_workspace):
        """Fixes filepath for given map layer
        :type map_layer: <map layer>
        :type new_path: str
        :rtype: Doesn't return anything
        """
        try:
            print 'old data path ' + map_layer.dataSource
            map_layer.findAndReplaceWorkspacePath(old_workspace, new_workspace, False)
            print 'new data path ' + map_layer.dataSource
        except:
            # If you get an error, make sure all drives are mapped
            raise
