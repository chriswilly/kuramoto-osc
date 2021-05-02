"""
second order neural interrupting interactions
interaction is class, gamma is function
"""
# import sys
# from pathlib import Path
# sys.path.append(Path(__file__).resolve().parents[1])
# if __name__ == '__main__' and __package__ is None:
#     __package__ = 'kuramotoNeighbor.secondOrderInteraction'

from lib.plotformat import setup

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


""" Eqn 13 + Fig 4
"""

class interaction(object):
    def __init__(self,
                 index: np.ndarray = np.array([0,0])
                 ):
        self.index = index

    def delta(self,
              phase_array: np.array = np.array([[1,5],[8,100]])
              ) -> np.ndarray:
        """pase difference of element from global array"""
        return phase_array[self.index[0],self.index[1]] - phase_array


    def gamma(self,
              x: np.ndarray,
              beta: float = 1/4,
              r: float = 8/10
              ) -> np.ndarray:
        return -np.sin(x+beta) + r*np.sin(2*x)


    def plot_phase(self,
                   X: np.ndarray,
                   plot_title:str = 'placeholder',
                   y_axis:str = 'y',
                   x_axis:str = 'x',
                   ):
        fmt = setup(plot_title)  # plotting format obj
        fig = plt.figure(figsize=(9,9))
        ax = fig.add_subplot(111)
        ax.plot(X[...,0]/np.pi,X[...,1],'-b')
        ax.plot(np.asarray([X[0,0],X[-1,0]])/np.pi,[0,0],'-k',linewidth=1)  #

        # plt.autoscale(enable=True, axis='both', tight=True)
        # plt.axis('tight')
        # ax.legend(loc=3)
        plt.title(plot_title)
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)

        ax.xaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%g $\pi$'))
        ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(base=1))
        plt.grid(b=True, which='major', axis='both')
        plt.show()
        fig.savefig(fmt.plot_name(plot_title,'png'))


def main():
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
                    '',
                    # r'$\frac{d\theta}{dt}$',
                    r'$\phi$')


if __name__ == '__main__':
    main()
