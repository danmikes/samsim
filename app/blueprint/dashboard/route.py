from flask import Blueprint, render_template
from app.service import service

dashboard = Blueprint('dashboard', __name__,
                      static_folder='.',
                      static_url_path='/static',
                      template_folder='.',
                      url_prefix='/dashboard')

@dashboard.route('/')
def view():
  data = service.get_dashboard_data()

  return render_template('blueprint/dashboard/view.htm', data=data)
