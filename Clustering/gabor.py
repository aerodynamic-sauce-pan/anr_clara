"""Gabor Filter module.

This module provides functions to apply a gabor filter on images.
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


def get_img(input_Path):
    """Return paths of images recursively from an input directory.

    Returns .jpg and .png files from all directories and their sub-directories
    of an input path.

    Args:
        input_Path (str): Path from which to start probing for images.

    Returns:
        (tuple): Tuple of images' paths and names.
    """
    img_paths = []
    filenames = []
    for (path, _, files) in os.walk(input_Path):
        for filename in files:
            if filename.endswith(('.jpg', '.png')):
                filenames.append(filename)
                img_paths.append(path+'/'+filename)
    return img_paths, filenames


def build_filters():
    """Build a Gabor filter.

    Returns:
        (list): Gabor filters.
    """
    filters = []
    ksize = [40, 50, 60, 70, 80, 90]  # gabor scale, 6
    lamda = 20  # wavelength
    for theta in np.arange(0, np.pi, np.pi/4):  # 0°, 45°, 90° and 135°
        for K, _ in enumerate(ksize):
            kern = cv2.getGaborKernel((ksize[K], ksize[K]), 10, theta,
                                      lamda, 0.5, 0, ktype=cv2.CV_32F)
            kern /= 1.5*kern.sum()
            filters.append(kern)
    plt.figure(1)

    # Used to draw filters
    for temp, _ in enumerate(filters):
        plt.subplot(4, len(ksize), temp + 1)
        plt.imshow(filters[temp])
    plt.show()
    return filters


def getGabor(filenames, img, filters):
    """Extract Gabor features.

    Args:
        filenames (str): Input images' names
        img (ndarray): Input image
        filters (list): Gabor filters

    Returns:
        list: Gabor features vector
    """
    res = []  # Filter result
    for j, _ in enumerate(filters):
        # res1 = process(img, filters[i])
        accum = np.zeros_like(img)
        for kern in filters[j]:
            fimg = cv2.filter2D(img, cv2.CV_8UC1, kern)
            accum = np.maximum(accum, fimg, accum)
        res.append(np.asarray(accum))

    # Used to draw filtering effects
    plt.figure(2)
    for temp, _ in enumerate(res):
        plt.subplot(4, 6, temp+1)
        plt.imshow(res[temp], cmap='gray')
    plt.show()
    print('res:', type(res), len(res), res[0].shape)
    cv2.imshow(filenames[0], res[0])
    cv2.waitKey(0)
    # Return the filtering result, the result is 24 pictures, arranged according
    # to the gabor angle.
    return res


def main():
    """Run main function."""
    input_Path = 'TrainImages/IS'
    img_paths, filename = get_img(input_Path)
    filters = build_filters()
    i = 0
    for img in img_paths:
        i = i+1
        img = cv2.imread(img)
        getGabor(filename, img, filters)


if __name__ == '__main__':
    main()
