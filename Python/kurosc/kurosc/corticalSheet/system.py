"""
"""
import oscillator.oscillatorArray as osc
from lib.plotformat import setup
import numpy as np




def differential_system(x):
    dx = x + 'k/n * sum all(xi - x_j)*dist(xi - x_j * sin(thi - thj))'
    redurn dx
