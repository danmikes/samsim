from flask import Blueprint, jsonify, render_template
from .service import setting_service

setting = Blueprint('setting', __name__,
                     static_folder='.',
                     static_url_path='/static',
                     template_folder='.')

@setting.route('/')
def view():
  return render_template('blueprint/setting/view.htm')

@setting.route('/data')
def get_data():
  data = setting_service.get_setting_data()
  return jsonify(data)

@setting.route('/data/<key>')
def get_specific_data(key):
  value = setting_service.get_setting_by_key(key)
  if value is not None:
    return jsonify({key: value})
  return jsonify({'error': 'Key absent'}), 404
