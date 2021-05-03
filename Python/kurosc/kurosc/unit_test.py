"""
"""
import sys
from pathlib import Path
sys.path.append(Path(__file__).resolve())
if __name__ == '__main__' and __package__ is None:
    __package__ = 'kurosc'
import numpy as np

from datetime import datetime as dt

from corticalSheet.oscillator import oscillatorArray
from secondOrderInteraction.decouple import interaction
from spatialKernel.wavelet import kernel

np.set_printoptions(precision=2, suppress=True)
"""
unit test dist in array
call wavelet

"""

def distance_test(m:int = 128,
                  n:int = 128):
    domain = (-np.pi,np.pi)
    osc = oscillatorArray((m,n),domain)

    print(dt.now(),#.strftime('%y%m%d_%H%M%S'),
          '\nics\n',
          osc.ic,
          '\n\ndistance shape\n',
          osc.distance.shape,
          '\n\ndistance vector\n',
          osc.distance.flatten())

    return osc.ic,osc.distance.flatten()

def wavelet_test():
    _,y = distance_test(3,3)

    s = kernel()
    params = {'a': 10000/3*2,
              'b': 0,
              'c': 10,
              'order': 17,
              }
    w = s.wavelet(s.spatial_wavelet,y,*params.values(),True)
    print(dt.now(),'\nwavelet\n',w)



def decouple_test():

    x,_ = distance_test(3,3)
    a = interaction(x.shape)
    y = a.delta(x)
    p = {'beta': 0.25, 'r':0.95}
    g = a.gamma(y,**p)
    print(dt.now(),'\ngamma\n',g,
          '\n\nphase difference vector\n',
          g.flatten(),
          '\n\nmean difference vector\n',
          np.mean(g))
    return g.flatten()

def system():
    #initialize an osc array
    dimension = (2,2)
    domain = (0,np.pi)
    osc = oscillatorArray(dimension,domain)

    # fixed time wavelet kernel
    s = kernel()
    kernel_params = {'a': 10000/3*2,
                     'b': 0,
                     'c': 10,
                     'order': 4,
                     }
    interaction_params = ({'beta': 0, 'r':0},
                          {'beta': 0.25, 'r':0.95})
    w = s.wavelet(s.spatial_wavelet,
                  osc.distance.flatten(),
                  *kernel_params.values(),True)
    # print(dt.now(),'\nwavelet\n',w)

    a = interaction(osc.ic.shape)
    phase_difference = a.delta(osc.ic)
    g = a.gamma(phase_difference,**interaction_params[0])

    print(dt.now(),
          '\nwavelet\n',
          w,'\n',type(w),
          '\n\nphase difference vector\n',
          g.flatten(),'\n',
          type(g.flatten()),
          '\nwavelet*difference\n',
          w*g.flatten()
          )





def main():
    # distance_test(3,3)
    # wavelet_test()
    decouple_test()

if __name__ == '__main__':
    main()
    # build_ics(16,16)
    # spatial_kernel()
    # decouple()
