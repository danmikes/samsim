import pytest

@pytest.mark.system
@pytest.mark.control
def test_control_routes_work(client):
  assert client.get('/control/').status_code == 200
