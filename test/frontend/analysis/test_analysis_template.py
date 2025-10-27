import pytest

@pytest.mark.system
def test_analysis_route(client):
  response = client.get('/analysis/')
  assert response.status_code == 200

@pytest.mark.system
def test_analysis_static_files(client):
  response = client.get('/analysis/')
  html = response.data.decode('utf-8')

  assert 'style.css' in html
  assert 'script.js' in html
