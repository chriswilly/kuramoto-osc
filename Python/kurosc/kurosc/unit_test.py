"""
"""
import sys
from pathlib import Path
print(Path(__file__).resolve().parents[1])
sys.path.append(Path(__file__).resolve().parents[1])
if __name__ == '__main__' and __package__ is None:
    __package__ = 'kurosc'
#
# from lib.plotformat import setup


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
    y = a.delta(x.ravel())
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





def load_j():
    import json
    f = open('model_config.json')
    var = json.load(f)
    [print(var['test_set0'][k]) for k,v in var['test_set0'].items()]


def index_ts():
    zshape = (24,24,500)

    rng = np.random.default_rng()

    rnd_idx = rng.choice(np.arange(zshape[0]),
                         size=2,
                         replace=False,
                         )
    print(rnd_idx)
    idx = np.array(
    [[ 6,  1],
     [ 6, -1],
     [ 4,  1],
     [ 4, -1],
     [ 5,  1],
     [ 5, -1],
     [ 6 , 0],
     [ 4,  0]]
    )

    idl0 = np.where(idx[:,0]<=zshape[0])[0]
    idl1 = np.where(idx[:,1]<=zshape[1])[0]

    idz0 = np.where(idx[:,0]>=0)[0]
    idz1 = np.where(idx[:,1]>=0)[0]

    print(idl0,idl1,idz0,idz1)
    idu = np.intersect1d(idl0,idz0)
    idv = np.intersect1d(idl1,idz1)
    idw = np.intersect1d(idu,idv)

    print( idu, idv, idw, idx[idw,:])




def plt_title():


    interaction_params:dict = {'beta': 0.75,'r': 0.25}
    kernel_params:dict = {'a': 10000/3*2,
                          'b': 0,
                          'c': 10, # breadth of wavelet
                          'order': 4}
    title=None
    domain = [0,np.pi]
    kn=11.1
    samples = 5
    if abs(domain[0]) % np.pi == 0 and not domain[0] == 0:
        ti = r'\pi'
        ti = '-'+ti
    else:
        ti = str(domain[0])

    if abs(domain[1]) % np.pi == 0 and not domain[1] == 0:
        tf = r'\pi'
    else:
        tf = str(domain[1])

    if not title:
        print(interaction_params,
                kernel_params,
                            )

        title = 'Timeseries for {s} Random Neighbors R={r:.2f} $\\beta$={beta:.2f} K/N={kn:.1f} & c={c:.0f})'.format(s=samples,
                                                                                                                     **interaction_params,
                                                                                                                     **kernel_params,
                                                                                                                     kn=kn)

    print(title)




def spatial_wavelet(self,
                    x: np.ndarray,
                    a: float,
                    b: float,
                    c: float,
                    d: int = 4,  # 4th derivative
                    ) -> np.ndarray:
    """arbitrary derivation of the gaussian to nth order and substitute params """
    wavelet = derivative(d)
    fn = lambdify(['x','a','b','c'], wavelet, 'numpy')
    return fn(x,a,b,c)


def LSA():
    from spatialKernel.symdiff import derivative

    from sympy import (symbols,
                        sin)
    x,t,b,r = symbols('x,theta,beta,r')

    fn = lambda x,t,b,r: -sin(t-x+b) + r*sin(2*(t-x))
    fnc = lambda x,t,b,r: (-1 if r else 1)*sin(t-x+b) + r*sin(2*(t-x))

    df = derivative(fnc(x,t,b,r),1,x)
    vals = {'r':0.8,'beta':0,'theta':0,'x':0}
    print(df)
    print(df.subs(vals))




def main():
    # distance_test(3,3)
    # wavelet_test()
    # decouple_test()
    LSA()
    # gif_test()
    # normal_test()
    # move_dirs()
    # load_j()
    # index_ts()
    # plt_title()


if __name__ == '__main__':
    main()
    # build_ics(16,16)
    # spatial_kernel()
    # decouple()
