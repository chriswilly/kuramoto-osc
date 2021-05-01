"""
koramoto oscillator system with the modifications:

######
2D Array of weekly coupled oscillators: corticalSheet.oscillatorArray
initial_conditions(m:int = 16,
                   n:int = 16,
                   scale: float = 2*np.pi,
                   offset:float = -np.pi,
                   )->np.ndarray:

distance...

######
Spatial considerations: spatialKernel.spatial_kernel
kernel(fn,
       x: np.ndarray,
       a: float = 10000/3*2,
       b: float = 0,  # mean
       c: float = 10,
       d: float = 4,
       normalize = False,
       ) -> np.ndarray:

w = kernel(spatial_wavelet,x,*params.values(),True)

plot_wavelet(np.asarray([x,w]).T,
             '{}th Derivative Gaussian'.format(str(params['order'])),
             'Arbitrary Magnitube',
             'Node Distance')

######
Second Order Interaction: secondOrderInteraction.neuralInteraction
class based on index
gamma(x: np.ndarray,
      beta: float = 1/4,
      r: float = 8/10
      ) -> np.ndarray:
      return -np.sin(x+beta) + r*np.sin(2*x)

g = gamma(x,**p)

"""
"""this architecture will be moved into package under a new name"""

import corticalSheet.oscillatorArray as array
import spatialKernel.spatial_kernel as wavelet
from secondOrderInteraction.neuralInteraction import interaction

print('ok')



def main():
    ic = array.initial_conditions() # fn
    # kernel = wavelet.kernel() # change to class
    neighbors = interaction()  # class

    import numpy as np
    test = neighbors.gamma(np.linspace(-np.pi,np.pi,10))
    print(neighbors.delta())
    # array.main()

if __name__ == '__main__':
    main()
