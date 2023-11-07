# Simulation Readme

This is Python code `(SamSim)` for simulating and analysing data related to insolation and sampling. The code uses various functions and parameters to create time series data, perform simulations, and analyse results. Below, we describe main components and how to use `SamSim`.

## Dependencies

Before running the code, have following Python libraries installed:

- matplotlib
- numpy
- pandas
- scipy
Install these libraries with pip
`pip install matplotlib numpy pandas scipy`

## Functions

- `SamSim` includes several functions for generating data and performing simulations. Here are some key functions:
- `sine(A, T, t, p=0)`: Generates sine wave with given `amplitude (A)`, `period (T)`, `time values (t)`, and `phase (p)`.
- `cosine(Am, Tm, t, p=0)`: Generates modulated cosine wave with given `amplitude modulation (Am)`, `period modulation (Tm)`, `time values (t)`, and `phase (p)`.
- `cross(signal)`: Calculates number of zero-crossings in a signal.
- `compare(signal, sample)`: Calculates fit between signal and sample.
- `logistic_function(x, a, b, c)`: Logistic function for fitting data.
- `logistic_fit(x_data, y_data, params, maxfev=1e4)`: Fit data to logistic function using curve fitting.

## Parameters

`SamSim` uses various parameters to configure simulations. These parameters include `period (T)`, `amplitude (A)`, `period modulation (Tm)`, `amplitude modulation (Am)`, and `phase (p)`. Adjust these parameters to customise simulations.

## Scenarios

`SamSim` defines scenarios for simulating data, such as changing `amplitude`, `period`, `amplitude modulation`, or all parameters simultaneously. These scenarios are provided as functions like `base`, `fullA`, `fullM`, and `fullX`. Select a scenario to perform simulations with specific parameter configurations.

## Property

`SamSim` defines properties for plotting, such as labels, colors, linestyles, and markers. Use these properties to customise appearance of plots.

## Figure

Functions are provided for creating figures and customizing their properties. Adjust figure size and other settings to change appearance.

## Plot

Plot function generates plots for `insolation`, `simulations`, and `sampling`, and displays results for various scenarios and parameter ranges.

## Usage

Use `SamSim` to perform simulations and analyse the results by adjusting parameters, scenarios, and property settings. To create plots and visualise data, call plot function with desired parameters. `SamSim` includes examples at the end of the script, demonstrating how to use it.

Feel free to explore and modify `SamSim` to suit your specific simulation and analysis needs.
