"""takes oscect oscillatorArray: "self.osc" instance from model.py and constructs plot
"""
import numpy as np
from scipy.interpolate import RectBivariateSpline


def plot_contour(osc,
                 z:np.ndarray,
                 t:float = None,
                 title:str = None,
                 scale:int = 1):
    """
    """
    # want to keep this dependence on init setup may also use z.shape[]
    x = np.linspace(0,osc.ic.shape[0],
                      osc.ic.shape[1])
    y = np.linspace(0,osc.ic.shape[1],
                      osc.ic.shape[0])

    # X,Y = np.meshgrid(x,y,sparse=False)
    print('x:',x.shape,'y:',y.shape,'z:',z.shape)
    input('debug pause')
    s = RectBivariateSpline(x,y,z)

    # Rescale, overwrite x,y to scale
    x = np.linspace(0,osc.ic.shape[0],
                      osc.ic.shape[1]*scale)
    y = np.linspace(0,osc.ic.shape[1],
                      osc.ic.shape[0]*scale)
    Z = s.__call__(x,y)
    print(Z.shape)


    X,Y = np.meshgrid(x,y,sparse=False)

    phase_array = np.asarray([X.ravel(),
                              Y.ravel(),
                              Z.ravel()%np.pi]
                              ).T

    if abs(osc.domain[0]) % np.pi == 0 and not osc.domain[0] == 0:
        ti = r'\pi'
        ti = '-'+ti
    else:
        ti = str(osc.domain[0])

    if abs(osc.domain[1]) % np.pi == 0 and not osc.domain[1] == 0:
        tf = r'\pi'
    else:
        tf = str(osc.domain[1])

    if not title:
        title = 'Oscillator Phase $\in$ [${0}$,${1}$)'.format(ti,tf)
        # title_trans = ''

        if t or not (t==None):
            if t>10:
                title+=f' at t = {t:.0f}'
            else:
                title+=f' at t = {t:2.1f}'
    """Make 2 copies for  to smooth graphics by avg, don't want to make fake data
    between timepoints bc that is questionable to me"""

    osc.plot_phase(phase_array,
                    title,
                    'Location y',
                    'Location x'
                    )
