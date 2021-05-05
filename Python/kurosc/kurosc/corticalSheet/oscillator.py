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

from lib.plotformat import setup

# print(sys.path[0])

# curious if this

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
        self.natural_frequency = None
        self.distance = self.distance()
        self.level = output_level
        self.plot_directory = None

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


        """
        d = np.zeros([self.ic.shape[0]*self.ic.shape[1],
                      self.ic.shape[1],
                      self.ic.shape[0]])


        k=0
        for j in np.arange(self.ic.shape[1]):
            for i in np.arange(self.ic.shape[0]):
                # print(i*j,j,i)
                d[k,...] = self.indiv_distance((i,j),integer)
                k+=1
        return d
        """



    """
    def indiv_distance(self,
                 indx:tuple = (0,0),
                 integer:bool = False,
                 ) -> np.ndarray:
        ###construct m*n array of euclidian distance as integer or float

        x,y = np.meshgrid(np.arange(self.ic.shape[0]),
                          np.arange(self.ic.shape[1]),
                          sparse=False, indexing='xy')


        print('dx:\n',(indx[0] - x),
              '\ndy:\n',(indx[1] - y),
              '\nsq(dx^2+dy^2):\n',
              np.sqrt((indx[0] - x)**2 + (indx[1] - y)**2),
              '\n')


        if not integer:
            return np.sqrt((indx[0] - x)**2 + (indx[1] - y)**2)
        else:
            return np.asarray(np.sqrt((indx[0] - x)**2 + (indx[1] - y)**2),dtype = int)

    """




    def plot_phase(self,
                   X: np.ndarray,
                   plot_title:str = None,
                   y_axis:str = 'y',
                   x_axis:str = 'x',
                   resolution:int = 24
                   ):
        """
        """
        fldr = plot_title.replace('at t = ','')
        fldr = re.sub('[*\d\.\d*]','',fldr).strip()
        # print(fldr)
        fmt = setup(fldr,self.level)
        self.plot_directory = fmt.directory

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
        plt.colorbar(ticks=colorscale[::5],format='%1.2f')

        ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
        ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
        # ax.xaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%g $\pi$'))
        # ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(base=1))

        plt.title(plot_title)
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)

        plt.grid(b=None, which='major', axis='both')
        # plt.show()
        fig.savefig(fmt.plot_name(plot_title,'png'))
        plt.close('all')



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
