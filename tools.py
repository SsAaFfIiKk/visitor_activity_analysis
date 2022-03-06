import os
import zipfile
import random


def generate_predict():
    labels = ["laptop", "smartphone", "paper", "talking", "nothing"]
    index = random.randrange(0, len(labels))
    return labels[index]


def create_folders(path_to_dir, file_name):
    path_to_save = os.path.join(path_to_dir, file_name)
    if not os.path.exists(path_to_save):
        os.mkdir(path_to_save)
    return path_to_save + "/"


def unpack_archive(file_name, path_to_save, support_ext):
    with zipfile.ZipFile(os.path.join(path_to_save, file_name)) as f:
        for file in f.namelist():
            ext = file.split(".")[-1]
            if ext in support_ext:
                f.extract(file, path_to_save)
