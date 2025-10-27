import pytest

@pytest.mark.system
def test_home_static_files(client):
  response = client.get('/')
  html = response.data.decode('utf-8')

  assert 'index.css' in html
