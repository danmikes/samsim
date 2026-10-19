from typing import NamedTuple

class Sim(NamedTuple):
  time_span: int
  signal_rate: int
  sample_rate: int
  target_fit: float
