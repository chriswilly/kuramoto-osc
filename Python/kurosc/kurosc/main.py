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
# annotate:
#
# note on mthds for ode soln
# https://scicomp.stackexchange.com/questions/27178/bdf-vs-implicit-runge-kutta-time-stepping

"""


def run():
    """subfn to keep obj dep going
    """
    def plot_output(data:np.ndarray,
                    time:np.ndarray,
                    file_name:str = 'model_data'):
        for t,image in enumerate(data):
            # print(image)
            kuramoto.plot_contour(image,solution.t[t])
    """
    """
    def save_data(data:np.ndarray,
                  file_name:str = 'model_data',
                  level:int = 3):
        print(file_name)
        fmt = setup(file_name,level)
        np.save(fmt.plot_name(file_name,'npy'),data)

    """
    # notes 96x96 for LSODA @ c = 3 & gain = 10*nodes**2
    #
    #
    #
    #
    """


    nodes = 96
    time =  5
    frames = 100
    gain = 12*nodes**2
    output_dir_level = 2
    indx = 1 # inspection param dict

    normalize_kernel = False

    kernel_params = {'a': int(np.round(10000/3*2)), # arbitrary iff normalize in model self.wavelet = true
                     'b': 0,
                     'c': 3,
                     'order': 4,
                     }
    interaction_params = ({'beta': 0, 'r':0},
                          {'beta': 0.25, 'r':0.95}
                          )

    kuramoto = kuramoto_system((nodes,nodes),
                                kernel_params,
                                interaction_params[indx],
                                normalize_kernel,
                                gain,
                                output_dir_level
                                )
    """Run Model"""
    time_eval = np.linspace(0,time,frames)

    continuous = False

    solution = kuramoto.solve((0,time),
                              'LSODA',   # too stiff for 'RK45', use ‘BDF’, 'LSODA', 'Radau'
                              continuous,
                              time_eval,
                              )


    osc_state = solution.y.reshape((solution.t.shape[0],
                                    nodes,
                                    nodes))%np.pi

    print('\nsol.shape:',solution.y.shape, '\nt.shape:',solution.t.shape, '\nosc.shape:',osc_state.shape)
    # print(osc_state[0])


    """Data labeling"""
    param = lambda d: [''.join(f'{key}={value}') for (key,value) in d.items()]
    title = f'{nodes}_osc_with_k-n{int(gain/nodes)}_at_t_{time}_'
    title+='_'.join(param(interaction_params[indx]))
    title+='_'+'_'.join(param(kernel_params))

    save_data(solution,title,output_dir_level)


    """Plotting & animation """
    ### kuramoto.plot_solution(osc_state[-1],solution.t[-1])
    plot_output(osc_state,solution.t)
    print(kuramoto.osc.plot_directory)

    frame_rate = 60/140 # 120 bpm -> 0.5 s/f
    vid = animate(kuramoto.osc.plot_directory,output_dir_level)
    vid.to_gif(None,frame_rate,True)





if __name__ == '__main__':
    # test_case()
    run()
