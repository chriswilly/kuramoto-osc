"""
"""

import sys
from pathlib import Path
sys.path.append(Path(__file__).resolve())
if __name__ == '__main__' and __package__ is None:
    __package__ = 'kurosc'

from datetime import datetime as dt
import numpy as np
np.set_printoptions(precision=3, suppress=True)


from model import kuramoto_system
from lib.plotformat import setup
from lib.animate import animate


"""
"""

def save_data(data:np.ndarray,
              file_name:str = 'model_data'):
    print(file_name)
    # fmt = setup(file_name,2)
    # np.save(fmt.plot_name(file_name,'npy'))



def run():
    """
    """
    def plot_output(data:np.ndarray,
                    time:np.ndarray,
                    file_name:str = 'model_data'):
        for t,image in enumerate(data):
            # print(image)
            kuramoto.plot_solution(image,solution.t[t])
    """"""
    nodes = 64
    time =  10
    gain = 0.5
    normalize_kernel = False

    kernel_params = {'a': 10000/3*2, # arbitrary iff normalize in model self.wavelet = true
                     'b': 0,
                     'c': 10,
                     'order': 4,
                     }
    interaction_params = ({'beta': 0, 'r':0},
                          {'beta': 0.25, 'r':0.95}
                          )

    indx = 0 # inspection param dict
    kuramoto = kuramoto_system((nodes,nodes),
                                kernel_params,
                                interaction_params[indx],
                                normalize_kernel,
                                gain
                                )

    solution = kuramoto.solve((0,time))
    osc_state = solution.y.reshape((solution.t.shape[0],nodes,nodes))%np.pi
    print(solution.y.shape, solution.t.shape)
    # print(osc_state[0])
    param = lambda d: [''.join(f'{key}={value}') for (key,value) in d.items()]
    title = f'{nodes}osc_at_t_{time}_'
    title+='_'.join(param(interaction_params[indx]))


    plot_output(osc_state,solution.t)
    print(kuramoto.osc.plot_directory)

    vid = animate(kuramoto.osc.plot_directory)
    vid.to_gif(kuramoto.osc.plot_directory,0.75,True)
    # save_data(title,solution)
    # kuramoto.plot_solution(osc_state[-1],solution.t[-1])


if __name__ == '__main__':
    # test_case()
    run()
