from app.config import Config
from app.service.insolation_manager import InsolationManager

class SettingsService:
  def __init__(self):
    self.config = Config.CONFIG
    self.insolation_manager = InsolationManager()

  def get_settings(self):
    return {
      'duration': self.config['DURATION'],
      'signal_rate': self.config['SIGNAL_RATE'],
      'sample_size': self.config['SAMPLE_SIZE'],
      'repetitions': self.config['REPETITIONS'],
      'sample_sizes': Config.SAMPLE_SIZE_RANGE,
      'default_parameters': self.insolation_manager.default_pars
    }

  @staticmethod
  def analyse_dataFrame(df):
    return {
      'descriptive_stats': df.describe().to_dict(),
      'correlations': df.corr().to_dict(),
      'memory_usage': df.memory_usage(deep=True).to_dict(),
    }
