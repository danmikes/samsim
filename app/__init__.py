from __future__ import annotations
import json
from enum import Enum, EnumMeta
from flask import Flask
from flask.json.provider import DefaultJSONProvider
from app.config import Config
from app.util.template_filters import register_template_filters
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from app.service.app_service import AppService

class CustomJSONProvider(DefaultJSONProvider):
  def default(self, obj):
    if isinstance(obj, EnumMeta):
      return obj.__name__
    elif isinstance(obj, Enum):
      return obj.name
    elif hasattr(obj, 'tolist'):
      return obj.tolist()
    return super().default(obj)

class ServiceApp(Flask):
  service: 'AppService'

def create_app(config_name=None):
  app = ServiceApp(__name__)
  app.config.from_object(Config)
  app.json = CustomJSONProvider(app)

  from app.service.app_service import AppService
  app.service = AppService()

  _register_blueprints(app)
  register_template_filters(app)

  return app

def _register_blueprints(app):
  for bp_path in app.config['BLUEPRINTS']:
    try:
      module_path, bp_name = bp_path.rsplit('.', 1)
      module = __import__(module_path, fromlist=[bp_name])
      blueprint = getattr(module, bp_name)
      app.register_blueprint(blueprint)
    except (ImportError, AttributeError) as e:
      print(f'Warning: Failed to register blueprint {bp_path}: {e}')
