import os
import re
import argparse
import numpy as np
import cv2 as cv
import pandas as pd

from tqdm import tqdm
from time import time
from sklearn import cluster
from matplotlib import pyplot as plt


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


def compute_distance(array1, array2, norm='one'):
    if norm == 'one':
        return np.abs(np.square(array1-array2))
    else:
        raise ValueError('Unknown norm. Please choose between the following :'
                         'one.')

def compute_distance3D(array1, array2, norm='euclidian'):
    if norm == 'euclidian':
        return np.sqrt(np.sum(np.square(array1-array2), axis=2))
    else:
        raise ValueError('Unknown norm. Please choose between the following :'
                         'euclidian.')


def get_closest_color(a_value, colors):
    closest_col = {'dist': np.inf, 'ind': -1}
    for idx, col in colors.iterrows():
        dist = compute_distance3D(a_value, col)
        if dist < closest_col['dist']:
            closest_col['dist'] = dist
            closest_col['ind'] = idx
    return closest_col['ind']


def recolor_pixel(pix, colors):
    ccol_id = get_closest_color(pix, colors)
    pix = np.array(colors.loc[ccol_id][['R','G','B']])
    return pix


def recolor_pixel_fast(img, img_gray, colors):
    n, m, d = img.shape
    img_candidates = np.zeros((n, m, colors.shape[0]))
    img_clustered = np.zeros((n, m, d), dtype=np.uint8)
    for (_, val), idx in zip(colors.iterrows(), range(colors.shape[0])):
        colors_array = np.ones((n, m))*val['Gray']
        dist = compute_distance(img_gray, colors_array)
        print('dist : ', type(dist), dist.shape, dist)
        img_candidates[:, :, idx] = dist
    print('img_candidates : ', img_candidates.shape)
    img_candidates = np.argmin(img_candidates, axis=2)
    print('argmin : ', img_candidates.shape, img_candidates)

    print('img_clustered : ', img_clustered.shape)
    for idx in range(colors.shape[0]):
        img_clustered[np.where(img_candidates == idx)] = colors.iloc[idx][['R', 'G', 'B']]
    # vfunc = np.vectorize(lambda x: colors.iloc[x][['R', 'G', 'B']])
    # img_clustered = vfunc(img_candidates)
    print('img_clustered after vectorize :',img_clustered.shape, img_clustered)
    return img_clustered


def get_id(x):
    debut = x.split('.')[0]
    debut = debut.split('/')[-1]
    return int(debut)


def main(source_dir, out_dir, method, colors_csv=None):
    if method == 'manual':
        colors = pd.read_csv(colors_csv)
        # colors[['R','G','B']] = colors[['R','G','B']].applymap(lambda x: x*255)
        print('colors : ', colors)
    fps = get_files_path(source_dir, 'png')
    fps_number = list(map(get_id, fps))
    ind_sort = np.argsort(np.array(fps_number))
    for ind in tqdm(ind_sort[:1]):
        img = cv.cvtColor(cv.imread(fps[ind]), cv.COLOR_BGR2RGB)
        img_gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        n, m, d = img.shape
        if method == 'kmeans':
            img = img.reshape((n*m, d))
            kmeans_dep = cluster.KMeans(n_clusters = 14) # 12 trees + sky + ground
            kmeans_dep.fit(img)
            centers = np.uint8(kmeans_dep.cluster_centers_)
            print('centers : ', centers)
            Xseg = kmeans_dep.predict(img)
            Xseg = np.array([centers[n] for n in Xseg])
            Xseg = np.uint8(Xseg.reshape(n, m, d))

            plt.figure()
            plt.imshow(Xseg)
            plt.title(fps[ind].split('/')[-1])
            plt.show()
        elif method == 'manual':
            t1 = time()
            colors = colors.set_index('Color_ID')
            img_clust = recolor_pixel_fast(img[:300,:300], img_gray[:300, :300], colors)
            # img_small = img[:200,:200]
            # for i in tqdm(range(img_small.shape[0])):
            #     for j in range(img_small.shape[1]):
            #         img_small[i, j] = recolor_pixel(img_small[i, j], colors)
                    
            #vfunc = np.vectorize(recolor_pixel, excluded=['colors'])
            #img_clust = vfunc(pix=img_test, colors=colors)
            print(f'Time for manual clustering : {time()-t1} s.')
            plt.figure()
            plt.imshow(img_clust)
            plt.title(fps[ind].split('/')[-1] + 'clustered')
            plt.show()


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-s', '--source',
                        nargs=1,
                        type=str,
                        help='Source directory containing images to apply'
                             ' clustering on.')
    PARSER.add_argument('--method',
                        nargs=1,
                        type=str,
                        default='manual',
                        help='Clustering method. Chose between : manual, '
                             'kmeans.')
    PARSER.add_argument('--colors',
                        nargs=1,
                        type=str,
                        help='CSV file containing the list of colors used for '
                             'the labels.')
    PARSER.add_argument('-o', '--output',
                        nargs=1,
                        type=str,
                        default='CAPTURES_clustered',
                        help='Output directory.')
    args = PARSER.parse_args()
    if args.output[-1] != '/':
        args.output += '/'
    if args.method == 'manual':
        main(args.source[0], args.output, args.method, colors_csv=args.colors[0])
    elif args.method == 'kmeans':
        main(args.source[0], args.output, args.method)