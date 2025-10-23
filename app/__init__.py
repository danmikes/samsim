from flask import Flask

def create_app():
  app = Flask(__name__)

  from .route import home
  from .blueprint.analysis.route import analysis
  from .blueprint.dashboard.route import dashboard
  from .blueprint.setting.route import setting

  app.register_blueprint(home)
  app.register_blueprint(analysis, url_prefix='/analysis')
  app.register_blueprint(dashboard, url_prefix='/dashboard')
  app.register_blueprint(setting, url_prefix='/setting')

  return app
