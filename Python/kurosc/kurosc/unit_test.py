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
    # print(idx.shape,'\n',idx[:,0])
    ##validate in range, since these are 2d but coupled pairs and where returns 1d just use unique

    ##validate in range, since these are 2d but coupled pairs and where returns 1d just use unique
    # idy = np.unique(np.where(idx<=zshape[0:2])[0])

    # idz0 = np.where(idx[:,0]>=0)[0]
    # idz1 = np.where(idx[:,1]>=0)[0]
    # idz = (idx[np.in1d(idz0.view(dtype='i,i').reshape(idz0.shape[0]),
    #        idz1.view(dtype='i,i').reshape(idz1.shape[0]))])
    # idz = np.unique(np.concatenate([idz0,idz1]))

######

    # idy = np.arange(idx.shape[0])[np.in1d(
    #         np.where(idx[:,0]<=zshape[0])[0],
    #         np.where(idx[:,1]<=zshape[1])[0])]
    # print(idy)
    #
    #
    # idz = np.arange(idx.shape[0])[np.in1d(
    #     np.where(idx[:,0]>=0)[0],
    #     np.where(idx[:,1]>=0)[0])]
    # print(idz)
####
    # print( np.squeeze(idx[np.in1d(idy,idz),:]) )
# k[np.in1d(k.view(dtype='i,i').reshape(k.shape[0]),k2.view(dtype='i,i').reshape(k2.shape[0]))]



    # idu = np.where(idx<=zshape[0:2])[0]
    # idv = np.where(idx>=0)[0]
    # # idw = idx[np.in1d(idx,idu.reshape()]
    # # idy = idx[np.in1d(idx,idv.reshape()]
    # # idz = idx[np.in1d(idw,idy),:]
    # # test= np.in1d(idu.view(dtype='i,i').reshape(idu.shape[0]),
    # #               idv.view(dtype='i,i').reshape(idv.shape[0]))
    #
    # p1 = np.where(idx[:,0]<=zshape[0])[0]
    # p3 = np.where(idx[:,0]>=0)[0]
    # p2 = np.where(idx[:,1]<=zshape[1])[0]
    # p4 = np.where(idx[:,1]>=0)[0]
    # # test1 = np.in1d(t1,t3)
    # # test2 = np.in1d(t2,t4)
    # ll = (set(t1),set(t2),set(t3),set(t4))
    # u = set.intersection(*pl)

    idl0 = np.where(idx[:,0]<=zshape[0])[0]
    idl1 = np.where(idx[:,1]<=zshape[1])[0]

    idz0 = np.where(idx[:,0]>=0)[0]
    idz1 = np.where(idx[:,1]>=0)[0]

    print(idl0,idl1,idz0,idz1)
    idu = np.intersect1d(idl0,idz0)
    idv = np.intersect1d(idl1,idz1)
    idw = np.intersect1d(idu,idv)

    print( idu, idv, idw, idx[idw,:])


def main():
    # distance_test(3,3)
    # wavelet_test()
    # decouple_test()
    # gif_test()
    # normal_test()
    # move_dirs()
    # load_j()

    index_ts()


if __name__ == '__main__':
    main()
    # build_ics(16,16)
    # spatial_kernel()
    # decouple()
