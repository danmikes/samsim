from app.util import SimulationManager

class AppService:
  def __init__(self):
    self.sim = SimulationManager()

  def get_dashboard_data(self):
    t, signals, total = self.sim.run_insolation()
    return {
      'time_data': t.tolist(),
      'signals': [s.tolist() for s in signals],
      'total_signal': total.tolist()
    }

  def analyse_simulation(self):
    data = self.get_dashboard_data()
    total = data['total_signal']

    return {
      'max_amplitude': max(total),
      'min_amplitude': min(total),
      'mean_amplitude': sum(total) / len(total),
      'data_points': len(total)
    }

  def get_settings(self):
    return {
      'duration': self.sim.config['DUR'],
      'signal_rate': self.sim.config['SIG'],
      'sample_rate': self.sim.config['SAM'],
      'default_parameters': self.sim.default_pars
    }

service = AppService()
