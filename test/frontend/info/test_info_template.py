import pytest

@pytest.mark.system
def test_info_route(client):
  response = client.get('/info/')
  assert response.status_code == 200

@pytest.mark.system
def test_info_static_files(client):
  response = client.get('/info/')
  html = response.data.decode('utf-8')

  assert 'style.css' in html
  assert 'script.js' in html
