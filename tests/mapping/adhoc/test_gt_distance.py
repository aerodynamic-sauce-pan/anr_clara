import pandas as pd
import numpy as np

from tqdm import tqdm
from time import time

from mapping.adhoc.gt_distance import main, compute_distance, get_distances, select_in_bounds, get_distance_series


PATH = 'tests/mapping/adhoc/'
TREE_LOG_PATH = PATH + 'tree_log_test.csv'
DRONE_LOG_PATH = PATH + 'drone_log_test.csv'


def test_main():
    # Tests both main and dist_series_to_csv
    out = 'distances_test.csv'
    main(TREE_LOG_PATH, DRONE_LOG_PATH, dmax=30, export=PATH+out)
    dist_test = pd.read_csv(PATH+out)
    dist_valid = pd.read_csv(PATH+'distances_valid.csv')
    assert dist_test.equals(dist_valid)

def test_compute_distance():
    dronePos = np.array([0,24])
    treePos = np.array([7,0])
    dst = compute_distance(dronePos, treePos, norm='euclidian2D')
    assert dst == 25

def test_get_distances():
    tree_log = pd.read_csv(TREE_LOG_PATH)
    drone_log = pd.read_csv(DRONE_LOG_PATH)
    row_drone = drone_log.iloc[0, :]
    dsts = get_distances(row_drone, tree_log)
    dsts_valid = np.array([5, 12.36931687685298])
    assert np.array_equal(dsts, dsts_valid)

def test_select_in_bounds():
    PATH = 'tests/mapping/adhoc/'
    tree_log = pd.read_csv(TREE_LOG_PATH)
    drone_log = pd.read_csv(DRONE_LOG_PATH)
    in_bounds = select_in_bounds(drone_log.iloc[0, :], tree_log, dmax=10)
    in_bounds_valid = tree_log.iloc[:1, :]
    assert in_bounds.equals(in_bounds_valid)

def test_get_distance_series():
    tree_log = pd.read_csv(TREE_LOG_PATH)
    drone_log = pd.read_csv(DRONE_LOG_PATH)

    df1 = tree_log.drop(1, axis=0)
    df1.insert(len(df1.columns), 'Distance', [5.0])
    print('df1: ', df1)
    df2 = df1.copy()
    df2['Distance'] = [1.0]
    print('df2: ', df2)

    dst_series = get_distance_series(tree_log, drone_log, 6)
    print('dst_series: ', dst_series)
    dst_series_valid = {10: df1, 20: df2}
    print('dst_series_valid: ', dst_series_valid)
    for (idx1, val1), (idx2, val2) in zip(dst_series.items(), dst_series_valid.items()):
        assert (idx1 == idx2) and (val1.equals(val2))