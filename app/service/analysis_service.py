import numpy as np
from app.service.insolation_manager import InsolationManager
from app.service.simulation_manager import SimulationManager

class AnalysisService:
  def __init__(self):
    self.insolation_manager = InsolationManager()
    self.simulation_manager = SimulationManager()

  def get_analysis(self, sample_size=None):
    df = self.insolation_manager.run_insolation()

    sim_result = self.simulation_manager.run_simulation(df, sample_size)

    multi_sim_results = self.simulation_manager.run_many_simulations(df)

    logistic_result = self.simulation_manager.logistic_analysis(multi_sim_results)

    optimal_size = self.simulation_manager.find_optimal_sample_size(0.9, multi_sim_results)

    stats = self.simulation_manager.get_simulation_statistics(multi_sim_results)

    return {
      'single_simulation': sim_result,
      'many_simulations': multi_sim_results.to_dict('records'),
      'logistic_analysis': logistic_result,
      'optimal_sample_size': optimal_size,
      'statistics': stats,
      'insolation_stats': self._get_insolation_stats(df)
    }

  def get_enhanced_analysis(self):
    df = self.insolation_manager.run_insolation()

    param_ranges = self.simulation_manager.parameter_ranges

    sensitivity_results = self.simulation_manager.run_parameter_sensitivity(
      param_ranges['A'], df
    )

    return {
      'basic_stats': self._get_basic_stats(df),
      'correlation_analysis': self.calculate_correlations(df),
      'signal_properties': self.analyse_signal_properties(df),
      'sensitivity_analysis': sensitivity_results.to_dict('records'),
      'parameter_ranges': {k: {k2: v2.tolist() for k2, v2 in v.items()}
                         for k, v in param_ranges.items()}
    }

  def _get_insolation_stats(self, df):
    return {
      'max_amplitude': int(df['total_signal'].max()),
      'min_amplitude': int(df['total_signal'].min()),
      'mean_amplitude': int(df['total_signal'].mean()),
      'data_points': len(df),
      'std_amplitude': int(df['total_signal'].std()),
      'median_amplitude': int(df['total_signal'].median()),
      'signal_stats': {
        col: {
          'max': int(df[col].max()),
          'min': int(df[col].min()),
          'mean': int(df[col].mean()),
        }
        for col in df.columns if col.startswith('signal_')
      }
    }

  def _get_basic_stats(self, df):
    return {
      'max_amplitude': int(df['total_signal'].max()),
      'min_amplitude': int(df['total_signal'].min()),
      'mean_amplitude': int(df['total_signal'].mean()),
      'std_amplitude': int(df['total_signal'].std()),
      'median_amplitude': int(df['total_signal'].median()),
      'data_points': len(df)
    }

  def calculate_correlations(self, df=None):
    if df is None:
      df = self.insolation_manager.run_insolation()

    signal_cols = [col for col in df.columns if col.startswith('signal_')]

    if len(signal_cols) > 1:
      corr_matrix = df[signal_cols].corr()
      return {
        'correlation_matrix': corr_matrix.values.tolist(),
        'signal_names': signal_cols
      }
    else:
      return {
        'correlation_matrix': [],
        'signal_names': signal_cols
      }

  def analyse_signal_properties(self, df=None):
    if df is None:
      df = self.insolation_manager.run_insolation()

    signal_cols = [col for col in df.columns if col.startswith('signal_')]

    properties = {}
    for col in signal_cols:
      signal_data = df[col]
      properties[col] = {
        'zero_crossings': int(self.simulation_manager._cross(signal_data)),
        'variance': float(np.var(signal_data, ddof=1)),
        'energy': float((signal_data ** 2).sum())
      }

    return properties

  @staticmethod
  def analyse_dataFrame(df):
    return {
      'descriptive_stats': df.describe().to_dict(),
      'correlations': df.corr().to_dict(),
      'memory_usage': df.memory_usage(deep=True).to_dict(),
    }
