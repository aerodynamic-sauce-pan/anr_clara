import math
import numpy as np
import pandas as pd
import pylab as pl
import matplotlib.transforms as mtransforms

from tqdm import tqdm
from matplotlib import pyplot as plt

from mapping.adhoc.gt_map import cart2pol, pol2cart, get_angle2D

def test_cart2pol():
    rho, _ = cart2pol(3, 4)
    _, phi = cart2pol(1, 1)
    assert (rho == 5) and (phi == np.deg2rad(45))


def test_pol2cart():
    x_test, y_test = pol2cart(np.deg2rad(45), np.sqrt(2))
    print('test : ', x_test, y_test)
    assert ((math.isclose(x_test, 1, abs_tol=1e-5)) and
            (math.isclose(y_test, 1, abs_tol=1e-5)))


def test_get_angle2D():
    pRef = [0, 0]
    p0 = [1, 0]
    pQuad1 = [1, 1]
    p90 = [0, 1]
    pQuad2 = [-1, 1]
    p180 = [-1, 0]
    pQuad3 = [-1, -1]
    p270 = [0, -1]
    pQuad4 = [1, -1]
    assert (get_angle2D(pRef, p0) == 0 and
            get_angle2D(pRef, pQuad1) == 45 and         
            get_angle2D(pRef, p90) == 90 and 
            get_angle2D(pRef, pQuad2) == 135 and
            get_angle2D(pRef, p180) == 180 and 
            get_angle2D(pRef, pQuad3) == 225 and 
            get_angle2D(pRef, p270) == 270 and
            get_angle2D(pRef, pQuad4) == 315)