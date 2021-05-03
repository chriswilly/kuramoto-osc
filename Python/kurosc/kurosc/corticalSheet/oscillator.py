"""
construct 2d array of pase state
distance array

"""
import sys
import os
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
# from pathlib import Path
# sys.path.append(Path(__file__).resolve().parents[1])
# print(sys.path[0])

from lib.plotformat import setup

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter


class oscillatorArray(object):
    def __init__(self,
                 dimension: tuple = (16,16),
                 domain:tuple = (0,np.pi),
                 output_level:int = 3  # not sure if need to be passing this thru
                 ):
        self.domain = domain
        self.ic = self.initial_conditions(*dimension)
        self.distance = self.entire_distance()
        self.level = output_level


    def initial_conditions(self,
                           m:int = 16,
                           n:int = 16,
                           )->np.ndarray:
        """return random 2D phase array"""
        scale = np.max(np.absolute(self.domain))
        offset = np.min(self.domain)
        # print(scale, offset)
        rng = np.random.default_rng()
        return scale*rng.random((m,n)) + offset



    def entire_distance(self,
                        integer:bool = False) -> np.ndarray:
        """construct m*n*(m*n) array of euclidian distance as integer or float"""

        d = np.zeros([self.ic.shape[0]*self.ic.shape[1],
                      self.ic.shape[1],
                      self.ic.shape[0]])
        # print(d.shape)
        k=0
        for j in np.arange(self.ic.shape[1]):
            for i in np.arange(self.ic.shape[0]):
                # print(i*j,j,i)
                d[k,...] = self.distance((i,j),integer)
                k+=1
        return d



    def distance(self,
                 indx:tuple = (0,0),
                 integer:bool = False,
                 ) -> np.ndarray:
        """construct m*n array of euclidian distance as integer or float"""

        x,y = np.meshgrid(np.arange(self.ic.shape[0]),
                          np.arange(self.ic.shape[1]),
                          sparse=False, indexing='xy')  # ij ?
        """
        print('dx:\n',(indx[0] - x),
              '\ndy:\n',(indx[1] - y),
              '\nsq(dx^2+dy^2):\n',
              np.sqrt((indx[0] - x)**2 + (indx[1] - y)**2),
              '\n')
        """
        if not integer:
            return np.sqrt((indx[0] - x)**2 + (indx[1] - y)**2)
        else:
            return np.asarray(np.sqrt((indx[0] - x)**2 + (indx[1] - y)**2),dtype = int)





    def plot_phase(self,
                   X: np.ndarray,
                   plot_title:str = None,
                   y_axis:str = 'y',
                   x_axis:str = 'x',
                   resolution:int = 16
                   ):
        """
        """
        fldr = plot_title.replace('at t = ','')
        fldr = re.sub('\d*\.\d*','',fldr).strip()

        fmt = setup(fldr,self.level)  # plotting format obj

        fig = plt.figure(figsize=(10,8))
        ax = fig.add_subplot(111)



        colorscale = np.linspace(np.min(self.domain),
                                 np.max(self.domain),
                                 resolution,
                                 endpoint=True)

        plt.tricontourf(X[...,0],X[...,1],X[...,2],
                        colorscale,cmap=plt.cm.nipy_spectral,
                        )
        plt.gca().invert_yaxis()
        plt.grid(b=True, which='major', axis='both')

        plt.clim(colorscale[0],colorscale[-1])
        plt.colorbar(ticks=colorscale,format='%1.2f')

        # if self.ic.shape[1] < 20:
        ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
        # if self.ic.shape[0] < 20:
        ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
        plt.title(plot_title)
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)

        # ax.xaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%g $\pi$'))
        # ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(base=1))
        plt.grid(b=None, which='major', axis='both')
        # plt.show()
        fig.savefig(fmt.plot_name(plot_title,'png'))




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

    phase_array = np.asarray([x.flatten(),
                              y.flatten(),
                              corticalArray.ic.flatten()]
                              ).T

    corticalArray.plot_phase(phase_array,
                             'Oscillator Phase $\in$ [-$\pi$,$\pi$)',
                             'Location y',
                             'Location x'
                             )

if __name__ == '__main__':
    main()
