from flask import Blueprint, render_template
from app import service

analysis = Blueprint('analysis', __name__,
                     static_folder='.',
                     static_url_path='/static',
                     template_folder='.')

@analysis.route('/')
def view():
  data = service.get_dashboard_data()
  analysis_result = service.analyse_simulation()

  return render_template('blueprint/analysis/view.htm',
    data=data,
    analysis=analysis_result
  )
