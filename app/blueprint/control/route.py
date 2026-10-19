from re import S
from flask import Blueprint, render_template, request, jsonify, session
from app.config import Config

control = Blueprint('control', __name__,
                    static_folder='.',
                    static_url_path='/static',
                    template_folder='.',
                    url_prefix='/control')

def get_config():
  if 'config' not in session:
    session['config'] = Config.get_default()

  Config.update(session['config'])
  return session['config']

@control.route('/')
def view():
  config = get_config()

  return render_template(
    'blueprint/control/view.htm',
    page_title="Control",
    config=Config.get()
  )

@control.route('/update', methods=['POST'])
def update_config():
  config = get_config()

  if updates := request.get_json():
    for category, params in updates.items():
      if category not in config:
        config[category] = {}

      if category == 'signal':
        for signal_name, signal_updates in params.items():
          if signal_name not in config[category]:
            config[category][signal_name] = {}
          config[category][signal_name].update(signal_updates)
      else:
        config[category].update(params)

    session['config'] = config
    session.modified = True
    Config.update(config)

    return jsonify(status='success')
  return jsonify(status='error', message='No data received'), 400


@control.route('/reset', methods=['POST'])
def reset_config():
  try:
    data = request.get_json() or {}
    category = data.get('category')

    if category:
      default = Config.get_default()
      if category in default:
        if 'config' in session:
          session['config'][category] = default[category].copy()
        else:
          session['config'] = {category: default[category].copy()}
    else:
      session['config'] = Config.get_default()

    session.modified = True
    Config.update(session['config'])

    return jsonify(status='success')
  except Exception as e:
    return jsonify(status='error', message=str(e)), 400
