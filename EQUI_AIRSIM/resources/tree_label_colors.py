import os
import cv2 as cv
import numpy as np
import pandas as pd
import argparse

from matplotlib import pyplot as plt


def add_gray(src_fp, out_fp):
    df = pd.read_csv(src_fp)
    df[['R','G','B']] = df[['R','G','B']].applymap(lambda x: x*255)
    img_color = []

    for i in range(df.shape[0]):
        img_color.append(list(df.iloc[i][['R','G','B']]))
    img_color = np.reshape(np.array(img_color, dtype=np.uint8), (1, df.shape[0], 3))
    cv.imwrite('img_color.png', img_color)
    img_color_gray = cv.cvtColor(cv.imread('img_color.png'), cv.COLOR_BGR2GRAY)

    df['Gray'] = list(img_color_gray[0])
    df.to_csv(out_fp, index=False, sep=',')
    #os.system('rm img_color.png')

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-source', '--source',
                        nargs=1,
                        type=str,
                        help='Source csv containing color correspondance.')
    PARSER.add_argument('-o', '--output',
                        nargs=1,
                        type=str,
                        help='Output csv containing colors correspondance '
                             'plus gray values.')
    args = PARSER.parse_args()
    add_gray(args.source[0], args.output[0])