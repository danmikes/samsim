import pytest

@pytest.mark.system
@pytest.mark.dashboard
def test_dashboard_routes_work(client):
  assert client.get('/dashboard/').status_code == 200
