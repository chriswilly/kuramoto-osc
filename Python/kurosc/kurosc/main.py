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
import argparse

##
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


def run_process(set:str = 'global_sync',
                config_file:str = 'model_config.json'):
                print('\n',set,'\n')
                run(set,config_file)


def run(set:str = 'global_sync',
        config_file:str = 'model_config.json'):
    """
    """
    config_file = Path(config_file).resolve()
    f = open(config_file)
    var = json.load(f)

    """Load all variables from specified set in json"""
    method = var[set]['ODE_method']   # too stiff for 'RK45', use 'LSODA',‘BDF’,'Radau'

    nodes = var[set]['sqrt_nodes']
    time =  var[set]['time']
    max_delta_t = var[set]['max_delta_t']
    inspect_t_seconds = var[set]['inspect_t_seconds']
    inspect_t_samples = var[set]['inspect_t_samples']



    frames = var[set]['frames']
    frame_rate = var[set]['frame_rate'] # 120 bpm -> 0.5 s/f
    interpolate = (False if var[set]['interpolate_plot']=='False' else True)
    save_numpy = (False if var[set]['save_numpy']=='False' else True)

    gain_ratio = var[set]['gain_ratio']


    output_dir_level = var[set]['output_dir_level']
    interaction_complexity = var[set]['interaction_complexity']

    normalize_kernel = (False if var[set]['normalize_kernel']=='False' else True)
    continuous_soln =  (False if var[set]['continuous_soln']=='False' else True)
    zero_ics = (False if var[set]['zero_ics']=='False' else True)

    kernel_params = var[set]['kernel_params']
    interaction_params = var[set]['interaction_params']
    natural_freq_params = var[set]['natural_freq_params']

    external_input = (False if var[set]['external_input']=='False' else True)
    external_input_weight = var[set]['external_input_weight']


    """Init model"""
    gain = gain_ratio*nodes**2

    kuramoto = kuramoto_system((nodes,nodes),
                                kernel_params,
                                interaction_params[interaction_complexity],
                                natural_freq_params,
                                normalize_kernel,
                                gain,
                                external_input,
                                external_input_weight,
                                output_dir_level
                                )
    """Run Model"""
    time_eval = np.linspace(0,time,frames)



    solution = kuramoto.solve((0,time),
                              method,
                              continuous_soln,
                              time_eval,
                              max_delta_t,
                              zero_ics,
                              )


    osc_state = solution.y.reshape((nodes,
                                    nodes,
                                    solution.t.shape[0]
                                    ))

    print('\nsol.shape:',solution.y.shape,
          '\nt.shape:',solution.t.shape,
          '\nosc.shape:',osc_state.shape)


    """Data labeling"""
    param = lambda d: [''.join(f'{key}={value}') for (key,value) in d.items()]
    title = f'{nodes}_osc_with_kn={int(gain/nodes**2)}_at_t_{time}_'
    title+='_'.join(param(interaction_params[interaction_complexity]))
    title+='_'+'_'.join(param(kernel_params))



    if save_numpy:
        print('\ndata save is set to:',save_numpy,'type', type(save_numpy),
        '\noutput to:', title,output_dir_level,'levels up from lib')
        save_data(solution,title,output_dir_level)


    """Plotting & animation """
    ### kuramoto.plot_solution(osc_state[-1],solution.t[-1])

    plot_output(kuramoto,kuramoto.osc,
                osc_state,solution.t,
                inspect_t_samples,
                inspect_t_seconds,
                interpolate)

    vid = animate(kuramoto.osc.plot_directory,output_dir_level)
    vid.to_gif(None,frame_rate,True,True)
    print(vid.img_name)

    #TODO post process numpy array to have time series or just hadle it in this chain


def main():
    parser = argparse.ArgumentParser(description='Select model_config scenario & path (optional):')

    parser.add_argument('--set', metavar='scenario | variable set',
                        type=str, nargs='?',
                        help='model_config.json key like global_sync',
                        default='test_set0')


    parser.add_argument('--path', metavar='directory to config.json',
                        type=str, nargs='?',
                        help='model_config.json path, default is pwd',
                        default='model_config.json')

    args = parser.parse_args()
    run(args.set, args.path)



if __name__ == '__main__':
    main()
