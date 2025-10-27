def create_insolation_chart(insolation):
  time_millions = [t / 1e6 for t in insolation['time']]

  signals = {
    'signal_0': {
      'border_width': 1.5,
      'color': 'rgb(255,0,0,0.4)',
      'name': 'S₁',
      'point_radius': 0,
    },
    'signal_1': {
      'border_width': 1.5,
      'color': 'rgb(0,255,0,0.4)',
      'name': 'S₂',
      'point_radius': 0,
    },
    'signal_2': {
      'border_width': 1.5,
      'color': 'rgb(0,0,255,0.4)',
      'name': 'S₃',
      'point_radius': 0,
    },
    'total_signal': {
      'border_width': 2,
      'color': 'rgb(255,0,255,1)',
      'name': 'Sᵀ',
      'point_radius': 0,
    }
  }

  chart_data = {
    'time': time_millions,
    'datasets': []
  }

  for col, style in signals.items():
    if col in insolation:
      chart_data['datasets'].append({
        'backgroundColor': style['color'] + '20',
        'borderColor': style['color'],
        'borderWidth': style['border_width'],
        'data': insolation[col],
        'label': style['name'],
        'pointRadius': style['point_radius'],
      })

  return chart_data
