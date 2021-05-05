"""
"""
import sys

from scipy.integrate import solve_ivp
import numpy as np
# np.set_printoptions(precision=3, suppress=True)
from datetime import datetime as dt

from pathlib import Path
sys.path.append(Path(__file__).resolve().parents[1])
if __name__ == '__main__' and __package__ is None:
    __package__ = 'kurosc'

from corticalSheet.oscillator import oscillatorArray
from secondOrderInteraction.decouple import interaction
from spatialKernel.wavelet import kernel
# from kurosc.lib.plotformat import setup

from lib.plot_solution import plot_contour


class kuramoto_system(object):
    def __init__(self,
                 array_size:tuple = (16,16),
                 # initial_conditions:tuple = (0,np.pi),

                 kernel_params:dict = {'a': 10000/3*2,
                                       'b': 0,
                                       'c': 10, # breadth of wavelet
                                       'order': 4},

                 interaction_params:dict = {'beta': 0,
                                            'r': 0},
                 normalize_kernel = False,
                 gain:float = 10*16**2, # k-term
                 ):
        self.osc = oscillatorArray(array_size,(0,np.pi))
        self.kernel = kernel()
        self.gain = gain
        self.kernel_params = kernel_params
        self.interaction_params = interaction_params
        self.osc.natural_frequency = self.normal_dist(3/2)  # lookup x to gaussian

        print('\nmean natural frequency:',np.round(np.mean(self.osc.natural_frequency),3),
              '\nstdev:',np.round(np.std(self.osc.natural_frequency),3))

        self.wavelet = self.kernel.wavelet(self.kernel.spatial_wavelet,
                                           self.osc.distance.ravel(),
                                           *self.kernel_params.values(),
                                           normalize_kernel
                                           )
        # this bool determines if the wavelet is normalized
        self.interaction = interaction(self.osc.ic.shape)



    def normal_dist(self,distance:float = 3/2):
        """construct a normal dist frequency lookup"""
        resolution = 1e6 #1mln samples
        x = np.linspace(0,distance,int(resolution)) # Half curve
        # by eye
        params = {'a': 1/7,
                  'b': 0,
                  'c': 1/2,
                  }

        g = self.kernel.wavelet(self.kernel.gaussian,x,*params.values(),True)
        rng = np.random.default_rng()
        p = rng.choice(g,size=np.prod(self.osc.ic.shape),replace=False)
        # print('***********',p.shape,g.shape)
        #init a bool indx
        indx = np.zeros((*g.shape,*p.shape),dtype=bool)
        # print(indx.shape[1])
        indy = np.arange(*g.shape)
        for k,q in enumerate(p):
            indx[indy[g==q],k] = 1
            #return a mxn big list of frequencies
        # print(x[indx.any(axis=1)].shape)
        y = x[indx.any(axis=1)]
        y *= (-np.ones(*y.shape))**rng.choice((0,1),size=y.shape[0])
        return y



    def differential_equation(self,
                              t:float,
                              x:np.ndarray,
                              ):
        """ of the form: xi - 'k/n * sum_all(x0:x_N)*fn_of_dist(xi - x_j) * sin(xj - xi))'
        """

        K = self.gain
        W = self.wavelet
        ## unknown: is it ok to flatten
        G = (self.interaction.gamma(self.interaction.delta(x.ravel()),
                                    **self.interaction_params)).ravel()
        print(G.shape)
        N = np.prod(self.osc.ic.shape)
        return K/N*np.sum(W*G)+ self.osc.natural_frequency.ravel()


        # print('osc shape:',np.prod(self.osc.shape),
        #       '\nG shape:',G.shape[0])



    def solve(self,
              time_scale:tuple = (0,10),
              ode_method:str = 'Radau',
              continuous = True,
              time_eval:np.ndarray = None
              ):
        """
        """
        fn = self.differential_equation  # np.vectorize ?
        x0 = self.osc.ic.ravel()

        """option to vectorize but need to change downstream, keep false
        """
        return solve_ivp(fn,
                         time_scale,
                         x0,
                         t_eval = time_eval,
                         method=ode_method,
                         dense_output = continuous,
                         vectorized = False
                         )

    def plot_contour(self,
                     z:np.ndarray,
                     t:float = None,
                     title:str = None):
        """takes instance of oscillatorArray and plots like the plot_solution below"""
        plot_contour(self.osc,z,t,title)



    """packaged to lib, use plot()"""
    def plot_solution(self,
                      z:np.ndarray,
                      t:float = None,
                      title:str = None):
        pass


def test_case():
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
                  osc.distance.ravel(),
                  *kernel_params.values(),
                  True)
    # print(dt.now(),'\nwavelet\n',w)

    # test case using initial conditions
    a = interaction(osc.ic.shape)
    phase_difference = a.delta(osc.ic)
    g = a.gamma(phase_difference,**interaction_params[0])

    print(dt.now(),
          '\nwavelet\n',
          w,'\n',type(w),
          '\n\nphase difference vector\n',
          g.ravel(),'\n',
          type(g.ravel()),
          '\nwavelet*difference\n',
          (w*g.ravel()).shape
          )

def run():
    nodes = 128
    time =  10
    kernel_params = {'a': 10000/3*2,
                     'b': 0,
                     'c': 1,
                     'order': 4,
                     }
    interaction_params = ({'beta': 0, 'r':0},
                          {'beta': 0.25, 'r':0.95}
                          )

    kuramoto = kuramoto_system((nodes,nodes),
                                kernel_params,
                                interaction_params[0]
                                )
    solution = kuramoto.solve((0,time))
    """
    python -c "import numpy as np;
    a=np.array([[[2,3],[1,4]],[[0,1],[1,0]],[[6,7],[4,5]]]);
    b = a.flatten(); print(b);
    print(a,a.shape,'\n\n',b.reshape(3,2,2))"
    """
    osc_state = solution.y.reshape((solution.t.shape[0],nodes,nodes))%np.pi
    print(solution.y.shape, solution.t.shape)
    # print(osc_state[0])
    kuramoto.plot_solution(osc_state[-1],solution.t[-1])

if __name__ == '__main__':
    # test_case()
    run()


    """
    system of m*n indep variables subject to constraints:
    x - xij for all other ij to feed into sin (phase diff)
    w(m,n) for all other ij distances calculate once
    w(m,n) is distance dependent scalar but may be calculated more than once
    idea to evolve w(m,n) kernel function with time or provide feedback just for fun
    as if derivative power (n) or breadth of wave (a,c) or strength is modulated with system state
    """
