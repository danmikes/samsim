from typing import NamedTuple

import numpy as np

class Sample(NamedTuple):
  min_power: int
  max_power: int
  steps: int

  @property
  def range(self):
    return 2 ** np.linspace(self.min_power, self.max_power, self.steps)
