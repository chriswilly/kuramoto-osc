"""
construct wavelet for distance decay spatial kernel
w = kernel(spatial_wavelet,x,*params.values(),True)
returns a normalized gaussian nth order derivative
"""
# import sys
# from pathlib import Path
# sys.path.append(Path(__file__).resolve().parents[1])
# if __name__ == '__main__' and __package__ is None:
#     __package__ = 'spatialKernel'

from lib.plotformat import setup
from spatialKernel.symdiff import main as derivative

import numpy as np
import matplotlib.pyplot as plt
from sympy import (symbols,
                   lambdify
                   )


class kernel(object):
    def __init__(self,
                 index: np.ndarray = np.array([0,0])
                 ):
        self.index = index


    def wavelet(self,
                fn,
                x: np.ndarray,
                a: float = 10000/3*2,
                b: float = 0,  # mean
                c: float = 10,
                d: float = 4,
                normalize = False,
                ) -> np.ndarray:
        """generalized kernel using gaussian paramaterization"""
        if d > 19:
            print('derivative order too high')
            return None
        y = fn(x,a,b,c,d)
        if normalize:
            y = y/np.max(np.absolute(y))
        return y


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


    def gaussian(self,
                 x: np.ndarray,
                 a: float = 1,
                 b: float = 0,
                 c: float = 1,
                 d: int = None, # dummy
                 ) -> np.ndarray:
        """generalized gaussian function"""
        return a*np.exp(-(x-b)**2/2/c**2)


    def spatial_wavelet_old(self,
                            x: np.ndarray,
                            a: float,
                            b: float,
                            c: float,
                            d: int = None,
                            ) -> np.ndarray:
        """fourth derivative of gaussian calculated with sympy manually pasted"""
        return (
                3*a*np.exp(-(-b + x)**2/(2*c**2))/c**4
                - a*(-8*b + 8*x)*(-2*b + 2*x)*np.exp(-(-b + x)**2/(2*c**2))/(8*c**6)
                - a*(-2*b + 2*x)**2*np.exp(-(-b + x)**2/(2*c**2))/c**6
                + a*(-2*b + 2*x)**4*np.exp(-(-b + x)**2/(2*c**2))/(16*c**8)
                )


    def plot_wavelet(self,
                     X: np.ndarray,
                     plot_title:str = 'placeholder',
                     y_axis:str = 'y',
                     x_axis:str = 'x',
                     ):
        """plot the wave form for spatial kernel"""
        fmt = setup(plot_title)  # plotting format obj
        fig = plt.figure(figsize=(9,9))
        ax = fig.add_subplot(111)

        ax.plot(X[...,0],X[...,1],'-b')

        # plt.autoscale(enable=True, axis='both', tight=True)
        # plt.axis('tight')
        # ax.legend(loc=3)
        plt.title(plot_title)
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.grid(b=True, which='major', axis='both')
        plt.show()
        fig.savefig(fmt.plot_name(plot_title,'png'))





def main():
    s = kernel()
    distance = 60
    resolution = 1000
    x = np.linspace(-distance,distance,resolution)
    # scale a nonlinearly ~10^n for magnitude
    # b is center mass
    # scale c linearly for width
    # d is order of derivative for arbitrary spatial_wavelet
    params = {'a': 10000/3*2,
              'b': 0,
              'c': 10,
              'order': 7,
              }
    # print(*params.values())
    # g = kernel(gaussian,x,*params.values(),True)
    w = s.wavelet(s.spatial_wavelet,x,*params.values(),True)
    if isinstance(w,np.ndarray):
        # plot_wavelet(np.asarray([x,g]).T,
        #              'Gaussian',
        #              'Arbitrary Magnitube',
        #              'Node Distance')

        # print(type(params['order']))

        s.plot_wavelet(np.asarray([x,w]).T,
                      '{}th Derivative Gaussian'.format(str(params['order'])),
                      'Arbitrary Magnitube',
                      'Node Distance')

if __name__ == '__main__':
    main()
