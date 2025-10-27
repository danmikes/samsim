import json
from flask import Blueprint, render_template, session, jsonify
from app.config import Config

dashboard = Blueprint('dashboard', __name__,
                      static_folder='.',
                      static_url_path='/static',
                      template_folder='.',
                      url_prefix='/dashboard')

@dashboard.route('/')
def view():
  from app.service.dashboard_service import DashboardService

  if 'config' not in session:
    session['config'] = Config.get_default()
  else:
    Config.update(session['config'])

  dashboard = DashboardService()
  charts = dashboard.run_dashboard()

  sim = {k: str(v) if not isinstance(v, (int, float, str, bool)) else v for k, v in Config.sim.sim._asdict().items()}
  signals = Config.signal.signals

  return render_template(
    'blueprint/dashboard/view.htm',
    page_title="Dashboard",
    sim=sim,
    signals=signals,
    **charts
  )

@dashboard.route('/chart-data')
def chart_data():
  from app.service.dashboard_service import DashboardService

  dashboard = DashboardService()
  charts = dashboard.run_dashboard()

  def make_serialisable(obj):
    if hasattr(obj, 'tolist'):
      return obj.tolist()
    if isinstance(obj, dict):
      return {k : make_serialisable(v) for k, v in obj.items()}
    if isinstance(obj, list):
      return [make_serialisable(item) for item in obj]
    return obj


  return jsonify(make_serialisable(charts))
