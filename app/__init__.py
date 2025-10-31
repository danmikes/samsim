from __future__ import annotations
from flask import Flask
from app.config.base import Config
from app.util.template_filters import register_template_filters
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from app.service.app_service import AppService

class ServiceApp(Flask):
  service: AppService

def create_app():
  app = ServiceApp(__name__)
  app.config.from_object(Config)

  from app.service.app_service import AppService
  app.service = AppService()

  _register_blueprints(app)
  register_template_filters(app)

  return app

def _register_blueprints(app):
  for bp_path in app.config['BLUEPRINTS']:
    module_path, bp_name = bp_path.rsplit('.', 1)
    module = __import__(module_path, fromlist=[bp_name])
    blueprint = getattr(module, bp_name)
    app.register_blueprint(blueprint)
