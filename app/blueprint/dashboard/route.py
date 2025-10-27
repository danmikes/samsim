from flask import Blueprint, render_template
from app.service.dashboard_service import DashboardService
from app.config import Config

dashboard = Blueprint('dashboard', __name__,
                      static_folder='.',
                      static_url_path='/static',
                      template_folder='.',
                      url_prefix='/dashboard')

@dashboard.route('/')
def view():
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
