from .core import CoreConfig
from .sim import SimConfig
from .sample import SampleConfig
from .signal import SignalConfig

class Config:
  core = CoreConfig()
  sample = SampleConfig()
  signal = SignalConfig()
  sim = SimConfig()

  @classmethod
  def get_default(cls):
    return {
      'signal': {
        name: signal._asdict()
        for name, signal in cls.signal.defaults.items()
      },
      'sample': cls.sample.default._asdict(),
      'sim': cls.sim.default._asdict(),
    }

  @classmethod
  def update(cls, config_dict):
    for category, values in config_dict.items():
      config_obj = getattr(cls, category, None)
      if config_obj and hasattr(config_obj, 'update'):
        try:
          if category == 'signal':
            config_obj.update(values)
          else:
            config_obj.update(**values)
        except Exception as e:
          print(f'Warning: Could not update {category}: {e}')

  @classmethod
  def get(cls):
    return {
      'signal': {
        name: signal._asdict()
        for name, signal in cls.signal.signals.items()
      },
      'sample': cls.sample.sample._asdict(),
      'sim': cls.sim.sim._asdict(),
    }

Config.update(Config.get_default())
