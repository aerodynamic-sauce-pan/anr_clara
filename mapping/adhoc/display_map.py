import argparse
import numpy as np
import pandas as pd
import pylab as pl
import matplotlib.transforms as mtransforms

from time import time
from matplotlib import pyplot as plt

from mapping.adhoc.geometry import pol2cart, compute_distance


def get_closest_trees_index(gt_vals, pred_vals):
    gt_vals_closest = []
    for Tree_X, Tree_Y in zip(np.asarray(pred_vals['Tree_X']),
                              np.asarray(pred_vals['Tree_Y'])):
        min_idx = 0
        dist_min = np.inf
        for LocX, LocY, idx in zip(np.asarray(gt_vals['LocX']),
                                   np.asarray(gt_vals['LocY']),
                                   range(len(gt_vals['LocX']))):
            dist = compute_distance(np.array([Tree_X, Tree_Y]), np.array([LocX, LocY]))
            if dist < dist_min:
                min_idx = idx
                dist_min = dist
        gt_vals_closest.append(min_idx)

    return np.array(gt_vals_closest)

# Unfinished
def plot_tree_map_pol(tree_map, girths, dmax, display_path, display_type, compare=None):
    """Display a tree map on a radar like map.

    Displays trees position and girth on a polar projected map. Each tree is
    positioned on a depth level line at an angle relative to the 0° line.

    Args:
        tree_map (dictionnary): map of selected trees containing their polar
                                coordinates and girth.
    """
    print(f'Plotting ground truth map...')
    timestamps = tree_map['TimeStamp'].unique()
    print('Unique timestamps : ', len(timestamps))
    fig = plt.figure(figsize=(10, 10))

    for idx, ts in enumerate(timestamps[:1]):
        if idx % 1 == 0:
            ax = pl.subplot(121, projection='polar')
            trans_offset = mtransforms.offset_copy(ax.transData, fig=fig, y=6, units='dots')
            reduced_tree_map = tree_map[(tree_map['TimeStamp'] == ts) &
                                        (tree_map['Distance'] <= dmax)]
            pDrone = (reduced_tree_map.iloc[0]['POS_X'], reduced_tree_map.iloc[0]['POS_Y'])
            pTree_val = (np.array(reduced_tree_map['LocX']) - pDrone[0],
                     np.array(reduced_tree_map['LocY']) - pDrone[1])
            for row_i in range(reduced_tree_map.shape[0]):
                girth = girths[girths['Name'] == reduced_tree_map.iloc[row_i]['Name']].iloc[0]['Girth']
                # x, y = np.deg2rad(get_angle2D(pDrone, [pTree_val[0][row_i], pTree_val[1][row_i]])), reduced_tree_map.iloc[row_i]['Distance']
                x, y = np.deg2rad(np.arctan2([pTree_val[1][row_i]-pDrone[1], pTree_val[0][row_i]-pDrone[0]])), reduced_tree_map.iloc[row_i]['Distance']
                x_disp = np.rad2deg(x)

                plt.plot(x, y, 'ro', label='trees')
                plt.text(x, y, '%d, %d\n%.3fm' % (int(x_disp), int(y), girth), transform=trans_offset, horizontalalignment='center', verticalalignment='bottom')
                plt.plot(pDrone[0], pDrone[1], '+b', label='drone')
                plt.text(pDrone[0]+1, pDrone[1]+1, 'Drone', c='b', transform=trans_offset, horizontalalignment='center', verticalalignment='bottom')
                circle = pl.Circle(pol2cart(x, y), girth,
                                   transform=ax.transProjectionAffine + ax.transAxes,
                                   color="red", alpha=0.4)
                ax.add_artist(circle)

            plt.suptitle('Ground truth tree map', fontweight='bold')
            plt.title(f'Drone pos : {pDrone}')
            plt.tight_layout(rect=[0, 0.03, 1, 0.95])

            rlab = plt.ylabel('Distance', labelpad=40, c='blue', fontweight='bold')
            ax.set_rlabel_position(180)
            rlab.set_rotation(90)
            plt.setp(ax.get_yticklabels(), fontweight='bold', c='blue')
            plt.grid(True, c='deepskyblue')

            if not((display_path is None) or (display_type is None)):
                plt.subplot(122)
                if display_type == 'rgb':
                    img = plt.imread(display_path+str(ts)+'_rgb.png')
                elif display_type == 'ss':
                    img = plt.imread(display_path+str(ts)+'_ss.png')
                plt.imshow(img)
            plt.pause(0.001)
            #plt.clf()
    plt.show()


def plot_tree_map_cart(tree_map, girths, dmax, display_path=None,
                       display_type=None, relative_view=False, tree_pred=None):
    """Display a tree map on a radar like map.

    Displays trees position and girth on a polar projected map. Each tree is
    positioned on a depth level line at an angle relative to the 0° line.

    Args:
        tree_map (dictionnary): map of selected trees containing their polar
                                coordinates and girth.
        relative_view (bool): weither to center the view on the drone and
                              display relative tree coordinates.
    """
    print(f'Plotting ground truth map...')
    timestamps = tree_map['TimeStamp'].unique()
    print(f'Unique trees : {girths.shape[0]}.')
    print(f'Unique drone pose : {len(timestamps)}.')
    print(f'Unique distances : {tree_map.shape[0]}.')
    
    plt.figure(figsize=(10, 10))
    trace = np.array([[0], [0]])
    for idx, ts in enumerate(timestamps[:10]):
        if idx % 1 == 0:
            # Tree map
            plt.subplot(121)
            reduced_tree_map = tree_map[(tree_map['TimeStamp'] == ts) &
                                        (tree_map['Distance'] <= dmax)]
            pDrone = (np.array(reduced_tree_map.iloc[0]['POS_X']), 
                      np.array(reduced_tree_map.iloc[0]['POS_Y']))
            trace = np.append(trace, [[pDrone[0]], [pDrone[1]]], axis=1)
            pTree_val = [np.array(reduced_tree_map['LocX']),
                         np.array(reduced_tree_map['LocY'])]
            plt.title(f'Drone pos : {pDrone}')
            if tree_pred is not None:
                reduced_tree_pred = tree_pred[(tree_pred['TimeStamp'] == ts) &
                                              (tree_pred['Tree_distance'] <= dmax)].iloc[1:]
                reduced_tree_pred['Tree_X'] = reduced_tree_pred['Tree_X'].map(lambda x: -x)
                reduced_tree_pred['Tree_X'] = reduced_tree_pred['Tree_X'] + pDrone[0]
                reduced_tree_pred['Tree_Y'] = reduced_tree_pred['Tree_Y'] + pDrone[1]
                cti = get_closest_trees_index(reduced_tree_map, reduced_tree_pred)
                pTree_pred = [np.array(reduced_tree_pred['Tree_X']),
                              np.array(reduced_tree_pred['Tree_Y'])]
            if relative_view:
                pTree_val = (pTree_val[0] - pDrone[0], pTree_val[1] - pDrone[1])
                if tree_pred is not None:
                    pTree_pred = (pTree_pred[0] - pDrone[0], pTree_pred[1] - pDrone[1])
                pDrone = (0, 0)
            else:
                ind = [(abs(pDrone[0] - trace[0]) <= dmax), (abs(pDrone[1] - trace[1]) <= dmax)]
                ind = ind[np.argmax([len(ind[0]), len(ind[1])])]
                plt.scatter(trace[0][ind], trace[1][ind], marker='+', c='b')

            if tree_pred is not None:
                plt.plot(pTree_pred[0], pTree_pred[1], 'bo', label='trees_pred')
                for cti_idx, cti_val in enumerate(cti):
                    plt.plot([pTree_pred[0][cti_idx], pTree_val[0][cti_val]], 
                             [pTree_pred[1][cti_idx], pTree_val[1][cti_val]], '-.c', label='cti')
            plt.plot(pTree_val[0], pTree_val[1], 'ro', label='trees_val')
            plt.plot(pDrone[0], pDrone[1], marker='P', c='b')
            plt.text(pDrone[0]+1, pDrone[1]+1, 'Drone', c='b')

            if tree_pred is not None:
                for row_i in range(reduced_tree_pred.shape[0]):
                    plt.text(pTree_pred[0][row_i]+1, pTree_pred[1][row_i]+1, '%d, %d\n%.3fm' % (int(pTree_pred[0][row_i]), int(pTree_pred[1][row_i]), reduced_tree_pred.iloc[row_i]['Tree_girth']), color='b')
            for row_i in range(reduced_tree_map.shape[0]):
                girth = girths[girths['Name'] == reduced_tree_map.iloc[row_i]['Name']]['Girth']
                plt.text(pTree_val[0][row_i]+1, pTree_val[1][row_i]+1, '%d, %d\n%.3fm' % (int(pTree_val[0][row_i]), int(pTree_val[1][row_i]), girth))
            plt.suptitle('Ground truth tree map', fontweight='bold')
            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            plt.grid(True, c='deepskyblue')

            # Corresponding image
            if not((display_path is None) or (display_type is None)):
                plt.subplot(122)
                if display_type == 'rgb':
                    img = plt.imread(display_path+str(ts)+'_rgb.png')
                elif display_type == 'ss':
                    img = plt.imread(display_path+str(ts)+'_ss.png')
                plt.imshow(img)
            plt.pause(5)
            plt.clf()
    plt.show()


def main(src_dist=None, src_girth=None, dmax=None,
         display_path=None, display_type=None, view='cartesian',
         relative_view=False, compare=None):
    print(f'Loading data files...')
    distances = pd.read_csv(src_dist)
    girths = pd.read_csv(src_girth)
    if compare is not None:
        compare = pd.read_csv(compare)
    if view == 'polar':
        plot_tree_map_pol(distances, girths, dmax, display_path, display_type, compare)
    elif view == 'cartesian':
        plot_tree_map_cart(distances, girths, dmax, display_path, display_type, relative_view, compare)

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-s', '--source',
                        nargs=1,
                        type=str,
                        default='distances.csv',
                        help='Source distances csv file.')
    PARSER.add_argument('-g', '--girth',
                        nargs=1,
                        type=str,
                        default='girth.csv',
                        help='Source girth csv file.')
    PARSER.add_argument('--dmax',
                        nargs='?',
                        type=int,
                        default=np.inf,
                        help='Maximum depth to consider in the scene'
                             '(in meters).')
    PARSER.add_argument('--display_path',
                        nargs=1,
                        type=str,
                        default='rgb',
                        help='Path to images to display next to map.')
    PARSER.add_argument('--display_type',
                        nargs=1,
                        type=str,
                        default='rgb',
                        help='Image type to display next to map (rgb or ss)')
    PARSER.add_argument('--view',
                        nargs='*',
                        type=str,
                        default='polar',
                        help='Cartesian or polar projection.')
    PARSER.add_argument('--relative_view',
                        nargs='*',
                        action='store',
                        help='If true, rather than displaying the drone moving '
                             'in a fixed tree map, displays the map centered '
                             'on the drone with trees coordinates relative to '
                             'the drone\'s.')
    PARSER.add_argument('--compare',
                        nargs='*',
                        action='store',
                        default=None,
                        help='If true, plots the ground truth vs the estimated'
                             'trees.')
    ARGS = PARSER.parse_args()
    main(ARGS.source[0], ARGS.girth[0], ARGS.dmax, 
         ARGS.display_path[0], ARGS.display_type[0], ARGS.view[0],
         ARGS.relative_view is not None, ARGS.compare[0] if ARGS.compare is not None else None)