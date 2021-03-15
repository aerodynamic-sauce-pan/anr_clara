"""Module for easy reshape of multiple images.

This module aims at facilitating the automatic reshape of a single image or
multiple images inside a specified directory, based on the OpenCV resize
function. The target shape, allowed types and output directory are all
configurable.
"""


import os
import argparse
import cv2
from .tools import get_files_path, get_files_path_recursively


PARSER = argparse.ArgumentParser()
requiredArgs = PARSER.add_argument_group('Required arguments')
requiredArgs.add_argument('-s', '--source',
                          nargs='*',
                          required=True,
                          help='Source images or directories of images to '
                               'reshape')
PARSER.add_argument('-f', '--format',
                    nargs='*',
                    default=['png', 'jpg', 'jpeg', 'bmp'],
                    help='Accepted image formats. By default, \'png\', \'jpg\''
                         ', \'jpeg\' and \'bmp\' formats are accepted.')

PARSER.add_argument('-p', '--shape',
                    nargs=2,
                    type=int,
                    default=[640, 480],
                    metavar=('width', 'height'),
                    help='Target shape. Defaults to 640x480.')
PARSER.add_argument('-d', '--directory',
                    nargs='?',
                    default='',
                    help='Output directory. By default, outputs the reshaped '
                         'images in the same directory as their original '
                         'versions.')
PARSER.add_argument('-m', '--method',
                    nargs='?',
                    default='basic',
                    help='Select a search method among : basic, resursive. '
                         'Basic: reshapes images passed as input and images '
                         'directly located in passed directories. '
                         'Recursive: recursively retrieves images from all '
                         'directories and sub-directories.')
PARSER.add_argument('-v', '--verbose',
                    nargs='*',
                    action='store',
                    help='If true, prints out additional info.')


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


def reshape_imgs(img_fps, shape, out_dir, default_dir=True, verbose=False):
    """Reshape all images into a folder.

    Loads and reshapes all images from a list of file paths and saves them
    inside a given folder.

    Args:
        img_fps (list of str): File paths to the source images
        shape (tuple of ints): Target shape
        out_dir (str): Output directory to store the reshaped images
    """
    if verbose:
        print('==== Reshaped images ====')
    for img_fp in img_fps:
        img_reshaped = reshape_img(img_fp, shape)
        fp, ext = os.path.splitext(img_fp)
        fn = fp.split('/')[-1] + '_' + str(shape[0]) + 'x' + str(shape[1]) + ext
        if default_dir:
            fp = '/'.join(fp.split('/')[:-1]) + '/' + out_dir
        else:
            fp = out_dir
        if not os.path.exists(fp):
            os.makedirs(fp)
        if verbose:
            print(f'{img_fp} -> {fp+fn}')
        cv2.imwrite(fp+fn, img_reshaped)


def main():
    """Run main function and handle arguments.

    Raises
    ------
    ValueError
        If the image search method is not known.
    """
    args = PARSER.parse_args()
    verbose = args.verbose is not None
    src = args.source
    formats = args.format
    shape = tuple(args.shape)
    method = args.method
    out_dir = args.directory
    default_dir = False
    if not out_dir:
        default_dir = True
        out_dir = 'reshaped_imgs/'
    if out_dir[-1] != '/':
        out_dir = out_dir+'/'

    paths = []
    if verbose:
        print(f'Reshaping at {shape[0], shape[1]} using {method} method.'
              f' {len(src)} paths to process... ')
    for path in src:
        if os.path.exists(path):
            if os.path.isfile(path):
                paths.append(path)
            elif os.path.isdir(path):
                if method == 'recursive':
                    paths += get_files_path_recursively(path, *formats)
                elif method == 'basic':
                    paths += get_files_path(path, *formats)
                else:
                    raise ValueError('Unknown search method. Use one of the'
                                     ' following : basic, recursive')
        else:
            print('Invalid source path :', path)
    reshape_imgs(paths, shape, out_dir, default_dir, verbose)


if __name__ == '__main__':
    main()
