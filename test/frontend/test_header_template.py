import pytest

@pytest.mark.frontend
def test_header_navigation(client):
  response = client.get('/')
  html = response.data.decode('utf-8')

  assert 'SamSim' in html
  assert all(link in html for link in ['>Home', '>Dashboard', '>Analysis', '>Setting'])
  assert all(url in html for url in ['href="/"', 'href="/dashboard/"', 'href="/analysis/"', 'href="/setting/"'])
