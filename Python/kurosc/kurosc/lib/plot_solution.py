"""takes object oscillatorArray: "self.osc" instance from model.py and constructs plot
"""
import numpy as np

from lib.interp import smooth_image


def plot_contour(obj,
                 z:np.ndarray,
                 t:float = None,
                 title:str = None):
    """
    """
    # want to keep this dependence on init setup may also use z.shape[]
    x = np.linspace(0,obj.ic.shape[0],
                      obj.ic.shape[1])
    y = np.linspace(0,obj.ic.shape[1],
                      obj.ic.shape[0])

    # x,y = np.meshgrid(x,y,sparse=True)
    # z,x,y = smooth_image()
    x,y = np.meshgrid(x,y,sparse=False)


    phase_array = np.asarray([x.ravel(),
                              y.ravel(),
                              z.ravel()%np.pi]
                              ).T

    if abs(obj.domain[0]) % np.pi == 0 and not obj.domain[0] == 0:
        ti = r'\pi'
        ti = '-'+ti
    else:
        ti = str(obj.domain[0])

    if abs(obj.domain[1]) % np.pi == 0 and not obj.domain[1] == 0:
        tf = r'\pi'
    else:
        tf = str(obj.domain[1])

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

    obj.plot_phase(phase_array,
                    title,
                    'Location y',
                    'Location x'
                    )
