import pytest

class TestSettingService:
  @pytest.fixture
  def service(self):
    from app.blueprint.setting.service import SettingService
    return SettingService()

  @pytest.fixture
  def expected_settings(self):
    return {
      'T': 100_000,
      'A': 10_000,
      'Tm': 1_000,
      'Am': 100,
      'p': 0
    }

  def test_get_setting_data_returns_all_expected_keys(self, service, expected_settings):
    data = service.get_setting_data()

    for key in expected_settings.keys():
      assert key in data, f"Key '{key}' not found in settings data"

  def test_get_setting_data_returns_correct_values(self, service, expected_settings):
    data = service.get_setting_data()

    for key, expected_value in expected_settings.items():
      assert data[key] == expected_value, f"Value for '{key}' is incorrect"

  def test_get_setting_by_key_returns_correct_values(self, service, expected_settings):
    for key, expected_value in expected_settings.items():
      value = service.get_setting_by_key(key)
      assert value == expected_value, f"get_setting_by_key('{key}') returned incorrect value"

  def test_get_setting_by_key_returns_none_for_unknown_keys(self, service):
    unknown_keys = ['unknown', 'invalid', 'test', '']
    for key in unknown_keys:
      value = service.get_setting_by_key(key)
      assert value is None, f"get_setting_by_key('{key}') should return None"

  def test_all_setting_values_are_integers(self, service):
    data = service.get_setting_data()

    for key, value in data.items():
      assert isinstance(value, int), f"Value for '{key}' should be integer"

  def test_get_setting_data_returns_complete_dataset(self, service, expected_settings):
    data = service.get_setting_data()
    assert data == expected_settings
