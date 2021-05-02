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
kernel(fn,
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


def build_ics(m:int = 128,
              n:int = 128):
    """
    this demos how to construct a contour plot
    """
    oscillators = oscillatorArray(m,n)
    x = np.linspace(0,oscillators.ic.shape[0],
                      oscillators.ic.shape[1])
    y = np.linspace(0,oscillators.ic.shape[1],
                      oscillators.ic.shape[0])
    x,y = np.meshgrid(x,y)

    phase_array = np.asarray([x.flatten(),
                              y.flatten(),
                              oscillators.ic.flatten()]
                              ).T

    oscillators.plot_phase(phase_array,
                           'Oscillator Phase $\in$ [-$\pi$,$\pi$)',
                           'Location y',
                           'Location x'
                           )
def spatial_kernel():
    """"""
    s = kernel()
    distance = 50
    resolution = 1000
    x = np.linspace(-distance,distance,resolution)
    # scale a nonlinearly ~10^n for magnitude
    # b is center mass
    # scale c linearly for width
    # d is order of derivative for arbitrary spatial_wavelet
    params = {'a': 10000/3*2,
              'b': 0,
              'c': 10,
              'order': 4,
              }
    # g = kernel(s.gaussian,x,*params.values(),True)
    w = s.kernel(s.spatial_wavelet,x,*params.values(),True)
    if isinstance(w,np.ndarray):
        s.plot_wavelet(np.asarray([x,w]).T,
                      '{}th Derivative Gaussian'.format(str(params['order'])),
                      'Arbitrary Magnitube',
                      'Node Distance')

def decouple():
    """"""
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


if __name__ == '__main__':
    build_ics(64,64)
    spatial_kernel()
    decouple()


    # print(Path(__file__).resolve())
    # print(__package__)
