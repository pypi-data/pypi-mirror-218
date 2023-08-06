from os import path, listdir, remove
from shutil import rmtree

def read_lines(file_path):
    with open(file_path) as f:
            lines = f.readlines()
    return lines

def count_lines(file_path):
    return len(read_lines(file_path))

def count_folders(folder_path):
    return len(list_directories(folder_path))

def count_files(folder_path):
    return len(list_files(folder_path))

def get_file_info(file_path):
    split_path = path.splitext(file_path)
    file_name = file_path.split("/")[-1]
    file_extension = split_path[1]
    file_location = file_path.split("/" + file_name)[0]
    return [file_name, file_extension, file_location]

def get_file_name(file_path):
    return get_file_info(file_path)[0]

def get_file_extension(file_path):
    return get_file_info(file_path)[1]

def get_file_location(file_path):
    return get_file_info(file_path)[2]

def is_file(path_string):
    return path.isfile(path_string)
          
def is_folder(path_string):
    return path.isdir(path_string)

def is_existing(path_string):
    return path.exists(path_string) 

def list_directories(folder_path):
    return [
        d for d in (path.join(folder_path, d1) for d1 in listdir(folder_path))
        if path.isdir(d)
    ]

def list_files(folder_path):
    return [f for f in listdir(folder_path) if path.isfile(path.join(folder_path, f)) if f[0] != "."]

def is_empty(folder_path):
    return len(listdir(folder_path)) == 0

def delete_file(file_path):
    remove(file_path)

def delete_folder(folder_path):
    rmtree(folder_path)