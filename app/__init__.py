from flask import Flask

def create_app():
  app = Flask(__name__)

  @app.template_filter('format_number')
  def format_number(value):
    if isinstance(value, (int, float)):
        if value >= 1_000_000:
            return f"{value:_}"  # 1_000_000
        elif value >= 10_000:
            return f"{value:,}"  # 10,000
        elif value >= 1_000:
            return f"{value:_}"  # 1_000
        else:
            return str(value)
    return value

  from .route import base
  from .blueprint.info.route import info
  from .blueprint.analysis.route import analysis
  from .blueprint.dashboard.route import dashboard
  from .blueprint.setting.route import setting
  from .blueprint.help.route import help

  app.register_blueprint(base)
  app.register_blueprint(info)
  app.register_blueprint(analysis)
  app.register_blueprint(dashboard)
  app.register_blueprint(setting)
  app.register_blueprint(help)

  return app
