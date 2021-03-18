"""Toolbox with various convenient functions.

This file contains a set a useful functions which help to easily manage
and monitor files, performances...
"""

import os
import re
import time


def get_files_path_recursively(path, *args):
    """Retrieve specific files path recursively from directory.

    Retrieve the path of all files with one of the given extension names,
    in the given directory and all its subdirectories, recursively.
    The extension names should be given as a list of strings. The search for
    extension names is case sensitive.

    Args:
        path (str): root directory from which to search for files recursively
        *args: list of file extensions (as strings) to be considered

    Returns:
        result (list): list of paths of every files in the directory and all
                       its subdirectories
    """
    reg_list_img_format = ""
    for i in args:
        reg_list_img_format += str(i) + "|"
    reg_list_img_format = "".join(list(reg_list_img_format)[:-1])
    result = [os.path.join(dp, f)
              for dp, dn, filenames in os.walk(path)
              for f in filenames
              if re.search(rf".*\.({reg_list_img_format})",
                           os.path.splitext(f)[1])]
    return result


def get_files_path(path, *args):
    """Retrieve specific files path from a directory.

    Retrieves the path of all files with one of the given extension names,
    in the given directory. The extension names should be given as a list of
    strings. The search for extension names is case sensitive.

    Args:
        path (str): root directory from which to search for files recursively
        *args: list of file extensions (as strings) to be considered

    Returns:
        result (list): list of paths of every files in the directory and all
                       its subdirectories
    """
    reg_list_img_format = ""
    for i in args:
        reg_list_img_format += str(i) + "|"
    reg_list_img_format = "".join(list(reg_list_img_format)[:-1])
    result = [os.path.join(path, f)
              for f in os.listdir(path)
              if re.search(rf".*\.({reg_list_img_format})",
                           os.path.splitext(f)[1])]
    return result


def chronometer(function_to_time, function_name, *args):
    """Time the execution time of given function.

    Return in seconds the execution time of a given function with its name and
    arguments.

    Args:
        function_to_time: function to call, passed by reference
        function_name (str): function's name to call when displaying results
        *args: list a arguments to pass on to the function to call

    Returns:
        res: output of the function to call
    """
    t_before = time.time()
    res = function_to_time(*args)
    t_after = time.time()
    print("Execution time of function ", function_name, " : ", t_after-t_before,
          " sec")
    return res
