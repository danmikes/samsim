from flask import Blueprint, current_app, render_template
from app.service.app_service import service

analysis = Blueprint('analysis', __name__,
                     static_folder='.',
                     static_url_path='/static',
                     template_folder='.',
                     url_prefix='/analysis')

def prepare_analysis_for_template(analysis_data, analysis_type='regular'):
  if analysis_type == 'regular':
    return {
      **analysis_data,
      **analysis_data['insolation_stats'],
      'signal_stats': analysis_data['insolation_stats']['signal_stats']
    }
  else: # analysis_type == 'enhanced'
    return {
      **analysis_data,
      **analysis_data['basic_stats']
    }

@analysis.route('/')
def view():
  data = service.get_dashboard_data()
  analysis = service.get_analysis()
  analysis_flat = prepare_analysis_for_template(analysis, 'regular')
  return render_template('blueprint/analysis/view.htm',
    data=data,
    analysis=analysis_flat,
  )

@analysis.route('/enhanced')
def analyse():
  data = service.get_dashboard_data()
  analysis = service.get_enhanced_analysis()
  analysis_flat = prepare_analysis_for_template(analysis, 'enhanced')

  return render_template('blueprint/analysis/view.htm',
    data=data,
    analysis=analysis,
    enhanced=True,
  )
