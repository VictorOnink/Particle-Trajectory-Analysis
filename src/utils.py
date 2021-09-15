import os
import pickle
import numpy as np


def save_obj(filename, item):
    """
    Saving a item using pickle
    :param filename:
    :param item:
    :return:
    """
    with open(filename + '.pkl', 'wb') as f:
        pickle.dump(item, f, pickle.HIGHEST_PROTOCOL)


def load_obj(filename):
    """
    Loading the data that had been previously pickled using save_obj()
    :param filename:
    :return:
    """
    with open(filename + '.pkl', 'rb') as f:
        return pickle.load(f)


def check_file_exist(file_name: str):
    """
    Check if the file called file_name already exists
    :param file_name:
    :return:
    """
    return os.path.isfile(file_name)


def remove_file(conduct: bool, file_name: str):
    """
    Removing a file, but only if conduct is True and the file exists
    :param conduct:
    :param file_name:
    :return:
    """
    if conduct:
        if check_file_exist(file_name):
            os.remove(file_name)


def check_direc_exist(direc: str, create_direc=False):
    if not create_direc:
        return os.path.isdir(direc)
    if create_direc:
        if not os.path.isdir(direc):
            os.makedirs(direc)
