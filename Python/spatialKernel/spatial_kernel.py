import numpy as np
import matplotlib.pyplot as plt

from symbolic_calcs import main as derivative
from lib.plotformat import setup

# switch this nonsense to pathlib.Path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

def gaussian(x: np.ndarray,
             a: float,
             c: float,
             b: float = 0):
    return a*np.exp(-(x-b)**2/2/c**2)

def wavelet_dist(x: np.ndarray,
                 a: float,
                 c: float,
                 b: float = 0):
    return (
            3*a*np.exp(-(-b + x)**2/(2*c**2))/c**4
            - a*(-8*b + 8*x)*(-2*b + 2*x)*np.exp(-(-b + x)**2/(2*c**2))/(8*c**6)
            - a*(-2*b + 2*x)**2*np.exp(-(-b + x)**2/(2*c**2))/c**6
            + a*(-2*b + 2*x)**4*np.exp(-(-b + x)**2/(2*c**2))/(16*c**8)
            )

def wavelet_kernel(x: np.ndarray,
                   a: float,
                   c: float,
                   b: float = 0):
    # to accomodate symbolic exp expression
    import numpy.exp as exp
    wavelet = derivative(4).subs('a',a).subs('b',b).subs('c',c) # return sym exp to subs params


def plot_wavelet(X, plot_title = 'placeholder'):
    fmt = setup(plot_title)  # plotting format obj
    fig = plt.figure(figsize=(9,9))
    ax = fig.add_subplot(111)
    ax.plot(X[...,0],X[...,1],'-b')

    plt.axis('tight')
    # ax.legend(loc=3)
    plt.title(plot_title)
    plt.grid(b=True, which='major', axis='both')
    plt.show()
    fig.savefig(fmt.plot_name(plot_title,'png'))





def main():
    dist = 40
    a = 10000/3*2
    c = 10
    # b = 0 mean
    x = np.linspace(-dist,dist,1000)
    g = gaussian(x,a,c,0)
    w = wavelet_dist(x,a,c,0)

    plot_wavelet(np.asarray([x,g]).T,'Gaussian')
    plot_wavelet(np.asarray([x,w]).T,'Fourth Derivative Gaussian')


if __name__ == '__main__':
    main()
