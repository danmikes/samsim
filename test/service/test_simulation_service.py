from unittest.mock import patch
import pytest
import pandas as pd
import numpy as np
from app.service.simulation_service import SimulationService

class TestSimulationService:

  @pytest.fixture
  def mock_insolation_service(self):
    with patch('app.service.simulation_service.InsolationService') as mock:
      return mock.return_value

  @pytest.fixture
  def simulation_service(self, mock_insolation_service):
    return SimulationService()

  @pytest.fixture
  def sample_signal_data(self):
    return pd.DataFrame({
      'time': np.linspace(0, 100, 100),
      'total_signal': np.sin(np.linspace(0, 4*np.pi, 100)),
      'signal_0': 0.5 * np.sin(np.linspace(0, 4*np.pi, 100)),
      'signal_1': 0.3 * np.sin(np.linspace(0, 4*np.pi, 100))
    })

  def test_init(self, simulation_service):
    assert hasattr(simulation_service, 'time_span')
    assert hasattr(simulation_service, 'sample_rate')
    assert hasattr(simulation_service, 'sample_rate')
    assert hasattr(simulation_service, 'sample_range')

  def test_cross(self, simulation_service):
    signal = np.array([1, -1, 1, -1])
    result = simulation_service._cross(signal)
    assert result == 3

  def test_compare(self, simulation_service):
    original = np.array([1, -1, 1, -1])
    simulated = np.array([1, -1, 1, -1])
    result = simulation_service._compare(original, simulated)
    assert result == 1.0

  def test_compare_zero_crossings(self, simulation_service):
    original = np.array([1, 1, 1, 1])
    simulated = np.array([1, -1, 1, -1])
    result = simulation_service._compare(original, simulated)
    assert result == 0

  def test_run_simulation(self, simulation_service, sample_signal_data):
    result = simulation_service.run_simulation(sample_signal_data, sample_rate=10)

    assert 'average_fit' in result
    assert 'sample_rate' in result
    assert result['sample_rate'] == 10

  def test_run_many_simulations(self, simulation_service, sample_signal_data):
    sample_rate = [10, 20, 30]
    result = simulation_service.run_many_simulations(sample_signal_data, sample_rate)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3
    assert 'sample_rate' in result.columns
    assert 'average_fit' in result.columns
