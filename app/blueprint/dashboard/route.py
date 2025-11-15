from flask import Blueprint, render_template, session
from app.service.dashboard_service import DashboardService
from app.config import Config

dashboard = Blueprint('dashboard', __name__,
                      static_folder='.',
                      static_url_path='/static',
                      template_folder='.',
                      url_prefix='/dashboard')

@dashboard.route('/')
def view():
  print(f"Session config exists: {'config' in session}")

  if 'config' not in session:
    print("Initializing new session with defaults")
    session['config'] = Config.get_default()
  else:
    print("Using existing session config")
  Config.update(session['config'])
  print(f"Current config target_fit: {Config.sim.sim.target_fit}")

  dashboard = DashboardService()
  charts = dashboard.run_dashboard()

  sim = Config.sim.sim._asdict()
  signals = Config.signal.signals

  return render_template(
    'blueprint/dashboard/view.htm',
    page_title="Dashboard",
    sim=sim,
    signals=signals,
    **charts
  )
