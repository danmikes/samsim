from re import S
from flask import Blueprint, render_template, request, jsonify
from app.config import Config

control = Blueprint('control', __name__,
                    static_folder='.',
                    static_url_path='/static',
                    template_folder='.',
                    url_prefix='/control')

@control.route('/')
def view():

  return render_template(
    'blueprint/control/view.htm',
    page_title="Control",
    config=Config.serialise()
  )

@control.route('/update', methods=['POST'])
def update_config():
  if updates := request.get_json():
    for category, params in updates.items():
      Config.update(category, params)
    return jsonify(status='success')
  return jsonify(status='error', message='No data received'), 400

@control.route('/reset', methods=['POST'])
def reset_config():
  try:
    data = request.get_json() or {}
    Config.reset(data.get('category'))
    return jsonify(status='success')
  except Exception as e:
    return jsonify(status='error', message=str(e)), 400
