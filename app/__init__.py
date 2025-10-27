from __future__ import annotations
from enum import Enum, EnumMeta
from flask import Flask
from flask.json.provider import DefaultJSONProvider

from .config import Config
from .util.register import register_blueprint, register_filter

class CustomJSONProvider(DefaultJSONProvider):
  def default(self, obj):
    if isinstance(obj, EnumMeta):
      return obj.__name__
    elif isinstance(obj, Enum):
      return obj.name
    elif hasattr(obj, 'tolist'):
      return obj.tolist()
    return super().default(obj)

def create_app(config_name=None):
  app = Flask(__name__)
  app.config.from_object(Config.core)
  app.config.update(Config.sim.sim._asdict())
  app.json = CustomJSONProvider(app)

  register_blueprint(app)
  register_filter(app)

  return app
