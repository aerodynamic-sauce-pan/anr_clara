import pandas as pd
import os
import re
import numpy as np
import argparse

PARSER = argparse.ArgumentParser()
PARSER.add_argument('-s', '--source',
                    nargs='?',
                    type=str,
                    default='data.csv',
                    help='Source csv data to reduce.')
PARSER.add_argument('-d', '--dir',
                    nargs='?',
                    type=str,
                    default='./data',
                    help='Directory containing images to which to fit the csv file.')

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


def get_file_name(fp):
	return (fp.split('/')[-1]).split('.')[0]

if __name__ == '__main__':
    args = PARSER.parse_args()
    csv_src = args.source
    img_dir = args.dir

    fps = list(map(get_file_name, get_files_path(img_dir, 'png')))
    csv = pd.read_csv(csv_src, sep=',', dtype=str)

    csv.iloc[:len(fps), :].to_csv('data_reduced.csv', header=True, index=False)
