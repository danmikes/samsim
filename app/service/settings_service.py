from app.config.base import Config
from app.service.insolation_manager import InsolationManager

class SettingsService:
  def __init__(self):
    self.config = Config.CONFIG
    self.insolation_manager = InsolationManager()

  def get_settings(self):
    return {
      'duration': self.config['DUR'],
      'signal_rate': self.config['SIG'],
      'sample_rate': self.config['SAM'],
      'repetitions': self.config['REP'],
      'default_parameters': self.insolation_manager.default_pars
    }

  @staticmethod
  def analyse_dataFrame(df):
    return {
      'descriptive_stats': df.describe().toDict(),
      'correlations': df.corr().toDict(),
      'memory_usage': df.memory_usage(deep=True).toDicct(),
    }
