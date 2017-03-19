import hashlib
import os

VERBOSE = True

# Top level directories in ownCloud's data directory. 
IGNORED_DIRECTORIES = ['files_external']

# Previous version of the file list
last_files_tree = []


def hash_file(file_path):
    BLOCKSIZE = 65536
    hasher = hashlib.md5()
    with open(file_path, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()


def calculate_ignored(to_ignore, root):
    ignored = []
    for directory in to_ignore:
        ignored.append(root+directory)
    return ignored

def walk_directories(top):
    to_ignore = calculate_ignored(IGNORED_DIRECTORIES, top)
    list_of_files = []

    for root, dirs, files in os.walk(top, topdown=True):
        dict_of_files = {}

        for name in files:
            if root not in to_ignore:
                path = os.path.join(root, name)
                leaf_dict = {"path" : path, 'filename' : name, 'hash' : hash_file(path)}
                list_of_files.append(leaf_dict)
    return list_of_files
       # for name in dirs:
       #     print(os.path.join(root, name))

def construct_file_tree_dicts(top):
    top = os.path.expanduser(top)
    file_list = walk_directories(top)

    if VERBOSE is True:
        for f in file_list:
            print f['path']
            print f['filename']
            print f['hash']

    return file_list

if __name__ == '__main__':
    construct_file_tree_dicts("~/tmp/storage/")
    
