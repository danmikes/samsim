import json
from .store import ConfigStore
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
  def initialise_from_store(cls):
    config_store = ConfigStore.load()

    if config_store:
      for category, values in config_store.items():
        config_obj = getattr(cls, category, None)
        if config_obj and hasattr(config_obj, 'update'):
          try:
            if category == 'signal':
              config_obj.update(values)
            else:
              config_obj.update(**values)
          except Exception as e:
            print(f"Warning: Could not load {category} from store: {e}")

  @classmethod
  def update(cls, category, updates):
    config_obj = getattr(cls, category, None)
    if not config_obj:
      return False

    if hasattr(config_obj, 'update'):
      try:
        if category == 'signal':
          config_obj.update(updates)
        else:
          config_obj.update(**updates)
        ConfigStore.update_category(category, updates)
        return True
      except Exception as e:
        print(f"Error updating {category}: {e}")
        import traceback
        print(traceback.format_exc())
        return False
    return False

  @classmethod
  def reset(cls, category=None):
    if category:
      if hasattr(cls, category) and hasattr(getattr(cls, category), 'reset'):
        getattr(cls, category).reset()
    else:
      for attr_name in ['signal', 'sample', 'sim']:
        if hasattr(cls, attr_name) and hasattr(getattr(cls, attr_name), 'reset'):
          getattr(cls, attr_name).reset()

  @classmethod
  def serialise(cls):
    return {
      'signal': {
        name: signal._asdict()
        for name, signal in cls.signal.signals.items()
      },
      'sample': cls.sample.sample._asdict(),
      'sim': cls.sim.sim._asdict(),
    }

Config.initialise_from_store()
