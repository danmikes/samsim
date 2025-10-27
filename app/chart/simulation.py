def create_simulation_chart(simulation, insolation):
  sample = simulation

  chart_data = {
    'time': [t / 1e6 for t in insolation['time']],
    'signals': {},
    'samples': {}
  }

  signals = {
    'total_signal': {'name': 'Sᵀ', 'color': 'rgba(255,0,255,0.4)'}
  }

  samples = {
    'sampled_signal': {'name': 'Sᴬ', 'color': 'rgba(0,255,255,0.4)'},
    'simulated_signal': {'name': 'Sᴮ', 'color': 'rgba(255,255,0,1)'}
  }

  for col, style in signals.items():
    chart_data['signals'][col] = {
      'name': style['name'],
      'color': style['color'],
      'data': insolation[col]
    }

  for col, style in samples.items():
    if col == 'simulated_signal':
      x_data = chart_data['time']
    else:
      x_data = [t / 1e6 for t in sample['sampled_time']]

    chart_data['samples'][col] = {
      'name': style['name'],
      'color': style['color'],
      'time': x_data,
      'data': sample[col]
    }

  return chart_data
