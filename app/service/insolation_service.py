from functools import lru_cache
import math
from app.config import Config

class InsolationService:
  @lru_cache(maxsize=1)
  def run_insolation(self):
    params = Config.signal.signals

    num_points = int(1e3)
    t_start = 0
    t_end = int(1e6)
    t = [t_start + i * (t_end - t_start) / (num_points - 1) for i in range(num_points)]

    signals = {'time': t}
    all_signals = []

    for i, param in enumerate(params.values()):
      A_mod = param.A + param.Am
      signal = self.sine(A_mod, param.T, t, param.p) # type: ignore
      signals[f'signal_{i}'] = signal
      all_signals.append(signal)

    signals['total_signal'] = [sum(values) for values in zip(*all_signals)]

    return signals

  def clear_cache(self):
    self.run_insolation.cache_clear() # type: ignore

  def sine(self, A, T, t, p=0):
    if isinstance(t, (list, tuple)):
      return [A * math.sin(2 * math.pi * (1/T) * x + p) for x in t]
    else:
      return A * math.sin(2 * math.pi * (1/T) * t + p)

  def cosine(self, Am, Tm, t, p=0):
    if isinstance(t, (list, tuple)):
      return [Am * math.cos(2 * math.pi * (1/Tm) * x + p) for x in t]
    else:
      return Am * math.cos(2 * math.pi * (1/Tm) * t + p)
