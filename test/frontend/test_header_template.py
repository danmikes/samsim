import pytest

@pytest.mark.frontend
def test_header_navigation(client):
  response = client.get('/')
  html = response.data.decode('utf-8')

  assert 'SamSim' in html

  assert '>Dashboard' in html
  assert '>Analysis' in html
  assert '>Info' in html
  assert '>Help' in html
  assert '>Setting' in html

  assert 'href="/"' in html
  assert 'href="/dashboard/"' in html
  assert 'href="/analysis/"' in html
  assert 'href="/help/"' in html
  assert 'href="/info/"' in html
  assert 'href="/setting/"' in html
