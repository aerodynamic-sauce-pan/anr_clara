import os
import re
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import argparse
from tqdm import tqdm

PARSER = argparse.ArgumentParser()
PARSER.add_argument('-s', '--source',
                    nargs='?',
                    type=str,
                    default='./data/',
                    help='Source img data to blur.')
PARSER.add_argument('-c', '--csv',
                    nargs='?',
                    type=str,
                    default='data.csv',
                    help='Source csv to pick new names from.')

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

def strip_name(x):
    debut = x.split('_0')[0]
    debut = debut.split('/')[-1]
    return int(debut)

if __name__ == '__main__':
    args = PARSER.parse_args()
    src = args.source
    if src[-1] != '/':
    	src += '/'
    csv = args.csv

    timestamps = np.array(pd.read_csv(csv, sep=',')['TimeStamp'])
    timestamps = np.sort(timestamps)
    fps = get_files_path(src, 'png')
    fps_number = list(map(strip_name, fps))
    fps_number = np.sort(np.array(fps_number))

    for _, (idx, nb) in zip(tqdm(range(len(fps_number))), enumerate(fps_number)):
        fp = src+str(nb)+'_0.png'
        ts = timestamps[idx]
        new_fp = src+str(timestamps[idx])+'.png'
        os.system(' '.join(('mv', fp, new_fp)))
