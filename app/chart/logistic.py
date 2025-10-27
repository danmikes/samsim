def create_logistic_chart(logistic, simulation):
  logistic_fit = logistic['logistic_fit']
  sim_data = logistic['simulation_data']
  target_fit = logistic['target_fit']
  optimal_sample_rate = logistic['optimal_sample_rate']

  chart_data = {
    'simulation': {
      'sample_rates': [item['sample_rate'] for item in sim_data],
      'fits': [item['fit'] for item in sim_data]
    },
    'current': {
      'sample_rate': simulation['sample_rate'],
      'fit': simulation['fit']
    },
    'target': {
      'sample_rate': optimal_sample_rate,
      'fit': target_fit
    }
  }

  if logistic_fit['success'] and logistic_fit['x_fit']:
    chart_data['fit'] = {
      'x': logistic_fit['x_fit'],
      'y': logistic_fit['y_fit']
    }

    chart_data['current']['fit'] = _interpolate_value(
      simulation['sample_rate'],
      logistic_fit['x_fit'],
      logistic_fit['y_fit']
    )

  return chart_data

def _interpolate_value(x, xp, fp):
  if not xp or not fp:
    return 0

  for i in range(len(xp) - 1):
    if xp[i] <= x <= xp[i+1]:
      x0, x1 = xp[i], xp[i+1]
      f0, f1 = fp[i], fp[i+1]
      if x1 == x0:
        return f0
      return f0 + (f1 - f0) * (x - x0) / (x1 - x0)

  if x <= xp[0]:
    return fp[0]
  else:
    return fp[-1]
