from collections import namedtuple
from app.config import Config

import numpy as np

Par = namedtuple('Pars', ['T','A','Tm','Am','p'])

class SimulationManager:
  def __init__(self):
    self.default_pars = self._get_default_parameters()
    self.config = Config.SIMULATION_CONFIG

  def _get_default_parameters(self):
    T1, T2, T3 = int(1.0e5), int(4.1e4), int(2.6e4)
    A1, A2, A3 = int(2), int(25), int(15)
    Tm1, Tm2, Tm3 = int(T1 * 5), int(T2 * 5), int(T3 * 5)
    Am1, Am2, Am3 = int(A1 / 2), int(A2 / 2), int(A3 / 2)

    return (
      Par(T1, A1, Tm1, Am1, 0),
      Par(T2, A2, Tm2, Am2, 0),
      Par(T3, A3, Tm3, Am3, 0)
    )

  def run_insolation(self, pars=None):
    if pars is None:
      pars = self.default_pars

    t = np.linspace(0, int(1e6), int(1e3))
    signals = []

    for par in pars:
      A_mod = par.A + self.cosine(par.Am, par.Tm, t)
      signal = self.sine(A_mod, par.T, t)
      signals.append(signal)

    total_signal = np.sum(signals, axis=0)

    return t, signals, total_signal

  def sine(self, A, T, t, p=0):
    return A * np.sin(2 * np.pi * 1/T * t + p)

  def cosine(self, Am, Tm, t, p=0):
    return Am * np.cos(2 * np.pi * 1/Tm * t + p)
