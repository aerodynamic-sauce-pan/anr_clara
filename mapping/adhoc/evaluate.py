import numpy as np
import pandas as pd
import argparse

from mapping.adhoc.geometry import get_angle2D
from IPython.display import display


def get_closest_trees_index(gt_vals, pred_vals):
    gt_vals_closest = []
    array = np.asarray(gt_vals['Distance'])
    for value in pred_vals['Distance']:
        idx = np.abs(array - value).argmin()
        gt_vals_closest.append(idx)

    return np.array(gt_vals_closest)


def compute_errors(pred, gt, girths):
    errors = dict()
    gt_angle = []
    gt_dist = []
    gt_girth = []
    pred_vals = {'Angle': np.array(pred['Tree_angle'])+180, # Offset to avoid treating negative angles separately
                 'Distance': np.array(pred['Tree_distance']),
                 'Girth': np.array(pred['Tree_girth'])}
    cti = get_closest_trees_index(gt, pred_vals)

    for idx in cti:
        row = gt.iloc[idx, :]
        gt_angle.append(np.arctan2(row['LocY']-row['POS_Y'], row['LocX']-row['POS_X']))
        gt_dist.append(row['Distance'])
        gt_girth.append(list(girths['Girth'][girths['Name'] == row['Name']])[0])
    gt_vals = {'Angle': np.array(gt_angle)+180, # Offset to avoid treating negative angles separately
               'Distance': np.array(gt_dist),
               'Girth': np.array(gt_girth)}

    # print('gt_vals : ', gt_vals['Angle'].shape, gt_vals['Distance'].shape, gt_vals['Girth'].shape, gt_vals['Angle']-180)
    # print('pred_vals : ', pred_vals['Angle'].shape, pred_vals['Distance'].shape, pred_vals['Girth'].shape, pred_vals['Angle']-180)
    errors['Absolute'] = {'Angle': np.abs(pred_vals['Angle']-gt_vals['Angle']),
                          'Distance': np.abs(pred_vals['Distance']-gt_vals['Distance']),
                          'Girth': np.abs(pred_vals['Girth']-gt_vals['Girth'])}
    errors['Mean'] = {'Angle': np.mean(errors['Absolute']['Angle']),
                      'Distance': np.mean(errors['Absolute']['Distance']),
                      'Girth': np.mean(errors['Absolute']['Girth'])}
    errors['Median'] = {'Angle': np.median(errors['Absolute']['Angle']),
                        'Distance': np.median(errors['Absolute']['Distance']),
                        'Girth': np.median(errors['Absolute']['Girth'])}
    errors['RMSE'] = {'Angle': np.sqrt(np.sum(np.square(errors['Absolute']['Angle']))),
                      'Distance': np.sqrt(np.sum(np.square(errors['Absolute']['Distance']))),
                      'Girth': np.sqrt(np.sum(np.square(errors['Absolute']['Girth'])))}
    thresh_rel = np.mean(pred_vals['Distance']) * 1.15 # 15% flexibility
    tp = pred_vals['Distance'][pred_vals['Distance'] <= thresh_rel]
    fp = pred_vals['Distance'][pred_vals['Distance'] > thresh_rel]
    errors['Precision'] = len(tp)/(len(tp) + len(fp))
    errors['Recall'] = len(tp)/gt.shape[0]
    return errors


def main(src_pred=None, src_val=None, src_girths=None, dmax=None, out=None):
    pred = pd.read_csv(src_pred, sep=',')
    gt = pd.read_csv(src_val, sep=',')
    gt = gt[(gt['TimeStamp'] == pred.iloc[0]['TimeStamp']) &
            (gt['Distance'] <= dmax)]
    girths = pd.read_csv(src_girths, sep=',')
    errors = compute_errors(pred, gt, girths)

    print('=== Errors ===\n')
    for item in list(errors.items()):
        display(item)


if __name__=='__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-p', '--prediction',
                        nargs=1,
                        type=str,
                        default='tree_prediction.csv',
                        help='Tree prediction file containing estimated'
                             'polar coordinates of trees.')
    PARSER.add_argument('-v', '--validation',
                        nargs=1,
                        type=str,
                        default='distances_gt_all_meters.csv',
                        help='Ground truth tree and drone positions (polar and'
                             'cartesian).')
    PARSER.add_argument('-g', '--girths',
                        nargs=1,
                        type=str,
                        default='trees_girth.csv',
                        help='Ground truth tree girths.')
    PARSER.add_argument('--dmax',
                        nargs='?',
                        type=int,
                        default=np.inf,
                        help='Maximum depth to consider in the scene'
                             '(in meters).')
    PARSER.add_argument('-o', '--output',
                        nargs='*',
                        type=str,
                        default='evaluation.csv',
                        help='Export path.')
    ARGS = PARSER.parse_args()
    main(ARGS.prediction[0], ARGS.validation[0], ARGS.girths[0], ARGS.dmax, ARGS.output[0])