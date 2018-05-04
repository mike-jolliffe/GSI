import os
import pickle

class PathMapper(object):
    def __init__(self, root):
        self.all_source_paths = {}
        self.root = root

    def _get_project_names(self):
        """Adds projects as outer keys to instance variable dictionary

        :type root: str
        :rtype: Dictionary
        """
        for folder in os.listdir(self.root):
            if folder[0].isdigit():
                try:
                    self.all_source_paths[folder] = {}
                except KeyError:
                    raise KeyError ('Non-unique project name, already exists in dictionary.')
        return self.all_source_paths

    def _walk_dirs(self):
        """Walks from root through all sub-directories, stores into dict
        :rtype: Dictionary
        """
        for project_name in self.all_source_paths.keys():
            print "-------- Now mapping ---- " + project_name
            search_path = self.root + project_name + '\\Data'
            for dirpath, subdirs, files in os.walk(search_path):
                for file in files:
                    self.all_source_paths[project_name][file] = dirpath
        print "------------ Finished mapping ------- " + project_name
        return self.all_source_paths

    def _pickler(self):
        '''Pickles an object'''
        output = open('all_source_paths_pickle', 'wb')
        print 'Pickling all source paths'
        pickle.dump(self.all_source_paths, output)
        output.close()

if __name__ == '__main__':
    try:
        with open('all_source_paths_pickle', 'rb') as fp:
            paths = pickle.load(fp)
            print type(paths)
            for path in paths:
                print path
    except:
        print "Whoops, didn't work"
        # mapper = PathMapper('Y:\\')
        # mapper._get_project_names()
        # print "Got all projects. Building filepaths for all files..."
        # print(mapper._walk_dirs())
        # mapper.pickler()
