"""Module for tree mapping inspired by the Bitterlich method.

This module provides an ad-hoc solution, inspired by the Bitterlich method,
to construct a 2D map of trees based on RGB, Depth estimation and Semantic
Segmentation views of an equirectangular projection of a 360° scene.
"""

import os
import argparse
import numpy as np
import cv2 as cv
import pylab as pl

from copy import copy
from PIL import Image
from math import cos, sin, pi
from matplotlib import pyplot as plt
import matplotlib.transforms as mtransforms
import matplotlib.ticker as ticker

PARSER = argparse.ArgumentParser()
PARSER.add_argument('-s', '--source',
                    nargs=3,
                    type=str,
                    default=['./rgb.png', './depth.png', './segsem.png'],
                    metavar=('RGB', 'Depth', 'SegSem'),
                    help='Source images used to compute the occupation'
                         'grid.')
PARSER.add_argument('--dmax',
                    nargs='?',
                    type=int,
                    default=50,
                    help='Maximum depth to consider in the scene'
                         '(in meters).')

PARSER.add_argument('--nsw',
                    nargs='?',
                    type=int,
                    default=10,
                    help='Number of samples of the image\'s width.'
                         'nsw must be smaller than the image\'s width.'
                         'If nsw is not a multiple of the image\'s width,'
                         'it will be rounded to its smaller'
                         'nearest.'
                         'By default, no sampling is applied.')

PARSER.add_argument('--nsd',
                    nargs='?',
                    type=int,
                    default=5,
                    help='Number of samples of the image\'s depth.'
                         'nsd must be smaller than the image\'s depth'
                         'minus dmax.'
                         'If nsd is not a multiple of the image\'s'
                         'depth, it will be rounded to its smaller'
                         'nearest.'
                         'By default, no sampling is applied.')

PARSER.add_argument('--nsh',
                    nargs='?',
                    type=int,
                    default=0,
                    help='Number of samples of the image\'s height.'
                         'nsh must be smaller than the image\'s height'
                         'minus dmax. nsh should be higher than nh.'
                         'If nsh is not a multiple of the image\'s'
                         'height, it will be rounded to its smaller'
                         'nearest.'
                         'By default, no sampling is applied.')

PARSER.add_argument('--nh',
                    nargs='?',
                    type=int,
                    default=5,
                    help='Number of sampled lines to scan, starting from'
                         'the center and expanding around it.')

PARSER.add_argument('-m', '--method',
                    nargs='?',
                    type=str,
                    default='median',
                    help='Method used to determine tree positions on the'
                         'occupation map. Available methods : mean, median.')

PARSER.add_argument('-v', '--verbose',
                    nargs='*',
                    action='store',
                    help='If true, prints out additional info.')


def get_tree_percentage(imgSS):
    """Return the percentage of tree pixels in the image.

    Args:
        imgSS (ndarray): Semantic segmentation image

    Returns:
        (float): Percentage of pixels belonging to trees
    """
    return None


def get_smaller_nearest_multiple(numerator, denominator):
    while not(numerator%denominator == 0):
        denominator -= 1
    return denominator


def cut_img_in_height(img, hstep, return_boundaries=False):
    # Cut in height
    ## Image has even height
    if HEIGHT % 2 == 0:
        mid_inf = int(HEIGHT//2)
        mid_sup = int(HEIGHT//2) + 1

        ### Number of height samples is even
        if N_HEIGHT % 2 == 0:
            shift = int((N_HEIGHT / 2)*hstep)
            inf = mid_inf - shift if shift <= min(mid_inf, HEIGHT-mid_sup) else 1
            sup = mid_sup + shift if shift <= min(mid_inf, HEIGHT-mid_sup) else HEIGHT
            img_cut = np.concatenate((img[inf-1:mid_inf-1],
                                      img[mid_sup-1:sup-1]))

        ### Number of height samples is odd
        else:
            #### Height sample step is even
            if hstep % 2 == 0:
                shift = int(((N_HEIGHT - 1) / 2)*hstep + hstep/2)
                inf = mid_inf - shift if shift <= min(mid_inf, HEIGHT-mid_sup) else 1
                sup = mid_sup + shift if shift <= min(mid_inf, HEIGHT-mid_sup) else HEIGHT
                img_cut = np.concatenate((img[inf-1:mid_inf-1],
                                          img[mid_sup-1:sup-1]))

            #### Height sample step is odd
            else:
                shift = int(((N_HEIGHT - 1) / 2)*hstep + hstep//2)
                inf = mid_inf - shift if shift < min(mid_inf-1, HEIGHT-mid_sup) else 2
                sup = mid_sup + shift if shift <= min(mid_inf, HEIGHT-mid_sup) else HEIGHT
                img_cut = np.concatenate((img[inf-2:mid_inf-1],
                                          img[mid_sup-1:sup-1]))

    ## Image has odd height
    else:
        mid = int(HEIGHT//2) + 1

        ### Number of height samples is even
        if N_HEIGHT % 2 == 0:
            shift = int((N_HEIGHT / 2)*hstep)
            inf = mid-1 - shift if shift <= mid else 1
            sup = mid+1 + shift if shift <= mid else HEIGHT
            img_cut = np.concatenate((img[inf-1:mid-2], img[mid:sup-1]))

        ### Number of height samples is odd
        else:
            #### Height sample step is even (should never arise as long as hstep is based on next smaller denominator)
            if hstep % 2 == 0:
                shift = int(((N_HEIGHT - 1) / 2)*hstep + hstep/2)
                inf = mid-1 - shift if shift <= mid else 1
                sup = mid+1 + shift if shift <= mid else HEIGHT
                img_cut = np.concatenate((img[inf-1:mid-2], img[mid:sup-1]))
            
            #### Height sample step is odd
            else:
                shift = int(((N_HEIGHT - 1) / 2)*hstep + hstep//2)
                inf = mid - shift if shift <= mid else 1
                sup = mid + shift if shift <= mid else HEIGHT
                img_cut = np.concatenate((img[inf-1:mid+1], img[mid:sup-1]))

    if return_boundaries:
        return img_cut, inf, sup
    else:
        return img_cut

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(phi, rho):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

def x_equi_to_angle(x):
    def transform(val):
        return val*360/WIDTH - 180

    if type(x) is list:
        return -np.array(list(map(transform, x)))
    else:
        return -(np.round(transform(x)))

def plot_map(map, girths):
    fig = plt.figure(figsize=(8,8))
    ax = pl.subplot(111, projection='polar')
    trans_offset = mtransforms.offset_copy(ax.transData, fig=fig,
                                           y=6, units='dots')
    for point, girth in zip(map, girths):
        x, y = np.deg2rad(point[0]), point[1]
        plt.plot(x, y, 'ro', label='trees')
        plt.text(x, y, '%d, %d\n%.2fm' % (int(point[0]), int(point[1]), girth),
                 transform=trans_offset,
                 horizontalalignment='center',
                 verticalalignment='bottom')
        circle = pl.Circle(pol2cart(x, y), girth, transform=ax.transData._b, color="red", alpha=0.4)

        ax.add_artist(circle)
    plt.suptitle('Tree map from equirectangular ({0}x{1}) RGB depth.'.format(WIDTH, HEIGHT), fontweight='bold')
    plt.title('Sampling : depth={0}, width={1}, height={2})\n'
              'Height samples considered to locate trees : {3}\n'
              'Max depth : {4}'.format(N_SAMPLE_DEPTH, N_SAMPLE_WIDTH, N_SAMPLE_HEIGHT, N_HEIGHT, DMAX))
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    rlab = plt.ylabel('Distance', labelpad=40, c='blue', fontweight='bold')
    ax.set_rlabel_position(180)
    rlab.set_rotation(90)
    plt.setp(ax.get_yticklabels(), fontweight='bold', c='blue')
    plt.grid(True, c='deepskyblue')
    plt.show()

def get_occupation_table(imgSS_clip, imgDepth_clip, dstep, hstep, wstep):
    tab = np.zeros((N_SAMPLE_DEPTH, N_HEIGHT, N_SAMPLE_WIDTH))
    perimeters = []
    for d in range(1, N_SAMPLE_DEPTH+1, 1):
        perimeters.append(2*pi*(d*dstep - dstep//2))
        mask = np.where((imgDepth_clip < (d-1)*dstep) | (imgDepth_clip > d*dstep), 0, 1)
        imgSS_masked = imgSS_clip*mask
        if VERBOSE:
            _, ((ax), (ax2)) = plt.subplots(2, 1)
            ax.imshow(255*mask, cmap='gray')
            ax.set_title('Depth mask of range [{0} - {1}] (max depth {2})'.format((d-1)*dstep, d*dstep, DMAX))
            ax.set_xlabel('Image width')
            secax = ax.secondary_xaxis('top', functions=(x_equi_to_angle, x_equi_to_angle))
            secax.set_xlabel('Real world angle')

            ax2.imshow(imgSS_masked, cmap='gray')
            ax2.set_title('Mask applied to Seg Sem')
            ax2.set_xlabel('Image width')
            secax2 = ax2.secondary_xaxis('top', functions=(x_equi_to_angle, x_equi_to_angle))
            secax2.set_xlabel('Real world angle')
            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            plt.show()

        for h in range(1, N_HEIGHT+1, 1):
            for w in range(1, N_SAMPLE_WIDTH+1, 1):
                section = imgSS_masked[(h-1)*hstep:h*hstep, (w-1)*wstep:w*wstep]
                tree_ratio = ((TREE_GRAY-5 <= section) & (section <= TREE_GRAY+5)).sum() / (section.shape[0]*section.shape[1])
                tab[d-1, h-1, w-1] = tree_ratio
                # if VERBOSE:
                #     plt.figure(figsize=(10, 10))
                #     plt.subplot(1,2,1)
                #     plt.imshow(imgSS_masked, cmap='gray')
                #     plt.subplot(1,2,2)
                #     plt.imshow(imgSS_masked[(h-1)*hstep:h*hstep, (w-1)*wstep:w*wstep], cmap='gray')
                #     plt.show()
    return tab


def get_tree_map(tab, dstep, wstep):
    tree_map = [(0,0)]
    girths = [0]
    if METHOD == 'median':
        tab2 = np.median(tab, axis=1)  # Option 1 : use values median along height
    elif METHOD == 'mean':
        tab2 = np.mean(tab, axis=1)  # Option 2 : mean out values along height

    for d in range(tab2.shape[0]):
        patch = {'start': [],
                 'stop': [],
                 'state': False}
        for w in range(tab2.shape[1]):
            if (tab2[d,w] > 0.2) and not(patch['state']):
                patch['start'].append(w)
                patch['state'] = True
            if (tab2[d,w] <= 0.2) and (patch['state']):
                patch['stop'].append(w)
                patch['state'] = False
                tree_map.append((x_equi_to_angle(w*wstep-wstep//2), (d+1)*dstep))
                girths.append((patch['stop'][-1]-patch['start'][-1])*(d+1)*dstep/wstep)
    return tree_map, girths


def main():
    """Run main function and handle arguments."""
    dstep = DMAX//N_SAMPLE_DEPTH
    wstep = WIDTH//N_SAMPLE_WIDTH
    hstep = HEIGHT//N_SAMPLE_HEIGHT

    _, ext = os.path.splitext(SOURCE[1])
    if ext in ['.png', 'jpg', 'jpeg', 'bmp']:
        imgDepth = cv.cvtColor(cv.imread(SOURCE[1]), cv.COLOR_BGR2GRAY)
    elif ext == '.dep':
        imgDepth = np.loadtxt(SOURCE[1])
    else:
        raise TypeError('Depth file format not handled. Please use one of the'
                        'following: dep, png, jpg, jpeg, bmp.') 
    imgSS = cv.cvtColor(cv.imread(SOURCE[2]), cv.COLOR_BGR2GRAY)


    imgSS_clip = copy(imgSS)
    imgSS_clip = cut_img_in_height(imgSS_clip, hstep)
    imgDepth_clip = copy(imgDepth)
    imgDepth_clip = cut_img_in_height(imgDepth_clip, hstep)

    imgSS_clip[np.where(imgDepth_clip >= DMAX)] = 255
    imgDepth_clip[np.where(imgDepth_clip >= DMAX)] = 255

    if VERBOSE:
        plt.figure(figsize=(18, 18))
        plt.subplot(1,2,1)
        plt.imshow(imgSS, cmap='gray')
        plt.title('Semantic segmentation')
        plt.subplot(1,2,2)
        plt.imshow(imgSS_clip, cmap='gray')
        plt.title('Semantic segmentation (cut)')
        plt.grid()
        plt.show()
    
    tab = get_occupation_table(imgSS_clip, imgDepth_clip, dstep, hstep, wstep)
    tree_map, girths = get_tree_map(tab, dstep, wstep)
    
    plot_map(tree_map, girths)
    

if __name__ == '__main__':
    args = PARSER.parse_args()
    SOURCE = args.source
    METHOD = args.method
    DMAX = args.dmax
    VERBOSE = args.verbose is not None
    WIDTH, HEIGHT = Image.open(SOURCE[2]).size
    # /!\ If WIDTH or HEIGHT is a prime number, their corresponding N_SAMPLE will fall to 1 -> drop the ratio constraint and work with remainders
    N_SAMPLE_DEPTH = get_smaller_nearest_multiple(DMAX, args.nsd)
    N_SAMPLE_WIDTH = get_smaller_nearest_multiple(WIDTH, args.nsw)
    if args.nsh == 0:
        N_SAMPLE_HEIGHT = HEIGHT
    else:
        N_SAMPLE_HEIGHT = get_smaller_nearest_multiple(HEIGHT, args.nsh)
    N_HEIGHT = args.nh
    TREE_GRAY = 140
    main()
