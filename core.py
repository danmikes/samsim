import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys
from collections import namedtuple
from itertools import product
from matplotlib.table import Table
from scipy.optimize import curve_fit

plt.style.use('dark_background')
DARK_COLORS = {
  'red': '#ff6b6b', 'green': '#51cf66', 'yellow': '#ffd43b', 'cyan': '#22b8cf',
  'magenta': '#cc5de8', 'darkcyan': '#20c997', 'darkmagenta': '#be4bdb',
  'white': '#f8f9fa', 'grid': '#495057', 'background': '#212529'
}

_T1, _T2, _T3 = 100000, 41000, 26000
_A1, _A2, _A3 = 2, 25, 15
_Tm1, _Tm2, _Tm3 = _T1 * 5, _T2 * 5, _T3 * 5
_Am1, _Am2, _Am3 = _A1 // 2, _A2 // 2, _A3 // 2
_p1, _p2, _p3 = 0, 0, 0

DUR, SIG, SAM, REP = 1000000, 1000, 100, 10

Par = namedtuple('Pars', ['T', 'A', 'Tm', 'Am', 'p'])
PARS = PAR1, PAR2, PAR3 = (
  Par(_T1, _A1, _Tm1, _Am1, _p1),
  Par(_T2, _A2, _Tm2, _Am2, _p2), 
  Par(_T3, _A3, _Tm3, _Am3, _p3)
)

def create_range(prefix, values):
  return {f'{prefix}{i}': np.asarray(values) for i in (1, 2, 3)}

T = create_range('T', 2. ** np.arange(2, 5) * 1e4)
A = create_range('A', np.arange(0, 26, 5))
Tm = create_range('Tm', 2. ** np.arange(0, 3) * 1e5)
Am = create_range('Am', np.arange(0, 13, 2.5))
p = create_range('p', 2. ** np.arange(-3, -1) * np.pi)

_SAM_X_ = 2 ** np.arange(1, 10, 0.5)
SAM_L = {'sam': _SAM_X_}

_T_, _A_, _Tm_, _Am_, _p_ = (
  d | SAM_L for d in (T, A, Tm, Am, p)
)

def fullX(T1=_T1, T2=_T2, T3=_T3, A1=_A1, A2=_A2, A3=_A3, 
  Tm1=_Tm1, Tm2=_Tm2, Tm3=_Tm3, Am1=_Am1, Am2=_Am2, Am3=_Am3,
  p1=_p1, p2=_p2, p3=_p3):
  Ts, As = [T1, T2, T3], [A1, A2, A3]
  Tms, Ams, ps = [Tm1, Tm2, Tm3], [Am1, Am2, Am3], [p1, p2, p3]
  return tuple(Par(T, A, Tm, Am, p) for T, A, Tm, Am, p in zip(Ts, As, Tms, Ams, ps))

def sine(A, T, t, p=0):
  return A * np.sin(2 * np.pi * 1/T * t + p)

def cosine(Am, Tm, t, p=0):
  return Am * np.cos(2 * np.pi * 1/Tm * t + p)

def run_ins(par1=PAR1, par2=PAR2, par3=PAR3):
  t = np.linspace(0, DUR, SIG)
  pars = [par1, par2, par3]
  A = [p.A + cosine(p.Am, p.Tm, t) for p in pars]
  signals = [sine(a, p.T, t) for a, p in zip(A, pars)]
  return t, *signals, sum(signals)

def cross(signal):
  centered = signal - np.mean(signal)
  return np.sum(np.diff(np.sign(centered)) != 0)

def compare(signal, sample):
  return cross(sample) / cross(signal)

def run_sim(t, signal, sam=SAM):
  total_fit = 0.0
  sim_t = np.linspace(0, DUR, sam)
  last_sam_i = last_sam_y = last_sim_x = None
  
  for _ in range(REP):
    sam_i = np.sort(np.random.choice(len(signal), sam, replace=False))
    sam_y = signal[sam_i]
    sim_x = np.interp(t, sim_t, sam_y)
    total_fit += compare(signal, sim_x)
    last_sam_i, last_sam_y, last_sim_x = sam_i, sam_y, sim_x
  
  return t[last_sam_i], last_sam_y, sim_t, last_sim_x, total_fit / REP

def run_sims(t, signal):
  sams, fits = [], []
  for sam in _SAM_X_:
    _, _, _, _, fit = run_sim(t, signal, int(sam))
    sams.append(sam)
    fits.append(fit)
  return sams, fits

def run_params(param_ranges):
  sams, fits = [], []
  defaults = {
    'T1': _T1, 'T2': _T2, 'T3': _T3, 'A1': _A1, 'A2': _A2, 'A3': _A3,
    'Tm1': _Tm1, 'Tm2': _Tm2, 'Tm3': _Tm3, 'Am1': _Am1, 'Am2': _Am2, 'Am3': _Am3,
    'p1': _p1, 'p2': _p2, 'p3': _p3, 'sam': SAM
  }
  
  for combination in product(*param_ranges.values()):
    params = defaults.copy()
    for param, value in zip(param_ranges.keys(), combination):
      params[param] = int(value) if param == 'sam' else value
    
    pars = fullX(**{k: params[k] for k in ['T1','T2','T3','A1','A2','A3','Tm1','Tm2','Tm3','Am1','Am2','Am3','p1','p2','p3']})
    t, _, _, _, signal = run_ins(*pars)
    _, _, _, _, fit = run_sim(t, signal, params['sam'])
    sams.append(params['sam'])
    fits.append(fit)
  
  return sams, fits

def set_plot_prop(ax, x_scale, y_scale, x_title, y_title, title, xlim=None, ylim=None):
  ax.set_facecolor(DARK_COLORS['background'])
  ax.set(xscale=x_scale, yscale=y_scale, xlabel=x_title, ylabel=y_title, title=title)
  if xlim: ax.set_xlim(xlim)
  if ylim: ax.set_ylim(ylim)
  ax.grid(True, which='both', color='#333', alpha=0.7)

def logistic_function(x, a, b, c):
  exponent = -b * (np.log(x) - c).np.clip(exponent, -700, 700)
  return a / (1 + np.exp(exponent))

def logistic_function(x, a, b, c):
  return a / (1 + np.exp(-b * (np.log(x) - c)))

def logistic_fit(x_data, y_data, params, maxfev=10000):
  return curve_fit(logistic_function, x_data, y_data, params, maxfev=int(maxfev))

def find_x_for_y(y, a, b, c):
  return np.exp(c + np.log(a / (1 / y - 1)) / b)

def plot_ins(pars=PARS):
  fig, ax = plt.subplots(figsize=(20, 2))
  t, s1, s2, s3, s = run_ins(*pars)
  ax.plot(t, s1, color='red', linewidth=0.6)
  ax.plot(t, s2, color='green', linewidth=0.6)
  ax.plot(t, s3, color='yellow', linewidth=0.6)
  ax.plot(t, s, color='cyan')
  set_plot_prop(ax, 'linear', 'linear', 'time [Ma]', 'sea-level [m]', 'Insolation', (0, 1e6))
  return fig

def plot_sim(sam=SAM, pars=PARS):
  fig, ax = plt.subplots(figsize=(20, 2))
  t, _, _, _, signal = run_ins(*pars)
  sam_t, sam_y, sim_t, _, fit = run_sim(t, signal, sam)
  ax.plot(t, signal, color='darkcyan')
  ax.plot(sam_t, sam_y, color='darkmagenta', linewidth=1, marker='o', markersize=3)
  ax.plot(sim_t, sam_y, color='yellow', marker='o', markersize=3)
  set_plot_prop(ax, 'linear', 'linear', 'time [Ma]', 'sea-level [m]', 'Simulation', (0, 1e6))
  return fig

def plot_sims(sam=SAM, param_ranges=_A_, pars=PARS):
  fig = plt.figure(figsize=(20, 6))
  ax1 = plt.subplot2grid((3, 3), (0, 0), colspan=3)
  ax2 = plt.subplot2grid((3, 3), (1, 0), rowspan=2)
  ax3 = plt.subplot2grid((3, 3), (1, 1), rowspan=2)
  ax4 = plt.subplot2grid((3, 3), (1, 2), colspan=2)
  ax4.axis('off')

  t, _, _, _, signal = run_ins(*pars)
  fit = run_sim(t, signal, sam)[-1]
  
  sam_t, sam_y, sim_t, _, _ = run_sim(t, signal, sam)
  ax1.plot(t, signal, color='darkcyan')
  ax1.plot(sam_t, sam_y, color='darkmagenta', linewidth=1, marker='o', markersize=3)
  ax1.plot(sim_t, sam_y, color='yellow', marker='o', markersize=3)
  set_plot_prop(ax1, 'linear', 'linear', 'time [Ma]', 'sea-level [m]', 'Simulation', (0, 1e6))

  sams_con, fits_con = run_sims(t, signal)
  sams_var, fits_var = run_params(param_ranges)
  
  for ax, sams, fits in [(ax2, sams_con, fits_con), (ax3, sams_var, fits_var)]:
    ax.scatter(sams, fits, s=20, color='darkcyan')
    set_plot_prop(ax, 'log', 'linear', 'samples', 'fit', 'Simulations', (1, 1e3), (0, 1))
    params, _ = logistic_fit(sams, fits, (1, 0.4, 60), 1e5)
    x_fit = np.linspace(min(sams), max(sams), 100)
    ax.plot(x_fit, logistic_function(x_fit, *params), color='cyan')

  params, _ = logistic_fit(sams_con, fits_con, (1, 0.4, 60), 1e5)

  y = fit
  x_y = find_x_for_y(y, *params)
  x_x = np.interp(y, fits_con, sams_con)  
  ax2.axhline(y=y, color='yellow', linestyle='--', linewidth=1, label=f'Average: {x_y:.2f}')
  ax2.axvline(x=x_x, color='magenta', linestyle='--', linewidth=1)

  y_vals = [0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95]
  data = [[find_x_for_y(y, *params), y] for y in y_vals][::-1]
  
  table = Table(ax4, bbox=[0.15, -2, 0.5, 3])
  table_data = [['sam', 'fit']] + [[f'{x:.0f}', f'{y:.2f}'] for x, y in data]
  
  for i, row in enumerate(table_data):
    for j, cell in enumerate(row):
      table.add_cell(i, j, width=0.1, height=0.2, text=cell, 
        loc='center', facecolor='black', edgecolor='#333')
  
  ax4.add_table(table)
  ax4.set_title('Values', fontsize=12, x=0.4, y=1.1)
  
  plt.subplots_adjust(hspace=0.8)
  return fig

# ToDo : make
def plot_animation(sam=SAM, param_ranges=_A_, pars=PARS):
  return plot_sims(sam, param_ranges, pars)  # Temporary fallback

def plot_pars():
  fig, axes = plt.subplots(2, 3, figsize=(20, 8))
  variables = [
    ('Period', _T_), ('Amplitude', _A_), ('Default', SAM_L),
    ('Period mod', _Tm_), ('Amplitude mod', _Am_), ('Phase', _p_)
  ]
  
  for ax, (title, ranges) in zip(axes.flatten(), variables):
    sams, fits = run_params(ranges)
    ax.scatter(sams, fits, s=5, color='darkcyan')
    set_plot_prop(ax, 'log', 'linear', 'samples', 'fit', title, (1, 1e3), (0, 1))
  
  plt.subplots_adjust(hspace=0.4)
  return fig

def all(ax, param_ranges, title):
  sams, fits = run_params(param_ranges)
  ax.scatter(sams, fits, s=5, color='darkcyan')
  set_plot_prop(ax, 'log', 'linear', 'samples', 'fit', title, (1, 1e3), (0, 1))
  return sams, fits

def logistic(ax, x_data, y_data):
  params = (1, 0.4, 60)
  covariance = np.zeros((3, 3))
  params, covariance = logistic_fit(x_data, y_data, params, 1e5)
  x_fit = np.linspace(min(x_data), max(x_data), 100)
  y_fit = logistic_function(x_fit, *params)
  ax.plot(x_fit, y_fit, color='cyan')
  return params, covariance

def func_par(axes, variables):
  for ax, (title, ranges) in zip(axes, variables):
    sams, fits = all(ax, ranges, title)
    params, _ = logistic(ax, sams, fits)
    set_plot_prop(ax, 'log', 'linear', 'samples', 'fit', title, (1, 1e3), (0, 1))

def plot_pars():
  fig, axes = plt.subplots(2, 3, figsize=(20, 8))
  axes = axes.flatten()

  variables = [
    ('Period', _T_),
    ('Amplitude', _A_),
    ('Default', SAM_L),
    ('Period mod', _Tm_),
    ('Amplitude mod', _Am_),
    ('Phase', _p_),
  ]

  func_par(axes, variables)

  plt.subplots_adjust(hspace=0.4)
  return fig

def reset_params():
  globals().update({
    '_T1': int(1.0e5), '_T2': int(4.1e4), '_T3': int(2.6e4),
    '_A1': int(2), '_A2': int(25), '_A3': int(15),
    '_Tm1': int(_T1 * 5), '_Tm2': int(_T2 * 5), '_Tm3': int(_T3 * 5),
    '_Am1': int(_A1 / 2), '_Am2': int(_A2 / 2), '_Am3': int(_A3 / 2)
  })
  return "Parameters reset to defaults"

def update_params(**kwargs):
  for key, value in kwargs.items():
    if value is not None and hasattr(sys.modules[__name__], f'_{key}'):
      setattr(sys.modules[__name__], f'_{key}', int(value))
  return "Parameters updated"

def get_current_params():
  return {name.strip('_'): getattr(sys.modules[__name__], name) 
    for name in ['_T1','_T2','_T3','_A1','_A2','_A3','_Tm1','_Tm2','_Tm3','_Am1','_Am2','_Am3']}
