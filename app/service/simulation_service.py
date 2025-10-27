from functools import lru_cache
import random
import math
from app.config import Config
from app.service.insolation_service import InsolationService

class SimulationService:
  def __init__(self):
    self.sim = Config.sim.sim
    self.signal = Config.signal
    self.sample = Config.sample
    self.insolation = InsolationService()

    self.time_span = self.sim.time_span
    self.signal_rate = self.sim.signal_rate
    self.sample_rate = self.sim.sample_rate

    self.sample_range = self.sample.range

  def _cross(self, signal):
    mean_val = sum(signal) / len(signal)
    centered = [x - mean_val for x in signal]
    crossings = 0
    for i in range(1, len(centered)):
      if (centered[i-1] < 0 and centered[i] >= 0) or (centered[i-1] >=0 and centered[i] < 0):
        crossings += 1
    return crossings

  def _compare(self, original_signal, simulated_signal):
    simulated_crossings = self._cross(simulated_signal)
    original_crossings = self._cross(original_signal)
    return simulated_crossings / original_crossings if original_crossings != 0 else 0

  def _interp(self, x, xp, fp):
    result = []
    for xi in x:
      for i in range(len(xp) - 1):
        if xp[i] <= xi <= xp[i+1]:
          x0, x1 = xp[i], xp[i+1]
          f0, f1 = fp[i], fp[i+1]
          if x1 == x0:
            result.append(f0)
          else:
            result.append(f0 + (f1 - f0) * (xi - x0) / (x1 - x0))
          break
      else:
        if xi <= xp[0]:
          result.append(fp[0])
        else:
          result.append(fp[-1])
    return result

  @lru_cache(maxsize=1)
  def run_simulation(self, sample_rate=None):
    sample_rate = sample_rate or Config.sim.sim.sample_rate
    signals = self.insolation.run_insolation()

    t = signals['time']
    signal = signals['total_signal']

    sampled_indices = sorted(random.sample(range(len(signal)), min(sample_rate, len(signal))))
    sampled_t = [float(t[i]) for i in sampled_indices]
    sampled_signal = [float(signal[i]) for i in sampled_indices]

    max_t = max(t)
    sim_t = [i * max_t / (sample_rate -1) for i in range(sample_rate)] if sample_rate > 1 else [0]
    simulated_signal = sampled_signal

    fit_value = self._compare(signal, simulated_signal)

    return {
      'sample_rate': sample_rate,
      'sampled_time': sampled_t,
      'sampled_signal': sampled_signal,
      'simulated_time': sim_t,
      'simulated_signal': simulated_signal,
      'fit': fit_value,
    }

  @lru_cache(maxsize=1)
  def run_many_simulations(self):
    results = []
    for sample_rate in self.sample_range:
      sample_rate = int(sample_rate)
      sim_result = self.run_simulation(sample_rate)

      results.append({
        'sample_rate': sample_rate,
        'fit': sim_result['fit'],
      })

    self._cache_many = results
    return results

  def clear_cache(self):
    self.run_simulation.cache_clear() # type: ignore
    self.run_many_simulations.cache_clear() # type: ignore
