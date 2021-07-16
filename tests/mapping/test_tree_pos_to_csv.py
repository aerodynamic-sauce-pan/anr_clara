import numpy as np
import pandas as pd
from tqdm import tqdm
from mapping.tree_pos_to_csv import parse_to_csv as parser

def test_main():
    out = parser('tests/mapping/log_output_tree_transformations_small.txt',
                 ['Name', 'ID', 'LocX', 'LocY', 'LocZ', 'RotP', 'RotY', 'RotR', 'ScaX', 'ScaY', 'ScaZ'])
    out_valid = pd.read_csv('tests/mapping/log_parsed_valid.csv', dtype=str)
    out_valid.loc[:, 'ID':] = out_valid.loc[:, 'ID':].astype(np.float64)
    assert out.equals(out_valid)