import os
import pickle

class PathMapper(object):
    def __init__(self, root):
        self.all_source_paths = {}
        self.new_source_paths = {}
        self.root = root

    def _get_project_names(self):
        """Adds projects as outer keys to instance variable dictionary

        :type root: str
        :rtype: Dictionary
        """
        for folder in os.listdir(self.root):
            if folder[0].isdigit():
                try:
                    self.new_source_paths[folder]
                    pass
                except:
                    self.new_source_paths[folder] = {}
        return self.new_source_paths

    def _walk_dirs(self):
        """Walks from root through all sub-directories, stores into dict
        :rtype: Dictionary
        """
        for project_name in self.new_source_paths.keys():
            # print "-------- Now mapping ---- " + project_name
            search_path = self.root + project_name + '\\Data'
            for dirpath, subdirs, files in os.walk(search_path):
                for file in files:
                    self.new_source_paths[project_name][file] = dirpath
            # print "------------ Finished mapping ------- " + project_name
        return self.new_source_paths

    def _merge_new_into_all_paths(self):
        """Merges any new source paths into previously mapped all_source_paths
        :rtype: No return
        """
        self.all_source_paths.update(self.new_source_paths)

    def _pickler(self):
        '''Pickles an object'''
        output = open('all_source_paths_pickle2', 'ab')
        print 'Pickling all source paths'
        pickle.dump(self.all_source_paths, output)
        output.close()

    def _unpickler(self):
        '''Unpickles an object'''
        with open('all_source_paths_pickle', 'rb') as fp:
            paths = pickle.load(fp)
            self.all_source_paths = paths

if __name__ == '__main__':
    # mapper = PathMapper('Y:\\')
    # mapper._unpickler()
    # print 'Unpickled ' + str(len(mapper.all_source_paths)) + ' objects'
    # # print mapper.all_source_paths
    # mapper._get_project_names()
    # # print "Got all projects. Building filepaths for all files..."
    # print mapper._walk_dirs()
    # mapper._merge_new_into_all_paths()
    # print 'Pickling ' + str(len(mapper.all_source_paths)) + ' objects'
    # mapper._pickler()

    try:
        with open('all_source_paths_pickle2', 'rb') as fp:
            paths = pickle.load(fp)
            print paths['0137_LWG']
            print("----------------------------------------------------------")
            print("\n\n\n")
        with open('all_source_paths_pickle', 'rb') as fp2:
            paths2 = pickle.load(fp2)
            print paths2['0136_MadisonMcCarty_ASR']
            for path in sorted(list(paths.keys())):
                print path
    except:
        print "Whoops, didn't work"
