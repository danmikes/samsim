class TestAppInitialisation:
  def test_app_creation(self, app):
    assert app is not None

  def test_blueprints_registered(self, app):
    url_map = str(app.url_map)
    assert all(route in url_map for route in [
      '/control/',
      '/dashboard/',
      '/info/',
    ])

  def test_blueprint_names(self, control_blueprint, dashboard_blueprint, info_blueprint):
    assert control_blueprint.name == 'control'
    assert dashboard_blueprint.name == 'dashboard'
    assert info_blueprint.name == 'info'
