"""Module for parsing UE4 retrieved tree instances positions.

This modules parses a text file containing references and transformations of
tree instances retrieved from the RedwoodForest environment through the
BP_Collector blueprint in UE4 Editor.
"""

import argparse
import numpy as np
import pandas as pd
from tqdm import tqdm


def get_name(string):
    """Get the component's name.

    Args:
        string (str): Component info given by blueprint output.

    Returns:
        (str): Component's name
    """
    return string.split('Component : ')[-1].split(' of ID')[0]


def get_ID(string):
    """Get the ID of a component instance.

    Args:
        string (str): Component info given by blueprint output.

    Returns:
        (str): Instance ID
    """
    return string.split('ID #')[-1].split(' | ')[0]


def get_loc(string):
    """Get the location of a component instance.

    Args:
        string (str): Component info given by blueprint output.

    Returns:
        (list): List of X, Y, Z coordinates of the component instance relatively
                to the environment's origin.
    """
    LocX = string.split('Location : X=')[-1].split(' | ')[0].split(' ')[0]
    LocY = string.split('Y=')[1].split(' ')[0]
    LocZ = string.split('Z=')[1].split(' ')[0]
    return [LocX, LocY, LocZ]


def get_rot(string):
    """Get the rotations of a component instance.

    Args:
        string (str): Component info given by blueprint output.

    Returns:
        (list): List of Pitch, Yaw, Roll rotations of the component instance.
    """
    RotX = string.split('Rotation : P=')[-1].split(' | ')[0].split(' ')[0]
    RotY = string.split('Y=')[2].split(' ')[0]
    RotZ = string.split('R=')[1].split(' ')[0]
    return [RotX, RotY, RotZ]


def get_sca(string):
    """Get the scale factors of a component instance.

    Args:
        string (str): Component info given by blueprint output.

    Returns:
        (list): List of X, Y, Z scale factors of the component instance.
    """
    ScaX = string.split('Scale : X=')[-1].split(' | ')[0].split(' ')[0]
    ScaY = string.split('Y=')[3].split(' ')[0]
    ScaZ = string.split('Z=')[2].split('\n')[0]
    return [ScaX, ScaY, ScaZ]


def parse_a_line(line, cols):
    """Parse a line of the text document created for the blueprint output.

    Args:
        line (str): Component info given by blueprint output.
        cols (list): List of column names.

    Returns:
        (pd.Series): Parsed line as a pandas series.
    """
    df_line = pd.DataFrame(columns=cols)
    df_line.loc[0, 'Name'] = get_name(line)
    df_line.loc[0, 'ID'] = get_ID(line)
    for i in range(1, 4, 1):
        df_line.loc[0, cols[i+1]] = get_loc(line)[i-1]
        df_line.loc[0, cols[i+4]] = get_rot(line)[i-1]
        df_line.loc[0, cols[i+7]] = get_sca(line)[i-1]
    return df_line


def parse_to_csv(src_log, cols):
    """Parse the text document as a csv.

    Args:
        src_log (str): Path to source text file.
        cols (list): List of column names.

    Returns:
        (pd.DataFrame): Parsed csv.
    """
    out_csv = pd.DataFrame(columns=cols)
    with open(src_log, 'r', encoding=('utf-8')) as file:
        lines = file.readlines()
        for line in tqdm(lines):
            parsed_line = parse_a_line(line, cols)
            out_csv = out_csv.append(parsed_line.iloc[0, :], ignore_index=True)
        out_csv.loc[:, 'ID':] = out_csv.loc[:, 'ID':].astype(np.floatmgzn64)
        return out_csv


def main(src_log, out_log, cols):
    """Run parsing methods and save results.

    Args:
        src_log (str): Path to source text file.
        out_log (str): Path to output csv file.
        cols (list): List of column names.
    """
    out = parse_to_csv(src_log, cols)
    out.to_csv(out_log, header=True, index=False, float_format=str)


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-s', '--source',
                        nargs=1,
                        type=str,
                        default='log.txt',
                        help='Source log text file.')
    PARSER.add_argument('-o', '--output',
                        nargs=1,
                        type=str,
                        default='log_parsed.csv',
                        help='Output log file parsed as csv.')
    PARSER.add_argument('--cols',
                        nargs='*',
                        type=str,
                        default=['Name', 'ID', 'LocX', 'LocY', 'LocZ', 'RotP',
                                 'RotY', 'RotR', 'ScaX', 'ScaY', 'ScaZ'],
                        help='Output log file parsed as csv.')
    ARGS = PARSER.parse_args()
    main(ARGS.source[0], ARGS.output[0], ARGS.cols)
