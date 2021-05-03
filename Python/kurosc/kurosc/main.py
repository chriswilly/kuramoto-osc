import sys
from pathlib import Path
sys.path.append(Path(__file__).resolve())
if __name__ == '__main__' and __package__ is None:
    __package__ = 'kurosc'

from corticalSheet.oscillator import oscillatorArray
from secondOrderInteraction.decouple import interaction
from spatialKernel.wavelet import kernel


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
                                interaction_params[0],
                                1.0
                                )
    solution = kuramoto.solve((0,time))
    osc_state = solution.y.reshape((solution.t.shape[0],nodes,nodes))%np.pi
    print(solution.y.shape, solution.t.shape)
    # print(osc_state[0])
    kuramoto.plot_solution(osc_state[-1],solution.t[-1])


if __name__ == '__main__':
    # test_case()
    run()
