import pytest
from app import create_app

class TestConfig:
  def test_app_creation(self):
    app = create_app()

    assert app is not None
    assert hasattr(app, 'config')
    assert hasattr(app, 'test_client')

  def test_app_configuration_loaded(self):
    app = create_app()

    assert app.config is not None
    from app.config import Config
    assert Config.signal is not None
    assert Config.sample is not None

  def test_app_responds_to_requests(self):
    app = create_app()

    with app.test_client() as client:
      response = client.get('/')
      assert response.status_code in [200, 404, 302, 301]

  def test_custom_json_provider(self):
    app = create_app()

    assert hasattr(app, 'json')
    from app import CustomJSONProvider
    assert isinstance(app.json, CustomJSONProvider)
