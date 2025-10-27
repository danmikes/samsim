def create_simulation_chart(simulation, insolation):
  sample = simulation

  chart_data = {
    'time': [t / 1e6 for t in insolation['time']],
    'datasets': []
  }

  signals = {
    'total_signal': {
      'border_width': 2,
      'color': 'rgba(255,0,255,0.4)',
      'name': 'Sᵀ',
      'point_radius': 0,
      'source': insolation,
      'time_source': 'common',
    },
    'sampled_signal': {
      'border_width': 2,
      'color': 'rgba(0,255,255,0.4)',
      'name': 'Sᴬ',
      'point_radius': 2,
      'source': sample,
      'time_source': 'sampled_time',
    },
    'simulated_signal': {
      'border_width': 2,
      'color': 'rgba(255,255,0,1)',
      'name': 'Sᴮ',
      'point_radius': 2,
      'source': sample,
      'time_source': 'simulated_time',
    }
  }

  for col, style in signals.items():
    if col in style['source']:
      if style['time_source'] == 'common':
        time_data = chart_data['time']
      else:
        time_data = [t / 1e6 for t in sample[style['time_source']]]

    dataset = {
      'backgroundColor': style['color'] + '20',
      'borderColor': style['color'],
      'borderWidth': style['border_width'],
      'data': style['source'][col],
      'label': style['name'],
      'pointRadius': style['point_radius'],
      'time': time_data,
    }

    if style['point_radius'] > 0:
      dataset.update({
        'pointBackgroundColor': style['color'],
        'pointBorderColor': style['color'],
      })

    chart_data['datasets'].append(dataset)

  return chart_data
