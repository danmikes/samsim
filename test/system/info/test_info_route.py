import pytest

@pytest.mark.system
@pytest.mark.info
def test_info_routes_work(client):
  assert client.get('/info/').status_code == 200
 