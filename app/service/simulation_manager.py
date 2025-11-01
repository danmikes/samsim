# simulation_manager.py
import numpy as np
import pandas as pd
from collections import namedtuple
from scipy.optimize import curve_fit
from app.config import Config, SampleSizeRange
from app.service.insolation_manager import InsolationManager

class SimulationManager:
  def __init__(self):
    self.duration = Config.CONFIG['DURATION']
    self.signal_rate = Config.CONFIG['SIGNAL_RATE']
    self.sample_size = Config.CONFIG['SAMPLE_SIZE']
    self.repetitions = Config.CONFIG['REPETITIONS']

    self.sample_size_range = Config.DEFAULT_SAMPLE_SIZE_RANGE
    self.sample_sizes = self.sample_size_range.get_sizes()

    self.parameter_ranges = Config.PARAMETER_RANGES
    self.insolation_manager = InsolationManager()

  def set_sample_size_range(self, preset):
    if isinstance(preset, str):
      preset = SampleSizeRange[preset.upper()]
    self.sample_size_preset = preset
    self.sample_sizes = preset.get_sizes()

  def get_available_size_ranges(self):
    return {
      preset.name: {
        'sizes': preset.get_sizes().tolist() if preset != SampleSizeRange.CUSTOM else [],
        'description': f"{preset.name.lower()} range"
      }
      for preset in SampleSizeRange
      if preset != SampleSizeRange.CUSTOM
    }

  def _cross(self, signal):
    centered = signal - np.mean(signal)
    return np.sum(np.diff(np.sign(centered)) != 0)

  def _compare(self, original_signal, simulated_signal):
    simulated_crossings = self._cross(simulated_signal)
    original_crossings = self._cross(original_signal)

    return simulated_crossings / original_crossings if original_crossings != 0 else 0

  def run_simulation(self, signals=None, sample_size=None, repetitions=None, duration=None):
    if signals is None:
      signals = self.insolation_manager.run_insolation()

    if sample_size is None:
      sample_size = self.sample_size

    if repetitions is None:
      repetitions = self.repetitions

    if duration is None:
      duration = self.duration

    t = signals['time'].values
    signal = signals['total_signal'].values

    results = []

    for _ in range(repetitions):
      sampled_indices = np.sort(
        np.random.choice(len(signal), size=sample_size, replace=False)
      )
      sampled_t = t[sampled_indices].astype(float)
      sampled_signal = signal[sampled_indices].astype(float)

      sim_t = np.linspace(0, duration, sample_size)
      simulated_signal = np.interp(t.astype(float), sim_t, sampled_signal)

      fit_value = self._compare(signal, simulated_signal)

      results.append({
        'sampled_time': sampled_t.tolist(),
        'sampled_signal': sampled_signal.tolist(),
        'simulated_time': sim_t.tolist(),
        'simulated_signal': simulated_signal.tolist(),
        'fit': fit_value
      })

    df = pd.DataFrame(results)
    avg_fit = df['fit'].mean()

    return {
      'average_fit': avg_fit,
      'sample_size': sample_size,
      'repetitions': repetitions,
      'individual_runs': results,
      'fit_std': df['fit'].std(),
      'fit_min': df['fit'].min(),
      'fit_max': df['fit'].max()
    }

  def run_many_simulations(self, signal_data=None, sample_sizes=None):
    if signal_data is None:
      signal_data = self.insolation_manager.run_insolation()

    if sample_sizes is None:
      sample_sizes = self.sample_sizes

    t = signal_data['time'].values
    signal = signal_data['total_signal'].values

    results = []

    for sample_size in sample_sizes:
      sample_size = int(sample_size)
      sim_result = self.run_simulation(signal_data, sample_size, repetitions=5)

      results.append({
        'sample_size': sample_size,
        'average_fit': sim_result['average_fit'],
        'fit_std': sim_result['fit_std'],
        'fit_min': sim_result['fit_min'],
        'fit_max': sim_result['fit_max']
      })

    return pd.DataFrame(results)

  def run_parameter_sensitivity(self, param_ranges, signal_data=None):
    if signal_data is None:
      signal_data = self.insolation_manager.run_insolation()

    results = []

    param_names = list(param_ranges.keys())
    param_values = list(param_ranges.values())

    from itertools import product
    combinations = list(product(*param_values))

    for combo in combinations:
      params = dict(zip(param_names, combo))

      modified_signal = self._modify_signal_with_params(signal_data, params)

      sim_result = self.run_simulation(modified_signal, sample_size=self.sample_size, repetitions=3)

      results.append({
        **params,
        'average_fit': sim_result['average_fit'],
        'fit_std': sim_result['fit_std']
      })

    return pd.DataFrame(results)

  def _modify_signal_with_params(self, signal_data, params):
    modified_data = signal_data.copy()

    scale_factors = []

    for key, value in params.items():
      if key.startswith('A') and key[1:].isdigit():
        signal_idx = int(key[1:]) - 1
        if f'signal_{signal_idx}' in modified_data.columns:
          default_amp = 25 if signal_idx == 1 else 15 if signal_idx == 2 else 2
          scale_factor = value / default_amp
          modified_data[f'signal_{signal_idx}'] = modified_data[f'signal_{signal_idx}'] * scale_factor
          scale_factors.append(scale_factor)

    if scale_factors:
      signal_cols = [col for col in modified_data.columns if col.startswith('signal_')]
      modified_data['total_signal'] = modified_data[signal_cols].sum(axis=1)

    return modified_data

  def logistic_analysis(self, simulation_results):
    if isinstance(simulation_results, pd.DataFrame):
      x_data = simulation_results['sample_size'].values
      y_data = simulation_results['average_fit'].values
    else:
      x_data = np.array(simulation_results['sample_sizes'])
      y_data = np.array(simulation_results['fits'])

    def logistic_function(x, a, b, c):
      return a / (1 + np.exp(-b * (np.log(x) - c)))

    try:
      initial_params = (1.0, 0.4, 60)
      params, covariance = curve_fit( # type: ignore
        logistic_function, x_data, y_data,
        p0=initial_params,
        maxfev=10000
      )

      x_fit = np.linspace(min(x_data), max(x_data), 100)
      y_fit = logistic_function(x_fit, *params)

      return {
        'parameters': params.tolist(),
        'covariance': covariance.tolist(),
        'x_fit': x_fit.tolist(),
        'y_fit': y_fit.tolist(),
        'success': True
      }
    except Exception as e:
      return {
        'parameters': [],
        'covariance': [],
        'x_fit': [],
        'y_fit': [],
        'success': False,
        'error': str(e)
      }

  def find_optimal_sample_size(self, target_fit=0.9, simulation_results=None):
    if simulation_results is None:
      simulation_results = self.run_many_simulations()

    logistic_result = self.logistic_analysis(simulation_results)

    if not logistic_result['success']:
      return None

    a, b, c = logistic_result['parameters']

    def find_x_for_y(y, a, b, c):
      if y >= a or y <= 0:
        return None
      try:
        return float(np.exp(c + np.log(a / y - 1) / b))
      except (ValueError, ZeroDivisionError):
        return None

    optimal_size = find_x_for_y(target_fit, a, b, c)

    return {
      'target_fit': target_fit,
      'optimal_sample_size': optimal_size,
      'logistic_parameters': logistic_result['parameters']
    }

  def get_simulation_statistics(self, simulation_results):
    if isinstance(simulation_results, pd.DataFrame):
      df = simulation_results
    else:
      df = pd.DataFrame(simulation_results)

    stats = {
      'basic_stats': {
        'total_simulations': len(df),
        'mean_fit': float(df['average_fit'].mean()),
        'std_fit': float(df['average_fit'].std()),
        'min_fit': float(df['average_fit'].min()),
        'max_fit': float(df['average_fit'].max()),
        'median_fit': float(df['average_fit'].median())
      },
      'sample_size_analysis': {
        'min_sample_size': int(df['sample_size'].min()),
        'max_sample_size': int(df['sample_size'].max()),
        'optimal_sample_size': self.find_optimal_sample_size()
      },
      'correlation_analysis': {
        'fit_sample_correlation': float(df['average_fit'].corr(df['sample_size']))
      }
    }

    return stats

  def set_sample_size(self, size):
    if not isinstance(size, int) or size <= 0:
      raise ValueError("Sample size must be a positive integer")
    self.sample_size = size

  def set_repetitions(self, reps):
    if not isinstance(reps, int) or reps <= 0:
      raise ValueError("Repetitions must be a positive integer")
    self.repetitions = reps

  @property
  def current_config(self):
    return {
      'duration': self.duration,
      'signal_rate': self.signal_rate,
      'sample_size': self.sample_size,
      'repetitions': self.repetitions,
      'sample_range': self.sample_size_range.name,
      'available_ranges': list(self.get_available_size_ranges().keys())
      }

  @property
  def parameter_info(self):
    return {
      param_type: {
          param: values.tolist() for param, values in params.items()
      }
      for param_type, params in self.parameter_ranges.items()
    }

  def update_parameters(self, **kwargs):
    valid_params = ['sample_size', 'repetitions', 'sample_size_range']
    for key, value in kwargs.items():
      if key in valid_params:
        if key == 'sample_size_range':
          self.set_sample_size_range(value)
        elif key == 'sample_size':
          self.set_sample_size(value)
        elif key == 'repetitions':
          self.set_repetitions(value)
      else:
        raise ValueError(f"Invalid parameter: {key}")
