import pytest
import numpy as np
from app.service import AppService
from app.util import Par

class TestAppService:
  def setup_method(self):
    self.service = AppService()

  def test_initialization(self):
    assert hasattr(self.service, 'sim')
    assert self.service.sim is not None

  def test_get_dashboard_data(self):
    data = self.service.get_dashboard_data()

    assert 'time_data' in data
    assert 'signals' in data
    assert 'total_signal' in data

    assert isinstance(data['time_data'], list)
    assert isinstance(data['signals'], list)
    assert isinstance(data['total_signal'], list)

    assert len(data['time_data']) == 1000
    assert len(data['signals']) == 3
    assert len(data['total_signal']) == 1000
    assert all(isinstance(s, list) for s in data['signals'])
    assert all(len(s) == 1000 for s in data['signals'])

  def test_analyse_simulation(self):
    analysis = self.service.analyse_simulation()

    assert 'max_amplitude' in analysis
    assert 'min_amplitude' in analysis
    assert 'mean_amplitude' in analysis
    assert 'data_points' in analysis

    assert isinstance(analysis['max_amplitude'], (int, float))
    assert isinstance(analysis['min_amplitude'], (int, float))
    assert isinstance(analysis['mean_amplitude'], (int, float))
    assert isinstance(analysis['data_points'], int)

    assert analysis['max_amplitude'] >= analysis['min_amplitude']
    assert analysis['mean_amplitude'] >= analysis['min_amplitude']
    assert analysis['mean_amplitude'] <= analysis['max_amplitude']
    assert analysis['data_points'] == 1000

  def test_get_settings(self):
    settings = self.service.get_settings()

    assert 'duration' in settings
    assert 'signal_rate' in settings
    assert 'sample_rate' in settings
    assert 'default_parameters' in settings

    assert settings['duration'] == 1000000
    assert settings['signal_rate'] == 1000
    assert settings['sample_rate'] == 100
    assert isinstance(settings['default_parameters'], tuple)
    assert len(settings['default_parameters']) == 3

  def test_service_singleton(self):
    service1 = AppService()
    service2 = AppService()

    assert service1 is not service2
    data1 = service1.get_dashboard_data()
    data2 = service2.get_dashboard_data()

    assert len(data1['time_data']) == len(data2['time_data'])
    assert len(data1['signals']) == len(data2['signals'])

  def test_data_serialization(self):
    import json

    data = self.service.get_dashboard_data()

    json_str = json.dumps(data)
    assert isinstance(json_str, str)

    analysis = self.service.analyse_simulation()
    json_str = json.dumps(analysis)
    assert isinstance(json_str, str)

  def test_analysis_calculation(self):
    data = self.service.get_dashboard_data()
    total_signal = data['total_signal']

    analysis = self.service.analyse_simulation()

    expected_max = max(total_signal)
    expected_min = min(total_signal)
    expected_mean = sum(total_signal) / len(total_signal)
    expected_points = len(total_signal)

    assert analysis['max_amplitude'] == expected_max
    assert analysis['min_amplitude'] == expected_min
    assert analysis['mean_amplitude'] == pytest.approx(expected_mean)
    assert analysis['data_points'] == expected_points
