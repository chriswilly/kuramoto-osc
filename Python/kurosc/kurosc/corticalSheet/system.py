"""
"""
import oscillator.oscillatorArray as osc
from lib.plotformat import setup
import numpy as np




def differential_system(x):
    dx = x + 'k/n * sum all(xi:x_j)*fun_of_dist(xi - x_j) * sin(thi - thj))'
    """
    system of m*n indep variables subject to constraints:
    x - xij for all other ij to feed into sin (phase diff)
    w(m,n) for all other ij distances calculate once
    w(m,n) is distance dependent scalar but may be calculated more than once
    idea maybe evaolve w(m,n) kernel function with time or provide feedback just for fun
    as if derivative power (n) or breadth of wave (a,c) or strength is modulated with system state


    calculate distance --> vec /flatten
    feed into kernel
    --> this is scalar apatial kernel



    """

    return dx

"""
there is a phase delta fn in secondorderinteraction.decouple
that may be iterated over for a given index
we then feed that into the decoupling function gamma

    def delta(self,
              phase_array: np.array = np.array([[1,5],[8,100]])
              ) -> np.ndarray:
        ###pase difference of element from global array
        return phase_array[self.index[0],self.index[1]] - phase_array
"""



"""
beta = 0 r = 0 is basic kuramoto gamma


    def gamma(self,
              x: np.ndarray,
              beta: float = 1/4,
              r: float = 8/10
              ) -> np.ndarray:
        return -np.sin(x+beta) + r*np.sin(2*x)


"""
