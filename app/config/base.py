import os

class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY') or'top-secret'

  CONFIG = {
    'DUR': int(1e6),
    'SIG': int(1e3),
    'SAM': int(1e2),
    'REP': int(1e1),
  }

  BLUEPRINTS = [
    'app.route.base',
    'app.blueprint.info.route.info',
    'app.blueprint.analysis.route.analysis',
    'app.blueprint.dashboard.route.dashboard',
    'app.blueprint.setting.route.setting',
    'app.blueprint.help.route.help',
  ]
