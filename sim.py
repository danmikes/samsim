# Simulation
## Import
import matplotlib.pyplot as plt
import time
from collections import namedtuple
from itertools import product
from IPython.display import clear_output
from scipy.optimize import curve_fit
## Parameter
'''
Define Parameters and Values

This code block sets up various parameters and values for a simulation or model. Each parameter represents a specific aspect of the model, such as periods, amplitudes, modulation, phase, and other simulation parameters.

- The parameters are assigned with values, and these values are formatted for readability.
- The parameters are organised using the namedtuple 'Pars' for better code structure.
- The simulation duration, signal rate, sample rate, and repeat rate are defined as constants.

Parameters:
- _T1, _T2, _T3: Periods in millions of years (Ma).
- _A1, _A2, _A3: Amplitudes (unitless).
- _Tm1, _Tm2, _Tm3: Period modulations in millions of years (Ma).
- _Am1, _Am2, _Am3: Amplitude modulations (unitless).
- _p1, _p2, _p3: Phase values in radians.

Constants:
- DUR: Simulation duration in millions of years (Ma).
- SIG: Signal-rate.
- SAM: Sample-rate.
- REP: Repeat.

The parameters and values are organised into named tuples (PAR1, PAR2, PAR3) for easier access.

Prints the parameters and the sample rate (SAM) for reference.
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
_A1 = 2
_A2 = 25
_A3 = 15

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
## Range
'''
Generate Parameter Ranges and Values

This code generates various parameter ranges and values used for simulations or models. The parameters represent different aspects of the model, and they are organised into named dictionaries for easier access.

- _SAM_SHORT_ and _SAM_LONG_ are arrays of sample rates.
- Functions like create_range, ranges, and ranges(*args) are used to create dictionaries of parameter ranges.
- Parameters like T, A, Tm, Am, and p are organised into named dictionaries with different prefixes.

Generated Parameter Dictionaries:
- _T_: Period ranges with 'T' prefix.
- _A_: Amplitude ranges with 'A' prefix.
- _Tm_: Period modulation ranges with 'Tm' prefix.
- _Am_: Amplitude modulation ranges with 'Am' prefix.
- _p_: Phase ranges with 'p' prefix.

The sample rates are also organised into dictionaries (SAM_S and SAM_L) and individual variables (_SAM_SHORT_ and _SAM_LONG_).

Prints the parameter ranges and values for reference.
'''
import numpy as np

_SAM_SHORT_ = 2 ** np.arange(2, 7, 1)
_SAM_LONG_ = 2 ** np.arange(1, 10, 0.5)

def create_range(prefix, values):
  return {f'{prefix}{i}': values for i in range(1, 4)}

def ranges(*args):
  result = {}
  for arg in args:
    result.update(arg)
  return result

T = create_range('T', np.arange(1, 3) * 1e5)
A = create_range('A', np.arange(0, 4))
Tm = create_range('Tm', np.arange(4.0, 5.1) * 1e5)
Am = create_range('Am', 2. ** np.arange(-3, -1))
p = create_range('p', 2. ** np.arange(-3, -1) * np.pi)

SAM_S = {'sam': _SAM_SHORT_}
SAM_L = {'sam': _SAM_LONG_}

_T_ = ranges(T, SAM_L)
_A_ = ranges(A, SAM_L)
_Tm_ = ranges(Tm, SAM_L)
_Am_ = ranges(Am, SAM_L)
_p_ = ranges(p, SAM_L)
_TA_ = ranges(T, A, SAM_S)
_AAm_ = ranges(A, Am, SAM_L)
_X_ = ranges(T, A, Tm, Am, SAM_S)
_SAM_S_ = _SAM_SHORT_
_SAM_L_ = _SAM_LONG_

print_params(_X_)
print(type(_SAM_SHORT_))
## Scenario
'''
Edit Amplitude or Modulation | Generate Parameter Sets

This code defines functions to generate different parameter sets for a simulation or model. These functions allow you to edit the amplitude (A) or modulation (Tm and Am) of specific parameters. The available functions are as follows:

- `base(A1=_A1, A2=_A2, A3=_A3)`: Edit amplitude with no modulation.
- `fullA(A1=_A1, A2=_A2, A3=_A3)`: Edit amplitude with default modulation.
- `fullM(Tm1=_Tm1, Tm2=_Tm2, Tm3=_Tm3, Am1=_Am1, Am2=_Am2, Am3=_Am3)`: Edit modulation with specified Tm and Am values.
- `fullX(T1=_T1, T2=_T2, T3=_T3, A1=_A1, A2=_A2, A3=_A3, Tm1=_Tm1, Tm2=_Tm2, Tm3=_Tm3, Am1=_Am1, Am2=_Am2, Am3=_Am3, p1=_p1, p2=_p2, p3=_p3)`: Edit all parameters, including amplitude, modulation, and phase.
- `full()`: Use default values for all parameters.

These functions return sets of parameters represented as tuples of named tuples (Par), each specifying different combinations of period (T), amplitude (A), period modulation (Tm), amplitude modulation (Am), and phase (p).

Examples of generating parameter sets are also provided.

Note: Parameters such as T, A, Tm, Am, and p have specific meanings and units in the context of the simulation or model.

For reference, the code prints an example parameter set (par8).
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
  return PAR1, PAR2, PAR3

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
## Insolation
'''
Simulating Insolation Time Series

This code defines functions and an example to simulate an insolation time series. Insolation represents the amount of solar radiation received at a specific location and time. The code combines sine and cosine functions to generate the insolation signal.

Functions:
1. `sine(A, T, t, p=0)`: Generates a sine wave with amplitude (A), period (T), phase (p), and time values (t).
2. `cosine(Am, Tm, t, p=0)`: Generates a cosine wave with modulated amplitude (Am), modulated period (Tm), phase (p), and time values (t).
3. `run_ins(dur=DUR, sig=SIG, par1=PAR1, par2=PAR2, par3=PAR3)`: Simulates insolation time series for multiple parameter sets. It modulates amplitude and combines three sine waves for different parameter sets. The function returns time values (t), and the corresponding insolation values for each parameter set (s1, s2, s3) as well as their sum (s).

Example:
The code provides an example of running the `run_ins` function with default or specified parameters. It plots the insolation time series and its components (s1, s2, s3) for visual inspection.

This code is useful for simulating insolation time series based on different parameter sets and visualising the resulting signals.
'''
def sine(A, T, t, p=0):
  return A * np.sin(2 * np.pi * 1/T * t + p)

def cosine(Am, Tm, t, p=0):
  return Am * np.cos(2 * np.pi * 1/Tm * t + p)

def run_ins(dur=DUR, sig=SIG, par1=PAR1, par2=PAR2, par3=PAR3):
  # Generate Time Series
  t = np.linspace(0, dur, sig)

  # Modulate Amplitude
  A1 = par1.A + cosine(par1.Am, par1.Tm, t)
  A2 = par2.A + cosine(par2.Am, par2.Tm, t)
  A3 = par3.A + cosine(par3.Am, par3.Tm, t)

  # Calculate sine values for corresponding time values
  s1 = sine(A1, par1.T, t)
  s2 = sine(A2, par2.T, t)
  s3 = sine(A3, par3.T, t)
  s = s1 + s2 + s3

  return t, s1, s2, s3, s

# Example
t, s1, s2, s3, s = run_ins(DUR, SIG, PAR1, PAR2, PAR3)
plt.figure(figsize=(20, 1))
plt.plot(t, s, color='cyan')
plt.plot(t, s1, color='red', linewidth=0.8)
plt.plot(t, s2, color='green', linewidth=0.8)
plt.plot(t, s3, color='yellow', linewidth=0.8)
plt.show()
## Simulation
'''
Signal Comparison and Simulation

This code cell performs a comparison between a signal and a simulated signal and visualises the results.

- `cross(signal)`: The function `cross` calculates the number of zero-crossings in the given signal, which is a measure of oscillations or periods in the signal.
- `compare(signal, sample)`: The `compare` function computes a similarity measure by dividing the number of zero-crossings in the sample by the number of zero-crossings in the original signal. This measure provides an indication of how well the sample replicates the signal's characteristics.
- `run_sim(signal, dur=DUR, sig=SIG, sam=SAM, rep=REP)`: This function simulates the process of randomly selecting samples from the signal and linearly interpolating them to match the signal's length. It calculates the similarity between the original signal and the simulated signal using the `compare` function. The result is an averaged fit value.
- Example: The example code at the end demonstrates the process by comparing an original signal (`signal`) with a simulated signal (`sim_x`). The comparison is visualised by plotting both signals along with the original signal, allowing for a visual assessment of how well the simulation replicates the original signal's characteristics.

The primary purpose of this code cell is to showcase the comparison and simulation process, which can be useful in assessing the accuracy of signal replication and its applicability in various domains such as data analysis and signal processing.
'''
def cross(signal):
  average = np.average(signal)
  return len(np.where(np.diff(np.sign(signal - average)))[0])

def compare(signal, sample):
  fit = cross(sample) / cross(signal)
  return fit

def run_sim(signal, dur=DUR, sig=SIG, sam=SAM, rep=REP):
  fit = 0

  # Create x-axis values for signal
  sig_t = np.linspace(0, dur, sig)

  for _ in range(rep):
    # Randomly select sample indices
    sam_i = np.sort(np.random.choice(len(signal), sam, replace=False))

    # Extract samples from signal
    sam_y = signal[sam_i]

    # Create x-axis values for sim
    sim_t = np.linspace(0, dur, sam)

    # Linearly interpolate samples to match signal lengths
    sim_x = np.interp(sig_t, sim_t, sam_y)

    # Calculate similarity between signal and sim
    fit += compare(signal, sim_x)

  return sig_t, sig_t[sam_i], sam_y, sim_t, sim_x, fit / rep

# Example
t, _, _, _, signal = run_ins(DUR, SIG, PAR1, PAR2, PAR3)
sig_t, sam_t, sam_y, sim_t, _, fit = run_sim(signal, DUR, SIG, SAM, REP)
plt.figure(figsize=(20, 1))
plt.plot(t, signal, color='darkcyan', linewidth=1)
plt.plot(sam_t, sam_y, color='darkmagenta', linewidth=1)
plt.plot(sim_t, sam_y, color='yellow')
plt.show()
## Simulations
'''
Run Simulations

This code cell defines a function for running simulations with varying sample sizes to assess the quality of sample data compared to the original signal.

Function:
- `run_sims(signal, dur=DUR, sig=SIG, rep=REP)`: Performs multiple simulations with different sample sizes and records the fit values for analysis.

The function runs simulations using the following parameters:
- `signal`: The original signal to compare with samples.
- `dur`: Duration of the signal (default: DUR).
- `sig`: Signal rate (default: SIG).
- `rep`: Number of repetitions for each sample size (default: REP).

The function iterates over a set of predefined sample sizes specified in the `_SAM_LONG_` array. For each sample size, it performs a simulation using the `run_sim` function and records the fit value. The sample sizes and fit values are then returned.

This function is useful for understanding how the quality of simulated data changes with different sample sizes and is a valuable tool for sensitivity analysis in simulations.
'''
def run_sims(signal, dur=DUR, sig=SIG, rep=REP):
  sams = []
  fits = []

  for sam in _SAM_LONG_:
    sam = int(sam)

    # Simulate samples
    _, _, _, _, _, fit = run_sim(signal, dur, sig, sam, rep)

    # Append results
    sams.append(sam)
    fits.append(fit)

  return sams, fits
## Parameters
'''
Parameter Combination and Signal Simulation

This code cell contains a function for simulating signals with varying parameter combinations and evaluating their fit values. It is useful for exploring the impact of different parameter settings on signal similarity.

Function:
- `run_params(param_ranges)`: Simulates signals with different parameter combinations defined in `param_ranges` and evaluates their fit scores. It generates all possible permutations of parameter values, applies these values to the signal generation, and calculates the fit score for each combination.

Example:
- The code allows you to vary parameters such as period (T), amplitude (A), period modulation (Tm), amplitude modulation (Am), and phase (p) to study their influence on signal similarity. It provides insights into how different parameter settings affect the similarity between signals.

This code is valuable for parameter sensitivity analysis and understanding the impact of parameter variations on signal characteristics.
'''
def run_params(param_ranges):
  sams = []
  fits = []

  # Generate all permutations of parameters
  param_combinations = list(product(*param_ranges.values()))

  # Iterate over all parameter combinations and perform operations
  for combination in param_combinations:
    # Set variables
    T1, T2, T3, A1, A2, A3, Tm1, Tm2, Tm3, Am1, Am2, Am3, p1, p2, p3, sam = _T1, _T2, _T3, _A1, _A2, _A3, _Tm1, _Tm2, _Tm3, _Am1, _Am2, _Am3, _p1, _p2, _p3, SAM
    param_values = {param: int(value) if param == 'sam' else value for param, value in zip(param_ranges.keys(), combination)}

    # Extract A values
    if 'T1' in param_values:
      T1, T2, T3 = [param_values[f'T{i}'] for i in range(1, 4)]
    if 'A1' in param_values:
      A1, A2, A3 = [param_values[f'A{i}'] for i in range(1, 4)]
    if 'Tm1' in param_values:
      Tm1, Tm2, Tm3 = [param_values[f'Tm{i}'] for i in range(1, 4)]
    if 'Am1' in param_values:
      Am1, Am2, Am3 = [param_values[f'Am{i}'] for i in range(1, 4)]
    if 'p1' in param_values:
      p1, p2, p3 = [param_values[f'p{i}'] for i in range(1, 4)]
    if 'sam' in param_values:
      sam = param_values['sam']

    # Generate signals
    parX = fullX(T1=T1, T2=T2, T3=T3, A1=A1, A2=A2, A3=A3, Tm1=Tm1, Tm2=Tm2, Tm3=Tm3, Am1=Am1, Am2=Am2, Am3=Am3, p1=p1, p2=p2, p3=p3)
    _, _, _, _, signal = run_ins(DUR, SIG, *parX)

    # Simulate samples
    _, _, _, _, _, fit = run_sim(signal, DUR, SIG, sam, REP)

    # Append results
    sams.append(sam)
    fits.append(fit)

  return sams, fits
## Data
'''
Logistic Function and Signal Analysis

This code cell defines a series of functions for performing logistic curve fitting and signal analysis. It allows to fit a logistic function to data, visualise insolation curves, simulate signals, and perform parameter sensitivity analysis.

Functions:
- `logistic_function(x, a, b, c)`: Defines the logistic function for curve fitting.
- `logistic_fit(x_data, y_data, params, maxfev=1e4)`: Fits the logistic function to data and returns the fitted parameters.
- `find_x_for_y(y, a, b, c)`: Calculates the x value for a given y value in the logistic curve.
- `set_plot_prop(ax, x_scale, y_scale, title, xlim, ylim)`: Sets various properties for plotting including scale, title, and axis limits.
- `insolation(ax, dur, sig, par1, par2, par3)`: Plots insolation curves based on provided parameters.
- `simulation(ax, signal, dur, sig, sam, rep)`: Simulates signals and compares them to the original signal.
- `simulations(ax, signal, dur, sig, rep)`: Runs simulations with varying sample rates and collects fit values.
- `parameters(ax, _1, _2, _3, param_ranges)`: Performs parameter sensitivity analysis and collects fit values.
- `all(ax, _1, _2, _3, param_ranges, title)`: Similar to 'parameters', but accepts a custom title.
- `logistic(ax, x_data, y_data)`: Fits a logistic curve to provided data and visualises the curve.

This code cell is a comprehensive toolkit for logistic curve fitting and signal analysis, making it easier to analyse and understand the behaviour of simulations.
'''
def logistic_function(x, a, b, c):
  return a / (1 + np.exp(-b * (np.log(x) - c)))

def logistic_fit(x_data, y_data, params, maxfev=1e4):
  return curve_fit(logistic_function, x_data, y_data, params, maxfev=int(maxfev))

def find_x_for_y(y, a, b, c):
  x = np.exp((np.log(a / (y * a)) / -b) + c)
  return x

def set_plot_prop(ax, x_scale, y_scale, title, xlim=None, ylim=None):
  ax.set(xscale=x_scale, yscale=y_scale, title=title, xlim=xlim, ylim=ylim)
  ax.grid(True, which='both', color='#333')
  if xlim is None:
    ax.autoscale(axis='x')
  if ylim is None:
    ax.autoscale(axis='y')

def insolation(ax, dur, sig, par1, par2, par3):
  t, s1, s2, s3, s = run_ins(dur, sig, par1, par2, par3)
  ax.plot(t, s1, color='red', linestyle='--', linewidth=0.8)
  ax.plot(t, s2, color='green', linestyle='--', linewidth=0.8)
  ax.plot(t, s3, color='yellow', linestyle='--', linewidth=0.8)
  ax.plot(t, s, color='cyan')
  set_plot_prop(ax, 'linear', 'linear', 'Insolation', (0, 1e6))
  return s

def simulation(ax, signal, dur, sig, sam, rep):
  sig_t, sam_t, sam_y, sim_t, _, fit = run_sim(signal, dur, sig, sam, rep)
  ax.plot(sig_t, signal, color='darkcyan')
  ax.plot(sam_t, sam_y, color='darkmagenta', linestyle='--', marker='o', markersize='3')
  ax.plot(sim_t, sam_y, color='yellow', marker='o', markersize='3')
  set_plot_prop(ax, 'linear', 'linear', 'Simulation', (0, 1e6))
  return fit

def simulations(ax, signal, dur, sig, rep):
  sams, fits = run_sims(signal, dur, sig, rep)
  ax.scatter(sams, fits, s=20, color='darkcyan')
  set_plot_prop(ax, 'log', 'linear', 'Simulations', (1, 1e3), (0, 1))
  return sams, fits

def parameters(ax, _1, _2, _3, param_ranges):
  sams, fits = run_params(param_ranges)
  ax.scatter(sams, fits, s=5, color='darkcyan')
  set_plot_prop(ax, 'log', 'linear', 'Parameters', (1, 1e3), (0, 1))
  return sams, fits

def all(ax, _1, _2, _3, param_ranges, title):
  sams, fits = run_params(param_ranges)
  ax.scatter(sams, fits, s=5, color='darkcyan')
  set_plot_prop(ax, 'log', 'linear', title, (1, 1e3), (0, 1))
  return sams, fits

def logistic(ax, x_data, y_data):
  params = (1, 0.4, 60) # (1.0, 0.4, 60)
  covariance = np.zeros((3, 3))
  params, covariance = logistic_fit(x_data, y_data, params, 1e5)
  x_fit = np.linspace(min(x_data), max(x_data), 100)
  y_fit = logistic_function(x_fit, *params)
  ax.plot(x_fit, y_fit, color='cyan')
  return params, covariance
## Text
'''
Text Formatting and Display

This code cell defines functions for formatting and displaying text in a plot. It is specifically designed to present key information in a structured and visually appealing way, making it easier to communicate results and insights from logistic curve fitting and signal analysis.

Functions:
- `format_vals(input, dec=0)`: Formats a single value or a list/tuple of values, rounding them to a specified number of decimal places.
- `format_list(input, dec=0)`: Formats a list of values, including the minimum, mean, and maximum, rounding them to a specified number of decimal places.
- `format_logi(a, b, c, dec=0)`: Formats logistic curve parameters (a, b, c) for display, rounding them to a specified number of decimal places.
- `display_text(ax, sam, fit, sams_con, fits_con, sams_var, fits_var, params, _)`: Displays formatted text on a plot, presenting logistic curve parameters, simulation results, and sample statistics.

This code cell enhances the readability and interpretability of results by structuring and displaying key information in a clear and concise manner within the generated plots.
'''
def format_vals(input, dec=0):
  if not isinstance(input, (list, tuple)):
    input = (input,)
  return tuple(
    round(value, dec)
      if value % 1 != 0
      else int(value)
    for value in input)

def format_list(input, dec=0):
  mean = np.mean(input)
  return format_vals((round(min(input), dec), round(mean, dec)
    if mean % 1 != 0 
    else int(mean), round(max(input), dec)), dec)

def format_logi(a, b, c, dec=0):
  return round(a, dec), round(np.log(b), dec), int(np.exp(c))

def display_text(ax, sam, fit, sams_con, fits_con, sams_var, fits_var, params, _):
  text = []
  text.append(f"Logistic {4*' '} (max, dip, flex)")
  text.append(f"  Params {2*' '} {str(format_logi(*params, 2))}")
  text.append(f"Simulation")
  text.append(f"  Samples {1*' '} {str(format_vals(sam))}")
  text.append(f"  Fit {11*' '} {str(format_vals(fit, 2))}")
  text.append(f"Constant")
  text.append(f"  Samples {1*' '} {str(format_list(sams_con))}")
  text.append(f"  Fit {11*' '} {str(format_list(fits_con, 2))}")
  text.append(f"Variable")
  text.append(f"  Samples {1*' '} {str(format_list(sams_var))}")
  text.append(f"  Fit {11*' '} {str(format_list(fits_var, 2))}")
  text.append(f"{18*' '} (min, avg, max)")
  for i, line in enumerate(text):
    lines = line.split('\n')
    for j, subline in enumerate(lines):
      plt.text(0, 0.9 - (i + j * 0.03) * 0.2, subline, transform=ax.transAxes, fontsize=12)
## Plot Insolation
'''
Plot Insolation

This code cell defines a function for creating a plot to visualise insolation data using the specified parameter combinations (parX). Insolation represents the amount of solar radiation received at different times, and this plot provides a visual representation of how various parameters impact insolation.

Function:
- `plot_ins(parX=PARS)`: Generates a plot of insolation data based on the provided parameter combinations and displays it in a clear and informative manner.

The function creates a single subplot within a figure, plots the insolation data using the given parameters, and presents the plot for analysis. This visualisation aids in understanding the effects of parameter changes on insolation.
'''
def plot_ins(parX=PARS):
  # Figure
  plt.close('all')
  fig = plt.figure(figsize=(20, 2))
  ax1 = plt.subplot2grid((1, 1), (0, 0))

  # Data
  insolation(ax1, DUR, SIG, *parX)
  plt.show()
  return fig
## Plot Simulation
'''
Plot Simulation

This code cell defines a function for creating a plot that visualises a simulation based on the specified parameters. The simulation involves generating and comparing samples with the original signal, helping to assess the quality of the simulation under various parameter combinations.

Function:
- `plot_sim(sam=SAM, parX=PARS)`: Generates a plot of a simulation using the specified parameters and displays the results in a clear format.

The function creates a figure with two subplots: one for the original signal and one for the simulation results. The original signal is hidden to focus on the simulation's quality, which is indicated by the fit value. The simulation plot aids in understanding how different parameters impact the quality of the simulated data.
'''
def plot_sim(sam=SAM, parX=PARS):
  # Figure
  plt.close('all')
  fig = plt.figure(figsize=(20, 4))
  ax1 = plt.subplot2grid((2, 1), (0, 0), colspan=3)
  ax2 = plt.subplot2grid((2, 1), (1, 0), colspan=3)
  ax1.set_visible(False)

  # Data
  signal = insolation(ax1, DUR, SIG, *parX)
  simulation(ax2, signal, DUR, SIG, sam, REP)

  plt.show()
  return fig
## Plot Simulations
'''
Plot Simulations and Analysis

This code cell defines a function for visualising simulation results and performing analysis on the sampled data.

Function:
- `plot_sims(sam=SAM, param_ranges=_A_, parX=PARS)`: Generates a multi-panel plot to display insolation, simulations, and analysis of sampled data.

The function performs the following actions:
1. Sets up a multi-panel figure with various subplots using Matplotlib.
2. Generates an insolation signal using the provided parameters from `parX`.
3. Runs simulations to compare the insolation signal with sampled data, recording fit values.
4. Analyses sampled data with different parameter ranges.
5. Performs logistic analysis on the simulations and records parameters and covariance.
6. Displays informative text about the analysis in the fifth subplot.
7. Adds horizontal and vertical lines to highlight the average fit and the corresponding sample size.

This function is designed for comprehensive analysis and visualisation of insolation data and simulations, making it a valuable tool for understanding the quality and characteristics of the sampled data and the impact of different parameters.
'''
def plot_sims(sam=SAM, param_ranges=_A_, parX=PARS):
  # Figure
  plt.close('all')
  fig = plt.figure(figsize=(20, 8))
  ax1 = plt.subplot2grid((4, 3), (0, 0), colspan=3)
  ax2 = plt.subplot2grid((4, 3), (1, 0), colspan=3)
  ax3 = plt.subplot2grid((4, 3), (2, 0), rowspan=2)
  ax4 = plt.subplot2grid((4, 3), (2, 1), rowspan=2)
  ax5 = plt.subplot2grid((4, 3), (2, 2), colspan=2)
  ax5.axis('off')

  # Insolation
  signal = insolation(ax1, DUR, SIG, *parX)

  # Simulation
  fit = simulation(ax2, signal, DUR, SIG, sam, REP)

  # Sampling
  sams_con, fits_con = simulations(ax3, signal, DUR, SIG, REP)

  # Variable
  sams_var, fits_var = parameters(ax4, DUR, SIG, REP, param_ranges)

  # Logistic
  params, covariance = logistic(ax3, sams_con, fits_con)
  params, covariance = logistic(ax4, sams_con, fits_con)

  # Text
  display_text(ax5, sam, fit, sams_con, fits_con, sams_var, fits_var, params, covariance)

  # Lines
  y = fit
  x_y = find_x_for_y(y, *params)
  x_x = np.interp(y, fits_con, sams_con)
  ax3.axhline(y=y, color='yellow', linestyle='--', linewidth='1', label=f'Average: {x_y:.2f}')
  ax3.axvline(x=x_x, color='magenta', linestyle='--')

  plt.show()
  return fig
## Plot Animation
'''
Update and Display Simulation Plots

This code cell defines functions for updating and displaying simulation plots in a dynamic manner.

Functions:
- `update_plot(sam, param_ranges)`: Updates and displays the simulation plots for a given sample size (sam) and parameter ranges (param_ranges).
- `plots_sims(sam_values, param_ranges=_A_)`: Iterates through a list of sample sizes (sam_values) and updates the simulation plots with different sample sizes.

These functions are used for interactive visualisation and analysis of sampling simulations. The process involves the following steps:
1. The `update_plot` function updates the simulation plots for a specific sample size and parameter ranges, clearing the previous plot and providing a brief delay for a smoother update.
2. The `plots_sims` function iterates through a list of sample sizes in reverse order, allowing users to observe how changing the sample size affects the simulation results and analysis.

These functions enable dynamic exploration of simulation results and their dependence on sample size and parameter variations, aiding in the understanding of insolation data and analysis.
'''
def update_plot(sam, param_ranges):
  plot_sims(sam, param_ranges)
  clear_output(wait=True)
  time.sleep(0.1)

def plots_sims(sam_values, param_ranges=_A_):
  for sam in sam_values[::-1]:
    update_plot(int(round(sam)), param_ranges)
## Plot Parameters
'''
Parameter Exploration Plot

This code cell defines functions and plots to explore the influence of different parameters on insolation simulations. The primary goal is to visualise how changes in various parameters affect the similarity between simulations and observed data.

Functions:
- `func_lin(ax, params, lines, x_vals, y_vals)`: Plots horizontal and vertical lines on the specified axes to indicate key points of interest. The lines represent specific values and their corresponding positions.
- `func_par(axes, variables, lines)`: Iterates through a set of parameters and plots key lines on multiple subplots, demonstrating the relationships between parameter values and simulation fit.
- `plot_pars()`: Generates a 2x3 grid of subplots for exploring different parameter variations. Each subplot focuses on a specific parameter, and key lines are plotted to highlight critical values.

The key lines plotted in the subplots indicate specific levels of simulation fit, and vertical lines show the corresponding parameter values that achieve these fits. These visualisations help users understand how parameter adjustments impact the quality of insolation simulations and provide insights into parameter tuning.

The subplots are organized by parameter type, including Period, Amplitude, Default, Period modulation, Amplitude modulation, and Phase. Each subplot provides a visual representation of how changing a particular parameter influences the similarity between simulated and observed insolation data.

The overall goal of this code cell is to facilitate parameter exploration and guide decision-making when configuring parameters for insolation simulations.
'''
def func_lin(ax, params, lines, x_vals, y_vals):
  for (y, color, linestyle, linewidth) in lines:
    ax.axhline(y=y, color=color, linestyle=linestyle, linewidth=linewidth)
    x_y = find_x_for_y(y, *params)
    x_x = np.interp(y, y_vals, x_vals)
    ax.axvline(x=x_x, color=color, label=f'{round(x_x)}', linestyle=linestyle, linewidth=linewidth)
  ax.legend(loc='center right')

def func_par(axes, variables, lines):
  for ax, (title, ranges) in zip(axes, variables):
    sams, fits = all(ax, DUR, SIG, REP, ranges, title)
    params, _ = logistic(ax, sams, fits)
    func_lin(ax, params, lines, sams, fits)

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

  lines = [
    (3/4, 'yellow', '--', 1),
    (1/2, 'lime', '--', 1),
    (1/4, 'red', '--', 1)
  ]

  func_par(axes, variables, lines)

  plt.show()
  return fig
## Insolation
'''
Generate and Plot Default Insolation Parameters

In this code cell, default insolation parameters are generated using the `full()` function, and the insolation curve is plotted using the `plot_ins()` function.

- `pars = full()`: This line initialises the `pars` variable with default insolation parameters using the `full()` function. These parameters represent a baseline configuration for insolation simulations.
- `plot_ins()`: This function call generates and displays the insolation curve based on the default parameters. The resulting plot showcases the insolation curve with its characteristic components, including variations in amplitude and phase.

The purpose of this code cell is to provide a visual representation of the default insolation parameters and the resulting insolation curve. It serves as a starting point for further exploration and analysis of insolation simulations, allowing users to understand the initial configuration and make comparisons with future parameter adjustments.
'''
pars = full()
plot_ins()
plt.show()
## Simulation
'''
Simulate and Plot Insolation with Variable Sampling

This code cell simulates and plots the insolation curve with variable sampling settings.

- `pars = full()`: The `pars` variable is initialised with default insolation parameters using the `full()` function, representing a baseline configuration.
- `sam = 60`: The variable `sam` is set to 60, which represents the number of samples to be taken from the insolation curve.
- `plot_sim(sam, pars)`: This function call simulates the insolation curve with the specified sampling setting and the given parameters. It then plots the original insolation curve and the simulated data, allowing for visual comparison.

The purpose of this code cell is to demonstrate how variable sampling affects the simulated insolation curve. Users can observe the impact of changing the number of samples on the simulation results, providing insights into the reliability and accuracy of the insolation simulations.
'''
pars = full()
sam = 60
plot_sim(sam, pars)
plt.show()
## Simulations
'''
Signal Sampling, Parameter Exploration, and Logistic Curve Fitting

This code cell combines various processes, including signal sampling, parameter exploration, and logistic curve fitting, to analyse and visualise signal characteristics.

- `plot_sims(sam, param_ranges=_A_, parX=PARS)`: The `plot_sims` function generates a multi-plot figure to illustrate different aspects of signal analysis. It performs the following steps:
    - Insolation: The original signal is generated and displayed, showing the insolation components.
    - Simulation: A simulated signal is generated based on the insolation components, and its fit to the original signal is visualised.
    - Sampling: The function `simulations` explores how varying the number of samples affects the fit to the original signal. The results are displayed in a scatter plot.
    - Variable: The function `parameters` explores the effect of varying multiple parameters on the fit. It visualises the results in a scatter plot.
    - Logistic: Logistic curve fitting is applied to the sampling and variable results, and the fitted curves are displayed.
    - Text Information: Textual information is provided in the figure, summarizing the analysis and displaying key values and statistics.
    - Lines: Vertical and horizontal lines are added to the scatter plots to highlight specific fit values and corresponding parameters.

- `update_plot(sam, param_ranges)`: This function updates the multi-plot figure to reflect changes in the number of samples (sam) and parameter ranges. It helps create an animated view of how adjustments affect the analysis.

- `plots_sims(sam_values, param_ranges=_A_)`: This function iterates through a range of sample values (sam_values) and updates the figure for each value, providing a dynamic representation of how sample size impacts the analysis.

- `func_lin(ax, params, lines, x_vals, y_vals)`: A utility function for adding horizontal and vertical lines to a plot based on specified parameters and values.

- `func_par(axes, variables, lines)`: A function that generates plots for different parameter variations, including period, amplitude, default parameters, period modulation, amplitude modulation, and phase. It also includes vertical and horizontal lines to highlight specific fit values and corresponding parameters.

- `plot_pars()`: The `plot_pars` function creates a multi-plot figure to explore the impact of various parameters on the fit. It visualises logistic curve fits and provides a visual representation of how different parameter changes affect the analysis.

Overall, this code cell demonstrates an extensive analysis of signal characteristics, parameter variations, and curve fitting, with a focus on providing both visual and numerical insights into the analysis.
'''
pars = _AAm_
sam = 65
plot_sims(sam, pars)
plt.show()
## Animation
'''
Signal Analysis and Visualisation - Parameter Exploration

This code cell focuses on analysing and visualising a signal under different conditions, primarily by exploring the effect of parameter variations on the signal analysis.

- `pars = _A_`: The variable `pars` is set to a predefined set of parameters defined in the `_A_` variable. These parameters represent the initial conditions for signal analysis.

- `sams = _SAM_L_`: The variable `sams` is set to a list of sample values defined in the `_SAM_L_` variable. These sample values represent different sample sizes to be used in the analysis.

- `plots_sims(sams, pars)`: The `plots_sims` function is called to create a multi-plot figure that provides insights into how different sample sizes (defined in `sams`) affect the analysis. The following aspects are explored:
    - Insolation: The original signal is generated and displayed.
    - Simulation: A simulated signal is generated based on the insolation components, and its fit to the original signal is visualised.
    - Sampling: The function explores how varying the number of samples affects the fit to the original signal and displays the results in a scatter plot.
    - Variable: The effect of varying multiple parameters on the fit is visualised in a scatter plot.
    - Logistic: Logistic curve fitting is applied to the sampling and variable results, and the fitted curves are displayed.
    - Text Information: Textual information summarizing the analysis is provided in the figure.

- `sam = 65`: A specific sample size (65) is selected for further analysis.

- `plot_sims(sam, pars)`: The `plot_sims` function is called with the selected sample size (sam) and the predefined parameters (pars). This function generates a multi-plot figure that provides a detailed analysis of the signal with the chosen sample size.

- `plt.show()`: The `plt.show()` function is used to display the generated figures, allowing for visual inspection and analysis of the results.

Overall, this code cell facilitates the exploration of signal characteristics and the impact of parameter variations by providing visual representations and insights into the analysis at different sample sizes.
'''
pars = _A_
sams = _SAM_L_
plots_sims(sams, pars)

sam = 65
plot_sims(sam, pars)
plt.show()
## Parameters
'''
Parameter Analysis and Visualisation

This code cell focuses on the analysis and visualisation of parameters used in signal analysis. It explores how changes in specific parameters affect the fit of a signal and provides visual representations of these effects.

- `plot_pars()`: The `plot_pars` function is called to create a multi-plot figure that analyses and visualises the impact of parameter variations on signal fitting. The following aspects are explored for different parameter types:
    - Period: Variations in the signal period (T) and its effect on the fit.
    - Amplitude: Variations in signal amplitudes (A) and their impact on fitting.
    - Default: Analysis of default parameters (SAM_L) and their effect on signal fitting.
    - Period Modulation: Exploration of the effect of period modulation (Tm) on fitting.
    - Amplitude Modulation: Analysis of amplitude modulation (Am) and its impact on signal fitting.
    - Phase: The effect of phase (p) on signal fitting.
    - Logistic: Logistic curve fitting is applied to the results, and the fitted curves are displayed.
    - Text Information: Textual information summarizing the analysis is provided in the figure.

- `plt.show()`: The `plt.show()` function is used to display the generated figures, allowing for visual inspection and analysis of the results.

Overall, this code cell provides a comprehensive analysis of how different parameter variations influence signal fitting, along with visual representations and insights into these effects.
'''
plot_pars()
plt.show()