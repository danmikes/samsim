# dashboard_service.py
from app.config import Config
from app.service.insolation_manager import InsolationManager
from app.service.simulation_manager import SimulationManager

class DashboardService:
  def __init__(self):
    self.config = Config.CONFIG
    self.insolation_manager = InsolationManager()
    self.simulation_manager = SimulationManager()

  def get_dashboard_data(self):
    df = self.insolation_manager.run_insolation()
    time_data = df['time'].astype(float).tolist()

    sim_result = self.simulation_manager.run_simulation(df, sample_size=65, repetitions=3)

    return {
      'time_data': time_data,
      'signals': [df[col].tolist() for col in df.columns if col.startswith('signal_')],
      'total_signal': df['total_signal'].tolist(),
      'simulation_fit': sim_result['average_fit'],
      'optimal_sample_size': self.simulation_manager.find_optimal_sample_size(0.9)
    }

  def run_simulation(self, sample_size=None):
    df = self.insolation_manager.run_insolation()
    return self.simulation_manager.run_simulation(df, sample_size)
