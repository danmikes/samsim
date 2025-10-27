import pytest
from dotenv import load_dotenv

load_dotenv('.flaskenv')

from app import create_app

@pytest.fixture(scope='session')
def app():
  _app = create_app()
  _app.config['TESTING'] = True
  _app.config['WTF_CSRF_ENABLED'] = False

  ctx = _app.app_context()
  ctx.push()

  yield _app

  ctx.pop()

@pytest.fixture(scope='session')
def client(app):
  """Create test client."""
  return app.test_client()

@pytest.fixture(scope='session')
def runner(app):
  """Create CLI test runner."""
  return app.test_cli_runner()

@pytest.fixture
def control_client(client):
  """Test client with control blueprint context."""
  return client

@pytest.fixture
def dashboard_client(client):
  """Test client with dashboard blueprint context."""
  return client

@pytest.fixture
def info_client(client):
  """Test client with info blueprint context."""
  return client

@pytest.fixture
def control_blueprint():
  from app.blueprint.control.route import control
  return control

@pytest.fixture
def dashboard_blueprint():
  from app.blueprint.dashboard.route import dashboard
  return dashboard

@pytest.fixture
def info_blueprint():
  from app.blueprint.info.route import info
  return info
