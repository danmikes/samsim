#!/usr/bin/env python
# coding: utf-8

# # Simulation

# ## Import

import matplotlib.pyplot as plt
import numpy as np
import time
import warnings
from collections import ChainMap, namedtuple
from functools import lru_cache
from itertools import product
from IPython.display import clear_output
from matplotlib.table import Table
from scipy.optimize import curve_fit

warnings.filterwarnings('ignore', category=RuntimeWarning)


# ## Parameter

'''
Define Parameters and Values

Code sets up various parameters and values for simulation or model. 
Each parameter represents specific aspect of model, such as period, amplitude, modulation, phase, and other simulation parameters.

- Parameters are assigned with values, and these values are formatted for readability.
- Parameters are organised using the namedtuple 'Pars' for better code structure.
- Simulation duration, signal rate, sample rate, and repeat number are defined as constants.

Parameter:
- _T1, _T2, _T3: Periods in millions of years (Ma).
- _A1, _A2, _A3: Amplitudes (unitless).
- _Tm1, _Tm2, _Tm3: Period modulations in millions of years (Ma).
- _Am1, _Am2, _Am3: Amplitude modulations (unitless).
- _p1, _p2, _p3: Phase values in radians.

Constant:
- DUR: Simulation duration in millions of years (Ma).
- SIG: Signal-rate.
- SAM: Sample-rate.
- REP: Repeat number.

Parameters and values are organised into named tuples (PAR1, PAR2, PAR3) for easier access.

Prints parameters and sample rate (SAM) for reference.
'''
def form(val):
  if val >= 1e3:
    return f'{val:.2e}'
  elif val.is_integer():
    return f'{val:.0f}'
  else:
    return f'{val:.2f}'

def print_params(params):
  for param, values in params.items():
    formatted_values = [
      form(val) for val in values
    ]
    print(f'{param}: {formatted_values}')

# Period Ma
_T1 = int(1.0e5)
_T2 = int(4.1e4)
_T3 = int(2.6e4)

# Amplitude -
_A1 = int(2)
_A2 = int(25)
_A3 = int(15)

# Period modulation Ma
_Tm1 = int(_T1 * 5)
_Tm2 = int(_T2 * 5)
_Tm3 = int(_T3 * 5)

# Amplitude modulation -
_Am1 = int(_A1 / 2)
_Am2 = int(_A2 / 2)
_Am3 = int(_A3 / 2)

# Phase radian
_p1 = int(0)
_p2 = int(0)
_p3 = int(0)

# Other
DUR = int(1e6) # duration Ma
SIG = int(1e3) # signal-rate
SAM = int(1e2) # sample-rate
REP = int(1e1) # repeat

Par = namedtuple('Pars', ['T', 'A', 'Tm', 'Am', 'p'])
PAR1 = Par(_T1, _A1, _Tm1, _Am1, 0)
PAR2 = Par(_T2, _A2, _Tm2, _Am2, 0)
PAR3 = Par(_T3, _A3, _Tm3, _Am3, 0)
PARS = PAR1, PAR2, PAR3

print(PARS)
print(SAM)


# ## Range

'''
Generate Parameter Ranges and Values

Code generates various parameter ranges and values used for simulation or model.
Parameters represent different aspects of model, and they are organised into named dictionaries for easier access.

- _SAM_SHORT_ and _SAM_LONG_ are arrays of sample rates.
- Functions like create_range, ranges, and ranges(*args) are used to create dictionaries of parameter ranges.
- Parameters like T, A, Tm, Am, and p are organised into named dictionaries with different prefixes.

Generated Parameter Dictionary:
- _T_: Period ranges with 'T' prefix.
- _A_: Amplitude ranges with 'A' prefix.
- _Tm_: Period modulation ranges with 'Tm' prefix.
- _Am_: Amplitude modulation ranges with 'Am' prefix.
- _p_: Phase ranges with 'p' prefix.

Sample rates are also organised into dictionaries (SAM_S and SAM_L) and individual variables (_SAM_SHORT_ and _SAM_LONG_).

Prints parameter ranges and values for reference.
'''
_SAM_SHORT_ = 2 ** np.arange(2, 7, 1)
_SAM_LONG_ = 2 ** np.arange(1, 10, 0.5)

def create_range(prefix, values):
  return {f'{prefix}{i}': np.asarray(values) for i in range(1, 4)}

def ranges(*args):
  return dict(ChainMap(*args))

T = create_range('T', 2. ** np.arange(2, 5) * 1e4)
A = create_range('A', np.arange(0, 26, 5))
Tm = create_range('Tm', 2. ** np.arange(0, 3) * 1e5)
Am = create_range('Am', np.arange(0, 13, 2.5))
p = create_range('p', 2. ** np.arange(-3, -1) * np.pi)

SAM_S = {'sam': _SAM_SHORT_}
SAM_L = {'sam': _SAM_LONG_}

_T_ = ranges(T, SAM_L)
_A_ = ranges(A, SAM_L)
_Tm_ = ranges(Tm, SAM_L)
_Am_ = ranges(Am, SAM_L)
_p_ = ranges(p, SAM_L)
_X_ = ranges(T, A, Tm, Am, SAM_S)
_SAM_S_ = _SAM_SHORT_
_SAM_L_ = _SAM_LONG_

print_params(_A_)


# ## Scenario

'''
Edit Amplitude or Modulation | Generate Parameter Sets

Code defines functions to generate different parameter sets for simulation or model.
These functions allow one to edit amplitude (A) or modulation (Tm and Am) of specific parameters.

Function:
- `base(A1=_A1, A2=_A2, A3=_A3)`: Edit amplitude with no modulation.
- `fullA(A1=_A1, A2=_A2, A3=_A3)`: Edit amplitude with default modulation.
- `fullM(Tm1=_Tm1, Tm2=_Tm2, Tm3=_Tm3, Am1=_Am1, Am2=_Am2, Am3=_Am3)`: Edit modulation with specified Tm and Am values.
- `fullX(T1=_T1, T2=_T2, T3=_T3, A1=_A1, A2=_A2, A3=_A3, Tm1=_Tm1, Tm2=_Tm2, Tm3=_Tm3, Am1=_Am1, Am2=_Am2, Am3=_Am3, p1=_p1, p2=_p2, p3=_p3)`: Edit all parameters, including amplitude, modulation, and phase.
- `full()`: Use default values for all parameters.

These functions return sets of parameters represented as tuples of named tuples (Par), each specifying different combinations of period (T), amplitude (A), period modulation (Tm), amplitude modulation (Am), and phase (p).

Example:
Parameter sets.

Prints example parameter set (par8) for reference.
'''
# (edit amplitude) | no modulation
def base(A1=_A1, A2=_A2, A3=_A3):
  return tuple(Par(T, A, 1, 0, 0) for T, A in zip([_T1, _T2, _T3], [A1, A2, A3]))

# (edit amplitude) | default modulation
def fullA(A1=_A1, A2=_A2, A3=_A3):
  return tuple(Par(T, A, Tm, Am, 0) for T, A, Tm, Am in zip([_T1, _T2, _T3], [A1, A2, A3], [_Tm1, _Tm2, _Tm3], [_Am1, _Am2, _Am3]))

# (edit modulation) # Tm Am
def fullM(Tm1=_Tm1, Tm2=_Tm2, Tm3=_Tm3, Am1=_Am1, Am2=_Am2, Am3=_Am3):
  return tuple(Par(T, A, Tm, Am, 0) for T, A, Tm, Am in zip([_T1, _T2, _T3], [_A1, _A2, _A3], [Tm1, Tm2, Tm3], [Am1, Am2, Am3]))

# (edit all) # X
def fullX(T1=_T1, T2=_T2, T3=_T3, A1=_A1, A2=_A2, A3=_A3, Tm1=_Tm1, Tm2=_Tm2, Tm3=_Tm3, Am1=_Am1, Am2=_Am2, Am3=_Am3, p1=_p1, p2=_p2, p3=_p3):
  return tuple(Par(T, A, Tm, Am, p) for T, A, Tm, Am, p in zip([T1, T2, T3], [A1, A2, A3], [Tm1, Tm2, Tm3], [Am1, Am2, Am3], [p1, p2, p3]))

# default all # -
def full():
  return PARS

# Examples
par1 = base()
par2 = base(1, 2, 3)
par3 = fullA()
par4 = fullA(1, 2, 3)
par5 = fullM()
par6 = fullM(1e6, 1e5, 1e4, 1, 2, 3)
par7 = fullX()
par8 = fullX(T1=2e5, A1=8, p1=np.pi/2)

print(par8)


# ## Insolation

'''
Simulating Insolation Time Series

Code defines functions and example to simulate insolation time series.
Insolation represents amount of solar radiation received as function of time.
Code combines sine and cosine functions to generate insolation signal.

Function:
1. `sine(A, T, t, p=0)`: Generates sine wave with amplitude (A), period (T), phase (p), and time (t).
2. `cosine(Am, Tm, t, p=0)`: Generates cosine wave with modulated amplitude (Am), modulated period (Tm), phase (p), and time values (t).
3. `run_ins(par1=PAR1, par2=PAR2, par3=PAR3)`: Simulates insolation time series for many parameter sets. It modulates amplitude and combines three sine waves for different parameter sets. Function returns time values (t), and corresponding insolation values for each parameter set (s1, s2, s3) as well as their sum (s).

Example:
Provides example of running `run_ins` function with default or specified parameters. It plots insolation time series and its components (s1, s2, s3) for visual inspection.
'''
def sine(A, T, t, p=0):
  return A * np.sin(2 * np.pi * 1/T * t + p)

def cosine(Am, Tm, t, p=0):
  return Am * np.cos(2 * np.pi * 1/Tm * t + p)

def run_ins(par1=PAR1, par2=PAR2, par3=PAR3):
  # Generate Time Series
  t = np.linspace(0, DUR, SIG)
  pars = [par1, par2, par3]
  A = [p.A + cosine(p.Am, p.Tm, t)]

  # Modulate Amplitude
  A = [p.A + cosine(p.Am, p.Tm, t) for p in pars]
  signals = [sine(a, p.T, t) for a, p in zip(A, pars)]
  s = sum(signals)

  return t, *signals, s


# ## Simulation

'''
Signal Comparison and Simulation

Code performs comparison between signal and simulated signal and visualises results.

Function:
- `cross(signal)`: Calculates number of zero-crossings in given signal, which is measure of oscillations or periods.
- `compare(signal, sample)`: Computes similarity by dividing number of zero-crossings in sample by number of zero-crossings in original signal. This measure provides indication of how well sample replicates signal characteristics.
- `run_sim(signal, sam=SAM)`: Simulates process of randomly selecting samples from signal and linearly interpolating them to match signal length. It calculates similarity between original signal and simulated signal using `compare` function. Result is averaged fit value.

Example:
Demonstrates process by comparing original signal (`signal`) with simulated signal (`sim_x`). Visualises comparison by plotting both signals along with original signal.
'''
def cross(signal):
  centered = signal - np.mean(signal)
  return np.sum(np.diff(np.sign(centered)) != 0)

def compare(signal, sample):
  fit = cross(sample) / cross(signal)
  return fit

def run_sim(t, signal, sam=SAM):
  total_fit = 0.0
  # Pre-allocate arrays
  sim_t = np.linspace(0, DUR, sam)
  last_sam_i = last_sam_y = last_sim_x = None
  
  for _ in range(REP):
    sam_i = np.sort(np.random.choice(len(signal), sam, replace=False))
    sam_y = signal[sam_i]
    sim_x = np.interp(t, sim_t, sam_y)
    total_fit += compare(signal, sim_x)
    last_sam_i, last_sam_y, last_sim_x = sam_i, sam_y, sim_x
  
  return t[last_sam_i], last_sam_y, sim_t, last_sim_x, total_fit / REP


# ## Simulations

'''
Run Simulations

Code defines function for running simulations with varying sample sizes to assess quality of sample data compared to original signal.

Function:
- `run_sims(signal, dur=DUR, sig=SIG, rep=REP)`: Performs many simulations with different sample sizes and records fit.

Function runs simulations using following parameters:
- `signal`: Original signal to compare with samples.
- `dur`: Duration of signal (default: DUR).
- `sig`: Signal rate (default: SIG).
- `rep`: Number of repetitions for each sample size (default: REP).

Function iterates over set of predefined sample sizes specified in `_SAM_LONG_` array. For each sample size, it performs simulation using `run_sim` function and records fit.
Sample sizes and fit values are then returned.
'''
def run_sims(t, signal):
  sams = []
  fits = []

  for sam in _SAM_LONG_:
    sam = int(sam)

    # Simulate samples
    _, _, _, _, fit = run_sim(t, signal, sam)

    # Append results
    sams.append(sam)
    fits.append(fit)

  return sams, fits


# ## Parameters

'''
Parameter Combination and Signal Simulation

Code contains function for simulating signals with varying parameter combinations and evaluating their fit. It is useful for exploring impact of different parameter settings.

Function:
- `run_params(param_ranges)`: Simulates signals with different parameter combinations defined in `param_ranges` and evaluates their fit. It generates all possible permutations of parameter values, applies these values to signal generation, and calculates fit for each combination.

Example:
- Code allows to vary parameters such as period (T), amplitude (A), period modulation (Tm), amplitude modulation (Am), and phase (p) to study their influence on signal similarity. It provides insights into how different parameter settings affect similarity between signals.
'''

def run_params(param_ranges):
  sams = []
  fits = []
  param_combinations = product(*param_ranges.values())
  
  # Predefine default values
  defaults = {
    'T1': _T1, 'T2': _T2, 'T3': _T3,
    'A1': _A1, 'A2': _A2, 'A3': _A3,
    'Tm1': _Tm1, 'Tm2': _Tm2, 'Tm3': _Tm3,
    'Am1': _Am1, 'Am2': _Am2, 'Am3': _Am3,
    'p1': _p1, 'p2': _p2, 'p3': _p3,
    'sam': SAM
  }
  
  for combination in param_combinations:
    params = defaults.copy()
    # Update with current combination
    for param, value in zip(param_ranges.keys(), combination):
      params[param] = int(value) if param == 'sam' else value
    
    # Generate signals
    pars = fullX(**{k: params[k] for k in ['T1','T2','T3','A1','A2','A3',
                                          'Tm1','Tm2','Tm3','Am1','Am2','Am3',
                                          'p1','p2','p3']})

    t, _, _, _, signal = run_ins(*pars)

    # Simulate samples
    _, _, _, _, fit = run_sim(t, signal, sam)

    # Append results
    sams.append(sam)
    fits.append(fit)

  return sams, fits


# ## Data

'''
Logistic Function and Signal Analysis

Code defines series of functions for performing logistic curve fitting and signal analysis.
It allows to fit logistic function to data, visualise insolation curves, simulate signals, and perform parameter sensitivity analysis.

Function:
- `logistic_function(x, a, b, c)`: Defines logistic function for curve fitting.
- `logistic_fit(x_data, y_data, params, maxfev=1e4)`: Fits logistic function to data and returns fitted parameters.
- `find_x_for_y(y, a, b, c)`: Calculates x-value for given y-value in logistic curve.
- `set_plot_prop(ax, x_scale, y_scale, title, xlim, ylim)`: Sets various properties for plotting including scale, title, and axis limits.
- `insolation(ax, par1, par2, par3)`: Plots insolation curve and composing signals based on provided parameters.
- `simulation(ax, signal, sam)`: Simulates signal and compares it to original signal.
- `simulations(ax, signal)`: Runs simulations with varying sample rates and collects fit values.
- `parameters(ax, _1, _2, _3, param_ranges)`: Performs parameter sensitivity analysis and collects fit values.
- `all(ax, _1, _2, _3, param_ranges, title)`: Similar to 'parameters', but accepts custom title.
- `logistic(ax, x_data, y_data)`: Fits logistic curve to provided data and visualises curve.
'''
def logistic_function(x, a, b, c):
  return a / (1 + np.exp(-b * (np.log(x) - c)))

def logistic_fit(x_data, y_data, params, maxfev=1e4):
  x_tuple = tuple(x_data)
  y_tuple = tuple(y_data)
  params_tuple = tuple(params)
  return curve_fit(logistic_function, x_tuple, y_tuple, params_tuple, maxfev=int(maxfev))

def find_x_for_y(y, a, b, c):
  x = np.exp(c + np.log(a / (1 / y - 1)) / b)
  return x

def set_plot_prop(ax, x_scale, y_scale, x_title, y_title, title, xlim=None, ylim=None):
  ax.set(
    xscale=x_scale, yscale=y_scale,
    xlabel=x_title, ylabel=y_title,
    title=title,
    xlim=xlim if xlim is not None else ax.get_xlim(),
    ylim=ylim if ylim is not None else ax.get_ylim()
  )
  ax.grid(True, which='both', color='#333', alpha=0.7)

def insolation(fig, pars):
  t, s1, s2, s3, s = run_ins(*pars)
  fig.plot(t, s1, color='red', linestyle='-', linewidth=0.6)
  fig.plot(t, s2, color='green', linestyle='-', linewidth=0.6)
  fig.plot(t, s3, color='yellow', linestyle='-', linewidth=0.6)
  fig.plot(t, s, color='cyan')
  set_plot_prop(fig, 'linear', 'linear', 'time [Ma]', 'sea-level [m]', 'Insolation', (0, 1e6))
  return t, s

def simulation(ax, t, signal, sam):
  sam_t, sam_y, sim_t, _, fit = run_sim(t, signal, sam)
  ax.plot(t, signal, color='darkcyan')
  ax.plot(sam_t, sam_y, color='darkmagenta', linestyle='-', linewidth=1, marker='o', markersize='3')
  ax.plot(sim_t, sam_y, color='yellow', marker='o', markersize='3')
  set_plot_prop(ax, 'linear', 'linear', 'time [Ma]', 'sea-level [m]', 'Simulation', (0, 1e6))
  return fit

def simulations(ax, t, signal):
  sams, fits = run_sims(t, signal)
  ax.scatter(sams, fits, s=20, color='darkcyan')
  set_plot_prop(ax, 'log', 'linear', 'samples', 'fit', 'Simulations', (1, 1e3), (0, 1))
  return sams, fits

def parameters(ax, param_ranges):
  sams, fits = run_params(param_ranges)
  ax.scatter(sams, fits, s=5, color='darkcyan')
  set_plot_prop(ax, 'log', 'linear', 'samples', 'fit', 'Parameters', (1, 1e3), (0, 1))
  return sams, fits

def all(ax, param_ranges, title):
  sams, fits = run_params(param_ranges)
  ax.scatter(sams, fits, s=5, color='darkcyan')
  set_plot_prop(ax, 'log', 'linear', 'samples', 'fit', title, (1, 1e3), (0, 1))
  return sams, fits

def logistic(ax, x_data, y_data):
  params = (1, 0.4, 60) # (1.0, 0.4, 60)
  covariance = np.zeros((3, 3))
  params, covariance = logistic_fit(x_data, y_data, params, 1e5)
  x_fit = np.linspace(min(x_data), max(x_data), 100)
  y_fit = logistic_function(x_fit, *params)
  ax.plot(x_fit, y_fit, color='cyan')
  return params, covariance


# ## Table

'''
Text Formatting and Display

Code defines functions for formatting and displaying key information in plot.

Functions:
- `display_tab(ax, params)`: Displays formatted text in table, presenting sample-rate against fit for many values
'''
def display_tab(ax, params):
  y_vals = [0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95]
  x_vals = [find_x_for_y(y, *params) for y in y_vals]

  data = [(x, y) for x, y in zip(x_vals, y_vals)][::-1]

  table_data = [['sam', 'fit']] + [[f'{x:.0f}', f'{y:.2f}'] for x, y in data]

  table = Table(ax, bbox=[0.2, -1.3, 0.4, 2])
  table.auto_set_font_size(False)
  table.set_fontsize(12)
  table.scale(2, 2)

  for i, row in enumerate(table_data):
    for j, cell in enumerate(row):
      table.add_cell(i, j, width=0.2, height=0.2, text=cell, loc='center', facecolor='black', edgecolor='#333')

  ax.add_table(table)
  ax.set_title('Values', fontsize=12, x=0.4, y=0.7)
  ax.axis('off')


# ## Plot Insolation

'''
Plot Insolation

Code defines function for creating plot to visualise insolation data using specified parameter combinations (pars).
Plot provides visual representation of how various parameters impact insolation.

Function:
- `plot_ins(pars=PARS)`: Generates plot of insolation data based on provided parameter combinations.
'''
def plot_ins(pars=PARS):
  # Figure
  plt.close('all')
  fig, ax = plt.subplots(figsize=(20, 2))

  # Data
  insolation(ax, pars)
  plt.show()
  return fig


# ## Plot Simulation

'''
Plot Simulation

Code defines function for creating plot that visualises simulation based on specified parameters.
Simulation involves generating and comparing samples with original signal, helping to assess quality of simulation under various parameter combinations.

Function:
- `plot_sim(sam=SAM, parX=PARS)`: Generates plot of simulation using specified parameters.
'''
def plot_sim(sam=SAM, pars=PARS):
  # Figure
  plt.close('all')
  fig, ax = plt.subplots(figsize=(20, 2))

  # Data
  t, _, _, _, signal = run_ins(*pars)
  simulation(ax, t, signal, sam)

  plt.show()
  return fig


# ## Plot Simulations

'''
Plot Simulations and Analysis

Code defines function for visualising simulation results and performing analysis on sampled data.

Function:
- `plot_sims(sam=SAM, param_ranges=_A_, parX=PARS)`: Generates multi-panel plot to display insolation, simulations, and analysis of sampled data.

Function performs following actions:
1. Sets up multi-panel figure with various subplots using Matplotlib.
2. Generates insolation signal using provided parameters from `parX`.
3. Runs simulations to compare insolation signal with sampled data, recording fit values.
4. Analyses sampled data with different parameter ranges.
5. Performs logistic analysis on simulations and records parameters and covariance.
6. Displays informative text about analysis in fifth subplot.
7. Adds horizontal and vertical lines to highlight average fit and corresponding sample size.
'''
def plot_sims(sam=SAM, param_ranges=_A_, pars=PARS):
  # Figure
  plt.close('all')
  fig = plt.figure(figsize=(20, 6))
  ax1 = plt.subplot2grid((3, 3), (0, 0), colspan=3)
  ax2 = plt.subplot2grid((3, 3), (1, 0), rowspan=2)
  ax3 = plt.subplot2grid((3, 3), (1, 1), rowspan=2)
  ax4 = plt.subplot2grid((3, 3), (1, 2), colspan=2)
  ax4.axis('off')

  # Insolation
  t, _, _, _, signal = run_ins(*pars)

  # Simulation
  fit = simulation(ax1, t, signal, sam)

  # Sampling
  sams_con, fits_con = simulations(ax2, t, signal)

  # Variable
  sams_var, fits_var = parameters(ax3, param_ranges)

  # Logistic
  params, covariance = logistic(ax2, sams_con, fits_con)
  params, covariance = logistic(ax3, sams_con, fits_con)

  # Table
  display_tab(ax4, params)

  # Lines
  y = fit
  x_y = find_x_for_y(y, *params)
  x_x = np.interp(y, fits_con, sams_con)
  ax2.axhline(y=y, color='yellow', linestyle='--', linewidth='1', label=f'Average: {x_y:.2f}')
  ax2.axvline(x=x_x, color='magenta', linestyle='--')

  plt.subplots_adjust(hspace=0.8)

  plt.show()
  return fig


# ## Plot Animation

'''
Update and Display Simulation Plots

Code cell defines functions for updating and displaying simulation plots in dynamic manner.

Function:
- `update_plot(sam, param_ranges)`: Updates and displays simulation plots for given sample size (sam) and parameter ranges (param_ranges).
- `plots_sims(sam_values, param_ranges=_A_)`: Iterates through list of sample sizes (sam_values) and updates simulation plots with different sample sizes.
'''
def update_plot(sam, param_ranges):
  plot_sims(sam, param_ranges)
  clear_output(wait=True)
  time.sleep(0.1)

def plots_sims(sam_values, param_ranges=_A_):
  for sam in sam_values[::-1]:
    update_plot(int(round(sam)), param_ranges)


# ## Plot Parameters

'''
Parameter Exploration Plot

Code defines functions and plots to explore influence of different parameters on insolation simulations.

Function:
- `plot_pars()`: Generates 2x3 grid of subplots for exploring different parameter variations.

The subplots are organised by parameter type, including Period, Amplitude, Default, Period modulation, Amplitude modulation, and Phase.
'''
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

  plt.show()
  return fig


# ## Insolation

'''
Generate and Plot Default Insolation Parameters

Code generates default insolation parameters using `full()` function, and plots insolation curve using `plot_ins()` function.

Function:
- `pars = full()`: Initialises `pars` variable with default insolation parameters using `full()` function. Parameters represent baseline configuration for insolation simulations.
- `plot_ins()`: Generates and displays insolation curve based on default parameters. Resulting plot showcases insolation curve with its characteristic components, including variations in amplitude and phase.
'''
pars = full()
plot_ins()
plt.show()


# ## Simulation

'''
Simulate and Plot Insolation with Variable Sampling

Code simulates and plots insolation curve with variable sampling settings.

Function:
- `pars = full()`: Initialises `pars` variable with default insolation parameters using `full()` function, representing baseline configuration.
- `sam = 65`: Sets sample-rate to 65, approximate mid-way point on logistic curve.
- `plot_sim(sam, pars)`: Simulates and plots insolation curve with specified sample-rate and given parameters.
'''
pars = full()
sam = 65
plot_sim(sam, pars)
plt.show()


# ## Simulations

'''
Signal Sampling, Parameter Exploration, and Logistic Curve Fitting

Code combines various processes, including signal sampling, parameter exploration, and logistic curve fitting.

Function:
- `plot_sims(sam, param_ranges=_A_, parX=PARS)`: `plot_sims` function generates multi-plot figure to illustrate different aspects of signal analysis. It performs following steps:
  - Insolation: Generates and displays original signal.
  - Simulation: Generates simulated signal and visualises its fit to original signal.
  - Sampling: Function `simulations` explores how varying number of samples affects fit to original signal and displayes results in scatter plot.
  - Variable: Function `parameters` explores effect of varying multiple parameters on fit and visualises results in scatter plot.
  - Logistic: Applies logistic curve fitting to sampling and variable results and displays fitted curves.
  - Text Information: Provides textual information on analysis.
  - Lines: Adds Vertical and horizontal lines for specific fit values and corresponding parameters.

- `update_plot(sam, param_ranges)`: Updates multi-plot figure to reflect changes in number of samples (sam) and parameter ranges.

- `plots_sims(sam_values, param_ranges=_A_)`: Iterates through range of sample values (sam_values) and updates figure for each value.

- `func_lin(ax, params, lines, x_vals, y_vals)`: Adds horizontal and vertical lines for specific values.

- `func_par(axes, variables, lines)`: Generates plots for different parameter variations, including period, amplitude, default parameters, period modulation, amplitude modulation, and phase.

- `plot_pars()`: Creates multi-plot figure to explore impact of various parameters on fit.
'''
pars = _A_
sam = 65
plot_sims(sam, pars)
plt.show()
plt.savefig('fig3.png')


# ## Animation

'''
Signal Analysis and Visualisation - Parameter Exploration

Code focuses on analysing and visualising signal under different conditions, primarily by exploring effect of parameter variations on signal analysis.

Function:
- `pars = _A_`: Sets variable `pars` to predefined set of parameters defined in `_A_` variable. These parameters represent initial conditions.

- `sams = _SAM_L_`: Sets variable `sams` to list of sample values defined in `_SAM_L_` variable. These sample values represent different sample sizes.

- `plots_sims(sams, pars)`: Creates multi-plot figure that provides insights into how different sample sizes (defined in `sams`) affect analysis. Following aspects are explored:
  - Insolation: Generates and displays original signal.
  - Simulation: Generates simulated signal and visualises fit to original signal.
  - Sampling: Explores how varying number of samples affects fit to original signal and displays results in scatter plot.
  - Variable: Visualises effect of varying many parameters on fit.
  - Logistic: Applies logistic curve fitting to sampling and variable results, and displays fitted curves.
  - Text Information: Provides textual information on analysis.

- `sam = 65`: Sets sample size to 65.

- `plot_sims(sam, pars)`: Generates multi-plot figure with detailed analysis of signal for chosen sample size and parameter values.

- `plt.show()`: Displays generated figures.
'''
pars = _A_
sams = _SAM_L_
plots_sims(sams, pars)

sam = 65
plot_sims(sam, pars)
plt.show()


# ## Parameters

'''
Parameter Analysis and Visualisation

Code focuses on analysis and visualisation of parameters used in signal analysis.
It explores how changes in specific parameters affect fit of signal and provides visual representations of effects.

Function:
- `plot_pars()`: Creates multi-plot figure that analyses and visualises impact of parameter variations on signal fitting.
Following aspects are explored for different parameter types:
  - Period: Variations in signal period (T) and its effect on fit.
  - Amplitude: Variations in signal amplitudes (A) and their impact on fitting.
  - Default: Analysis of default parameters (SAM_L) and their effect on signal fitting.
  - Period Modulation: Exploration of effect of period modulation (Tm) on fitting.
  - Amplitude Modulation: Analysis of amplitude modulation (Am) and its impact on signal fitting.
  - Phase: Effect of phase (p) on signal fitting.
  - Logistic: logistic curve fitting to results.
  - Text Information: Textual information on analysis.

- `plt.show()`: Displays generated figures.
'''
plot_pars()
plt.show()

