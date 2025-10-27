import pytest

@pytest.mark.frontend
def test_header_navigation(client):
  response = client.get('/')
  html = response.data.decode('utf-8')

  assert 'SamSim' in html

  assert '>Control' in html
  assert '>Dashboard' in html
  assert '>Info' in html

  assert 'href="/"' in html
  assert 'href="/control/"' in html
  assert 'href="/dashboard/"' in html
  assert 'href="/info/"' in html
