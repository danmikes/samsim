import pytest
from unittest.mock import Mock, patch
from app.service.dashboard_service import DashboardService

class TestDashboardService:

  @pytest.fixture
  def dashboard_service(self):
    service = DashboardService()
    service.insolation = Mock()
    service.simulation = Mock()
    service.logistic = Mock()

    service.insolation.run_insolation.return_value = {'test': 'insolation'}
    service.simulation.run_simulation.return_value = {'test': 'simulation'}
    service.logistic.run_logistic.return_value = {'test': 'logistic'}

    return service

  def test_init(self, dashboard_service):
    assert hasattr(dashboard_service, 'insolation')
    assert hasattr(dashboard_service, 'simulation')
    assert hasattr(dashboard_service, 'logistic')

  def test_run_dashboard(self):
    with patch('app.service.dashboard_service.create_dashboard_chart') as mock_chart:
      mock_chart.return_value = {
        'insolation_chart': '<div>insolation</div>',
        'simulation_chart': '<div>simulation</div>',
        'logistic_chart': '<div>logistic</div>'
      }

      service = DashboardService()
      service.insolation = Mock()
      service.simulation = Mock()
      service.logistic = Mock()

      service.insolation.run_insolation.return_value = {'test': 'insolation'}
      service.simulation.run_simulation.return_value = {'test': 'simulation'}
      service.logistic.run_logistic.return_value = {'test': 'logistic'}

      result = service.run_dashboard()

      service.insolation.run_insolation.assert_called_once()
      service.simulation.run_simulation.assert_called_once()
      service.logistic.run_logistic.assert_called_once()

      mock_chart.assert_called_once_with(
        {'test': 'insolation'},
        {'test': 'simulation'},
        {'test': 'logistic'}
      )

      assert result == {
        'insolation_chart': '<div>insolation</div>',
        'simulation_chart': '<div>simulation</div>',
        'logistic_chart': '<div>logistic</div>'
      }

  def test_run_dashboard_calls_services(self):
    with patch('app.service.dashboard_service.create_dashboard_chart') as mock_chart:
      mock_chart.return_value = {'test': 'charts'}

      service = DashboardService()
      service.insolation = Mock()
      service.simulation = Mock()
      service.logistic = Mock()

      service.insolation.run_insolation.return_value = {}
      service.simulation.run_simulation.return_value = {}
      service.logistic.run_logistic.return_value = {}

      service.run_dashboard()

      service.insolation.run_insolation.assert_called_once()
      service.simulation.run_simulation.assert_called_once()
      service.logistic.run_logistic.assert_called_once()
      mock_chart.assert_called_once()

  def test_run_dashboard_chart_creation(self):
    with patch('app.service.dashboard_service.create_dashboard_chart') as mock_chart:
      mock_chart.return_value = {
        'insolation_chart': 'chart1',
        'simulation_chart': 'chart2',
        'logistic_chart': 'chart3'
      }

      service = DashboardService()
      service.insolation = Mock()
      service.simulation = Mock()
      service.logistic = Mock()

      service.insolation.run_insolation.return_value = {'data': 'insolation'}
      service.simulation.run_simulation.return_value = {'data': 'simulation'}
      service.logistic.run_logistic.return_value = {'data': 'logistic'}

      result = service.run_dashboard()

      mock_chart.assert_called_once_with(
        {'data': 'insolation'},
        {'data': 'simulation'},
        {'data': 'logistic'}
      )

      assert result == {
        'insolation_chart': 'chart1',
        'simulation_chart': 'chart2',
        'logistic_chart': 'chart3'
      }

  def test_run_dashboard_chart_structure(self):
    with patch('app.service.dashboard_service.create_dashboard_chart') as mock_chart:
      mock_chart.return_value = {
        'insolation_chart': '<div>insolation</div>',
        'simulation_chart': '<div>simulation</div>',
        'logistic_chart': '<div>logistic</div>'
      }

      service = DashboardService()
      service.insolation = Mock()
      service.simulation = Mock()
      service.logistic = Mock()

      result = service.run_dashboard()

      assert 'insolation_chart' in result
      assert 'simulation_chart' in result
      assert 'logistic_chart' in result
      assert isinstance(result['insolation_chart'], str)
      assert isinstance(result['simulation_chart'], str)
      assert isinstance(result['logistic_chart'], str)
