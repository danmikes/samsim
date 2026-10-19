# service
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
    if not simulation_results or not isinstance(simulation_results, list):
      return self._create_error_response('No data or invalid data format')

    try:
      x_data = [item['sample_rate'] for item in simulation_results]
      y_data = [item['fit'] for item in simulation_results]
    except (KeyError, TypeError):
      return self._create_error_response('Invalid data structure - missing required fields')

    # Check if we have valid data points
    if len(x_data) == 0 or len(y_data) == 0:
      return self._create_error_response('No valid data points')

    best_params = self._find_best_logistic(x_data, y_data)

    x_min, x_max = min(x_data), max(x_data)
    x_fit = self._logspace(x_min, x_max, 100)
    y_fit = [self._logistic(x, *best_params) for x in x_fit]

    return {
      'parameters': best_params,
      'x_fit': x_fit,
      'y_fit': y_fit,
      'success': True
    }

  def _logistic(self, x, k, x0):
    if x <= 0:
      return 0.0
    return 1.0 / (1 + math.exp(-k * (math.log(x) - math.log(x0))))

  def _find_best_logistic(self, x_data, y_data):
    best_error = float('inf')
    best_params = (2.0, sum(x_data) / len(x_data))

    k_options = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
    x0_options = [x for x in x_data]

    for k in k_options:
      for x0 in x0_options:
        error = 0
        for x, y_true in zip(x_data, y_data):
          y_pred = self._logistic(x, k, x0)
          error += (y_true - y_pred) ** 2

        if error < best_error:
          best_error = error
          best_params = (k, x0)

    return best_params

  def _logspace(self, start, stop, num):
    log_start = math.log10(start)
    log_stop = math.log10(stop)
    log_step = (log_stop - log_start) / (num - 1)
    return [10 ** (log_start + i * log_step) for i in range(num)]

  def _create_error_response(self, error_msg):
    return {
      'parameters': [],
      'x_fit': [],
      'y_fit': [],
      'success': False,
      'error': error_msg
    }

  def find_optimal_sample_rate(self, target_fit=0.9, simulation_results=None):
    if simulation_results is None:
      logistic_data = self.run_logistic()
      simulation_results = logistic_data['simulation_data']

    logistic_result = self.logistic_analysis(simulation_results)
    if not logistic_result['success']:
      return None

    k, x0 = logistic_result['parameters']

    try:
      if target_fit <= 0 or target_fit >= 1:
        return None

      ratio = (1.0 / target_fit) - 1.0
      if ratio <= 0:
        return None

      return x0 / (ratio ** (1.0 / k))
    except:
      return None

  def get_logistic_statistics(self, logistic_data):
    if not logistic_data['logistic_fit']['success']:
      return {'error': 'Logistic fit failed'}

    params = logistic_data['logistic_fit']['parameters']
    return {
      'optimal_sample_rate': logistic_data['optimal_sample_rate'],
      'target_fit': logistic_data['target_fit'],
      'parameters': {
        'k': params[0],
        'x0': params[1]
      }
    }

  def clear_cache(self):
    self.run_logistic.cache_clear()
