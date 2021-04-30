import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import sys


# custom scripts
from lib.plotformat import setup


""" Eqn 13 + Fig 4
"""
def gamma(x: np.ndarray,
          beta: float = 1/4,
          r: float = 8/10):
    return -np.sin(x+beta) + r*np.sin(2*x)



def plot_phase(X, plot_title = 'placeholder'):
    fmt = setup(plot_title)  # plotting format obj
    fig = plt.figure(figsize=(9,9))
    ax = fig.add_subplot(111)
    ax.plot(X[...,0]/np.pi,X[...,1],'-b')
    ax.plot(np.asarray([X[0,0],X[-1,0]])/np.pi,[0,0],'-k')  #
    plt.axis('tight')
    # ax.legend(loc=3)
    plt.title(plot_title)

    ax.xaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%g $\pi$'))
    ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(base=1))
    plt.grid(b=True, which='major', axis='both')
    plt.show()
    fig.savefig(fmt.plot_name(plot_title,'png'))


def main():
    dist = np.pi

    params = [
              {'beta': 0.25, 'r':0.95},
              {'beta': 0.25, 'r':0.8},
              {'beta': 0.25, 'r':0.7},
              ]
    i =2
    x = np.linspace(-dist,dist,1000)
    g = gamma(x,**params[i])

    r = params[i]['r']
    plot_phase(np.asarray([x,g]).T,f'R = {r}')


if __name__ == '__main__':
    main()
