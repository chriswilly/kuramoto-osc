"""
construct 2d array of pase state
distance array

"""
import sys
import os
import re
# sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from pathlib import Path
sys.path.append(Path(__file__).resolve().parents[1])
if __name__ == '__main__' and __package__ is None:
    __package__ = 'kurosc'

import numpy as np
from lib.plot_solution import plot_phase
from spatialKernel.wavelet import kernel

class oscillatorArray(object):
    def __init__(self,
                 dimension: tuple = (16,16),
                 domain:tuple = (0,np.pi),
                 output_level:int = 3  # not sure if need to be passing this thru
                 ):
        self.domain = domain
        self.kernel = kernel()
        self.ic = self.initial_conditions(*dimension)
        self.natural_frequency = None  #  init & evalin model  ... self.natural_frequency_dist()   #TODO fix this
        self.distance = self.distance()
        self.level = output_level
        self.plot_phase = plot_phase
        self.plot_directory = None  # initialized in a plot module
        # for labeling plots:
        self.interaction_params = None
        self.kernel_params = None
        self.gain = None


    def initial_conditions(self,
                           m:int = 16,
                           n:int = 16,
                           params:dict = {'a': 1/6,
                                          'b': 0,
                                          'c': 2/5,
                                          'order':0,
                                           }
                           )->np.ndarray:
        """rtrn x vals for normal weighted across -pi pi
            #  distinct vals for replace = false
        """

        ### range discerned by eye fig 1 fitting a&c
        ### 1hz spread --> 2pi  t*2pi at 1 s gives 1 rev
        ### omega = 2pi/s so sin(omega*t) makes sense
        ### chose np.max(abs(domain)) to scale by pi even if -
        ###  np.max(np.abs(self.domain)) == pi
        x = np.linspace(params['b']-3.5*params['c'],
                        params['b']+3.5*params['c'],
                        int(1e6)
                        )*np.max(np.abs(self.domain))

        prob = self.kernel.wavelet(self.kernel.gaussian,
                                   x,
                                   *params.values(),
                                   True
                                   )

        prob = prob/np.sum(prob)  # pdf for weights

        rng = np.random.default_rng()

        phase = rng.choice(x,
                           size=np.prod(m*n),
                           p = prob,
                           replace=False,
                           ).reshape(m,n)

        print('\nintial contitions in phase space:',
              np.round(np.mean(phase),3),
              '\nstdev:',
              np.round(np.std(phase),3)
              )

        return phase


    def natural_frequency_dist(self,
                               params:dict = {'a': 1/6,
                                              'b': 0,
                                              'c': 2/5,
                                              'order':0,
                                              }
                               )->np.ndarray:
        """rtrn x vals for normal weighted abt 0hz
            #  distinct vals for replace = false
        """

        # range discerned by eye fig 1 fitting a&c
        x = np.linspace(params['b']-3.5*params['c'],
                        params['b']+3.5*params['c'],
                        int(1e6)
                        )

        prob = self.kernel.wavelet(self.kernel.gaussian,
                                   x,
                                   *params.values(),
                                   True
                                   )

        prob = prob/np.sum(prob)  # pdf for weights

        rng = np.random.default_rng()

        frequency = rng.choice(x,
                               size=np.prod(self.ic.shape),
                               p = prob,
                               replace=True,
                               )

        print('\nmean natural frequency in hz:',
              np.round(np.mean(frequency),3),
              '\nstdev:',
              np.round(np.std(frequency),3),
              '\nconverted to phase angle on output'
              )
        # t -->  pi
        return frequency*np.pi*2



    def uniform_initial_conditions(self,
                                   m:int = 16,
                                   n:int = 16,
                                   )->np.ndarray:
        """return random 2D phase array"""
        scale = np.max(np.absolute(self.domain))
        offset = np.min(self.domain)
        # print(scale, offset)
        rng = np.random.default_rng()

        return scale*rng.random((m,n)) + offset


    def distance(self,
                 t:str = 'float') -> np.ndarray:

        """construct m*n*(m*n) array of euclidian distance as integer or float
           this could be optimized but is only called once as opposed to eth phase difference calc
        """
        d = np.zeros([self.ic.shape[0]*self.ic.shape[1],
                      self.ic.shape[1]*self.ic.shape[0]])

        u,v = np.meshgrid(np.arange(self.ic.shape[0]),
                          np.arange(self.ic.shape[1]),
                          sparse=False, indexing='xy')
        u = u.ravel()
        v = v.ravel()
        z = np.array([u,v])

        for (k,x) in enumerate(z):
            d[k,:] = np.array(np.sqrt((u - x[0])**2 + (v - x[1])**2),dtype=t)
        return d






    #     d = np.zeros([self.ic.shape[0]*self.ic.shape[1],
    #                   self.ic.shape[1],
    #                   self.ic.shape[0]])
    #
    #
    #     k=0
    #     for j in np.arange(self.ic.shape[1]):
    #         for i in np.arange(self.ic.shape[0]):
    #             # print(i*j,j,i)
    #             d[k,...] = self.indiv_distance((i,j),integer)
    #             k+=1
    #     return d



    # def indiv_distance(self,
    #              indx:tuple = (0,0),
    #              integer:bool = False,
    #              ) -> np.ndarray:
    #     ###construct m*n array of euclidian distance as integer or float
    #
    #     x,y = np.meshgrid(np.arange(self.ic.shape[0]),
    #                       np.arange(self.ic.shape[1]),
    #                       sparse=False, indexing='xy')
    #
    #
    #     print('dx:\n',(indx[0] - x),
    #           '\ndy:\n',(indx[1] - y),
    #           '\nsq(dx^2+dy^2):\n',
    #           np.sqrt((indx[0] - x)**2 + (indx[1] - y)**2),
    #           '\n')
    #
    #
    #     if not integer:
    #         return np.sqrt((indx[0] - x)**2 + (indx[1] - y)**2)
    #     else:
    #         return np.asarray(np.sqrt((indx[0] - x)**2 + (indx[1] - y)**2),dtype = int)





def main():

    """
    this demos a random contour plot
    """
    corticalArray = oscillatorArray((64,64),(-np.pi,np.pi),1)
    x = np.linspace(0,corticalArray.ic.shape[0],
                      corticalArray.ic.shape[1])
    y = np.linspace(0,corticalArray.ic.shape[1],
                      corticalArray.ic.shape[0])
    x,y = np.meshgrid(x,y)

    phase_array = np.asarray([x.ravel(),
                              y.ravel(),
                              corticalArray.ic.ravel()]
                              ).T

    corticalArray.plot_phase(phase_array,
                             'Oscillator Phase $\in$ [-$\pi$,$\pi$)',
                             'Location y',
                             'Location x'
                             )

if __name__ == '__main__':
    main()
