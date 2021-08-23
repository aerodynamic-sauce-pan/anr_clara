import pandas as pd
import os

def test_valid_output():
    os.system('python src/augment_airsim_rec.py -s tests/test_airsim_rec.csv -o tests/test_csv_augmented.csv -n 1')
    csv_augmented = pd.read_csv('tests/test_csv_augmented.csv')
    csv_valid = pd.read_csv('tests/test_airsim_rec_valid.csv')
    assert csv_augmented.equals(csv_valid)

test_valid_output()