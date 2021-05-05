"""
"""
import sys
from pathlib import Path
sys.path.append(Path(__file__).resolve().parents[1])
if __name__ == '__main__' and __package__ is None:
    __package__ = 'kurosc'

from lib.plotformat import setup


import numpy as np
np.set_printoptions(precision=2, suppress=True)

from datetime import datetime as dt


"""
unit test dist in array
call wavelet
"""

def distance_test(m:int = 128,
                  n:int = 128,
                  ):
    from corticalSheet.oscillator import oscillatorArray

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
    from spatialKernel.wavelet import kernel

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
    from secondOrderInteraction.decouple import interaction

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

def gif_test():
    from lib.animate import animate
    filepath = Path('/Users/Michael/Documents/GitHub/kuramoto-osc/Python/Oscillator Phase in 0_pi')
    vid = animate(filepath)
    vid.to_gif(filepath,0.75,True)

def normal_test():
    from spatialKernel.wavelet import kernel
    s = kernel()
    """construct a normal dist frequency lookup"""
    distance = 3/2
    resolution = 20 #mln samples
    x = np.linspace(-distance,distance,resolution)
    # by eye
    params = {'a': 1/7,
              'b': 0,
              'c': 1/2,
              }
    g = s.wavelet(s.gaussian,x,*params.values(),False)
    rng = np.random.default_rng()
    p = np.array(rng.choice(g,size=np.prod((2,2))),dtype=float)
    print(type(p),'\n',g)
    indx = np.zeros([g.shape[0],p.shape[0]],dtype=bool)
    indy = np.arange(g.shape[0])
    for k,q in enumerate(p):
        indx[indy[g==q],k] = 1
    print(indx,indx.any(axis=1))
    # return

def move_dirs():
    from lib.plotformat import setup
    fmt = setup('test_dir',3)
    txt ='Oscillator Phase in pi'
    print(txt)
    print(fmt.plot_name(str(txt)))


def main():
    # distance_test(3,3)
    # wavelet_test()
    # decouple_test()
    # gif_test()
    # normal_test()
    move_dirs()


if __name__ == '__main__':
    main()
    # build_ics(16,16)
    # spatial_kernel()
    # decouple()
