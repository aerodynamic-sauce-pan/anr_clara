import os
import re
import cv2 as cv
import argparse
from tqdm import tqdm

PARSER = argparse.ArgumentParser()
PARSER.add_argument('-s', '--source',
                    nargs='?',
                    type=str,
                    default='./data',
                    help='Source img data to convert.')

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
    
if __name__ == '__main__':
    args = PARSER.parse_args()
    src = args.source

    fps = get_files_path(src, 'png')
    for fp in tqdm(fps):
        img = cv.cvtColor(cv.imread(fp, cv.IMREAD_UNCHANGED), cv.COLOR_RGB2GRAY)
        cv.imwrite(fp, img)
