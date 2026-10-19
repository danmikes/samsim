from app.model.sample import Sample

class SampleConfig:
  def __init__(self):
    self.default = Sample(
      min_power=1,
      max_power=9,
      steps=10
    )
    self.sample = self.default

  @property
  def range(self):
    return self.sample.range

  def update(self, **updates):
    self.sample = self.sample._replace(**updates)

  def reset(self):
    self.sample = self.default
