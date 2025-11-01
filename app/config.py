import os
import numpy as np
from enum import Enum

class SampleSizeRange(Enum):
  SHORT = tuple(2 ** np.arange(1, 6, 1))
  LONG = tuple(2 ** np.arange(1, 10, 0.5))
  CUSTOM = None

  def get_sizes(self, custom_sizes=None):
    if self == SampleSizeRange.CUSTOM:
      if custom_sizes is None:
        raise ValueError("Custom sizes must be provied for CUSTOM preset")
      return custom_sizes
    return np.array(self.value)

class Config:
  ENV = os.environ.get('FLASK_ENV', 'development')
  DEBUG = ENV == 'development'
  TESTING = False

  SECRET_KEY = os.environ.get('SECRET_KEY') or'top-secret'

  CONFIG = {
    'DURATION': int(1e6),
    'SIGNAL_RATE': int(1e3),
    'SAMPLE_SIZE': int(1e2),
    'REPETITIONS': int(1e1),
  }

  SAMPLE_SIZE_RANGE = SampleSizeRange
  DEFAULT_SAMPLE_SIZE_RANGE = SampleSizeRange.SHORT

  PARAMETER_RANGES = {
    'T': {f'T{i}': 2. ** np.arange(2, 5) * 1e4 for i in range(1, 4)},
    'A': {f'A{i}': np.arange(0, 26, 5) for i in range(1, 4)},
    'Tm': {f'Tm{i}': 2. ** np.arange(0, 3) * 1e5 for i in range(1, 4)},
    'Am': {f'Am{i}': np.arange(0, 13, 2.5) for i in range(1, 4)},
    'p': {f'p{i}': 2. ** np.arange(-3, -1) * np.pi for i in range(1, 4)},
  }

  BLUEPRINTS = [
    'app.route.base',
    'app.blueprint.info.route.info',
    'app.blueprint.analysis.route.analysis',
    'app.blueprint.dashboard.route.dashboard',
    'app.blueprint.setting.route.setting',
    'app.blueprint.help.route.help',
  ]
