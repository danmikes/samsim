import numpy as np
import plotly.graph_objects as go

def create_logistic_chart(logistic, simulation):
  logistic_fit = logistic['logistic_fit']
  sim_data = logistic['simulation_data']
  target_fit = logistic['target_fit']
  optimal_sample_rate = logistic['optimal_sample_rate']

  fig = go.Figure()

  color = 'rgba(000, 25, 100, 0.8)'
  current_color = 'rgba(255, 200, 0, 0.8)'
  target_color = 'rgba(100, 200, 0, 0.8)'
  curve_color = 'rgba(0, 25, 100, 0.6)'
  point_color = 'rgba(0, 25, 100, 0.8)'

  fig.add_trace(go.Scatter(
    x=sim_data['sample_rate'],
    y=sim_data['average_fit'],
    mode='markers',
    name='Simulation',
    marker=dict(color=point_color, size=8),
    hovertemplate='Samples: %{x}<br>Fit: %{y:.2f}<extra></extra>',
  ))

  fig.add_trace(go.Scatter(
    x=logistic_fit['x_fit'],
    y=logistic_fit['y_fit'],
    mode='lines',
    name='Fit',
    line=dict(color=curve_color, width=3),
    hovertemplate='Samples: %{x:.0f}<br>Fit: %{y:.2f}<extra></extra>',
  ))

  current_sample_rate = simulation['sample_rate']
  current_fit = simulation['fit']

  if logistic_fit['success'] and len(logistic_fit['x_fit']) > 0:
    current_fit = np.interp(current_sample_rate, logistic_fit['x_fit'], logistic_fit['y_fit'])

    fig.add_vline(
      x=current_sample_rate,
      line_dash="dot",
      line_color=current_color,
      line_width=2,
    )

    fig.add_hline(
      y=current_fit,
      line_dash="dot",
      line_color=current_color,
      line_width=2,
    )

  if optimal_sample_rate is not None and logistic_fit['success']:
    fig.add_vline(
      x=optimal_sample_rate,
      line_dash="dot",
      line_color=target_color,
      line_width=2,
    )

    fig.add_hline(
      y=target_fit,
      line_dash="dot",
      line_color=target_color,
      line_width=2,
    )

  fig.add_trace(go.Scatter(
    x=[None],
    y=[None],
    mode='lines',
    name=f'Target({optimal_sample_rate:.0f} {target_fit:.1f})',
    line=dict(color=target_color, dash='dot', width=2),
  ))

  fig.add_trace(go.Scatter(
    x=[None],
    y=[None],
    mode='lines',
    name=f'Current({current_sample_rate:.0f} {current_fit:.1f})',
    line=dict(color=current_color, dash='dot', width=2),
    showlegend=True,
  ))

  fig.update_layout(
    title=dict(
      text=f'Fit',
      x=0.5,
      xanchor='center',
      font=dict(size=16, color=color),
    ),
    xaxis_title='Samples',
    yaxis_title='Fit [-]',
    font=dict(color=color),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    autosize=True,
    margin=dict(l=0, r=0, b=0, t=25, pad=0),
  )

  fig.update_xaxes(
    type='log',
    dtick=1,
    gridcolor='rgba(128,128,128,0.5)',
    range=[0, 3],
    gridwidth=1,
    tickfont=dict(size=10, color=color),
    title_font=dict(size=12),
    minor=dict(
      dtick='D1',
      gridcolor='rgba(128,128,128,0.3)',
      showgrid=True
    ),
    zeroline=True,
    zerolinecolor='rgba(128,128,128,0.5)',
    zerolinewidth=10,
  )

  fig.update_yaxes(
    range=[0, 1.05],
    dtick=1,
    gridcolor='rgba(128,128,128,0.3)',
    tickfont=dict(size=10, color=color),
    title_font=dict(size=12),
    minor=dict(
      dtick=0.1,
      gridcolor='rgba(128,128,128,0.3)',
      showgrid=True
    ),
    zerolinecolor='rgba(128,128,128,0.5)',
  )

  fig.add_vline(
    x=1,
    line_dash="solid",
    line_color="rgba(128,128,128,0.5)",
    line_width=2,
  )

  fig.add_vline(
    x=1000,
    line_dash="solid",
    line_color="rgba(128,128,128,0.5)",
    line_width=2,
  )

  fig.add_hline(
    y=1,
    line_dash="solid",
    line_color="rgba(128,128,128,0.5)",
    line_width=2,
  )

  return fig.to_html()

def create_empty_logistic_chart(message):
  fig = go.Figure()
  fig.add_annotation(
    text=message,
    xref="paper",
    yref="paper",
    x=0.5,
    y=0.5,
    showarrow=False,
    font=dict(size=16),
  )

  fig.update_layout(
    title='Logistic Analysis',
    xaxis_title='Sample Size [-]',
    yaxis_title='Fit',
    template='plotly_white',
    height=400,
  )
  return fig.to_html()
