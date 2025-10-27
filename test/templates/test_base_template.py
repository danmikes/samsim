import pytest

@pytest.mark.frontend
def test_base_template_renders(client):
  response = client.get('/')
  assert response.status_code == 200
  assert b'SamSim' in response.data

@pytest.mark.frontend
def test_base_template_structure(client):
  response = client.get('/')
  html = response.data.decode('utf-8')

  assert b'SamSim' in response.data
  assert 'base.css' in html
  assert 'base.js' in html
  assert '<header>' in html
  assert '<main>' in html
  assert '<footer>' in html
