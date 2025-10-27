import numpy as np
import plotly.graph_objects as go

def create_simulation_chart(simulation, insolation):
  sample = simulation

  fig = go.Figure()

  signals = {
    'total_signal': {'name': 'S<sub>T</sub>', 'color': 'rgba(255, 000, 255, 0.4)', 'width': 3},
  }

  samples = {
    'sampled_signal': {'name': 'S<sub>A</sub>', 'color': 'rgba(000, 255, 255, 0.4)', 'width': 3},
    'simulated_signal': {'name': 'S<sub>B</sub>', 'color': 'rgba(255, 255, 000, 1)', 'width': 4},
  }

  color = 'rgba(000, 25, 100, 0.8)'

  for col, style in signals.items():
    fig.add_trace(go.Scatter(
      x=insolation['time'] / 1e6,
      y=insolation[col],
      name=style['name'],
      line=dict(color=style['color'], width=style['width']),
      hovertemplate='Time: %{x:.2f} Ma<br>Value: %{y:.2f}<extra></extra>',
    )
  )

  for col, style in samples.items():
    fig.add_trace(go.Scatter(
      x=(insolation['time'] if col == 'simulated_signal' else np.array(sample['sampled_time'])) / 1e6,
      y=sample[col],
      name=style['name'],
      line=dict(color=style['color'], width=style['width']),
      hovertemplate='Time: %{x:.2f} Ma<br>Value: %{y:.2f}<extra></extra>',
    )
  )

  fig.update_layout(
    title=dict(
      text=f'Simulation',
      x=0.5,
      xanchor='center',
      font=dict(size=16, color=color),
    ),
    xaxis_title='Time [Ma]',
    yaxis_title='Amplitude [m]',
    font=dict(color=color),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    autosize=True,
    height=None,
    width=None,
    margin=dict(l=0, r=0, b=0, t=25, pad=0),
  )

  fig.update_xaxes(
    dtick=0.1,
    tick0=0,
    minor=dict(
      dtick=0.02,
      ticklen=0,
      gridcolor='rgba(128,128,128,0.2)',
    ),
    gridcolor='rgba(128,128,128,0.5)',
    gridwidth=1,
    tickfont=dict(size=10, color=color),
    title_font=dict(size=12),
    zerolinecolor='rgba(128,128,128,0.5)',
  )

  fig.update_yaxes(
    dtick=50,
    minor=dict(
      dtick=25,
      ticklen=0,
      gridcolor='rgba(128,128,128,0.2)',
    ),
    gridcolor='rgba(128,128,128,0.5)',
    tickfont=dict(size=10, color=color),
    title_font=dict(size=12),
    zerolinecolor='rgba(128,128,128,0.5)',
  )

  return fig.to_html()
