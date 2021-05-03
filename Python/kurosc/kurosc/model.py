"""
"""
import sys
from pathlib import Path
sys.path.append(Path(__file__).resolve())

from scipy.integrate import solve_ivp
import numpy as np
np.set_printoptions(precision=3, suppress=True)
from datetime import datetime as dt

from corticalSheet.oscillator import oscillatorArray
from secondOrderInteraction.decouple import interaction
from spatialKernel.wavelet import kernel


class kuramoto_system(object):
    def __init__(self,
                 array_size:tuple = (2,2),
                 kernel_params:dict = {'a': 10000/3*2,
                                       'b': 0,
                                       'c': 10, # breadth of wavelet
                                       'order': 4},
                 interaction_params:dict = {'beta': 0,
                                            'r': 0},
                 gain:float = 1., # k-term
                 ):
        self.osc = oscillatorArray(array_size,(0,np.pi))
        self.kernel = kernel()
        self.gain = gain
        self.kernel_params = kernel_params
        self.interaction_params = interaction_params

        self.wavelet = self.kernel.wavelet(self.kernel.spatial_wavelet,
                                           self.osc.distance.flatten(),
                                           *self.kernel_params.values(),
                                           True
                                           )
        # this bool determines if the wavelet is normalized
        self.interaction = interaction(self.osc.ic.shape)


    def differential_equation(self,
                              t:float,
                              x:np.ndarray,
                              ):
        """ of the form: xi - 'k/n * sum_all(x0:x_N)*fn_of_dist(xi - x_j) * sin(xj - xi))'
        """
        phase_difference = self.interaction.delta(x)
        k = self.gain
        W = self.wavelet
        G = (self.interaction.gamma(phase_difference,
                                    **self.interaction_params)
                                    .flatten())
        N = G.shape[0]
        return x + k/N*np.sum(W*G)


    def solve(self,
              time_scale:tuple = (0,10),
              time_eval = None
              ):
        """ solve_ivp is ode45
        """
        fn = self.differential_equation
        x0 = self.osc.ic.flatten()
        sol = solve_ivp(fn,
                        time_scale,
                        x0,
                        t_eval = time_eval,
                        method='RK45',
                        vectorized = True)
        # print(sol.t)
        # print(sol.y)
        return sol



    def plot_solution(self,
                      z:np.ndarray,
                      t:float = None):
        """
        """
        x = np.linspace(0,self.osc.ic.shape[0],
                          self.osc.ic.shape[1])
        y = np.linspace(0,self.osc.ic.shape[1],
                          self.osc.ic.shape[0])
        x,y = np.meshgrid(x,y)

        phase_array = np.asarray([x.flatten(),
                                  y.flatten(),
                                  z.flatten()%np.pi]
                                  ).T
        if abs(self.osc.domain[0]) % np.pi == 0 and not self.osc.domain[0] == 0:
            ti = r'\pi'
            ti = '-'+ti
        else:
            ti = str(self.osc.domain[0])
        if abs(self.osc.domain[1]) % np.pi == 0 and not self.osc.domain[1] == 0:
            tf = r'\pi'
        else:
            tf = str(self.osc.domain[1])

        title = 'Oscillator Phase $\in$ [${0}$,${1}$)'.format(ti,tf)
        if t:
            title+=f' at t = {t:,.1f}'


        self.osc.plot_phase(phase_array,
                            title,
                            'Location y',
                            'Location x'
                            )



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
                  osc.distance.flatten(),
                  *kernel_params.values(),True)
    # print(dt.now(),'\nwavelet\n',w)

    # test case using initial conditions
    a = interaction(osc.ic.shape)
    phase_difference = a.delta(osc.ic)
    g = a.gamma(phase_difference,**interaction_params[0])

    print(dt.now(),
          '\nwavelet\n',
          w,'\n',type(w),
          '\n\nphase difference vector\n',
          g.flatten(),'\n',
          type(g.flatten()),
          '\nwavelet*difference\n',
          (w*g.flatten()).shape
          )

def run():
    nodes = 128
    time =  99
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
