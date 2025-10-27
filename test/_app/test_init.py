class TestAppInitialisation:
  def test_app_creation(self, app):
    assert app is not None

  def test_blueprints_registered(self, app):
    url_map = str(app.url_map)
    assert all(route in url_map for route in [
      '/analysis/',
      '/dashboard/',
      '/help/',
      '/info/',
      '/setting/'
    ])

  def test_blueprint_names(self, analysis_blueprint, dashboard_blueprint, help_blueprint, info_blueprint, setting_blueprint):
    assert info_blueprint.name == 'info'
    assert analysis_blueprint.name == 'analysis'
    assert dashboard_blueprint.name == 'dashboard'
    assert setting_blueprint.name == 'setting'
    assert help_blueprint.name == 'help'
