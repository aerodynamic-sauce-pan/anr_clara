"""Module for easy reshape of multiple images.

This module aims at facilitating the automatic reshape of a single image or
multiple images inside a specified directory, based on the OpenCV resize
function. The target shape, allowed types and output directory are all
configurable.
"""


import os
import argparse
import cv2
from copy import copy
from tools import get_files_path_recursively


PARSER = argparse.ArgumentParser()
PARSER.add_argument('-s', '--source',
                    nargs='*',
                    default='.',
                    help='Source image or directory of images to resize')
PARSER.add_argument('-t', '--type',
                    nargs='*',
                    default=['png', 'jpg', 'jpeg', 'bmp'],
                    help='Accepted image types')
PARSER.add_argument('-p', '--shape',
                    nargs='*',
                    default=(640, 480),
                    help='Target shape')
PARSER.add_argument('-d', '--directory',
                    nargs='?',
                    default='reshaped_imgs/',
                    help='Output directory')
PARSER.add_argument('-r', '--recursive',
                    nargs='?',
                    default=False,
                    help='Perform a recursive search through the directories')


def reshape_img(img_fp, shape):
    """Return a reshaped image.

    Args:
        img_fp (str): Source image file path
        shape (tuple of ints): Target shape

    Returns:
        (ndarray): Reshaped image
    """
    img = cv2.imread(img_fp, cv2.IMREAD_UNCHANGED)
    dim = (int(shape[0]), int(shape[1]))
    return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)


def reshape_imgs(img_fps, shape, out_dir):
    """Reshape all images into a folder.

    Loads and reshapes all images from a list of file paths and saves them
    inside a given folder.

    Args:
        img_fps (list of str): File paths to the source images
        shape (tuple of ints): Target shape
        out_dir (str): Output directory to store the reshaped images
    """
    for img_fp in img_fps:
        img_reshaped = reshape_img(img_fp, shape)
        fp, ext = os.path.splitext(img_fp)
        fn = fp.split('/')[-1]+'_'+str(shape[0])+'x'+str(shape[1])+ext # file name
        fp = '/'.join(fp.split('/')[:-1]) + '/' + out_dir # file path
        print(fp+fn)
        if not os.path.exists(fp):
            os.makedirs(fp)
        cv2.imwrite(fp+fn, img_reshaped)


def main():
    args = PARSER.parse_args()
    src = args.source
    types = args.type
    shape = args.shape
    out_dir = args.directory
    recursive = bool(args.recursive)
    if out_dir[-1] != '/':
        out_dir = out_dir+'/'
    print('SRC : ', type(src), src)

    if (len(src) == 1) and (os.path.isfile(src[0])):
        img_fps = copy(src)
    if (len(src) == 1) and (os.path.isdir(src[0])):  # if directory passed
        if recursive:
            print('recursive')
            img_fps = get_files_path_recursively(src, *types)
        else:
            print('non recursive')
            img_fps = get_files_path(src, *types)
            print('\nimg_fps : ', img_fps,'\n')
        reshape_imgs(img_fps, shape, out_dir)
    else:
        raise ValueError('Invalid source path')


if __name__ == '__main__':
    main()
