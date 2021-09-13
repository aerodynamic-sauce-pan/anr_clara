"""AirSim recordings interpolation script.

This script is intended for interpolating values of AirSim CSV record files.
Affected columns are the following : ['VehicleName', 'TimeStamp', 'POS_X',
'POS_Y', 'POS_Z', 'Q_W', 'Q_X', 'Q_Y', 'Q_Z']. Values are interpolated evenly
between two successive lines, as many times as requested by the user.
Although, 'TimeStamp' values must be intergers, therefore the maximum
number of interpolations is determined by the following expression :
max(n_interp, TimeStamp[i+1]-TimeStamp[i]-1). Values of 'VehicleName' are
simply repeated.
"""

import pandas as pd
import argparse
import numpy as np


PARSER = argparse.ArgumentParser()
PARSER.add_argument('-s', '--source',
                    nargs='?',
                    type=str,
                    default='airsim_rec.csv',
                    help='Source csv')
PARSER.add_argument('-n', '--n_interp',
                    nargs='?',
                    type=int,
                    default=1,
                    help='Number of interpolation')
PARSER.add_argument('-o', '--output',
                    nargs='?',
                    type=str,
                    default='csv_augmented.csv',
                    help='Output path.')

def get_min_ts_diff(csv):
    """Return the smallest difference between two successive TimeStamp values.

    Args:
        csv (pd.Dataframe): Source CSV as pandas dataframe.

    Returns:
        (int): smallest difference between 2 successive TimeStamp values.
    """
    diff = np.inf
    for vi, vip1 in zip(csv['TimeStamp'][:-1], csv['TimeStamp'][1:]):
        diff = min(diff, abs(vip1-vi))
    return diff


def compute_interp(col, line, next_line, iter):
    """Compute 1 interpolation value.

    For 2 given successive lines of the source CSV, represented as a pandas
    dataframe, this method computes 1 interpolated value for the specified
    column, based on the n-th interpolated value requested.

    Args:
        col (str): Column to interpolate values from.
        line (pd.core.series.Series): First line of values.
        next_line (pd.core.series.Series): Second line of values.
        iter (int): n-th interpolated value requested.

    Returns:
        Interpolated value (type may vary).
    """

    if col =='VehicleName':
        return line[col]
    elif col == 'TimeStamp':
        step = abs(line[col] - next_line[col])//(N_INTERP+1)
        return line[col] + iter*step
    elif col in ['POS_X', 'POS_Y', 'POS_Z', 'Q_W', 'Q_X', 'Q_Y', 'Q_Z']:
        step = abs(line[col] - next_line[col])/(N_INTERP+1)
        if line[col] <= next_line[col]:
            return round(line[col] + iter*step, 5)
        else:
            return round(line[col] - iter*step, 5)
    else:
        return np.NaN


def create_new_lines(cols, line, next_line):
    """Compute interpolated values between two given lines.

    This method computes every interpolated values for every column of two
    successive lines of the CSV, represented as a pandas dataframe.

    Args:
        cols (int): Columns to interpolate values from.
        line (pd.core.series.Series): First line of values.
        next_line (pd.core.series.Series): Second line of values.

    Returns:
        (pd.DataFrame): Interpolated values.
    """
    new_lines = pd.DataFrame(columns=cols)
    for iter in range(N_INTERP):
        new_line = pd.DataFrame(columns=cols)
        for col in cols[:-1]:
            new_line.loc[0, col] = compute_interp(col, line, next_line, iter+1)
        new_line.loc[0, cols[-1]] = 'img_machine_1__0_' + str(new_line.loc[0, 'TimeStamp'])+'.png'
        new_lines = new_lines.append(new_line, ignore_index=True)
    return new_lines


def augment_csv(src, out):
    """Create an augmented AirSim record CSV via interpolation.

    Args:
        src (str): File path to the source CSV.
        out (str): Output file path to the augmented CSV.
    """
    csv = pd.read_csv(src, sep='\t')
    csv_augmented = pd.DataFrame(columns=csv.columns)
    for i in range(csv.shape[0]-1):
        new_lines = create_new_lines(csv.columns, csv.iloc[i], csv.iloc[i+1])
        csv_augmented = csv_augmented.append(csv.iloc[i], ignore_index=True)
        csv_augmented = csv_augmented.append(new_lines, ignore_index=True)
        if i >= csv.shape[0]-2:
            csv_augmented = csv_augmented.append(csv.iloc[i+1], ignore_index=True)
    csv_augmented.replace(-0, 0.0, inplace = True)
    csv_augmented.to_csv(out, sep='\t', index=False)


if __name__ == '__main__':
    args = PARSER.parse_args()
    N_INTERP = min(get_min_ts_diff(pd.read_csv(args.source, sep='\t')), args.n_interp)
    augment_csv(args.source, args.output)