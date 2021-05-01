"""
construct 2d array of pase state
distance array

"""
import sys
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# from numpy.random import standard_normal
if __name__ == '__main__':
    from lib.plotformat import setup
else:
    from .lib.plotformat import setup

print(Path(__file__).resolve().parents[1])
# sys.path.append(Path(__file__).resolve().parents[1])
# from .lib.plotformat import setup


# np.ma.masked

def initial_conditions(m:int = 16,
                       n:int = 16,
                       scale: float = 2*np.pi,
                       offset:float = -np.pi,
                       )->np.ndarray:
    rng = np.random.default_rng()
    return scale*rng.random((m,n)) + offset

def distance():
    pass

def plot_phase(X: np.ndarray,
               plot_title:str = 'placeholder',
               y_axis:str = 'y',
               x_axis:str = 'x',
               ):
    fmt = setup(plot_title)  # plotting format obj
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111)

    scale = np.pi
    resolution = 13
    colorscale = np.linspace(-scale,scale,resolution,endpoint=True)

    plt.tricontourf(X[...,0],X[...,1],X[...,2],
                    colorscale,cmap=plt.cm.nipy_spectral)
    plt.clim(colorscale[0],colorscale[-1])
    plt.grid(b=True, which='major', axis='both')
    plt.colorbar(ticks=colorscale)

    plt.title(plot_title)  #  .join(r' Random IC $\in$ [-$\pi$,$\pi$)'))
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)

    # ax.xaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%g $\pi$'))
    # ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(base=1))
    plt.grid(b=None, which='major', axis='both')
    plt.show()
    fig.savefig(fmt.plot_name(plot_title,'png'))



"""
colorscale = np.linspace(lower,upper,20,endpoint=True)

plt.tricontourf(x,y,z,colorscale,cmap=plt.cm.nipy_spectral)
plt.clim(colorscale[0],colorscale[-1])
plt.grid(b=True, which='major', axis='both')
plt.colorbar(ticks=colorscale)

"""


def main():
    ic = initial_conditions(64,64)
    x = np.linspace(0,ic.shape[0],ic.shape[1])
    y = np.linspace(0,ic.shape[1],ic.shape[0])
    x,y = np.meshgrid(x,y)
    phase_array = np.asarray([x.flatten(),
                              y.flatten(),
                              ic.flatten()]).T
    # print(np.asarray([x.flatten(),
    #                   y.flatten(),
    #                   ic.flatten()]))
    plot_phase(phase_array,'Oscillator Phase')

if __name__ == '__main__':
    main()
