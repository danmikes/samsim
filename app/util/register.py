from markupsafe import Markup


def register_blueprint(app):
  for bp_path in app.config['BLUEPRINTS']:
    try:
      module_path, bp_name = bp_path.rsplit('.', 1)
      module = __import__(module_path, fromlist=[bp_name])
      blueprint = getattr(module, bp_name)
      app.register_blueprint(blueprint)
    except (ImportError, AttributeError) as e:
      print(f'Warning: Failed to register blueprint {bp_path}: {e}')

def register_filter(app):
  @app.template_filter('last')
  def last_filter(sequence):
    try:
      return sequence[-1] if sequence else None
    except (IndexError, TypeError):
      return None

  @app.template_filter('first')
  def first_filter(sequence):
    try:
      return sequence[0] if sequence else None
    except (IndexError, TypeError):
      return None

  @app.template_filter('format_number')
  def format_number(value):
    try:
      num = int(float(value))
      return f'{num:_}'
    except (ValueError, TypeError):
      return str(value)

  @app.template_filter('safe_subtract')
  def safe_subtract(values):
    try:
      if values and len(values) >= 2:
        first = float(values[0])
        last = float(values[-1])
        return last - first
      return 0
    except (ValueError, TypeError):
      return 0

  @app.template_filter('scientific')
  def scientific_filter(value, precision=1):
    try:
      num = float(value)
      if num == 0:
        return "0"

      formatted = format(num, f'.{precision}e')
      base, exp = formatted.split('e')
      exponent = int(exp)

      return Markup(f'{base} × 10<sup style="font-size: 0.7em; vertical-align: super; line-height: 0;">{exponent}</sup>')

    except (ValueError, TypeError):
      return str(value)

  @app.template_filter('format_param')
  def format_param(value, param_name):
    if param_name in ['T', 'Tm']:
      return scientific_filter(value, 1)
    elif param_name == 'p':
      return f"{value/3.14159:.2f}π"
    elif param_name == 'target_fit':
      return f"{value:.1f}"
    else:
      return f"{value:.0f}"

  @app.template_filter('format_input')
  def format_input(value, param_name):
    if param_name in ['T', 'Tm', 'time_span']:
      return f"{float(value):.1e}"
    elif param_name == 'target_fit':
      return f"{value:.1f}"
    else:
      return f"{value:.0f}"
