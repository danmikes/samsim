from typing import NamedTuple

class Sample(NamedTuple):
  min_power: int
  max_power: int
  steps: int

  @property
  def range(self):
    if self.steps == 1:
      return [2 ** self.min_power]

    result = []
    for i in range(self.steps):
      power = self.min_power + (self.max_power - self.min_power) * i / (self.steps - 1)
      result.append(2 ** power)
    return result
