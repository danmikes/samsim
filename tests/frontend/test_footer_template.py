import pytest

@pytest.mark.frontend
def test_footer_template_structure(client):
  response = client.get('/')
  html = response.data.decode('utf-8')

  assert 'D. Mikes' in html
