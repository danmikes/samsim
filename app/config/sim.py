from app.model.sim import Sim

class SimConfig:
  def __init__(self):
    self.default = Sim(
      time_span=int(1e6),
      sample_rate=int(1e1),
      signal_rate=int(1e2),
      target_fit=0.9
    )
    self.sim = self.default

  def update(self, **updates):
    self.sim = self.sim._replace(**updates)

  def reset(self):
    self.sim = self.default
