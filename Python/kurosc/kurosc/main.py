"""
"""
import sys
from pathlib import Path
sys.path.append(Path(__file__).resolve())
if __name__ == '__main__' and __package__ is None:
    __package__ = 'kurosc'

from datetime import datetime as dt
import numpy as np
import json

from model import kuramoto_system
from lib.animate import animate
from lib.plot_solution import ( plot_output,
                                save_data
                                )

"""
# annotate:
#
# note on mthds for ode soln
# https://scicomp.stackexchange.com/questions/27178/bdf-vs-implicit-runge-kutta-time-stepping

"""


def run(config_file:str = Path('model_config.json').resolve(),
        set:str = 'test_set0'):
    """
    """
    f = open(config_file)
    var = json.load(f)


    method = var[set]['ODE_method']   # too stiff for 'RK45', use 'LSODA',‘BDF’,'Radau'

    nodes = var[set]['nodes']
    time =  var[set]['time']
    frames = var[set]['frames']
    frame_rate = var[set]['frame_rate'] # 120 bpm -> 0.5 s/f
    interpolate = bool(var[set]['interpolate_plot'])

    gain_ratio = var[set]['gain_ratio']
    output_dir_level = var[set]['output_dir_level']
    interaction_complexity = var[set]['interaction_complexity']

    normalize_kernel = bool(var[set]['normalize_kernel'])
    continuous_soln =  bool(var[set]['continuous_soln'])

    kernel_params = var[set]['kernel_params']
    interaction_params = var[set]['interaction_params']
    natural_freq_params = var[set]['natural_freq_params']


    """Init model"""
    gain = gain_ratio*nodes**2

    kuramoto = kuramoto_system((nodes,nodes),
                                kernel_params,
                                interaction_params[interaction_complexity],
                                natural_freq_params,
                                normalize_kernel,
                                gain,
                                output_dir_level
                                )
    """Run Model"""
    time_eval = np.linspace(0,time,frames)



    solution = kuramoto.solve((0,time),
                              method,
                              continuous_soln,
                              time_eval,
                              )
    # print('\ny.shape:',solution.y.shape)   # for 32x32 : 1024 x 160
    # reshape(0,1,2)
    # thgen enumerate on ax 2
    # numpy.nditer(
    #
    # input('.')
    osc_state = solution.y.reshape((nodes,
                                    nodes,
                                    solution.t.shape[0]
                                    ))

    print('\nsol.shape:',solution.y.shape,
          '\nt.shape:',solution.t.shape,
          '\nosc.shape:',osc_state.shape)




    """Data labeling"""
    param = lambda d: [''.join(f'{key}={value}') for (key,value) in d.items()]
    title = f'{nodes}_osc_with_kn={int(gain/nodes)}_at_t_{time}_'
    title+='_'.join(param(interaction_params[interaction_complexity]))
    title+='_'+'_'.join(param(kernel_params))

    save_data(solution,title,output_dir_level)


    """Plotting & animation """
    ### kuramoto.plot_solution(osc_state[-1],solution.t[-1])

    plot_output(kuramoto,kuramoto.osc,
                osc_state,solution.t, interpolate)

    print(kuramoto.osc.plot_directory)

    vid = animate(kuramoto.osc.plot_directory,output_dir_level)
    vid.to_gif(None,frame_rate,True)





if __name__ == '__main__':
    run()
