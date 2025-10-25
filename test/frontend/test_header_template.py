import pytest

@pytest.mark.frontend
def test_header_navigation(client):
  response = client.get('/')
  html = response.data.decode('utf-8')

  assert 'SamSim' in html
  assert all(link in html for link in [
    '>Dashboard',
    '>Analysis',
    '>Info',
    '>Help',
    '>Setting'
  ])
  assert all(url in html for url in [
    'href="/"',
    'href="/dashboard/"',
    'href="/analysis/"',
    'href="/help/"',
    'href="/info/"',
    'href="/setting/"'
  ])
