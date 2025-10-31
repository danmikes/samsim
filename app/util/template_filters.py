def register_template_filters(app):
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
      return f"{num:_}"
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
