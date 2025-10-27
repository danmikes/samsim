from unittest.mock import patch
import pytest
from app.service.logistic_service import LogisticService

class TestLogisticService:

  @pytest.fixture
  def logistic_service(self):
    return LogisticService()

  @pytest.fixture
  def sample_simulation_data(self):
    return [
      {'sample_rate': 10, 'fit': 0.1},
      {'sample_rate': 20, 'fit': 0.3},
      {'sample_rate': 30, 'fit': 0.5},
      {'sample_rate': 40, 'fit': 0.7},
      {'sample_rate': 50, 'fit': 0.9}
    ]

  def test_logistic_analysis_success(self, logistic_service, sample_simulation_data):
    result = logistic_service.logistic_analysis(sample_simulation_data)

    assert 'success' in result
    assert 'parameters' in result

  def test_logistic_analysis_failure(self, logistic_service):
    invalid_data = "not a list or dataframe"

    result = logistic_service.logistic_analysis(invalid_data)

    assert result['success'] is False
    assert 'error' in result

  def test_find_optimal_sample_rate(self, logistic_service, sample_simulation_data):
    with patch.object(logistic_service, 'logistic_analysis') as mock_analysis:
      mock_analysis.return_value = {
        'success': True,
        'parameters': [1.0, 0.1, 5.0]
      }
      with patch.object(logistic_service, '_find_x_for_y', return_value=25.0):
        result = logistic_service.find_optimal_sample_rate(0.9, sample_simulation_data)
        assert result == 25.0

  def test_find_optimal_sample_rate_failed_fit(self, logistic_service, sample_simulation_data):
    with patch.object(logistic_service, 'logistic_analysis') as mock_analysis:
      mock_analysis.return_value = {'success': False}
      result = logistic_service.find_optimal_sample_rate(0.9, sample_simulation_data)
      assert result is None

  def test_find_x_for_y(self, logistic_service):
    result = logistic_service._find_x_for_y(0.5, 1.0, 0.1, 5.0)
    assert result is not None
    assert isinstance(result, float)

  def test_find_x_for_y_edge_cases(self, logistic_service):
    result = logistic_service._find_x_for_y(1.0, 1.0, 0.1, 5.0)
    assert result is None

    result = logistic_service._find_x_for_y(0.0, 1.0, 0.1, 5.0)
    assert result is None

  def test_get_logistic_statistics(self, logistic_service):
    logistic_data = {
      'logistic_fit': {
        'success': True,
        'parameters': [1.0, 0.1, 5.0]
      },
      'simulation_data': [
        {'sample_rate': 10, 'fit': 0.5},
        {'sample_rate': 20, 'fit': 0.6},
        {'sample_rate': 30, 'fit': 0.7}
      ],
      'optimal_sample_rate': 25.0,
      'target_fit': 0.9
    }

    result = logistic_service.get_logistic_statistics(logistic_data)
    assert 'optimal_sample_rate' in result
    assert 'parameters' in result

  def test_clear_cache(self, logistic_service):
    logistic_service.clear_cache()
