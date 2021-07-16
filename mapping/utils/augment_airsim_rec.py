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
    diff = np.inf
    for vi, vip1 in zip(csv['TimeStamp'][:-1], csv['TimeStamp'][1:]):
        diff = min(diff, abs(vip1-vi))
    return diff

def compute_interp(col, line, next_line, iter):
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
    new_lines = pd.DataFrame(columns=cols)
    for iter in range(N_INTERP):
        new_line = pd.DataFrame(columns=cols)
        for col in cols[:-1]:
            new_line.loc[0, col] = compute_interp(col, line, next_line, iter+1)
        new_line.loc[0, cols[-1]] = 'img_machine_1__0_'+str(new_line.loc[0, 'TimeStamp'])+'.png'
        new_lines = new_lines.append(new_line, ignore_index=True)
    return new_lines


def augment_csv(src, out):
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