import pytest
import time

@pytest.mark.system
@pytest.mark.slow
def test_critical_path_performance(client):
  critical_routes = ['/', '/dashboard/', '/analysis/']

  for route in critical_routes:
    start_time = time.time()
    response = client.get(route)
    load_time = time.time() - start_time

    assert response.status_code == 200
    assert load_time < 0.05
