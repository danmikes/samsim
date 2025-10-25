import pytest

@pytest.mark.system
def test_setting_route(client):
  response = client.get('/setting/')
  assert response.status_code == 200

@pytest.mark.system
def test_setting_static_files(client):
  response = client.get('/setting/')
  html = response.data.decode('utf-8')

  assert 'style.css' in html
  assert 'script.js' in html
