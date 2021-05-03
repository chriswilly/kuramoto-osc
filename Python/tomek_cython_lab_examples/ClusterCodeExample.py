import os
import json

import numpy as np
import pandas as pd
from abc import ABC, abstractmethod

from scipy.integrate import solve_ivp

from models.noise import build_noise
from models.stimulation import build_stimulator
from models.oscillators import build_oscillators, build_connection, build_sensitivity


class Network(ABC):
    """
    Base class for any collection of connected, interacting elements
    """

    def __init__(self):
        self.nodes = []
        self.time_course = None
        self.summary = None
        self.specification = None

    @abstractmethod
    def build(self, specification):
        pass

    @abstractmethod
    def build_equation(self):
        """Return a function that returns the vector dy/dt at any time step"""
        pass

    @abstractmethod
    def get_initial(self):
        """Return the initial conditions imposed on this cluster"""
        pass

    @abstractmethod
    def log_solution(self, solution):
        for node in self.nodes:
            try:
                node.ready_log()
            except AttributeError:
                pass

    def solve(self, t_span, max_step, method='RK45'):
        equation = self.build_equation()
        initial = self.get_initial()
        solution = solve_ivp(equation, t_span, initial, max_step=max_step, method=method)
        return solution


class Cluster(Network):
    """
    A special kind of network intended to be part of a larger collection of networks
    """

    def __init__(self):
        self.oscillators = []
        self.stimulator = None
        self.noise = None

        super(Cluster, self).__init__()

    def build(self, specification):

        self.specification = specification

        self.oscillators = build_oscillators(specification['oscillators'])
        self.stimulator = build_stimulator(specification['stimulator'])
        self.noise = build_noise(specification['noise'])

        connection = build_connection(specification['connection'])
        sensitivity = build_sensitivity(specification['sensitivity'])
        for oscillator in self.oscillators:
            oscillator.build(len(self.oscillators), connection, sensitivity, self.stimulator, self.noise)

        self.nodes.extend(self.oscillators)
        self.nodes.append(self.stimulator)
        self.nodes.append(self.noise)

    def get_initial(self):
        return [oscillator.initial_phi for oscillator in self.oscillators]

    def build_equation(self):
        stim = self.stimulator
        noise = self.noise

        def equation(t, phases):
            stim.update(t)
            noise.update(t)
            return [
                o.equation(t, phases[i], phases)
                for i, o in enumerate(self.oscillators)
            ]
        return equation

    def log_solution(self, solution):
        """Convert the ode solver solution in a format that is ready to be saved"""

        self.time_course = solution.t
        phases = np.mod(solution.y.T, 2 * np.pi)

        if self.stimulator:
            self.stimulator.ready_log(self.time_course)

        if self.noise:
            self.noise.ready_log(self.time_course)

        phase_summary = {'Time': self.time_course}
        for i, node in enumerate(self.oscillators):
            node.ready_log(self.time_course, phases[:, i])
            phase_summary[f'Phase {i}'] = node.summary['Phase']

        self.summary = pd.DataFrame.from_dict(phase_summary)

    def save(self, save_path, save_oscillators=False):

        # Save basic, top-level data about the cluster
        self.summary.to_csv(os.path.join(save_path, 'phases.csv'), float_format='%g')
        self.noise.summary.to_csv(os.path.join(save_path, 'noise.csv'), float_format='%g')
        self.stimulator.summary.to_csv(os.path.join(save_path, 'stimulation.csv'), float_format='%g')
        with open(os.path.join(save_path, 'specification.json'), 'w') as spec_out:
            json.dump(self.specification, spec_out, indent=2)

        # If desired, save all the data from the individual oscillators
        oscillator_path = os.path.join(save_path, 'oscillators')
        os.mkdir(oscillator_path)

        oscillator_metadata = []
        for i, o in enumerate(self.oscillators):
            oscillator_metadata.append({'i': i, 'initial phi': o.initial_phi, 'omega': o.omega})
            if save_oscillators:
                o.summary.to_csv(os.path.join(oscillator_path, f'{i}.csv'))

        with open(os.path.join(oscillator_path, 'initialization.json'), 'w') as init_out:
            json.dump(oscillator_metadata, init_out, indent=2)
