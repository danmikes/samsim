from functools import lru_cache
import numpy as np
import pandas as pd
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
    centered = signal - np.mean(signal)
    return np.sum(np.diff(np.sign(centered)) != 0)

  def _compare(self, original_signal, simulated_signal):
    simulated_crossings = self._cross(simulated_signal)
    original_crossings = self._cross(original_signal)
    return simulated_crossings / original_crossings if original_crossings != 0 else 0

  @lru_cache(maxsize=1)
  def run_simulation(self, sample_rate=None):
    sample_rate = sample_rate or Config.sim.sim.sample_rate
    signals = self.insolation.run_insolation()

    t = signals['time'].values
    signal = signals['total_signal'].values

    sampled_indices = np.sort(
      np.random.choice(len(signal), size=sample_rate, replace=False)
    )
    sampled_t = t[sampled_indices].astype(float)
    sampled_signal = signal[sampled_indices].astype(float)

    sim_t = np.linspace(0, self.time_span, sample_rate)
    simulated_signal = np.interp(t.astype(float), sim_t, sampled_signal)

    fit_value = self._compare(signal, simulated_signal)

    return {
      'average_fit': fit_value,
      'sample_rate': sample_rate,
      'sampled_time': sampled_t.tolist(),
      'sampled_signal': sampled_signal.tolist(),
      'simulated_time': sim_t.tolist(),
      'simulated_signal': simulated_signal.tolist(),
      'fit': fit_value,
      'fit_std': 0,
      'fit_min': fit_value,
      'fit_max': fit_value
    }

  @lru_cache(maxsize=1)
  def run_many_simulations(self):
    results = []
    for sample_rate in self.sample_range:
      sample_rate = int(sample_rate)
      sim_result = self.run_simulation(sample_rate)

      results.append({
        'sample_rate': sample_rate,
        'average_fit': sim_result['average_fit'],
        'fit_std': sim_result['fit_std'],
        'fit_min': sim_result['fit_min'],
        'fit_max': sim_result['fit_max']
      })

    result = pd.DataFrame(results)
    self._cache_many = result
    return result

  def clear_cache(self):
    self.run_simulation.cache_clear()
    self.run_many_simulations.cache_clear()
