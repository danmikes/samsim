import os

class CoreConfig:
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'top-secret'

  BLUEPRINTS = [
    'app.route.base',
    'app.blueprint.info.route.info',
    'app.blueprint.dashboard.route.dashboard',
    'app.blueprint.control.route.control',
  ]
