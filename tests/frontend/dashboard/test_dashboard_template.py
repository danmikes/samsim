import pytest

@pytest.mark.system
def test_dashboard_route(client):
  response = client.get('/dashboard/')
  assert response.status_code == 200

@pytest.mark.system
def test_dashboard_static_files(client):
  response = client.get('/dashboard/')
  html = response.data.decode('utf-8')

  assert 'style.css' in html
  assert 'script.js' in html
