import argparse
import pandas as pd
import numpy as np

from tqdm import tqdm
from time import time


def compute_distance(a_tree_pos, a_drone_pos, norm='euclidian2D'):
    if norm == 'euclidian2D':
        return round(np.sqrt(np.sum(np.square((a_tree_pos-a_drone_pos)))), 5)
    else:
        raise ValueError('Unknown norm. Please choose between the following :'
                         'euclidian2D.')


def get_distances(row_drone, trees_ib):
    dists = []
    for _, row_tree in trees_ib.iterrows():
        dists.append(compute_distance(np.array(row_tree[['LocX', 'LocY']]),
                                      np.array(row_drone[['POS_X', 'POS_Y']])))
    return np.array(dists)


def select_in_bounds(row_drone, tree_pos, dmax):
    tree_pos_in_bounds = tree_pos[(abs(tree_pos['LocX'] - row_drone['POS_X']) <= dmax) &
                                  (abs(tree_pos['LocY'] - row_drone['POS_Y']) <= dmax) &
                                  (abs(tree_pos['LocZ'] - row_drone['POS_Z']) <= dmax)]
    return tree_pos_in_bounds


def get_distance_series(tree_pos, drone_pos, dmax):
    print(f'Computing distances...')
    t1 = time()
    dist_series = dict()
    for _, iter in zip(tqdm(range(drone_pos.shape[0])), drone_pos.iterrows()):
        row_drone = iter[1]
        if dmax != np.inf:
            trees_in_bounds = select_in_bounds(row_drone, tree_pos, dmax)
        else:
            trees_in_bounds = tree_pos.copy()
        dst = get_distances(row_drone, trees_in_bounds)
        idx = np.argwhere(dst <= dmax).flatten()
        dist_series[int(row_drone['TimeStamp'])] = trees_in_bounds.iloc[idx, :]
        dist_series[int(row_drone['TimeStamp'])].insert(len(trees_in_bounds.columns), 'Distance', dst[idx])
        dist_series[int(row_drone['TimeStamp'])] = dist_series[int(row_drone['TimeStamp'])]
    print(f'Distances computed in {time()-t1}s.')
    return dist_series


def dist_series_to_csv(dist_series, drone_pos, output):
    print(f'Exporting distances as csv...')
    t1 = time()
    timestamps = list(dist_series.keys())
    dist_csv = drone_pos[drone_pos['TimeStamp'].isin(timestamps)]

    trees_dist = pd.DataFrame(columns=dist_series[list(dist_series.keys())[0]].columns)
    for ts in tqdm(timestamps):
        trees_dist = pd.concat([trees_dist, dist_series[ts]], ignore_index=True) # Build trees df by rows
        ts_row = dist_csv[dist_csv['TimeStamp'] == ts]
        dist_csv = pd.concat([dist_csv.loc[:ts_row.index.values[0]-1, :]] +
                             [ts_row]*(dist_series[ts].shape[0]) +
                             [dist_csv.loc[ts_row.index.values[0]+1:, :]],
                             ignore_index=True)
    dist_csv = pd.concat([dist_csv, trees_dist], axis=1)
    dist_csv.to_csv(output, sep=',', index=False)
    print(f'Csv exported in {time()-t1}s.')


def main(src_tree, src_drone, dmax=np.inf, output=None):
    tree_pos = pd.read_csv(src_tree)[['Name', 'ID', 'LocX', 'LocY', 'LocZ']]
    drone_pos = pd.read_csv(src_drone)[['TimeStamp', 'POS_X', 'POS_Y', 'POS_Z']]
    dist_series = get_distance_series(tree_pos, drone_pos, dmax)
    if output is not None:
        dist_series_to_csv(dist_series, drone_pos, output)
    return None


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-t', '--tree',
                        nargs=1,
                        type=str,
                        default='log_tree.csv',
                        help='Source parsed log of tree transformations.')
    PARSER.add_argument('-d', '--drone',
                        nargs=1,
                        type=str,
                        default='log_drone.csv',
                        help='Source drone pose log file.')
    PARSER.add_argument('--dmax',
                        nargs='?',
                        type=int,
                        default=np.inf,
                        help='Maximum depth to consider in the scene'
                             '(in meters).')
    PARSER.add_argument('-o', '--output',
                        nargs='*',
                        type=str,
                        default='distances.csv',
                        help='Export path.')
    ARGS = PARSER.parse_args()
    main(ARGS.tree[0], ARGS.drone[0], ARGS.dmax, ARGS.output[0])