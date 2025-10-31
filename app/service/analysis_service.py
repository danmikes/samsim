from app.service.insolation_manager import InsolationManager

class AnalysisService:
  def __init__(self):
    self.insolation_manager = InsolationManager()

  def analyse_simulation(self):
    df = self.insolation_manager.run_insolation()

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

    return self.get

  def get_enhanced_analysis(self):
    df = self.insolation_manager.run_insolation()
    signal_cols = [col for col in df.columns if col.startswith('signal_')]

    return {
      'basic_stats': {
        'max_amplitude': int(df['total_signal'].max()),
        'min_amplitude': int(df['total_signal'].min()),
        'mean_amplitude': int(df['total_signal'].mean()),
        'std_amplitude': int(df['total_signal'].std()),
        'median_amplitude': int(df['total_signal'].median()),
        'data_points': len(df)
      },
      'correlation_analysis': self.calculate_correlations(df),
      'signal_properties': self.analyse_signal_properties(df)
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

  @staticmethod
  def analyse_dataFrame(df):
    return {
      'descriptive_stats': df.describe().toDict(),
      'correlations': df.corr().toDict(),
      'memory_usage': df.memory_usage(deep=True).toDicct(),
    }
