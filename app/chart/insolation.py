def create_insolation_chart(insolation):
  time_millions = [t / 1e6 for t in insolation['time']]

  signals = {
    'signal_0': {'name': 'S₁', 'color': 'rgba(255,0,0,0.4)'},
    'signal_1': {'name': 'S₂', 'color': 'rgba(0,255,0,0.4)'},
    'signal_2': {'name': 'S₃', 'color': 'rgba(0,0,255,0.4)'},
    'total_signal': {'name': 'Sᵀ', 'color': 'rgba(255,0,255,1)'}
  }

  chart_data = {
    'time': time_millions,
    'datasets': []
  }

  for col, style in signals.items():
    if col in insolation:
      chart_data['datasets'].append({
        'label': style['name'],
        'data': insolation[col],
        'borderColor': style['color'],
        'backgroundColor': style['color'] + '20',
        'borderWidth': 2 if col == 'total_signal' else 1.5,
        'pointRadius': 0,
        'fill': False
      })

  return chart_data
