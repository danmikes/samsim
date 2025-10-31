from app.config.base import Config
from app.service.insolation_manager import InsolationManager

class DashboardService:
  def __init__(self):
    self.config = Config.CONFIG
    self.insolation_manager = InsolationManager()

  def get_dashboard_data(self):
    df = self.insolation_manager.run_insolation()
    time_data = df['time'].astype(float).tolist()

    return {
      'time_data': time_data,
      'signals': [df[col].tolist() for col in df.columns if col.startswith('signal_')],
      'total_signal': df['total_signal'].tolist(),
    }

  def run_simulation(self):
    pass
