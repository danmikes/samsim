from app.service.analysis_service import AnalysisService
from app.service.dashboard_service import DashboardService
from app.service.insolation_manager import InsolationManager
from app.service.simulation_manager import SimulationManager
from app.service.settings_service import SettingsService
from app.config.base import Config

class AppService:
  def __init__(self):
    self.config = Config.CONFIG
    self.insolation_manager = InsolationManager()
    self.simulation_manager = SimulationManager()
    self.dashboard_service = DashboardService()
    self.analysis_service = AnalysisService()
    self.settings_service = SettingsService()

  def get_dashboard_data(self):
    return self.dashboard_service.get_dashboard_data()

  def analyse_simulation(self):
    return self.analysis_service.analyse_simulation()

  def get_enhanced_analysis(self):
    return self.analysis_service.get_enhanced_analysis()

  def get_settings(self):
    return self.settings_service.get_settings()

service = AppService()
