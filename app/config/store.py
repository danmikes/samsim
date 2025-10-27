import fcntl
import json
import os
from pathlib import Path

CONFIG_FILE = Path('store_config.json')

class ConfigStore:
  @staticmethod
  def load():
    if CONFIG_FILE.exists():
      try:
        with open(CONFIG_FILE, 'r') as f:
          return json.load(f)
      except (json.JSONDecodeError, Exception):
        return {}
    return {}

  @staticmethod
  def save(config_data):
    with open(CONFIG_FILE, 'w') as f:
      json.dump(config_data, f, indent=2)

  @staticmethod
  def update_category(category, updates):
    current = ConfigStore.load()
    if category not in current:
      current[category] = {}

    if category == 'signal':
      for signal_name, signal_updates in updates.items():
        if signal_name not in current[category]:
          current[category][signal_name] = {}
        current[category][signal_name].update(signal_updates)
    else:
      current[category].update(updates)

    ConfigStore.save(current)
