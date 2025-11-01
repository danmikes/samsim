from app.service.analysis_service import AnalysisService
from app.service.dashboard_service import DashboardService
from app.service.insolation_manager import InsolationManager
from app.service.simulation_manager import SimulationManager
from app.service.settings_service import SettingsService
from app.config import Config

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

  def get_analysis(self):
    return self.analysis_service.get_analysis()

  def get_enhanced_analysis(self):
    return self.analysis_service.get_enhanced_analysis()

  def get_settings(self):
    return self.settings_service.get_settings()

  def run_quick_simulation(self, sample_size=65):
    return self.dashboard_service.run_simulation(sample_size)

service = AppService()
