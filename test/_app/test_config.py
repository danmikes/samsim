import os
import pytest
from app import create_app

class TestConfig:
  def test_environment_configurations(self):
    environments = ['development', 'production', 'testing']

    for env in environments:
      os.environ['FLASK_ENV'] = env
      app = create_app()

      assert app is not None
      assert hasattr(app, 'config')

      with app.test_client() as client:
        response = client.get('/')
        assert response.status_code in [200, 404, 302]

    os.environ['FLASK_ENV'] = 'testing'
