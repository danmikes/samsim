from flask import Flask

def create_app():
  app = Flask(__name__)

  from .route import base
  from .blueprint.info.route import info
  from .blueprint.analysis.route import analysis
  from .blueprint.dashboard.route import dashboard
  from .blueprint.setting.route import setting
  from .blueprint.help.route import help

  app.register_blueprint(base)
  app.register_blueprint(info, url_prefix='/info')
  app.register_blueprint(analysis, url_prefix='/analysis')
  app.register_blueprint(dashboard, url_prefix='/dashboard')
  app.register_blueprint(setting, url_prefix='/setting')
  app.register_blueprint(help, url_prefix='/help')

  return app
