from functools import lru_cache
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.special import expit
from app.config import Config
from app.service.simulation_service import SimulationService

class LogisticService:
  @lru_cache(maxsize=1)
  def run_logistic(self):
    simulation_service = SimulationService()
    simulations = simulation_service.run_many_simulations()
    target_fit = Config.sim.sim.target_fit

    logistic_result = self.logistic_analysis(simulations)
    optimal_size = self.find_optimal_sample_rate(
      target_fit=target_fit,
      simulation_results=simulations
    )

    return {
      'simulation_data': simulations.to_dict('list') if isinstance(simulations, pd.DataFrame) else simulations,
      'logistic_fit': logistic_result,
      'optimal_sample_rate': optimal_size,
      'target_fit': target_fit
    }

  def logistic_analysis(self, simulation_results):
    if isinstance(simulation_results, pd.DataFrame):
      x_data = simulation_results['sample_rate'].values
      y_data = simulation_results['average_fit'].values
    else:
      x_data = np.array(simulation_results['sample_rate'])
      y_data = np.array(simulation_results['fits'])

    def safe_sigmoid(x, a, b, c):
      x_safe = np.maximum(x, 1e-10)
      z = -b * (np.log(x_safe) - c)
      return a * expit(z)

    try:
      params, _ = curve_fit(safe_sigmoid, x_data, y_data, maxfev=10000) # type: ignore

      x_fit = np.linspace(min(x_data), max(x_data), 100)
      y_fit = safe_sigmoid(x_fit, *params)

      return {
        'parameters': params.tolist(),
        'covariance': [],
        'x_fit': x_fit.tolist(),
        'y_fit': y_fit.tolist(),
        'success': True,
        'original_x': x_data.tolist(),
        'original_y': y_data.tolist()
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

  def find_optimal_sample_rate(self, target_fit=0.9, simulation_results=None):
    if simulation_results is None:
      logistic_data = self.run_logistic()
      simulation_results = logistic_data['simulation_data']

    logistic_result = self.logistic_analysis(simulation_results)

    if not logistic_result['success']:
      return None

    a, b, c = logistic_result['parameters']
    return self._find_x_for_y(target_fit, a, b, c)

  def _find_x_for_y(self, y, a, b, c):
    if y >= a or y <= 0:
      return None
    try:
      if abs(b) < 1e-10:
        return None
      if a / y - 1 <= 0:
        return None

      result = float(np.exp(c + np.log(a / y - 1) / b))
      if result <= 0 or result > 1e6:
        return None
      return result
    except (ValueError, ZeroDivisionError, RuntimeWarning):
      return None

  def get_logistic_statistics(self, logistic_data):
    if not logistic_data['logistic_fit']['success']:
      return {'error': 'Logistic fit failed'}

    sim_data = logistic_data['simulation_data']
    logistic_fit = logistic_data['logistic_fit']

    return {
      'optimal_sample_rate': logistic_data['optimal_sample_rate'],
      'target_fit': logistic_data['target_fit'],
      'parameters': {
        'a': logistic_fit['parameters'][0],
        'b': logistic_fit['parameters'][1],
        'c': logistic_fit['parameters'][2]
      },
      'fit_range': {
        'min_fit': min(sim_data['average_fit']),
        'max_fit': max(sim_data['average_fit']),
        'min_samples': min(sim_data['sample_rate']),
        'max_samples': max(sim_data['sample_rate'])
      }
    }

  def clear_cache(self):
    self.run_logistic.cache_clear()
