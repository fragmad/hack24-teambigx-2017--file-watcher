import os

# Top level directories in ownCloud's data directory. 
IGNORED_DIRECTORIES = ['files_external']

def calculate_ignored(to_ignore, root):
    ignored = []
    for directory in to_ignore:
        ignored.append(root+directory)
    return ignored

def walk_directories(top):
    to_ignore = calculate_ignored(IGNORED_DIRECTORIES, top)

    for root, dirs, files in os.walk(top, topdown=True):
        list_of_files = [] 
        for name in files:
            if root not in to_ignore:
                print root
                print(os.path.join(root, name))
       # for name in dirs:
       #     print(os.path.join(root, name))

def do_magic(top):
    top = os.path.expanduser(top)
    walk_directories(top)

if __name__ == '__main__':
    do_magic("~/tmp/storage/")
