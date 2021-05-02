"""
construct 2d array of pase state
distance array

"""
# import sys
# from pathlib import Path
# sys.path.append(Path(__file__).resolve().parents[1])
# print(sys.path[0])

# if __name__ == '__main__' and __package__ is None:
#     __package__ = 'corticalSheet'
from lib.plotformat import setup

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt



class oscillatorArray(object):
    def __init__(self,
                 m:int = 16,
                 n:int = 16,
                 output_level:int = 3  # not sure if required to be passing this thru
                 ):
        self.level = output_level
        self.ic = self.initial_conditions(m,n)


    def initial_conditions(self,
                           m:int = 16,
                           n:int = 16,
                           scale: float = 2*np.pi,
                           offset:float = -np.pi,
                           )->np.ndarray:
        rng = np.random.default_rng()
        return scale*rng.random((m,n)) + offset

    def distance(self,
                 ):
        pass

    def plot_phase(self,
                   X: np.ndarray,
                   plot_title:str = None,
                   y_axis:str = 'y',
                   x_axis:str = 'x',
                   ):
        # print(self.level,'\n',type(self.level))
        fmt = setup(plot_title,self.level)  # plotting format obj
        fig = plt.figure(figsize=(10,8))
        ax = fig.add_subplot(111)

        scale = np.pi
        resolution = 16
        colorscale = np.linspace(-scale,scale,resolution,endpoint=True)

        plt.tricontourf(X[...,0],X[...,1],X[...,2],
                        colorscale,cmap=plt.cm.nipy_spectral,
                        )
        plt.gca().invert_yaxis()
        plt.grid(b=True, which='major', axis='both')

        plt.clim(colorscale[0],colorscale[-1])
        plt.colorbar(ticks=colorscale,format='%1.2f')

        plt.title(plot_title)
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)

        # ax.xaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%g $\pi$'))
        # ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(base=1))
        plt.grid(b=None, which='major', axis='both')
        plt.show()
        fig.savefig(fmt.plot_name(plot_title,'png'))




def main():

    """
    this demos a random contour plot
    """
    corticalArray = oscillatorArray(64,64,1)
    x = np.linspace(0,corticalArray.ic.shape[0],
                      corticalArray.ic.shape[1])
    y = np.linspace(0,corticalArray.ic.shape[1],
                      corticalArray.ic.shape[0])
    x,y = np.meshgrid(x,y)

    phase_array = np.asarray([x.flatten(),
                              y.flatten(),
                              corticalArray.ic.flatten()]
                              ).T

# np.ma.masked

    corticalArray.plot_phase(phase_array,
                             'Oscillator Phase $\in$ [-$\pi$,$\pi$)',
                             'Location y',
                             'Location x'
                             )

if __name__ == '__main__':
    main()
