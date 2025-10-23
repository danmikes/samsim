import pytest

@pytest.mark.system
@pytest.mark.setting
def test_setting_routes_work(client):
  assert client.get('/setting/').status_code == 200
  assert client.get('/setting/data').status_code == 200
