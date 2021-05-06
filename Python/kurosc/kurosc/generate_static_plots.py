"""
koramoto oscillator system with the modifications:

######
2D Array of weekly coupled oscillators: corticalSheet.oscillator
initial_conditions(m:int = 16,
                   n:int = 16,
                   scale: float = 2*np.pi,
                   offset:float = -np.pi,
                   )->np.ndarray:

distance...

######
Spatial considerations: spatialKernel.wavelet
wavelet(fn,
        x: np.ndarray,
        a: float = 10000/3*2,
        b: float = 0,  # mean
        c: float = 10,
        d: float = 4,
        normalize = False,
        ) -> np.ndarray:

w = kernel(spatial_wavelet,x,*params.values(),True)

plot_wavelet(np.asarray([x,w]).T,
             '{}th Derivative Gaussian'.format(str(params['order'])),
             'Arbitrary Magnitube',
             'Node Distance')

######
Second Order Interaction: secondOrderInteraction.decouple
class based on index
gamma(x: np.ndarray,
      beta: float = 1/4,
      r: float = 8/10
      ) -> np.ndarray:
      return -np.sin(x+beta) + r*np.sin(2*x)

g = gamma(x,**p)

"""
import numpy as np
import sys
from pathlib import Path
sys.path.append(Path(__file__).resolve())
if __name__ == '__main__' and __package__ is None:
    __package__ = 'kurosc'

from corticalSheet.oscillator import oscillatorArray
from secondOrderInteraction.decouple import interaction
from spatialKernel.wavelet import kernel

np.set_printoptions(precision=3, suppress=True)


def build_ics(m:int = 128,
              n:int = 128):
    """
    this demos how to construct a contour plot
    """
    domain = (0,np.pi)
    oscillators = oscillatorArray((m,n),domain)

    x = np.linspace(0,oscillators.ic.shape[0],
                      oscillators.ic.shape[1])
    y = np.linspace(0,oscillators.ic.shape[1],
                      oscillators.ic.shape[0])
    x,y = np.meshgrid(x,y)

    phase_array = np.asarray([x.ravel(),
                              y.ravel(),
                              oscillators.ic.ravel()]
                              ).T
    if abs(domain[0]) % np.pi == 0 and not domain[0] == 0:
        ti = r'\pi'
        ti = '-'+ti
    else:
        ti = str(domain[0])
    if abs(domain[1]) % np.pi == 0 and not domain[1] == 0:
        tf = r'\pi'
    else:
        tf = str(domain[1])

    oscillators.plot_phase(phase_array,
                           'Oscillator Phase $\in$ [${0}$,${1}$)'.format(ti,tf),
                           'Location y',
                           'Location x'
                           )
def spatial_kernel():
    """
    """
    s = kernel()
    distance = 3/2
    resolution = 1000
    x = np.linspace(-distance,distance,resolution)
    # scale a nonlinearly ~10^n for magnitude
    # b is center mass
    # scale c linearly for width
    # d is order of derivative for arbitrary spatial_wavelet
    params = {'a': 1/6,
              'b': 0,
              'c': 2/5,
              'order':0,
              }
    # w = s.wavelet(s.gaussian,x,*params.values(),False)
    w = s.wavelet(s.spatial_wavelet,
                  x,
                  *params.values(),
                  False
                  )
    if isinstance(w,np.ndarray):
        s.plot_wavelet(np.asarray([x,w]).T,
                      '{}th Derivative Gaussian'.format(str(params['order'])),
                      'Likelihood',
                      'Node Distance')

def decouple():
    """
    """
    a = interaction()
    params = ({'beta': 0.25, 'r':0.95},
              {'beta': 0.25, 'r':0.8},
              {'beta': 0.25, 'r':0.7},
              )
    x = np.linspace(-np.pi,np.pi,1000)

    for p in params:
        g = a.gamma(x,**p)
        a.plot_phase(np.asarray([x,g]).T,
                    'R = {0}'.format(p['r']),
                    # '',
                    # r'$\frac{d\theta}{dt}$',
                    r'$\d\theta$\'',
                    r'$\phi$')


    neighbors = interaction()

def test():
    domain = (0,np.pi)
    osc = oscillatorArray(3,3)

    x = np.linspace(0,osc.ic.shape[0],
                      osc.ic.shape[1])
    y = np.linspace(0,osc.ic.shape[1],
                      osc.ic.shape[0])

    print(osc.ic,'\n',osc.distance)


if __name__ == '__main__':
    # test()
    # build_ics(256,256)
    spatial_kernel()
    # decouple()


    # print(Path(__file__).resolve())
    # print(__package__)
