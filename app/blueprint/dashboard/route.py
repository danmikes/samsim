from flask import Blueprint, render_template

dashboard = Blueprint('dashboard', __name__,
                      static_folder='.',
                      static_url_path='/static',
                      template_folder='.')

@dashboard.route('/')
def view():
  return render_template('blueprint/dashboard/view.htm')

@dashboard.route('/data')
def get_data():
  return {'data': 'some data'}
