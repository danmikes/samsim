from functools import lru_cache
import numpy as np
import pandas as pd
from app.config import Config

class InsolationService:
  @lru_cache(maxsize=1)
  def run_insolation(self):
    params = Config.signal.signals

    t = np.linspace(0, int(1e6), int(1e3))
    signals = pd.DataFrame({'time': t})

    for i, param in enumerate(params.values()):
      A_mod = param.A + param.Am
      signal = self.sine(A_mod, param.T, t, param.p) # type: ignore
      signals[f'signal_{i}'] = signal

    signal_columns = [col for col in signals.columns if col.startswith('signal')]
    signals['total_signal'] = signals[signal_columns].sum(axis=1)

    return signals

  def clear_cache(self):
    self.run_insolation.cache_clear()

  def sine(self, A, T, t, p=0):
      return A * np.sin(2 * np.pi * 1/T * t + p)

  def cosine(self, Am, Tm, t, p=0):
      return Am * np.cos(2 * np.pi * 1/Tm * t + p)
