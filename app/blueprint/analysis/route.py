from flask import Blueprint, render_template

analysis = Blueprint('analysis', __name__,
                     static_folder='.',
                     static_url_path='/static',
                     template_folder='.')

@analysis.route('/')
def view():
  return render_template('blueprint/analysis/view.htm')

@analysis.route('/data')
def get_data():
  return {'data': 'some data'}
