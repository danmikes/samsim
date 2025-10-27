from app.model.signal import Signal

class SignalConfig:
  def __init__(self):
    self.defaults = {
      's1': Signal(
        T=1.0e5,
        A=2,
        Tm=5.0e5,
        Am=1,
        p=0
      ),
      's2': Signal(
        T=4.1e4,
        A=25,
        Tm=2.5e5,
        Am=12.5,
        p=0
      ),
      's3': Signal(
        T=2.6e4,
        A=15,
        Tm=1.3e5,
        Am=7.5,
        p=0
      ),
    }
    self.signals = self.defaults.copy()

  def update(self, updates) -> None:
    for signal_name, params in updates.items():
      if signal_name in self.signals:
        self.signals[signal_name] = self.signals[signal_name]._replace(**params)

  def reset(self):
    self.signals = self.defaults.copy()
