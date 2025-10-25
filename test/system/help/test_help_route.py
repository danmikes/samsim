import pytest

@pytest.mark.system
@pytest.mark.help
def test_help_routes_work(client):
  assert client.get('/help/').status_code == 200
