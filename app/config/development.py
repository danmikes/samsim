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
    'route.base',
    'blueprint.info.route.info',
    'blueprint.analysis.route.analysis',
    'blueprint.dashboard.route.dashboard',
    'blueprint.setting.route.setting',
    'blueprint.help.route.help',
  ]
