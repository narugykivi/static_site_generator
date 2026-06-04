import os
from shutil import copy, rmtree

def copy_all(source, destination):
    working_dir = os.path.abspath(source)
    target_dir = os.path.abspath(destination)
    delete_all(target_dir)
    files, dirs = get_files(working_dir)
    #print(files)
    for dir in dirs:
        dir_relative_path = os.path.relpath(dir, working_dir)
        new_dir = os.path.join(target_dir, dir_relative_path)
        print(dir_relative_path, "Directory copyed to:", new_dir)
        os.mkdir(new_dir)
    
    for file in files:
        file_relative_path = os.path.relpath(file, working_dir)
        new_file = os.path.join(target_dir, file_relative_path)
        print(file_relative_path, "File copyed to:", new_file)
        # copy file to destination and make dir if not exists
        copy(file, new_file)
        # print what file copied where
        pass
    pass

def delete_all(target_dir):
    # delete all files and directories of destination
    #print(os.listdir(target_dir))
    rmtree(target_dir)
    os.mkdir(target_dir)
    #print(os.listdir(target_dir))
    return

def get_files(working_dir, file_paths=[], dir_paths=[]):
    # get files to file_paths
    files = os.listdir(working_dir)
    #print(files)
    # get directories of current directory
    # loop through dirs and get_files_and_dir_paths(dir)
    for file in files:
        path = os.path.normpath(os.path.join(working_dir, file))
        if os.path.isdir(path):
            dir_paths.append(path)
            get_files(path, file_paths, dir_paths)
            continue
        file_paths.append(path)
        # repeat til all files gathered
    return file_paths, dir_paths