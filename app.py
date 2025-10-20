import io
import os
import sys
from flask import Flask, render_template, jsonify, request, send_file
from datetime import datetime
import matplotlib.pyplot as plt

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
  sys.path.insert(0, current_dir)

app = Flask(__name__)

PARAM_GROUPS = [
  ('red', [('T1', 11), ('A1', 6), ('Tm1', 10), ('Am1', 6)]),
  ('green', [('T2', 11), ('A2', 6), ('Tm2', 10), ('Am2', 6)]),
  ('yellow', [('T3', 11), ('A3', 6), ('Tm3', 10), ('Am3', 6)]),
  ('white', [('sam', 8)])
]

ACTIONS = [
  {'action': 'reset', 'label': 'Reset', 'color': 'red'},
  {'action': 'insolation', 'label': 'Insolation', 'color': 'yellow'},
  {'action': 'simulation', 'label': 'Simulation', 'color': 'cyan'},
  {'action': 'simulations', 'label': 'Simulations', 'color': 'magenta'},
  {'action': 'parameters', 'label': 'Parameters', 'color': 'lime'},
]

def get_params():
  import core as ss
  params = []
  for color, param_list in PARAM_GROUPS:
    for name, size in param_list:
      value = getattr(ss, f'_{name}', getattr(ss, f'SAM', None))
      params.append({
        'name': name, 'label': name, 'type': 'number', 
        'value': value, 'size': size, 'color': color
      })
  return params

def create_plot_response(plot_func, *args, **kwargs):
  try:
    import core as ss
    fig = plot_func(*args, **kwargs)
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return send_file(buf, mimetype='image/png')
  except Exception as e:
    return jsonify({'error': str(e)}), 500

@app.context_processor
def inject_build_date():
  return {'build': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

@app.route('/')
def index():
  return render_template('index.htm', params=get_params(), runs=ACTIONS)

@app.route('/update_params', methods=['POST'])
def update_parameters():
  try:
    import core as ss
    data = request.get_json()
    result = ss.update_params(**data)
    return jsonify({
      'status': 'success', 
      'message': result, 
      'current_params': ss.get_current_params()
    })
  except Exception as e:
    return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/reset')
def reset():
  try:
    import core as ss
    result = ss.reset_params()
    return jsonify({
      'status': 'success', 
      'message': result, 
      'current_params': ss.get_current_params()
    })
  except Exception as e:
    return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/current_params')
def current_params():
  try:
    import core as ss
    return jsonify(ss.get_current_params())
  except Exception as e:
    return jsonify({'error': str(e)}), 500

@app.route('/insolation')
def insolation():
  import core as ss
  current = ss.get_current_params()
  pars = ss.fullX(**current)
  return create_plot_response(ss.plot_ins, pars)

@app.route('/simulation')
def simulation():
  import core as ss
  sam = int(request.args.get('sam', 65))
  current = ss.get_current_params()
  pars = ss.fullX(**current)
  return create_plot_response(ss.plot_sim, sam, pars)

@app.route('/simulations')
def simulations():
  import core as ss
  sam = int(request.args.get('sam', 65))
  param_ranges = getattr(ss, request.args.get('range', '_A_'))
  return create_plot_response(ss.plot_sims, sam, param_ranges)

@app.route('/parameters')
def parameters():
  import core as ss
  return create_plot_response(ss.plot_pars)

@app.route('/health')
def health_check():
  return jsonify({'status': 'healthy'}), 200

application = app
