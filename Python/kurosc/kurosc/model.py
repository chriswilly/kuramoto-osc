"""
"""
import sys

from scipy.integrate import solve_ivp
import numpy as np
np.set_printoptions(precision=3, suppress=True)
from datetime import datetime as dt

from pathlib import Path
sys.path.append(Path(__file__).resolve().parents[1])
if __name__ == '__main__' and __package__ is None:
    __package__ = 'kurosc'

from corticalSheet.oscillator import oscillatorArray
from secondOrderInteraction.decouple import interaction
# from spatialKernel.wavelet import kernel
from lib.plot_solution import (plot_contour,
                               plot_timeseries)


class kuramoto_system(object):
    def __init__(self,
                 array_size:tuple = (16,16),

                 kernel_params:dict = {'a': 10000/3*2,
                                       'b': 0,
                                       'c': 10, # breadth of wavelet
                                       'order': 4},

                 interaction_params:dict = {'beta': 0,
                                            'r': 0},

                 natural_freq_params:dict = {'a': 1/6,
                                             'b': 0,
                                             'c': 2/5,
                                             'order':0,
                                             },

                 normalize_kernel = False,
                 gain:float = 10*16**2, # k-term

                 external_input:bool=False,
                 input_weight:float=0,

                 out_dir:int = 3,
                 ):

        """
        """
        self.osc = oscillatorArray(array_size,(0,np.pi),out_dir)

        self.osc.interaction_params = interaction_params  # pass thru maybe to label plots
        self.osc.kernel_params = kernel_params
        self.osc.gain = gain

        self.osc.natural_frequency = self.osc.natural_frequency_dist(natural_freq_params)

        self.wavelet = self.osc.kernel.wavelet(self.osc.kernel.spatial_wavelet,
                                               self.osc.distance.ravel(),
                                               *self.osc.kernel_params.values(),
                                               normalize_kernel
                                               )

        self.interaction = interaction(self.osc.ic.shape)
        self.plot_contour = plot_contour
        self.plot_timeseries = plot_timeseries
        self.external_input = external_input
        self.input_weight = input_weight



    def differential_equation(self,
                              t:float,
                              x:np.ndarray,
                              ):
        """ of the form: xi - 'k/n * sum_all(x0:x_N)*fn_of_dist(xi - x_j) * sin(xj - xi))'
        """

        K = self.osc.gain
        W = self.wavelet

        G = (self.interaction.gamma(self.interaction.delta(x.ravel()),
                                    **self.osc.interaction_params)).ravel()
        N = np.prod(self.osc.ic.shape)

        dx = K/N*np.sum(W*G) + self.osc.natural_frequency.ravel()


        if self.external_input:
            dx+=self.input_weight*self.external_input_fn(t)

        # if t==0:
        #     print(N)
        print('t_step:',np.round(t,4))
        return dx


    def solve(self,
              time_scale:tuple = (0,10),
              ode_method:str = 'LSODA',  # 'Radau' works too, RK45 not so much
              continuous_fn = True,
              time_eval:np.ndarray = None,
              max_delta_t:float = 0.1,
              zero_ics:bool = False,
              ):
        """Solve ODE using methods, problem may be stiff so go with inaccurate to hit convergence
        """
        fn = self.differential_equation  # np.vectorize ?

        if not zero_ics:
            x0 = self.osc.ic.ravel()
        else:
            x0 = np.zeros(np.prod(self.osc.ic.shape))

        """option to vectorize but need to change downstream, keep false
        """
        return solve_ivp(fn,
                         time_scale,
                         x0,
                         t_eval = time_eval,
                         max_step = max_delta_t,
                         method=ode_method,
                         dense_output = continuous_fn,
                         vectorized = False
                         )



    def external_input_fn(self,t:float,w:float):
        # cos(w*t)
        return 0


###############################################################################
## unit tests may need update below but not called into model
###############################################################################
def test_case():
    from spatialKernel.wavelet import kernel
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
