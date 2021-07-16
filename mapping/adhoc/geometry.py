import numpy as np


def cart2pol(x, y):
    """Convert 2D cartesian coordinates to polar coordinates.

    Args:
        x (int or float): cartesian x coordinate.
        y (int or float): cartesian y coordinate.

    Returns:
        rho, phi (float, float): polar coordinates (radius and angle).
    """
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(x, y)
    return (rho, phi)


def compute_distance(p1, p2, norm='euclidian2D'):
    if norm == 'euclidian2D':
        return round(np.sqrt(np.sum(np.square(p1-p2))), 5)
    else:
        raise ValueError('Unknown norm. Please choose between the following :'
                         'euclidian2D.')


def checkerboard(shape):
    return np.indices(shape).sum(axis=0) % 2


def get_angle2D(p1, p2):
    """Get agnel between 2 points of the plane.

    Let p1 be the reference point, return the trigonometric angle between p1
    and p2. The angles range is [0, 360[ depending on the quadrant p2 is
    relatively to p1.

    Args:
        p1 (list): 2D coordinates of the reference point.
        p2 (list): 2D coordinates of the other point.

    Returns:
        (float): angle in the range [0, 360[.
    """
    x_diff = p2[0] - p1[0]
    y_diff = p2[1] - p1[1]
    angle = np.arctan2(x_diff, y_diff) * 180 / np.pi
    if (x_diff >= 0) and (y_diff >= 0):
        return -angle + 90
    elif (x_diff <= 0) and (y_diff > 0):
        return angle + 180
    elif (x_diff < 0) and (y_diff <= 0):
        return -angle + 90
    elif (x_diff >= 0) and (y_diff < 0):
        return -angle + 450


def pol2cart(phi, rho):
    """Convert polar coordinates to 2D cartesian coordinates.

    Args:
        phi (int, float): polar angle coordinate (in radians).
        rho (int, float): polar radius coordinate.

    Returns:
        x, y (float, float): 2D cartesian coordinates.
    """
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return (x, y)
