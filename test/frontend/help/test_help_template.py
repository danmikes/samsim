import pytest

@pytest.mark.system
def test_help_route(client):
  response = client.get('/help/')
  assert response.status_code == 200

@pytest.mark.system
def test_help_static_files(client):
  response = client.get('/help/')
  html = response.data.decode('utf-8')

  assert 'style.css' in html
  assert 'script.js' in html
