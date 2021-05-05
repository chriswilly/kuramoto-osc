from scipy.interpolate import interp2d, RectBivariateSpline
from scipy.ndimage.filters import gaussian_filter

import numpy as np


def smooth_image(#self,
                 z:np.ndarray,
                 x:np.ndarray,
                 y:np.ndarray,
                 scale:int = 2,
                 sigma:np.ndarray = np.array([7,7])
                 )->np.ndarray:

    # z = interp2d
    # x = interp2d
    # y = interp2d
    # interp2d
    # gaussian_filter
    pass
