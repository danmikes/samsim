import pytest

@pytest.mark.system
def test_control_route(client):
  response = client.get('/control/')
  assert response.status_code == 200

@pytest.mark.system
def test_control_static_files(client):
  response = client.get('/control/')
  html = response.data.decode('utf-8')

  assert 'style.css' in html
