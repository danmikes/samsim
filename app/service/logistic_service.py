from functools import lru_cache
import math
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
      'simulation_data': simulations,
      'logistic_fit': logistic_result,
      'optimal_sample_rate': optimal_size,
      'target_fit': target_fit
    }

  def logistic_analysis(self, simulation_results):
    if isinstance(simulation_results, list):
      x_data = [item['sample_rate'] for item in simulation_results]
      y_data = [item['fit'] for item in simulation_results]
    else:
      return {
        'parameters': [],
        'covariance': [],
        'x_fit': [],
        'y_fit': [],
        'success': False,
        'error': 'Unknown data format'
      }

    def safe_sigmoid(x, a, b, c):
      def sigmoid(z):
        if z > 0:
          return 1.0 / (1.0 + math.exp(-z))
        else:
          exp_z = math.exp(z)
          return exp_z / (1.0 + exp_z)

      x_safe = max(x, 1e-10)
      z = b * (math.log(x_safe) - c)
      z = max(min(z, 100), -100)
      return a * sigmoid(z)

    try:
      params = self._estimate_parameters(x_data, y_data)
      x_min, x_max = min(x_data), max(x_data)
      x_fit = self._linspace(x_min, x_max, 100)
      y_fit = [safe_sigmoid(x, *params) for x in x_fit]

      if max(y_fit) < 0.1:
        return {
          'parameters': [],
          'covariance': [],
          'x_fit': [],
          'y_fit': [],
          'success': False,
          'error': 'Poor fit quality'
        }

      return {
        'parameters': params,
        'covariance': [],
        'x_fit': x_fit,
        'y_fit': y_fit,
        'success': True,
        'original_x': x_data,
        'original_y': y_data
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

  def _estimate_parameters(self, x_data, y_data):
    if not x_data or not y_data:
      return [1.0, 1.0, 0]

    sorted_data = sorted(zip(x_data, y_data), key=lambda item: item[0])
    x_data = [item[0] for item in sorted_data]
    y_data = [item[1] for item in sorted_data]

    a_est = max(y_data)
    target_mid = a_est / 2

    closest_idx = min(range(len(y_data)), key=lambda i: abs(y_data[i] - target_mid))
    mid_x = x_data[closest_idx]

    c_est = math.log(mid_x) if mid_x > 0 else 0
    b_est = 2.0

    return [a_est, b_est, c_est]

  def _linspace(self, start, stop, num):
    if num == 1:
      return [start]
    step = (stop - start) / (num - 1)
    return [start + i * step for i in range(num)]

  def find_optimal_sample_rate(self, target_fit=0.9, simulation_results=None):
    if simulation_results is None:
      logistic_data = self.run_logistic()
      simulation_results = logistic_data['simulation_data']

    logistic_result = self.logistic_analysis(simulation_results)

    if not logistic_result['success']:
      return None

    params = logistic_result['parameters']
    if len(params) != 3:
      return None

    a, b, c = params
    return self._find_x_for_y(target_fit, a, b, c)

  def _find_x_for_y(self, y, a, b, c):
    if y >= a or y <= 0:
      return None
    try:
      if abs(b) < 1e-10:
        return None
      if a / y - 1 <= 0:
        return None

      result = float(math.exp(c - math.log(a / y - 1) / b))
      if result <= 0 or result > 1e6:
        return None
      return result
    except (ValueError, ZeroDivisionError):
      return None

  def get_logistic_statistics(self, logistic_data):
    if not logistic_data['logistic_fit']['success']:
      return {'error': 'Logistic fit failed'}

    logistic_fit = logistic_data['logistic_fit']

    return {
      'optimal_sample_rate': logistic_data['optimal_sample_rate'],
      'target_fit': logistic_data['target_fit'],
      'parameters': {
        'a': logistic_fit['parameters'][0],
        'b': logistic_fit['parameters'][1],
        'c': logistic_fit['parameters'][2]
      }
    }

  def clear_cache(self):
    self.run_logistic.cache_clear() # type: ignore
