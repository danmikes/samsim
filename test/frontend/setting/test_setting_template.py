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

@pytest.mark.system
def test_setting_parameters(client):
  response = client.get('/setting/')
  html = response.data.decode('utf-8')

  assert 'Period' in html
  assert 'Amplitude' in html
  assert 'Period mod' in html
  assert 'Amplitude mod' in html
  assert 'Phase' in html
