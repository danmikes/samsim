import pytest

@pytest.mark.system
@pytest.mark.analysis
def test_analysis_routes_work(client):
  assert client.get('/analysis/').status_code == 200
  assert client.get('/analysis/data').status_code == 200
