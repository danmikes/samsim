from flask import Blueprint, render_template

setting = Blueprint('setting', __name__,
                     static_folder='.',
                     static_url_path='/static',
                     template_folder='.')

@setting.route('/')
def view():
  return render_template('blueprint/setting/view.htm')

@setting.route('/data')
def get_data():
  return {'data': 'some data'}
