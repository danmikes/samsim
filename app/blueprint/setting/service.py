class SettingService:
  def __init__(self):
    self.data = {
      'T': 100_000,
      'A': 10_000,
      'Tm': 1_000,
      'Am': 100,
      'p': 0
    }

  def get_setting_data(self):
    return self.data.copy()

  def update_setting_data(self, new_data):
    pass

  def get_setting_by_key(self, key):
    return self.data.get(key)

  def update_setting(self, key: str, value: int):
    if key in self.data:
      self.data[key] = value
      return True
    return False

setting_service = SettingService()
