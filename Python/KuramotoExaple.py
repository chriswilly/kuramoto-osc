import numpy as np
import pandas as pd

cimport numpy as np

DTYPE = np.float
ctypedef np.float_t DTYPE_t
cdef float PI = np.pi

cdef class Kuramoto(object):

    cdef readonly float omega
    cdef readonly float initial_phi

    cdef public connections
    cdef public sensitivity
    cdef public stimulator
    cdef public noise

    cdef public summary

    def __init__(self, float omega, float initial_phi):

        self.omega = omega              # Natural frequency of this oscillator, in Hertz
        self.initial_phi = initial_phi

        self.connections = None         # List of connection functions between this and all other oscillators in the net
        self.sensitivity = None         # Function describing sensitivity to stim based on phase
        self.stimulator = None          # Stimulator object that provides stimulation
        self.noise = None               # Noise object that provides random noise

        self.summary = None

    def build(self, num_connections, connection_func, sensitivity, stimulator, noise):
        self.connections = [connection_func] * num_connections
        self.sensitivity = sensitivity
        self.stimulator = stimulator
        self.noise = noise

    cpdef equation(self, float t, float this_phase, np.ndarray[DTYPE_t, ndim=1] peer_phases):
        return self.omega \
               + self.phase_input(this_phase, peer_phases) \
               + self.stim_input(this_phase) \
               + self.noise_input()

    cdef float phase_input(self, float this_phase, np.ndarray[DTYPE_t, ndim=1] peer_phases):
        cdef int i = 0
        cdef int len_p = peer_phases.shape[0]
        cdef float total

        i = 0
        total = 0
        while i < len_p:
            delta = peer_phases[i] - this_phase
            total += self.connections[i](delta)
            i += 1

        return total / len_p

    cdef float stim_input(self, float this_phase):
        cdef float sensitivity = self.sensitivity(this_phase)
        cdef float stim_effect = self.stimulator.voltage * sensitivity
        return stim_effect

    cdef float noise_input(self):
        return self.noise.value

    def ready_log(self, time_course, phases):
        """"""
        summary_dict = {
            'Time': time_course,
            'Phase': phases
        }

        self.summary = pd.DataFrame.from_dict(summary_dict)
