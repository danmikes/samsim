from unittest.mock import patch
import pytest
from app.service.simulation_service import SimulationService

class TestSimulationService:

  @pytest.fixture
  def simulation_service(self):
    with patch('app.service.simulation_service.InsolationService') as mock_insolation:
      mock_insolation.return_value.run_insolation.return_value = {
        'time': [i for i in range(100)],
        'total_signal': [0.5 for _ in range(100)],
        'signal_0': [0.5 for _ in range(100)]
      }
      return SimulationService()

  def test_init(self, simulation_service):
    assert hasattr(simulation_service, 'time_span')
    assert hasattr(simulation_service, 'signal_rate')
    assert hasattr(simulation_service, 'sample_rate')
    assert hasattr(simulation_service, 'sample_range')

  def test_cross(self, simulation_service):
    signal = [1, -1, 1, -1]
    result = simulation_service._cross(signal)
    assert result == 3

  def test_compare(self, simulation_service):
    original = [1, -1, 1, -1]
    simulated = [1, -1, 1, -1]
    result = simulation_service._compare(original, simulated)
    assert result == 1.0

  def test_compare_zero_crossings(self, simulation_service):
    original = [1, 1, 1, 1]
    simulated = [1, -1, 1, -1]
    result = simulation_service._compare(original, simulated)
    assert result == 0

  def test_run_simulation(self, simulation_service):
    with patch.object(simulation_service.insolation, 'run_insolation') as mock_insolation:
      mock_insolation.return_value = {
        'time': [i for i in range(100)],
        'total_signal': [0.5 for _ in range(100)],
        'signal_0': [0.5 for _ in range(100)]
      }
      result = simulation_service.run_simulation()
      assert 'sample_rate' in result
      assert 'sampled_time' in result
      assert 'sampled_signal' in result
      assert 'simulated_time' in result
      assert 'simulated_signal' in result
      assert 'fit' in result

  def test_run_simulation_with_sample_rate(self, simulation_service):
    with patch.object(simulation_service.insolation, 'run_insolation') as mock_insolation:
      mock_insolation.return_value = {
        'time': [i for i in range(100)],
        'total_signal': [0.5 for _ in range(100)],
        'signal_0': [0.5 for _ in range(100)]
      }
      result = simulation_service.run_simulation(sample_rate=50)
      assert result['sample_rate'] == 50

  def test_run_many_simulations(self, simulation_service):
    with patch.object(simulation_service, 'run_simulation') as mock_run:
      mock_run.return_value = {'fit': 0.8}
      result = simulation_service.run_many_simulations()
      assert isinstance(result, list)
      assert len(result) > 0
      assert 'sample_rate' in result[0]
      assert 'fit' in result[0]

  def test_clear_cache(self, simulation_service):
    simulation_service.clear_cache()
