import hashlib
import os
import sys
import time

VERBOSE = False

# Top level directories in ownCloud's data directory. 
IGNORED_DIRECTORIES = ['files_external']

# Previous version of the file list
last_file_tree = []


# shamelessly borrowed for a Hackathon! 
def hash_file(file_path):
    BLOCKSIZE = 65536
    hasher = hashlib.md5()
    with open(file_path, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()

def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o : (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    same = set(o for o in intersect_keys if d1[o] == d2[o])
    return added, removed, modified, same

## my code

def calculate_ignored(to_ignore, root):
    ignored = []
    for directory in to_ignore:
        ignored.append(root+directory)
    return ignored

def walk_directories(top):
    to_ignore = calculate_ignored(IGNORED_DIRECTORIES, top)
    list_of_files = []
    file_number = 0

    for root, dirs, files in os.walk(top, topdown=True):
        dict_of_files = {}

        for name in files:
            if root not in to_ignore:
                path = os.path.join(root, name)
                leaf_dict = {"path" : path, 'filename' : name, 'hash' : hash_file(path)}
                list_of_files.append((file_number, leaf_dict))
                file_number = file_number + 1 
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

def compare_file_trees(last_tree, current_tree):
    last_tree.sort()
    current_tree.sort()
    last_len =  len(last_tree)
    current_len =  len(current_tree)


    if VERBOSE is True:
        print last_tree
        print current_tree

    for last_item, last_file_leaf in last_tree:
        for current_item, current_file_leaf in current_tree:
            if last_item == current_item:
                print last_item
           # print last_file_leaf
                print current_item
                print last_file_leaf
                print current_file_leaf
                print "--"
                added, removed, modified, same = dict_compare(last_file_leaf, current_file_leaf)
                print "added:", added
                print "removed:", removed
                print "modified:", modified
                print "same:", same


def main(top):
    current_file_tree = []
    while True:
        last_file_tree = current_file_tree
        current_file_tree = construct_file_tree_dicts(top)

        same_tree = compare_file_trees(last_file_tree, current_file_tree)

        #print same_tree
        raw_input('>')
        #time.sleep(10)

if __name__ == '__main__':
    #construct_file_tree_dicts("~/tmp/storage/")
    main("~/tmp/storage/")
