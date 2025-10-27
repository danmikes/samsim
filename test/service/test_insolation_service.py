import pytest
import pandas as pd
import numpy as np
from app.service.insolation_service import InsolationService
from app.model.signal import Signal

class TestInsolationService:

  @pytest.fixture
  def insolation_service(self):
    return InsolationService()

  def test_init(self, insolation_service):
    assert hasattr(insolation_service, 'default_params')
    assert len(insolation_service.default_params) == 3
    for key, param in insolation_service.default_params.items():
      assert isinstance(key, str)
      assert key in ['s1', 's2', 's3']
      assert isinstance(param, Signal)

  def test_get_default_params(self, insolation_service):
    params = insolation_service.default_params

    assert len(params) == 3
    first_param = list(params.values())[0]
    assert isinstance(first_param, Signal)

  def test_run_insolation_default_params(self, insolation_service):
    result = insolation_service.run_insolation()

    assert isinstance(result, pd.DataFrame)
    assert 'time' in result.columns
    assert 'total_signal' in result.columns
    assert 'signal_0' in result.columns
    assert 'signal_1' in result.columns
    assert 'signal_2' in result.columns
    assert len(result) == int(1e3)

  def test_run_insolation_custom_params(self, insolation_service):
    custom_params = {
      'custom_1': Signal(T=1000, A=10, Tm=5000, Am=5, p=0),
      'custom_2': Signal(T=2000, A=20, Tm=10000, Am=10, p=0)
    }

    result = insolation_service.run_insolation(custom_params)

    assert isinstance(result, pd.DataFrame)
    assert 'signal_0' in result.columns
    assert 'signal_1' in result.columns
    assert 'signal_2' not in result.columns

  def test_sine(self, insolation_service):
    t = np.array([0, 1, 2])
    result = insolation_service.sine(A=1, T=1, t=t)

    expected = 1 * np.sin(2 * np.pi * 1/1 * t + 0)
    np.testing.assert_array_equal(result, expected)

  def test_cosine(self, insolation_service):
    t = np.array([0, 1, 2])
    result = insolation_service.cosine(Am=1, Tm=1, t=t)

    expected = 1 * np.cos(2 * np.pi * 1/1 * t + 0)
    np.testing.assert_array_equal(result, expected)

  def test_total_signal_calculation(self, insolation_service):
    result = insolation_service.run_insolation()

    signal_cols = [col for col in result.columns if col.startswith('signal_')]
    calculated_total = result[signal_cols].sum(axis=1)

    pd.testing.assert_series_equal(result['total_signal'], calculated_total, check_names=False)
